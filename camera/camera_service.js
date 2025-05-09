const { spawn } = require('child_process');
const path = require('path');
const { database } = require('../firebase/firebase_connection');
const { ref, set } = require('firebase/database');

const IMAGE_OUTPUT_PATH = path.join(__dirname, 'captured.jpg');

async function runCamera() {
  console.log("Capturing pool table image...");

  return new Promise((resolve, reject) => {
    const capture = spawn('libcamera-still', [
      '-o', IMAGE_OUTPUT_PATH,
      '--width', '1280',
      '--height', '720',
      '--timeout', '1000'
    ]);

    capture.on('close', async (code) => {
      if (code === 0) {
        console.log("Image captured. Processing with Python...");

        const py = spawn('python3', ['camera/ball_tracker.py', 'camera/test_images/initial.jpg']);

        py.stdout.on('data', async (data) => {
          try {
            const ballData = JSON.parse(data.toString());
            console.log("Detected ball positions:", ballData);

            await set(ref(database, "/table_state/"), ballData);
            
            // Pass the ballData as a JSON string to graph.py
            const pyGraph = spawn('python3', ['graph.py', JSON.stringify(ballData)]);

            pyGraph.stdout.on('data', (data) => {
              console.log("Graphing complete:", data.toString());
            });

            pyGraph.stderr.on('data', (data) => {
              console.error("Python error while graphing:", data.toString());
            });

            console.log("Uploaded table state to Firebase.");
            resolve();
          } catch (err) {
            reject("Failed to parse ball data: " + err);
          }
        });

        py.stderr.on('data', (data) => {
          console.error("Python error:", data.toString());
        });

        py.on('close', (code) => {
          if (code !== 0) {
            reject(`Python exited with code ${code}`);
          }
        });

      } else {
        reject(new Error(`Camera exited with code ${code}`));
      }
    });
  });
}

module.exports = { runCamera };