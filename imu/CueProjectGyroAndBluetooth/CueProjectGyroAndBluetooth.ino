#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>  // To access both Gyroscope and Accelerometer data

#define BUFSIZE 40
#define SAMPLE_SIZE 10

BLEService uartService("6E400001-B5A3-F393-E0A9-E50E24DCCA9E"); // Define the BLE service
BLEStringCharacteristic txChar("6E400002-B5A3-F393-E0A9-E50E24DCCA9E", BLEWrite, 20);  // TX characteristic for receiving data
BLEStringCharacteristic rxChar("6E400003-B5A3-F393-E0A9-E50E24DCCA9E", BLERead | BLENotify, BUFSIZE); // RX characteristic for sending data

float gyroXSamples[SAMPLE_SIZE] = {0};
float gyroYSamples[SAMPLE_SIZE] = {0};
float gyroZSamples[SAMPLE_SIZE] = {0};
float accelXSamples[SAMPLE_SIZE] = {0};
float accelYSamples[SAMPLE_SIZE] = {0};
float accelZSamples[SAMPLE_SIZE] = {0};
int sampleIndex = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  BLE.setLocalName("CueGyro");
  BLE.setAdvertisedService(uartService);
  uartService.addCharacteristic(txChar);
  uartService.addCharacteristic(rxChar);
  BLE.addService(uartService);
  BLE.advertise();
  Serial.println("BLE Device Ready.");
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {
      float gyroX, gyroY, gyroZ;
      float accelX, accelY, accelZ;

      if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(gyroX, gyroY, gyroZ);
      }

      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(accelX, accelY, accelZ);
      }

      // Store samples for averaging
      gyroXSamples[sampleIndex] = gyroX;
      gyroYSamples[sampleIndex] = gyroY;
      gyroZSamples[sampleIndex] = gyroZ;
      accelXSamples[sampleIndex] = accelX;
      accelYSamples[sampleIndex] = accelY;
      accelZSamples[sampleIndex] = accelZ;
      sampleIndex = (sampleIndex + 1) % SAMPLE_SIZE;

      // Calculate averages of the samples
      float avgGyroX = calculateAverage(gyroXSamples, SAMPLE_SIZE);
      float avgGyroY = calculateAverage(gyroYSamples, SAMPLE_SIZE);
      float avgGyroZ = calculateAverage(gyroZSamples, SAMPLE_SIZE);
      float avgAccelX = calculateAverage(accelXSamples, SAMPLE_SIZE);
      float avgAccelY = calculateAverage(accelYSamples, SAMPLE_SIZE);
      float avgAccelZ = calculateAverage(accelZSamples, SAMPLE_SIZE);

      // Prepare the data string to send
      char buffer[BUFSIZE];
      snprintf(buffer, BUFSIZE, "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f", avgGyroX, avgGyroY, avgGyroZ, avgAccelX, avgAccelY, avgAccelZ);
      rxChar.writeValue(buffer);

      Serial.print("Sent: ");
      Serial.println(buffer);

      delay(500);  // Send data every 1 second
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}

// Function to calculate the average of an array
float calculateAverage(float arr[], int size) {
  float sum = 0;
  for (int i = 0; i < size; i++) sum += arr[i];
  return sum / size;
}
