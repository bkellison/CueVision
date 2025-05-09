// cue-vision.js
//const { runCamera } = require('./camera/camera_service');
// cue-vision.js
const { runPhysics } = require('./ball-identification/physics-service');
const { runIMU } = require('./imu/imu_formatter');
const { initializeDatabase } = require('./firebase/firebase_connection');

async function main() {
  console.log("Starting Cue Vision...");

  // Initialize Firebase
  initializeDatabase();

  // Run camera and IMU logic concurrently
  try {
    await Promise.all([
      runPhysics(),
      //runCamera(),
      //runIMU()
    ]);
  } catch (err) {
    console.error("Error running components:", err);
  }
}

main();
