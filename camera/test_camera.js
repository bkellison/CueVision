const path = require('path');
const { spawn } = require('child_process');

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
            console.log("✅ Image captured successfully at", IMAGE_OUTPUT_PATH);
            resolve();
            } else {
            reject(new Error(`Camera exited with code ${code}`));
            }
        });
    });
}

module.exports = { runCamera };