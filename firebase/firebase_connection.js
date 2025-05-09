const { initializeApp } = require('firebase/app');
const { getDatabase, ref, set } = require('firebase/database');

// Firebase config
const firebaseConfig = {
    apiKey: "AIzaSyDoUpURSM-Cc6QUVJ48EOzIw0KAtZyHIWM",
    authDomain: "cue-vision-e6c0b.firebaseapp.com",
    databaseURL: "https://cue-vision-e6c0b-default-rtdb.firebaseio.com",
    projectId: "cue-vision-e6c0b",
    storageBucket: "cue-vision-e6c0b.appspot.com",
    messagingSenderId: "828433143063",
    appId: "1:828433143063:web:31a8858e54a2f048ab1352",
    measurementId: "G-5GLLE01ZKL"
};

// Initialize app and database
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

function initializeDatabase() {
    const initialData = {
        table_state: {
            "ball1": { "id": 1, "x": 0.15, "y": 0.70 },
            "ball2": { "id": 2, "x": 0.20, "y": 0.25 },
            "ball3": { "id": 3, "x": 0.30, "y": 0.20 },
            "ball4": { "id": 4, "x": 0.40, "y": 0.30 },
            "ball5": { "id": 5, "x": 0.70, "y": 0.60 },
            "ball6": { "id": 6, "x": 0.60, "y": 0.50 },
            "ball7": { "id": 7, "x": 0.70, "y": 0.50 },
            "ball8": { "id": 8, "x": 0.70, "y": 0.70 },
            "ball9": { "id": 9, "x": 0.80, "y": 0.30 },
            "ball10": { "id": 10, "x": 0.20, "y": 0.90 },
            "ball11": { "id": 11, "x": 0.35, "y": 0.90 },
            "ball12": { "id": 12, "x": 0.45, "y": 0.85 },
            "ball13": { "id": 13, "x": 0.55, "y": 0.80 },
            "ball14": { "id": 14, "x": 0.65, "y": 0.75 },
            "ball15": { "id": 15, "x": 0.75, "y": 0.70 },
            "cue-ball": { "id": 16, "x": 0.50, "y": 0.50 },
            "target-ball": { "id": 17, "x": 0.45, "y": 0.85 },
            "pocket": { "id": 18, "x": 1.00, "y": 1.00 }
        },
        cue_imu: {
            gyroX: 0.0,
            gyroY: 0.0,
            gyroZ: 0.0,
            accX: 0.0,
            accY: 0.0,
            accZ: 0.0,
            timestamp: Date.now()
        },
        trajectory: {
            vector1: {m: 0.0, b:0},
            vector2: {m: 0.0, b:0}
        },
        cue_impact: {
            x: 1.0,
            y: 0.0
        }
    };

    set(ref(database, "/"), initialData)
        .then(() => {
            console.log("✅ Firebase database initialized with default values.");
        })
        .catch((error) => {
            console.error("❌ Error initializing database:", error);
        });
}

module.exports = { initializeDatabase, database };