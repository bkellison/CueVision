const { spawn } = require('child_process');
const path = require('path');
const { database } = require('../firebase/firebase_connection');
const { ref, set, get } = require('firebase/database');
const { basename } = require('path/win32');

async function runPhysics() {
  console.log("Fetching ball positions from Firebase...");

  try {
    const snapshot = await get(ref(database, "/table_state/"));

    if (!snapshot.exists()) {
      throw new Error("No ball data found at /table_state/");
    }

    const ballData = snapshot.val();
    console.log("Retrieved ball data:", ballData);

    return new Promise((resolve, reject) => {
      const scriptPath = path.join(__dirname, '../ball-identification/ball-physics.py');
      const py = spawn('python3', [scriptPath, JSON.stringify(ballData)]);
      console.log("Retrieve Spawn:");

      py.stdout.on('data', async (data) => {
        try {
          console.log("Enter try block:", ballData);

          console.log("Entered:");
          const output = JSON.parse(data.toString());
          console.log("Parsed physics output:", output);
      
          if (output.trajectory) {
            const trajectoryRef = ref(database, '/trajectory/');
      
            // Transform array of tuples into Firebase-compatible object
            const formatted = output.trajectory.reduce((acc, [m, b], index) => {
              acc[`vector${index + 1}`] = { m, b };
              return acc;
            }, {});
      
            await set(trajectoryRef, formatted);
            console.log("Trajectory saved to Firebase:", formatted);
          }

          if (output.cue_impact) {
            const cueImpactRef = ref(database, '/cue_impact/');
          
            const formattedImpact = {
              x: output.cue_impact[0],
              y: output.cue_impact[1],
            };
          
            await set(cueImpactRef, formattedImpact);
            console.log("Cue impact saved to Firebase:", formattedImpact);
          }          
      
          resolve(output);
        } catch (err) {
          console.error("Failed to parse or save trajectory:", err);
          reject(err);
        }
      })
    });

  } catch (error) {
    console.error("Error running ball physics:", error);
  }
}

module.exports = { runPhysics };
