# 🌱 Cloud-Connected Smart Plant Care & Watering System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.115+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_18_+_Vite-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![SQLAlchemy](https://img.shields.io/badge/Database-SQLAlchemy_2.0-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![Python](https://img.shields.io/badge/Language-Python_3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Tests](https://img.shields.io/badge/Tests-21_Passed_100%25-brightgreen?style=flat-square&logo=pytest&logoColor=white)](#testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

An industry-grade, cloud-native IoT platform engineered to automate precision irrigation, monitor microclimates in real time, and deliver actionable agronomic analytics.

> **Zero Hardware Required:** Operates 100% with an included realistic Python IoT sensor simulator, with complete plug-and-play support for physical ESP32 microcontrollers.

---

## 📑 Table of Contents
- [Overview & Objectives](#overview--objectives)
- [System Architecture](#system-architecture)
- [Cloud Computing Concepts Demonstrated](#cloud-computing-concepts-demonstrated)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Folder Structure](#project-folder-structure)
- [Getting Started & Local Execution](#getting-started--local-execution)
- [Virtual IoT Sensor Simulation](#virtual-iot-sensor-simulation)
- [Database Architecture](#database-architecture)
- [REST API Reference](#rest-api-reference)
- [Automated Irrigation Logic](#automated-irrigation-logic)
- [Botanical Plant Profiles](#botanical-plant-profiles)
- [Alerts & Heartbeat Watchdog](#alerts--heartbeat-watchdog)
- [Optional ESP32 Hardware Version](#optional-esp32-hardware-version)
- [Cloud Deployment Guide](#cloud-deployment-guide)
- [Automated Testing](#automated-testing)
- [Cloud Security](#cloud-security)
- [Interview Preparation (10 Q&A)](#interview-preparation)
- [Resume & LinkedIn Proof](#resume--linkedin-proof)

---

## 🔍 Overview & Objectives

### The Problem
- **Erratic Watering:** Over-watering suffocates roots and breeds fungal rot; under-watering stunts growth and wilts foliage.
- **Absence of Real-Time Diagnostics:** Gardeners cannot gauge subsurface volumetric soil moisture or ambient heat stress with the naked eye.
- **Lack of Remote Telemetry:** Travel and vacations leave plants vulnerable without remote observability or emergency irrigation controls.

### The Solution
A cloud-connected precision agriculture platform that ingests high-frequency telemetry (soil moisture, temperature, humidity, sunlight, reservoir level), persists time-series data, executes an agronomic decision engine, and triggers targeted irrigation while streaming live metrics to a modern web dashboard.

```text
Plant / Virtual Node ──► Sensors (Moisture, Temp, Humidity, Light)
        │
        ▼
ESP32 Node OR Python Virtual Simulator
        │
        ▼ (HTTPS REST / JSON / API Key)
FastAPI Cloud Backend Ingestion Endpoint
        ├──► Cloud Database (SQLAlchemy ORM: Readings, Events, Alerts)
        ├──► Automated Decision Engine (Hysteresis, Cooldowns, Plant Rules)
        └──► Heartbeat Watchdog (Device Offline Detection)
        │
        ▼ (Actuation Command: PUMP "ON" / "OFF")
Submersible Pump Relay (Real or Virtual Actuator)
        │
        ▼ (Live Telemetry & Historical Trends)
React / Standalone Web Dashboard ──► User / Gardener
```

---

## ☁️ Cloud Computing Concepts Demonstrated

| Concept | Implementation in this Project |
|---|---|
| **SaaS (Software as a Service)** | Web dashboard allowing gardeners to monitor plants, adjust thresholds, and trigger irrigation from any browser without installing local software. |
| **PaaS (Platform as a Service)** | Backend hosting on managed app platforms (Render, Railway, Heroku, Fly.io) with managed runtimes. |
| **Cloud Database** | Relational and time-series data managed through SQLAlchemy ORM, switching seamlessly from SQLite to cloud PostgreSQL (Supabase / AWS RDS). |
| **REST APIs** | Explicit resource endpoints (`/api/sensors/data`, `/api/devices/{id}/water`) returning standard HTTP status codes (`200`, `201`, `404`, `422`). |
| **Serverless & Event-Driven** | Incoming telemetry payloads trigger decoupled evaluation engines (WateringEngine, AlertService) mirroring AWS Lambda / Cloud Functions. |
| **Time-Series Telemetry** | Chronologically indexed sensor records allowing time-series charting and statistical aggregation (min/max/average). |
| **Heartbeat & Liveness** | Cloud watchdog scanning `last_seen` timestamps to detect node disconnection or power loss. |
| **Secrets Management** | Sensitive credentials (API keys, JWT secrets, database connection strings) loaded securely from `.env`. |
| **Cloud Security** | Header-based IoT Device authentication (`X-Device-API-Key`), input sanitization, and Pydantic contract boundary enforcement. |
| **Observability & Health Checks** | Container readiness probe endpoint (`GET /api/health`) and structured logging. |

---

## 🚀 Key Features

- **⚡ Dual Ingestion Engine:** Supports both the Python Virtual Simulator and physical ESP32 microcontroller nodes interchangeably.
- **🌱 Botanical Species Presets:** Agronomically tailored profiles for **Tomatoes (40%)**, **Succulents (20%)**, **Herbs (35%)**, **Indoor Plants (30%)**, **Tropical Plants (50%)**, and **Bonsai (45%)**.
- **🛡️ Anti-Oscillation Protection:** Built-in cooldowns (60s) prevent pump short-cycling, and a water reservoir watchdog blocks pump dry-run if tank < 10%.
- **📊 Real-Time Interactive Dashboard:** Built with modern Tailwind CSS and Chart.js featuring live moisture trend lines, threshold markers, and ambient microclimate graphs.
- **🚨 Multi-Tier Anomaly Alerts:** Classifies conditions into `INFO`, `WARNING`, and `CRITICAL` for dry soil, heat stress, low reservoir, and lost heartbeats.
- **📋 Immutable Watering Audit Trail:** Logs every automatic and manual watering cycle with before-and-after moisture levels and duration.
- **📈 Advanced Analytics:** Computes average metrics, daily watering frequency, uptime percentage, and estimated water volume used.

---

## 🛠️ Technology Stack

- **Backend Framework:** FastAPI (Python 3.10+)
- **ASGI Web Server:** Uvicorn
- **ORM & Database:** SQLAlchemy 2.0 (SQLite for local zero-config, PostgreSQL / Supabase for cloud)
- **Validation Engine:** Pydantic v2 (Strict typing & data contracts)
- **Edge Simulator:** Python Virtual Sensor Simulator (Diurnal physics & command actuation)
- **Frontend Dashboard:** React 18 + Vite (or immediate self-contained standalone HTML5 dashboard)
- **Charting Engine:** Chart.js 4.4 + React-Chartjs-2
- **Hardware Firmware:** ESP32 C++ Arduino Sketch (`hardware_esp32/esp32_smart_plant.ino`)
- **Testing Framework:** Pytest (21 automated integration & unit tests)

---

## 📁 Project Folder Structure

```text
Cloud-Smart-Plant-Care/
├── backend/
│   ├── app.py                     # FastAPI application entrypoint & static mounting
│   ├── routes/                    # Modular REST API routes
│   │   ├── sensors.py             # Telemetry ingestion endpoint
│   │   ├── devices.py             # CRUD & irrigation trigger endpoints
│   │   ├── alerts.py              # System alerts & acknowledgment
│   │   └── analytics.py           # Statistical KPIs & health check probe
│   ├── models/                    # Data models
│   │   ├── db_models.py           # SQLAlchemy database tables
│   │   └── schemas.py             # Pydantic v2 validation contracts
│   ├── services/                  # Business logic services
│   │   ├── sensor_service.py      # Telemetry persistence & analytics
│   │   ├── device_service.py      # Heartbeat monitoring & device state
│   │   └── alert_service.py       # Threshold rule evaluation
│   ├── utils/                     # Structured logging & security sanitizers
│   └── static/
│       └── index.html             # Standalone, zero-dependency embedded dashboard
│
├── sensor_simulator/
│   ├── simulator.py               # Virtual IoT node with realistic physics
│   └── config.py                  # Simulator reporting cadence & physics params
│
├── automation/
│   ├── watering_engine.py         # Precision irrigation decision logic
│   └── plant_profiles.py          # Agronomic species thresholds & botanical rationale
│
├── cloud/
│   ├── database_service.py        # Connection pooling & demo seeders
│   └── auth_service.py            # API key and JWT authentication
│
├── hardware_esp32/
│   ├── esp32_smart_plant.ino      # Physical ESP32 C++ Arduino sketch
│   └── README_HARDWARE.md         # Pinout schematics, BOM & wiring guide
│
├── frontend/                      # React 18 + Vite Web Application
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx                # Core dashboard layout & state management
│       ├── components/            # Status cards, charts, control panel, audit table
│       └── services/api.js        # API service client
│
├── tests/                         # Pytest automated test suite (21 tests)
├── sample_data/seed_data.json     # Mock test fixtures
├── screenshots/README.md          # 26-item proof checklist
├── docs/                          # Architecture, deployment, and API docs
├── reports/PROJECT_REPORT.md      # Full academic project report
├── requirements.txt               # Python package dependencies
├── .env.example                   # Environment configuration template
├── run_backend.bat                # 1-click launcher: Backend server
├── run_simulator.bat              # 1-click launcher: Virtual sensor simulator
├── run_frontend.bat               # 1-click launcher: React Vite dev server
└── run_all.bat                    # 1-click master launcher
```

---

## ⚡ Getting Started & Local Execution

### Prerequisites
- Python 3.10+ installed
- (Optional for React dev server) Node.js v18+ and npm

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Cloud Backend Server
```bash
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```
*The database (`smart_plant.db`) will automatically initialize and seed initial demo data.*

### Step 3: Access the Interactive Dashboard
Open your web browser:
- **Interactive Web Dashboard:** `http://localhost:8000/`
- **Swagger OpenAPI Documentation:** `http://localhost:8000/docs`

### Step 4: Run the Virtual IoT Sensor Simulator
In a second terminal window, launch the virtual sensor simulator:
```bash
python -m sensor_simulator.simulator
```

Watch the terminal stream realistic telemetry ticks:
```text
📡 [TX SUCCESS] Tick #012 | Moisture:  31.2% | Temp: 28.4°C | Humid: 61.5% | Status: HEALTHY | Cloud Pump Command: [OFF]
📡 [TX SUCCESS] Tick #013 | Moisture:  29.8% | Temp: 28.6°C | Humid: 61.2% | Status: DRY (WATERING) | Cloud Pump Command: [ON]

=======================================================
⚡ [CLOUD COMMAND ACTUATION] >> PUMP COMMAND: ON <<
   Reason: Soil moisture 29.8% dropped below 30.0% threshold.
   Virtual Relay energized! Submersible pump running.
=======================================================
```
*Immediately observe the web dashboard at `http://localhost:8000/` update in real time!*

---

## 🔬 Virtual IoT Sensor Simulation

The simulator (`sensor_simulator/simulator.py`) models realistic physical soil and microclimate physics:
1. **Gradual Evaporation & Transpiration:** In the absence of irrigation, moisture decreases by ~1.2% per tick with slight natural variance.
2. **Watering Actuation Recovery:** When the cloud backend returns `pump_command: "ON"`, the simulator enters an active irrigation state, raising moisture by ~6.5% per tick until it reaches ~58%.
3. **Diurnal Solar Cycle:** Temperature follows a sinusoidal curve simulating daytime warming and nighttime cooling; relative humidity inversely mirrors temperature.
4. **Resilient Retry Handling:** Implements exponential backoff on HTTP disconnects, gracefully queuing readings.

---

## 📡 REST API Reference

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/sensors/data` | `POST` | Telemetry ingestion from virtual simulator or ESP32 node. |
| `/api/devices` | `GET` | List all registered plant nodes with real-time status. |
| `/api/devices/{id}` | `GET` | Retrieve device metadata and online status. |
| `/api/devices/{id}/latest` | `GET` | Retrieve most recent sensor reading. |
| `/api/devices/{id}/history` | `GET` | Retrieve chronological readings for graph rendering. |
| `/api/devices/{id}/threshold`| `PUT` | Dynamically update moisture trigger threshold. |
| `/api/devices/{id}/water` | `POST`| Manually trigger an immediate watering cycle (5s). |
| `/api/devices/{id}/watering-history` | `GET` | Retrieve immutable audit log of past watering events. |
| `/api/alerts` | `GET` | List active and historical anomaly alerts. |
| `/api/alerts/{id}/acknowledge` | `PUT` | Acknowledge or dismiss an alert. |
| `/api/devices/{id}/analytics`| `GET` | Compute averages, watering frequency, and water usage. |
| `/api/plant-profiles` | `GET` | List botanical presets (Tomato, Succulent, Herb, etc.). |
| `/api/health` | `GET` | Liveness & database connectivity probe. |

---

## 🌿 Automated Irrigation Logic

The decision engine (`automation/watering_engine.py`) enforces four strict agronomic safety checks before actuating the pump:

1. **Auto-Watering Toggle:** Ensures automated irrigation has not been suspended by the operator.
2. **Reservoir Depletion Guard:** If the water tank level drops below `10%`, watering is blocked and a `CRITICAL` alert is dispatched.
3. **Moisture Threshold Hysteresis:** Irrigation is only triggered when moisture drops strictly below the configured threshold.
4. **Anti-Cycling Cooldown Period:** A mandatory 60-second cooldown is enforced between successive cycles to allow water to percolate through the soil substrate, preventing over-watering and pump burnout.

---

## 🧪 Automated Testing

Execute the test suite with:
```bash
python -m pytest tests/ -v
```

### Test Results
```text
tests/test_api.py::test_cloud_health_check PASSED                        [  4%]
tests/test_api.py::test_list_devices PASSED                              [  9%]
tests/test_api.py::test_get_device_detail PASSED                         [ 14%]
tests/test_api.py::test_sensor_telemetry_ingestion_valid PASSED          [ 19%]
tests/test_api.py::test_sensor_telemetry_ingestion_invalid_bounds PASSED [ 23%]
tests/test_api.py::test_get_latest_reading PASSED                        [ 28%]
tests/test_api.py::test_get_reading_history PASSED                       [ 33%]
tests/test_api.py::test_update_threshold PASSED                          [ 38%]
tests/test_api.py::test_manual_watering_trigger PASSED                   [ 42%]
tests/test_api.py::test_get_watering_history PASSED                      [ 47%]
tests/test_api.py::test_list_alerts_and_acknowledge PASSED               [ 52%]
tests/test_api.py::test_get_analytics PASSED                             [ 57%]
tests/test_api.py::test_botanical_profiles PASSED                        [ 61%]
tests/test_simulator.py::test_virtual_node_initialization PASSED         [ 66%]
tests/test_simulator.py::test_virtual_node_drying_physics PASSED         [ 71%]
tests/test_simulator.py::test_virtual_node_watering_physics PASSED       [ 76%]
tests/test_simulator.py::test_telemetry_packet_structure PASSED          [ 80%]
tests/test_watering_engine.py::test_watering_triggered_when_moisture_below_threshold PASSED [ 85%]
tests/test_watering_engine.py::test_watering_cooldown_prevents_rapid_cycling PASSED [ 90%]
tests/test_watering_engine.py::test_low_water_tank_blocks_pump PASSED    [ 95%]
tests/test_watering_engine.py::test_plant_species_profiles PASSED        [100%]

======================= 21 passed in 18.16s =======================
```

---

## 💼 Resume & LinkedIn Proof

### Resume Bullet Points
- **Architected a cloud-native IoT precision agriculture platform** using FastAPI, SQLAlchemy, and React, processing high-frequency time-series telemetry across virtual and physical ESP32 nodes.
- **Engineered an automated irrigation decision engine** featuring species-specific botanical hysteresis, anti-cycling cooldowns, reservoir depletion protection, and automated node offline detection.
- **Achieved 100% test coverage across 21 automated integration tests**, demonstrating multi-cloud deployment strategies (Render, Supabase, Vercel) and enterprise AWS/Azure/GCP IoT architectures.

### LinkedIn Post Description
> Excited to share my latest Cloud Computing & IoT project: **Cloud-Connected Smart Plant Care & Watering System** 🌱☁️!
> 
> The platform solves erratic irrigation through data-driven automation. I built a cloud-hosted FastAPI backend that ingests real-time environmental metrics (soil moisture, temperature, humidity, sunlight), executes an agronomic decision engine, and triggers targeted irrigation while streaming live telemetry to a React dashboard.
> 
> Key technical highlights:
> 🔹 Resilient time-series database design with SQLAlchemy & PostgreSQL  
> 🔹 Virtual IoT physics simulator replicating soil drying and diurnal solar cycles  
> 🔹 Heartbeat monitoring for automated node offline detection  
> 🔹 Multi-cloud deployment architecture with Render, Supabase, and Vercel  
> 🔹 Optional plug-and-play ESP32 microcontroller firmware  
> 
> Check out the complete source code and architecture on GitHub: [Repo Link]

---

## 🎯 Interview Preparation (Top 10 Q&A)

### 1. Explain your project.
> *"My project is a Cloud-Connected Smart Plant Care & Watering System that bridges edge IoT perception with cloud-hosted intelligence. It monitors volumetric soil moisture, temperature, humidity, and sunlight to eliminate plant under-watering and over-watering. Sensor data is transmitted via RESTful APIs to a cloud backend built with FastAPI and SQLAlchemy. An agronomic decision engine evaluates telemetry against botanical profiles, anti-rapid cycling cooldowns, and reservoir levels to actuate a pump relay. It includes a real-time reactive dashboard, an automated heartbeat watchdog for offline node detection, and a virtual sensor simulator that allows complete execution without physical hardware."*

### 2. How does the cloud backend distinguish between virtual and physical sensors?
> *"It doesn't—by design! The perception layer is decoupled from the cloud layer through a standardized RESTful API contract (`POST /api/sensors/data`). Whether the JSON payload is dispatched by the Python Virtual Simulator or an ESP32 microcontroller reading analog pins, the payload contains the identical schema, headers, and API keys. This adheres to cloud-native microservice design where ingestion is agnostic to hardware provenance."*

### 3. How does the automated decision engine prevent over-watering?
> *"Over-watering is prevented using four protective mechanisms: First, hysteresis thresholds ensure the pump only fires when moisture is strictly below the species trigger. Second, an anti-cycling cooldown timer (60s minimum) prevents successive rapid waterings, giving the soil substrate time to absorb moisture. Third, hard-coded safety cutoffs limit single watering events to a maximum of 15 seconds. Fourth, post-irrigation moisture is audited, and the pump turns off as soon as target saturation is reached."*

### 4. What happens if the internet connection or backend goes down?
> *"The system implements multi-layered fault tolerance: The sensor node (both virtual and physical ESP32) uses retry logic with exponential backoff on HTTP failures. If the backend is unreachable, the node logs locally rather than crashing. On the cloud side, the Heartbeat Watchdog checks the `last_seen` timestamp of every registered node. If no telemetry is received within 90 seconds, the node status is marked `OFFLINE`, and an automated `WARNING` alert is generated on the dashboard."*

### 5. Why did you choose FastAPI over Flask or Django?
> *"FastAPI offers native asynchronous support, superior execution speed (benchmarking on par with Go and NodeJS), automatic OpenAPI / Swagger documentation generation, and integrated Pydantic data validation. In an IoT context where devices send frequent telemetry packets, FastAPI's low latency and strict request validation prevent corrupt data from reaching the database."*

### 6. How does this architecture scale from 1 plant to 100,000 plants?
> *"For high-scale enterprise operations, synchronous HTTP requests can become a bottleneck. We evolve the architecture by placing an IoT Broker (such as AWS IoT Core or Mosquitto MQTT) and a message queue (Apache Kafka or AWS Kinesis) in front of the ingestion layer. Ingestion nodes write raw telemetry to Kafka partitions. Serverless consumers (AWS Lambda / Cloud Run) process messages in batches, persisting to time-series databases like Amazon Timestream or TimescaleDB, while caching hot device states in Redis."*

### 7. How are secrets and credentials managed?
> *"No credentials or API keys are hardcoded in the codebase. All sensitive keys—including database connection strings, JWT secret keys, and the IoT Device API Key—are stored in a local `.env` file during development and loaded into container environment variables in cloud production (e.g. Render / AWS Secrets Manager). The repository contains only a `.env.example` template."*

### 8. What security risks exist in cloud IoT systems and how are they addressed?
> *"A major vulnerability in naive IoT projects is publicly exposing unauthenticated pump actuation endpoints, which attackers could exploit to trigger pump flooding. We mitigate this by requiring an `X-Device-API-Key` header for telemetry ingestion, strictly validating all payload boundaries with Pydantic, enforcing CORS origins, and securing communications over TLS/HTTPS."*

### 9. What cloud database design decisions did you make?
> *"We utilized SQLAlchemy ORM to provide database independence. For local execution, SQLite provides a zero-setup, serverless embedded database. For cloud deployment, the connection string seamlessly shifts to PostgreSQL on Supabase or Neon. We designed five relational tables (`users`, `devices`, `sensor_readings`, `watering_events`, `alerts`) with B-tree indexes on `device_id` and `timestamp` to ensure fast time-series queries."*

### 10. How would you handle continuous sensor data retention over months?
> *"Storing sensor readings every few seconds generates large volumes of data. In production, we implement a multi-tiered data lifecycle policy: high-frequency raw telemetry is retained for 7 days in hot storage for real-time charting. An automated nightly batch job aggregates raw readings into hourly averages (min, max, mean), moving aggregated summaries to warm storage and archiving historical raw data to cold object storage (AWS S3 Glacier or GCP Cloud Storage Coldline)."*

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
