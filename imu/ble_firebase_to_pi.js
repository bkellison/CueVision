const { createBluetooth } = require('node-ble');
const { initializeApp } = require('firebase/app');
const { getDatabase, ref, set } = require('firebase/database');

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

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

const ARDUINO_BLUETOOTH_ADDR = '09:a8:99:21:89:99';
const UART_SERVICE_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E';
const TX_CHARACTERISTIC_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E';
const RX_CHARACTERISTIC_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E';

async function saveToFirebase(path, data) {
  const now = Date.now();
  await set(ref(db, `${path}/${now}`), data);
}

async function main() {
  const { bluetooth, destroy } = createBluetooth();
  const adapter = await bluetooth.defaultAdapter();
  await adapter.startDiscovery();
  console.log('discovering...');

  const device = await adapter.waitDevice(ARDUINO_BLUETOOTH_ADDR.toUpperCase());
  console.log('found device. attempting connection...');
  await device.connect();
  console.log('connected to device!');

  const gattServer = await device.gatt();
  const uartService = await gattServer.getPrimaryService(UART_SERVICE_UUID.toLowerCase());
  const txChar = await uartService.getCharacteristic(TX_CHARACTERISTIC_UUID.toLowerCase());
  const rxChar = await uartService.getCharacteristic(RX_CHARACTERISTIC_UUID.toLowerCase());

  rxChar.on('valuechanged', buffer => {
    console.log('Received data:', buffer.toString());  // Log the raw data
    const data = buffer.toString().trim();
    const [gyroX, gyroY, gyroZ, accelX, accelY, accelZ] = data.split(',').map(Number);
  
    console.log(`Gyro - X: ${gyroX}, Y: ${gyroY}, Z: ${gyroZ}`);
    console.log(`Accel - X: ${accelX}, Y: ${accelY}, Z: ${accelZ}`);
  
    saveToFirebase('cue_imu', {
      gyro: { x: gyroX, y: gyroY, z: gyroZ },
      accel: { x: accelX, y: accelY, z: accelZ },
      timestamp: Date.now()
    });
  });
  
  const stdin = process.openStdin();
  stdin.addListener('data', async d => {
    let inStr = d.toString().trim();
    if (inStr === 'exit') {
      console.log('disconnecting...');
      await device.disconnect();
      destroy();
      console.log('disconnected.');
      process.exit();
    }
    inStr = inStr.slice(0, 20);
    await txChar.writeValue(Buffer.from(inStr));
    console.log('Sent:', inStr);
  });
}

main().catch(console.error);
