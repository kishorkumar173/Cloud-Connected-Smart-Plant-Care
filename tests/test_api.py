"""
Automated Integration Tests for REST API Endpoints
Uses FastAPI TestClient to validate contracts, HTTP status codes, and database mutations.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app import app
from cloud.database_service import init_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    """Ensure database is seeded before running tests."""
    init_db(seed_demo=True)


def test_cloud_health_check():
    """Test ID 1: Cloud health and readiness probe."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "degraded")
    assert "database" in data


def test_list_devices():
    """Test ID 2: Retrieve registered devices."""
    response = client.get("/api/devices")
    assert response.status_code == 200
    devices = response.json()
    assert isinstance(devices, list)
    assert len(devices) >= 1
    assert any(d["device_id"] == "PLANT-001" for d in devices)


def test_get_device_detail():
    """Test ID 3: Retrieve single device metadata."""
    response = client.get("/api/devices/PLANT-001")
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == "PLANT-001"
    assert "moisture_threshold" in data
    assert "plant_health_status" in data


def test_sensor_telemetry_ingestion_valid():
    """Test ID 4: Ingest valid sensor telemetry."""
    payload = {
        "device_id": "PLANT-001",
        "soil_moisture": 35.5,
        "temperature": 27.2,
        "humidity": 65.0,
        "light_level": 70.0,
        "water_tank_level": 85.0
    }
    response = client.post("/api/sensors/data", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "pump_command" in data
    assert "reading_id" in data


def test_sensor_telemetry_ingestion_invalid_bounds():
    """Test ID 5: Ingest invalid sensor reading (negative moisture) - should fail 422."""
    payload = {
        "device_id": "PLANT-001",
        "soil_moisture": -10.0,  # Invalid: ge=0.0
        "temperature": 25.0,
        "humidity": 50.0
    }
    response = client.post("/api/sensors/data", json=payload)
    assert response.status_code == 422


def test_get_latest_reading():
    """Test ID 6: Retrieve latest sensor reading."""
    response = client.get("/api/devices/PLANT-001/latest")
    assert response.status_code == 200
    reading = response.json()
    assert reading["device_id"] == "PLANT-001"
    assert "soil_moisture" in reading


def test_get_reading_history():
    """Test ID 7: Retrieve historical readings."""
    response = client.get("/api/devices/PLANT-001/history?limit=10")
    assert response.status_code == 200
    readings = response.json()
    assert isinstance(readings, list)
    assert len(readings) <= 10


def test_update_threshold():
    """Test ID 8: Update soil moisture threshold."""
    payload = {"moisture_threshold": 38.0}
    response = client.put("/api/devices/PLANT-001/threshold", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["moisture_threshold"] == 38.0


def test_manual_watering_trigger():
    """Test ID 9: Trigger manual watering."""
    payload = {"duration_seconds": 4}
    response = client.post("/api/devices/PLANT-001/water", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["pump_command"] == "ON"


def test_get_watering_history():
    """Test ID 10: Retrieve watering event audit logs."""
    response = client.get("/api/devices/PLANT-001/watering-history?limit=5")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    assert len(events) >= 1


def test_list_alerts_and_acknowledge():
    """Test ID 11: List alerts and acknowledge an active alert."""
    response = client.get("/api/alerts")
    assert response.status_code == 200
    alerts = response.json()
    assert isinstance(alerts, list)

    if len(alerts) > 0:
        alert_id = alerts[0]["alert_id"]
        ack_res = client.put(f"/api/alerts/{alert_id}/acknowledge", json={"status": "ACKNOWLEDGED"})
        assert ack_res.status_code == 200
        assert ack_res.json()["status"] == "ACKNOWLEDGED"


def test_get_analytics():
    """Test ID 12: Retrieve analytical KPIs."""
    response = client.get("/api/devices/PLANT-001/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "avg_soil_moisture" in data
    assert "total_watering_events" in data
    assert "estimated_water_used_liters" in data


def test_botanical_profiles():
    """Test ID 13: Retrieve species botanical profiles."""
    response = client.get("/api/plant-profiles")
    assert response.status_code == 200
    profiles = response.json()
    assert isinstance(profiles, list)
    assert len(profiles) >= 4
