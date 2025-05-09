# CueVision: Augmented Reality Billiards Overlay

CueVision is an Augmented Reality Billiards Overlay (ARBO) used as an assistive tool designed to enhance the casual pool-playing experience using real-time sensor data and spatial guidance.

## Project Overview

Built for the Meta Quest headset using Unity, ARBO overlays trajectory predictions and aiming assistance directly into the player's field of view, helping guide shots with precision. The system leverages an IMU-equipped cue stick and a Raspberry Pi connected to a camera for table state detection, both of which send data to Firebase for centralized real-time communication. Unity retrieves this data and uses it to calculate ideal shot vectors, visualizing how and where to strike the cue ball for a successful pocket. The headset's onboard IMU further enhances tracking accuracy.

## System Architecture

The CueVision system consists of three main components:

1. **IMU-equipped Pool Cue**: Tracks the orientation and movement of the cue stick
2. **Raspberry Pi with Camera**: Detects the table state (ball positions)
3. **Meta Quest Headset**: Displays trajectory overlays to the user

All components communicate through Firebase Realtime Database, allowing real-time updates across the system.

## Network Requirements

**IMPORTANT**: The Raspberry Pi must be connected to the **Eduroam** WiFi network on campus. The device was registered under UI DeviceNet but cannot be taken outside of this environment. This means the complete front-end and back-end integration could not be fully tested in a real-world setting.

**Note**: Due to these networking limitations, the system represents a prototype of code that could all work together under the right conditions rather than a fully deployed solution.

## Components and Files

### JavaScript Backend (Raspberry Pi)

- `cue-vision.js`: Main application entry point
- `firebase_connection.js`: Initializes and manages Firebase database connections
- `physics-service.js`: Handles ball physics calculations and trajectory predictions
- `ble_firebase_to_pi.js`: Manages BLE communication with the IMU-equipped cue
- `imu_reader.js`: Processes data from the inertial measurement unit
- `nodeble_accel_gyro_data.js`: Processes accelerometer and gyroscope data

### Python Scripts

- `ball_tracker.py`: Detects and tracks pool balls in camera images
- `ball-physics.py`: Calculates optimal trajectory and impact points
- `graph.py`: Generates visual representations of ball positions
- `plot_table.py`: Creates visual plots of the pool table state

### Arduino

- `CueProjectGyroAndBluetooth.ino`: Arduino sketch for the IMU-equipped cue stick
- `TimeoutTimer.h`: Helper library for timing operations

### Configuration

- `package.json`: Node.js package dependencies
- `requirements.txt`: Python package dependencies


## How It Works

1. **Table State Detection**:
   - The camera captures the pool table state
   - `ball_tracker.py` identifies the position of each ball
   - The data is sent to Firebase

2. **Shot Planning**:
   - `ball-physics.py` calculates the optimal trajectory
   - Impact point on the cue ball is determined
   - Trajectory lines and impact information are sent to Firebase

3. **Cue Orientation**:
   - IMU sensors track the cue stick's orientation
   - Data is transmitted via BLE to the Raspberry Pi
   - Processed data is sent to Firebase

4. **AR Overlay**:
   - Meta Quest reads Firebase data
   - Unity renders trajectory lines and impact points
   - Player sees guidance overlay in real-time

## Prototype Limitations

This is currently a prototype with the following limitations:

- The Raspberry Pi must remain connected to Eduroam on campus
- Full system integration testing was limited by networking constraints
- The components have been developed and tested individually but not as a complete system
- The device registration with UI DeviceNet prevents off-campus testing

## Future Improvements

- Migrate to a more portable networking solution
- Implement local processing to reduce reliance on cloud services
- Enhance ball detection for various lighting conditions
- Add multi-user support for competitive play
- Incorporate shot difficulty ratings and learning progression

## Contributors

- Blake Kellison
- Kenna Vanorny
- Kody Wixom
- Marissa Miller



## Acknowledgments

- University of Iowa for network access and device registration
- Firebase for real-time database services
- Meta for Quest development tools
