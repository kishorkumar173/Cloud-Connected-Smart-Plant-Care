# Optional Physical IoT Hardware Implementation Guide

This document explains how to connect physical IoT hardware components to the **Cloud-Connected Smart Plant Care & Watering System** without changing the cloud backend or dashboard architecture.

---

## 1. Bill of Materials (BOM)

| Component | Specification | Approximate Cost | Purpose |
|---|---|---|---|
| **Microcontroller** | ESP32 DevKit V1 (30 or 38 pin) | ~$4.00 - $6.00 | Wi-Fi connectivity, sensor reading, cloud HTTP client |
| **Soil Moisture Sensor** | Capacitive Soil Moisture Sensor v1.2 | ~$1.50 | Measures soil moisture without metallic corrosion |
| **Climate Sensor** | DHT22 (AM2302) or DHT11 | ~$2.00 - $3.50 | Measures ambient temperature & humidity |
| **Light Sensor** | LDR (5mm) + 10kΩ Resistor | ~$0.50 | Measures ambient sunlight / photoperiod |
| **Actuator** | 5V / 1-Channel Relay Module (Optoisolated) | ~$1.00 | Safely switches submersible pump circuit |
| **Water Pump** | Mini 3V–6V DC Submersible Pump | ~$2.00 | Irrigates soil via flexible silicone tubing |
| **Tubing** | 7mm / 8mm flexible silicone tube (1 meter) | ~$1.00 | Routes water from reservoir to plant root zone |
| **Power Supply** | 5V 2A Micro-USB or External 5V DC Supply | ~$4.00 | Powers ESP32 and pump |
| **Protection** | 1N4007 Diode & 100µF Capacitor | ~$0.30 | Flyback inductive spike protection |

---

## 2. Wiring & Pinout Schematic

```text
               +--------------------------------------------+
               |                 ESP32                      |
               |                                            |
  3.3V --------| 3V3                                    GND |-------- Common GND
               |                                            |
Capacitive AOUT| GPIO 34 (ADC1)                             |
DHT22 DATA ----| GPIO 4                                     |
LDR Divider ---| GPIO 35 (ADC1)                             |
               |                                            |
Relay IN ------| GPIO 16                                    |
               |                                            |
               +--------------------------------------------+

[Water Pump Circuit - Optically Isolated]
+5V External Power ────────── Relay COM
                               Relay NO ────────── (+) Submersible Pump Motor
                                                    (-) Submersible Pump Motor ─── GND
                                                    [1N4007 Flyback Diode across motor (+ / -)]
```

### Pin Summary Table

| ESP32 Pin | Sensor / Module | Connection Pin | Voltage Level |
|---|---|---|---|
| **GPIO 34** | Capacitive Soil Moisture v1.2 | `AOUT` | 3.3V Analog Input |
| **GPIO 4** | DHT22 Temp & Humidity | `DATA` (with 10kΩ pullup) | 3.3V Digital I/O |
| **GPIO 35** | LDR Photoresistor | Junction of LDR & 10kΩ | 3.3V Analog Input |
| **GPIO 16** | 5V Relay Module | `IN` | 3.3V Digital Output |
| **3V3** | All Sensor VCC pins | `VCC` | 3.3V Power Rail |
| **GND** | All Sensor GND + Relay GND | `GND` | Ground Reference |

---

## 3. Safe Electrical & Power Guidelines

1. **Common Ground**: Ensure the ESP32 ground and the external 5V pump supply ground are connected together.
2. **Inductive Spike Protection**: Always place a **1N4007 flyback diode** across the DC pump motor terminals (cathode with silver band to `+`, anode to `-`). This eliminates voltage spikes caused by inductive back-EMF when the pump relay switches off.
3. **Dedicated Pump Power**: Do not power the DC water pump directly from the ESP32 3.3V pin. Submersible pump inrush current can exceed 500mA, triggering an ESP32 brownout reboot. Power the pump from a dedicated 5V rail or external battery pack.
4. **Capacitive vs. Resistive Sensors**: Always choose **Capacitive** soil moisture sensors over cheap resistive fork sensors. Resistive sensors undergo rapid electrolysis corrosion within days, ruining readings and contaminating soil.

---

## 4. Calibration Instructions

1. **Dry Air Reading**: Leave the capacitive probe exposed to dry room air. Note the raw ADC value in the Arduino Serial Monitor (typically around `3000 - 3300`). Set `DRY_ADC_VALUE` in the code.
2. **Submerged Reading**: Gently immerse the lower coated part of the sensor probe in a cup of water (do NOT submerge past the white limit line or wet the electronics). Note the raw ADC value (typically around `1400 - 1600`). Set `WET_ADC_VALUE` in the code.
3. The sketch will automatically compute accurate, percentage-scaled moisture values (`0.0%` to `100.0%`).

---

## 5. Seamless Cloud Integration

Because the backend uses a standardized REST API (`POST /api/sensors/data`), the cloud application cannot distinguish between the Python Virtual Simulator and a real physical ESP32 node!
- Both provide identical telemetry contracts.
- Both receive identical cloud decision JSON payloads.
- Both enable complete remote monitoring, automated irrigation, threshold tuning, and audit logging on the dashboard.
