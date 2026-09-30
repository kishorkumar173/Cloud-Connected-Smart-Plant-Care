/*
 * =====================================================================================
 * Project: Cloud-Connected Smart Plant Care & Watering System
 * File: esp32_smart_plant.ino
 * Description: Production-ready ESP32 Arduino firmware for physical IoT hardware.
 *              Reads capacitive soil moisture, DHT22 temp/humidity, and LDR light sensor.
 *              Connects securely over Wi-Fi and transmits telemetry to the cloud backend.
 *              Actuates a 5V relay / MOSFET water pump based on cloud commands.
 * =====================================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>  // Install via Arduino Library Manager: "ArduinoJson" by Benoit Blanchon
#include <DHT.h>          // Install via Arduino Library Manager: "DHT sensor library" by Adafruit

// ================= Wi-Fi & Cloud Configuration =================
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Cloud Server Endpoint (Replace with your computer's local IP or cloud URL)
// Example Local: "http://192.168.1.100:8000/api/sensors/data"
// Example Cloud: "https://your-app.onrender.com/api/sensors/data"
const char* CLOUD_INGEST_URL = "http://192.168.1.100:8000/api/sensors/data";

// IoT Security Credentials
const char* DEVICE_ID      = "PLANT-001";
const char* DEVICE_API_KEY = "plant-iot-cloud-api-key-998877";

// Telemetry Reporting Cadence
const unsigned long TELEMETRY_INTERVAL_MS = 5000; // Send telemetry every 5 seconds
unsigned long lastTelemetryTime = 0;

// ================= GPIO Pin Assignments =================
#define PIN_SOIL_MOISTURE  34  // Analog ADC1 input (Capacitive Soil Moisture v1.2)
#define PIN_DHT            4   // Digital input for DHT22 / DHT11
#define PIN_LDR            35  // Analog ADC1 input for Light Dependent Resistor
#define PIN_PUMP_RELAY     16  // Digital output to Relay / N-Channel MOSFET module
#define PIN_STATUS_LED     2   // Built-in blue diagnostic LED

#define DHTTYPE DHT22          // Change to DHT11 if using the blue DHT11 module

// Sensor Calibration Constants (Calibrate with dry air vs. cup of water)
const int DRY_ADC_VALUE = 3200;  // Raw ADC in dry air (approx 0% moisture)
const int WET_ADC_VALUE = 1450;  // Raw ADC submerged in water (approx 100% moisture)

DHT dht(PIN_DHT, DHTTYPE);

// Active pump state
bool isPumpActive = false;
unsigned long pumpDeactivateTime = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n=======================================================");
  Serial.println("🌱 ESP32 Smart Plant Care Node Initializing...");
  Serial.println("=======================================================");

  // Configure GPIOs
  pinMode(PIN_PUMP_RELAY, OUTPUT);
  pinMode(PIN_STATUS_LED, OUTPUT);
  digitalWrite(PIN_PUMP_RELAY, LOW); // Safe default: pump OFF
  digitalWrite(PIN_STATUS_LED, LOW);

  // Initialize sensors
  dht.begin();
  analogReadResolution(12); // ESP32 12-bit ADC (0 - 4095)

  // Connect to Local Wi-Fi
  connectWiFi();
}

void loop() {
  // Ensure Wi-Fi remains connected
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  // Handle active pump timer shutoff (safety circuit)
  if (isPumpActive && millis() >= pumpDeactivateTime) {
    stopPump();
  }

  // Periodic Telemetry Transmission
  if (millis() - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = millis();
    transmitSensorTelemetry();
  }
}

void connectWiFi() {
  Serial.print("Connecting to Wi-Fi SSID: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    digitalWrite(PIN_STATUS_LED, !digitalRead(PIN_STATUS_LED));
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ Wi-Fi Connected Successfully!");
    Serial.print("   Assigned IP Address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(PIN_STATUS_LED, HIGH);
  } else {
    Serial.println("\n❌ Wi-Fi Connection Failed. Will retry in next loop.");
    digitalWrite(PIN_STATUS_LED, LOW);
  }
}

void transmitSensorTelemetry() {
  // 1. Read Capacitive Soil Moisture Sensor
  int rawSoil = analogRead(PIN_SOIL_MOISTURE);
  // Map raw ADC to 0.0 - 100.0% (Invert: high raw ADC = dry, low raw ADC = wet)
  float soilMoisture = map(rawSoil, DRY_ADC_VALUE, WET_ADC_VALUE, 0, 100);
  soilMoisture = constrain(soilMoisture, 0.0, 100.0);

  // 2. Read Ambient Temperature and Humidity
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Validate DHT readings; fallback to nominal if transient read failure occurs
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("⚠️ DHT sensor reading failed! Using previous or nominal values.");
    temperature = 25.0;
    humidity = 60.0;
  }

  // 3. Read Ambient Light Level
  int rawLdr = analogRead(PIN_LDR);
  float lightPercent = map(rawLdr, 0, 4095, 0, 100);
  lightPercent = constrain(lightPercent, 0.0, 100.0);

  // Print telemetry to Serial Console
  Serial.printf("\n[SENSORS] Moisture: %.1f%% | Temp: %.1f°C | Humid: %.1f%% | Light: %.1f%%\n",
                soilMoisture, temperature, humidity, lightPercent);

  // 4. Construct JSON Payload
  StaticJsonDocument<256> doc;
  doc["device_id"] = DEVICE_ID;
  doc["soil_moisture"] = soilMoisture;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["light_level"] = lightPercent;
  doc["water_tank_level"] = 85.0; // Can attach ultrasonic HC-SR04 or float switch

  String requestBody;
  serializeJson(doc, requestBody);

  // 5. Transmit HTTP POST to Cloud Backend
  HTTPClient http;
  http.begin(CLOUD_INGEST_URL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-Device-API-Key", DEVICE_API_KEY);

  int httpCode = http.POST(requestBody);

  if (httpCode == 200 || httpCode == 201) {
    String responseString = http.getString();
    Serial.println("☁️ [CLOUD RESPONSE RECEIVED]");

    // Parse Cloud JSON Command
    StaticJsonDocument<512> responseDoc;
    DeserializationError error = deserializeJson(responseDoc, responseString);

    if (!error) {
      const char* pumpCommand = responseDoc["pump_command"];
      bool triggered = responseDoc["watering_triggered"];

      Serial.printf("   Pump Actuation Command: [%s]\n", pumpCommand);

      // Cloud Decision Actuation: Turn relay ON
      if (strcmp(pumpCommand, "ON") == 0) {
        int durationSec = 5;
        if (responseDoc.containsKey("decision_metadata") &&
            responseDoc["decision_metadata"].containsKey("duration_seconds")) {
          durationSec = responseDoc["decision_metadata"]["duration_seconds"];
        }
        startPump(durationSec);
      } else {
        if (isPumpActive) {
          stopPump();
        }
      }
    }
  } else {
    Serial.printf("❌ [HTTP POST FAILED] Code: %d, Response: %s\n", httpCode, http.getString().c_str());
  }

  http.end();
}

void startPump(int durationSeconds) {
  if (!isPumpActive) {
    Serial.printf("💧 [ACTUATOR] Energizing Relay: PUMP ON for %d seconds\n", durationSeconds);
    digitalWrite(PIN_PUMP_RELAY, HIGH);
    isPumpActive = true;
    pumpDeactivateTime = millis() + (durationSeconds * 1000UL);
  }
}

void stopPump() {
  Serial.println("🛑 [ACTUATOR] De-energizing Relay: PUMP OFF");
  digitalWrite(PIN_PUMP_RELAY, LOW);
  isPumpActive = false;
}
