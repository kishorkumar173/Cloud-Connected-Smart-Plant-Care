# REST API Specification & Endpoint Documentation

The Smart Plant Care platform exposes RESTful endpoints with strict Pydantic v2 schemas and JSON contracts.

Interactive Swagger UI is available at `http://localhost:8000/docs` and ReDoc at `http://localhost:8000/redoc`.

---

## 1. Summary of Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/sensors/data` | Ingest real-time telemetry from simulator / ESP32 | `X-Device-API-Key` (Optional locally) |
| `GET` | `/api/devices` | List all registered plant nodes with live status | None |
| `POST` | `/api/devices` | Register a new plant monitoring node | None |
| `GET` | `/api/devices/{id}` | Retrieve specific device metadata & operational state | None |
| `PUT` | `/api/devices/{id}` | Update device configuration (species, auto-water) | None |
| `GET` | `/api/devices/{id}/latest` | Fetch most recent telemetry reading | None |
| `GET` | `/api/devices/{id}/history` | Fetch chronological time-series telemetry records | None |
| `PUT` | `/api/devices/{id}/threshold` | Update soil moisture trigger threshold | None |
| `POST` | `/api/devices/{id}/water` | Trigger immediate manual watering cycle | None |
| `GET` | `/api/devices/{id}/watering-history`| Retrieve audit history of watering events | None |
| `GET` | `/api/alerts` | List system alerts (optionally filtered by device) | None |
| `PUT` | `/api/alerts/{id}/acknowledge`| Acknowledge or resolve an active alert | None |
| `GET` | `/api/devices/{id}/analytics` | Compute statistical KPIs & water consumption | None |
| `GET` | `/api/plant-profiles` | List botanical species presets and agronomic rules | None |
| `GET` | `/api/health` | Service liveness & database connectivity probe | None |

---

## 2. In-Depth Endpoint Contracts

### `POST /api/sensors/data`
**Description:** Primary telemetry ingestion gateway for virtual simulators and physical ESP32 nodes.

**Request Headers:**
```http
Content-Type: application/json
X-Device-API-Key: plant-iot-cloud-api-key-998877
```

**Request Body:**
```json
{
  "device_id": "PLANT-001",
  "soil_moisture": 28.5,
  "temperature": 29.4,
  "humidity": 61.0,
  "light_level": 72.0,
  "water_tank_level": 82.0,
  "timestamp": "2026-09-30T10:30:00Z"
}
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Telemetry reading ingested successfully",
  "reading_id": 42,
  "pump_command": "ON",
  "watering_triggered": true,
  "current_moisture": 28.5,
  "threshold": 30.0,
  "decision_metadata": {
    "reason": "Soil moisture 28.5% dropped below 30.0% threshold.",
    "duration_seconds": 5,
    "event_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
  }
}
```

---

### `PUT /api/devices/{id}/threshold`
**Description:** Configures moisture percentage trigger level.

**Request Body:**
```json
{
  "moisture_threshold": 38.0
}
```

**Response (200 OK):**
```json
{
  "device_id": "PLANT-001",
  "plant_name": "Roma Tomato Plant",
  "plant_type": "TOMATO",
  "location": "Balcony Greenzone",
  "moisture_threshold": 38.0,
  "auto_water_enabled": true,
  "pump_status": "OFF",
  "is_online": true,
  "plant_health_status": "Healthy",
  "last_seen": "2026-09-30T10:30:00Z",
  "last_watered_at": "2026-09-30T06:30:00Z",
  "created_at": "2026-09-25T10:00:00Z"
}
```

---

### `POST /api/devices/{id}/water`
**Description:** Manually initiates a 5-second (configurable up to 30s) watering cycle.

**Request Body:**
```json
{
  "duration_seconds": 5
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "pump_command": "ON",
  "device_id": "PLANT-001",
  "details": {
    "message": "Manual watering cycle initiated for 5 seconds.",
    "duration_seconds": 5,
    "event_id": "c1f7375e-cf37-4d9f-a89c-48280f24951d"
  }
}
```
