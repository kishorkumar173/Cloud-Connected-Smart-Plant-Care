"""
Unit & Logic Tests for Automated Watering Engine
Tests threshold detection, anti-cycling cooldowns, reservoir depletion protection,
and botanical species profiles.
"""

from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.db_models import Base, Device, SensorReading, WateringEvent
from automation.watering_engine import WateringEngine
from automation.plant_profiles import get_plant_profile, PLANT_PROFILES

# Use in-memory SQLite database for deterministic unit testing
test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def setup_module():
    """Create fresh schema."""
    Base.metadata.create_all(bind=test_engine)


def test_watering_triggered_when_moisture_below_threshold():
    """Test ID 14: Engine triggers pump ON when soil drops below threshold."""
    db = TestingSessionLocal()
    try:
        now = datetime.now(timezone.utc)
        dev = Device(
            device_id="TEST-DEV-1",
            plant_name="Test Plant",
            plant_type="TOMATO",
            moisture_threshold=40.0,
            auto_water_enabled=True,
            pump_status="OFF",
            last_watered_at=now - timedelta(hours=2)  # Cooldown passed
        )
        db.add(dev)
        db.commit()

        # Telemetry below threshold (25% < 40%)
        reading = SensorReading(
            device_id="TEST-DEV-1",
            soil_moisture=25.0,
            temperature=26.0,
            humidity=55.0,
            water_tank_level=80.0,
            timestamp=now
        )
        db.add(reading)
        db.commit()

        should_water, pump_cmd, meta = WateringEngine.evaluate_reading(db, dev, reading)

        assert should_water is True
        assert pump_cmd == "ON"
        assert dev.pump_status == "ON"
        assert "event_id" in meta
    finally:
        db.close()


def test_watering_cooldown_prevents_rapid_cycling():
    """Test ID 15: Engine enforces cooldown to prevent overwatering."""
    db = TestingSessionLocal()
    try:
        now = datetime.now(timezone.utc)
        dev = Device(
            device_id="TEST-DEV-2",
            plant_name="Test Plant 2",
            plant_type="TOMATO",
            moisture_threshold=40.0,
            auto_water_enabled=True,
            pump_status="OFF",
            last_watered_at=now - timedelta(seconds=10)  # Cooldown NOT expired
        )
        db.add(dev)
        db.commit()

        reading = SensorReading(
            device_id="TEST-DEV-2",
            soil_moisture=22.0,  # Below threshold
            temperature=26.0,
            humidity=55.0,
            water_tank_level=80.0,
            timestamp=now
        )
        db.add(reading)
        db.commit()

        should_water, pump_cmd, meta = WateringEngine.evaluate_reading(db, dev, reading)

        # Should be blocked by cooldown
        assert should_water is False
        assert pump_cmd == "OFF"
        assert "Cooldown active" in meta.get("reason", "")
    finally:
        db.close()


def test_low_water_tank_blocks_pump():
    """Test ID 16: Depleted reservoir blocks pump to protect hardware from dry burn."""
    db = TestingSessionLocal()
    try:
        now = datetime.now(timezone.utc)
        dev = Device(
            device_id="TEST-DEV-3",
            plant_name="Test Plant 3",
            plant_type="HERB",
            moisture_threshold=35.0,
            auto_water_enabled=True,
            pump_status="OFF",
            last_watered_at=now - timedelta(hours=5)
        )
        db.add(dev)
        db.commit()

        reading = SensorReading(
            device_id="TEST-DEV-3",
            soil_moisture=15.0,
            temperature=26.0,
            humidity=55.0,
            water_tank_level=4.0,  # Depleted tank (<10%)
            timestamp=now
        )
        db.add(reading)
        db.commit()

        should_water, pump_cmd, meta = WateringEngine.evaluate_reading(db, dev, reading)

        assert should_water is False
        assert pump_cmd == "OFF"
        assert "reservoir" in meta.get("reason", "").lower()
    finally:
        db.close()


def test_plant_species_profiles():
    """Test ID 17: Botanical profile mappings return correct thresholds."""
    succulent = get_plant_profile("SUCCULENT")
    assert succulent["default_threshold"] == 20.0

    tomato = get_plant_profile("TOMATO")
    assert tomato["default_threshold"] == 40.0

    herb = get_plant_profile("HERB")
    assert herb["default_threshold"] == 35.0
