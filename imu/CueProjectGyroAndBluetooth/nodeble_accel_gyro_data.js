const { initializeApp } = require("firebase/app");
const { getDatabase, ref, set } = require("firebase/database");
const { createBluetooth } = require('node-ble');

// Firebase configuration
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

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// Bluetooth configuration
const ARDUINO_BLUETOOTH_ADDR = '2a:99:83:76:9a:cd';  // Update with your device's address
const UART_SERVICE_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E';
const TX_CHARACTERISTIC_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E';
const RX_CHARACTERISTIC_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E';

let txCharacteristic = null;

async function connectToArduino() {
    const { bluetooth, destroy } = createBluetooth();
    const adapter = await bluetooth.defaultAdapter();
    const discovery = await adapter.startDiscovery();
    console.log('discovering...');

    // Attempt to connect to the device
    const device = await adapter.waitDevice(ARDUINO_BLUETOOTH_ADDR.toUpperCase());
    console.log('found device. attempting connection...');
    await device.connect();
    console.log('connected to device!');

    // Get UART service and TX/RX characteristics
    const gattServer = await device.gatt();
    const uartService = await gattServer.getPrimaryService(UART_SERVICE_UUID.toLowerCase());
    const txChar = await uartService.getCharacteristic(TX_CHARACTERISTIC_UUID.toLowerCase());
    const rxChar = await uartService.getCharacteristic(RX_CHARACTERISTIC_UUID.toLowerCase());

    txCharacteristic = txChar;

    // Start notifications for RX characteristic
    await rxChar.startNotifications();
    rxChar.on('valuechanged', buffer => {
        const data = buffer.toString();
        console.log('Received: ' + data);
        // Process the received data for gyroscope and accelerometer
        processSensorData(data);
    });
}

// Function to process the received sensor data
function processSensorData(data) {
    const sensorData = data.split(','); // Assuming the data is comma-separated (e.g., "gyroX,gyroY,gyroZ,accX,accY,accZ")
    if (sensorData.length === 6) {
        const [gyroX, gyroY, gyroZ, accX, accY, accZ] = sensorData.map(Number);
        const timestamp = Date.now();

        // Log the gyroscope and accelerometer data
        console.log(`Gyroscope Data: X=${gyroX}, Y=${gyroY}, Z=${gyroZ}`);
        console.log(`Accelerometer Data: X=${accX}, Y=${accY}, Z=${accZ}`);

        // Send the data to Firebase
        const sensorDataRef = ref(db, "cue_imu");
        set(sensorDataRef, {
            gyroX,
            gyroY,
            gyroZ,
            accX,
            accY,
            accZ,
            timestamp
        }).then(() => {
            console.log('Sensor data sent to Firebase');
        }).catch((error) => {
            console.error('Error sending data to Firebase:', error);
        });
    } else {
        console.error('Invalid data format received:', data);
    }
}

async function sendToArduino(message) {
    if (!txCharacteristic) {
        console.error("TX Characteristic not available yet.");
        return;
    }

    const buffer = Buffer.from(message);
    await txCharacteristic.writeValue(buffer).then(() => {
        console.log(`Sent message to Arduino: ${message}`);
    });
}

// Start Bluetooth connection and listen for data
connectToArduino().then(() => {
    console.log('Bluetooth connection established');
}).catch((err) => {
    console.error('Error establishing Bluetooth connection:', err);
});
