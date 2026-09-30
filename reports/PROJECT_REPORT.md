# Academic & Technical Project Report

**Project Title:** Cloud-Connected Smart Plant Care & Watering System  
**Discipline:** Cloud Computing & Internet of Things (IoT)  
**Author:** Student Engineering Team  
**Date:** September 2026  
**Repository:** [https://github.com/your-username/Cloud-Connected-Smart-Plant-Care](https://github.com/your-username/Cloud-Connected-Smart-Plant-Care)

---

## 1. Abstract
The "Cloud-Connected Smart Plant Care & Watering System" is an end-to-end cloud-native IoT platform designed to automate precision irrigation, monitor plant microclimates in real-time, eliminate erratic manual watering, and deliver actionable agronomic analytics. The system integrates virtual and physical edge telemetry nodes with a scalable cloud backend built on FastAPI and SQLAlchemy, backed by a real-time reactive dashboard in React. A cloud-hosted automated decision engine utilizes biological plant profiles, hysteresis thresholds, anti-rapid cycling cooldowns, and reservoir safety barriers to control irrigation. The platform includes automated device heartbeat monitoring to detect offline nodes and dispatches multi-tier alert notifications. The system is verified through an automated 21-test test suite and offers zero-cost cloud deployment via Render, Supabase, and Vercel, alongside enterprise AWS/Azure/GCP architectural blueprints.

---

## 2. Introduction
In urban households, commercial greenhouses, and precision agricultural facilities, irregular irrigation remains the primary cause of plant morbidity. Under-watering induces cell dehydration and stomatal closure, stalling photosynthesis. Over-watering suffocates root systems, inducing anaerobic microbial growth and root rot. By combining Internet of Things (IoT) telemetry with modern Cloud Computing architectures, irrigation can transition from guesswork to precision, data-driven automation. This project demonstrates how cloud databases, REST APIs, time-series telemetry analysis, automated decision engines, and web dashboards operate synergistically to solve real-world agricultural challenges.

---

## 3. Problem Statement
Traditional plant irrigation suffers from critical vulnerabilities:
1. **Human Inconsistency:** Gardeners frequently forget scheduled waterings or overcompensate with excessive water volumes.
2. **Lack of Environmental Visibility:** Visual soil inspection fails to gauge subsurface moisture levels, ambient temperature, humidity, or sunlight exposure.
3. **Absence of Remote Telemetry:** When homeowners or greenhouse operators travel, plants remain unattended without remote diagnostics or actuation capabilities.
4. **No Historical Analytics:** Inability to track moisture trends or water consumption prevents optimization of plant growth.

---

## 4. Project Objectives
1. **Perception & Telemetry:** Capture high-frequency soil moisture, temperature, humidity, light, and reservoir level metrics using simulated virtual nodes or physical ESP32 hardware.
2. **Secure Cloud Ingestion:** Implement authenticated RESTful endpoints terminating TLS/HTTPS with schema-validated JSON payloads.
3. **Cloud Database Architecture:** Structure optimized relational and time-series schemas capturing devices, readings, watering events, and alerts.
4. **Intelligent Automation:** Build an agronomic decision engine that actuates pumps based on species-tailored thresholds while preventing short-cycling.
5. **Real-Time Interactive Dashboard:** Deliver a low-latency web UI with live telemetry gauges, historical trend charts, and manual control overrides.
6. **Resilience & Observability:** Integrate device heartbeat monitoring, automated offline detection, and multi-tier health alerts.

---

## 5. Existing Systems vs. Proposed System

| Feature / Metric | Conventional Timer / Manual Care | Basic Arduino Relay System | Proposed Cloud-Connected Platform |
|---|---|---|---|
| **Irrigation Logic** | Fixed schedule timer regardless of rain | Local hardcoded threshold | Dynamic cloud engine with plant profiles |
| **Telemetry Storage**| None | None (volatile RAM) | Cloud-persisted time-series history |
| **Remote Access** | None | Local Bluetooth / Wi-Fi only | Global access via cloud dashboard |
| **Sensor Diagnostics**| None | Serial monitor only | Live charts & automatic offline watchdog |
| **Overwatering Guard**| None | Prone to sensor failure loops | Cooldown hysteresis + reservoir cutoff |
| **Hardware Required**| None / Basic valve | Physical Arduino + relay required | Operates 100% virtual or on real ESP32 |

---

## 6. Cloud Computing Concepts Demonstrated
- **SaaS (Software as a Service):** The end-user web dashboard allowing gardeners to monitor plants and trigger watering from any web browser.
- **PaaS (Platform as a Service):** Backend hosting on managed platforms (Render, Railway, Heroku) abstracting operating system and server maintenance.
- **IaaS (Infrastructure as a Service):** Underlying virtual machines and container compute clusters (AWS EC2, Docker containers).
- **Cloud Database:** Managed persistence using SQLAlchemy ORM supporting both SQLite and cloud-hosted PostgreSQL (Supabase/AWS RDS).
- **Time-Series Data:** Chronologically indexed sensor telemetry enabling historical regression and trend analysis.
- **Serverless & Event-Driven Architecture:** Decoupled evaluation where incoming telemetry events trigger instant evaluation functions.
- **Security & Secrets Management:** Decoupling secrets into environment variables (`.env`) with API key validation for edge devices.
- **Observability:** Centralized structured logging, cloud liveness probes (`GET /api/health`), and automated alert dispatchers.

---

## 7. Industry Relevance & Real-World Use Cases
1. **Precision Farming:** Large-scale center-pivot irrigation systems dynamically adjusting water application based on distributed soil sensors.
2. **Commercial Greenhouses:** Maintaining exact microclimates for delicate crops (e.g., tomatoes, orchids) to maximize crop yield.
3. **Vertical Farming:** High-density urban indoor farming facilities requiring continuous recirculating irrigation monitoring.
4. **Smart Cities & Municipal Landscaping:** Automated irrigation of highway dividers, parks, and botanical conservatories, saving millions of gallons of water.

---

## 8. Hardware & Perception Layer

### Virtual IoT Simulator (Default)
To eliminate hardware barriers for students and evaluators, a complete Python-based simulator (`sensor_simulator/simulator.py`) models:
- Exponential soil moisture decay (drying physics).
- Rapid moisture recovery when the virtual pump is energized.
- Diurnal sinusoidal temperature and inverted humidity curves simulating daylight.
- Cloud command actuation processing (`pump_command: "ON" | "OFF"`).

### Physical Hardware Node (Optional ESP32)
When deployed physically, an ESP32 microcontroller connects to:
- A capacitive soil moisture sensor (corrosion-resistant).
- A DHT22 temperature and humidity sensor.
- An LDR photoresistor circuit.
- An optoisolated 5V relay switching a submersible DC pump with a 1N4007 flyback diode.
The ESP32 communicates over Wi-Fi using the identical JSON schema as the virtual simulator.

---

## 9. Automated Watering Algorithm

```text
Algorithm: Precision Cloud Irrigation Evaluation
Input: Current Reading R(moisture, temp, humidity, tank), Device Configuration D(threshold, auto_water, last_watered)
Output: Decision(should_water: Boolean, pump_command: "ON"|"OFF", duration: Seconds)

1. IF D.auto_water == FALSE THEN
2.     RETURN (FALSE, "OFF", "Automated irrigation disabled by operator")
3. END IF

4. IF R.tank < 10.0% THEN
5.     TriggerAlert(Severity="CRITICAL", Type="LOW_WATER_TANK")
6.     RETURN (FALSE, "OFF", "Water reservoir depleted")
7. END IF

8. IF R.moisture < D.threshold THEN
9.     elapsed = CurrentTime() - D.last_watered
10.    IF elapsed < 60 SECONDS THEN
11.        RETURN (FALSE, "OFF", "Anti-cycling cooldown in effect")
12.    END IF
13.
14.    profile = GetPlantProfile(D.plant_type)
15.    duration = Min(profile.watering_duration, 15 SECONDS)
16.    D.pump_status = "ON"
17.    D.last_watered = CurrentTime()
18.    LogWateringEvent(trigger="AUTOMATIC", moisture_before=R.moisture, duration=duration)
19.    RETURN (TRUE, "ON", duration)
20. ELSE
21.    IF D.pump_status == "ON" THEN
22.        D.pump_status = "OFF"
23.        UpdateLastWateringEvent(moisture_after=R.moisture)
24.    END IF
25.    RETURN (FALSE, "OFF", "Soil moisture within healthy parameters")
26. END IF
```

---

## 10. Verification & Test Results
The test suite consists of 21 automated integration and unit tests implemented in `pytest`, achieving **100% pass rate**:
- **API Tests (`test_api.py`):** Verified health probes, CRUD endpoints, telemetry ingestion validation, manual water overrides, and alert dismissal.
- **Engine Tests (`test_watering_engine.py`):** Verified hysteresis thresholds, anti-cycling cooldowns, reservoir depletion cutoffs, and botanical profiles.
- **Simulator Tests (`test_simulator.py`):** Verified drying decay curves, watering recovery, and payload conformity.

---

## 11. Conclusion
The Cloud-Connected Smart Plant Care & Watering System successfully demonstrates how cloud-native principles, modern API design, and edge telemetry converge into a scalable, industry-standard solution. By providing both a zero-hardware virtual simulation and physical ESP32 firmware, the project offers an accessible, placement-ready showcase of full-stack IoT and cloud engineering.
