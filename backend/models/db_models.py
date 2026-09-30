"""
Database Models for Cloud-Connected Smart Plant Care & Watering System
Defines SQLAlchemy ORM models representing entities in cloud storage.
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


def generate_uuid() -> str:
    """Generate unique identifier string."""
    return str(uuid.uuid4())


def get_utc_now() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


class User(Base):
    """Represents a system user/gardener managing smart plant devices."""
    __tablename__ = "users"

    user_id = Column(String(64), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=get_utc_now)

    # Relationships
    devices = relationship("Device", back_populates="owner", cascade="all, delete-orphan")


class Device(Base):
    """Represents a physical ESP32 or simulated IoT plant care device node."""
    __tablename__ = "devices"

    device_id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.user_id"), nullable=True)
    plant_name = Column(String(100), nullable=False, default="Tomato Plant")
    plant_type = Column(String(50), nullable=False, default="TOMATO")
    location = Column(String(100), nullable=False, default="Balcony Garden")
    moisture_threshold = Column(Float, nullable=False, default=30.0)
    auto_water_enabled = Column(Boolean, nullable=False, default=True)
    pump_status = Column(String(10), nullable=False, default="OFF")  # ON, OFF
    pump_active_until = Column(DateTime, nullable=True)
    last_watered_at = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, default=get_utc_now, index=True)
    created_at = Column(DateTime, default=get_utc_now)

    # Relationships
    owner = relationship("User", back_populates="devices")
    readings = relationship("SensorReading", back_populates="device", cascade="all, delete-orphan", order_by="desc(SensorReading.timestamp)")
    watering_events = relationship("WateringEvent", back_populates="device", cascade="all, delete-orphan", order_by="desc(WateringEvent.timestamp)")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan", order_by="desc(Alert.created_at)")


class SensorReading(Base):
    """Time-series telemetry readings transmitted from IoT sensors to the cloud."""
    __tablename__ = "sensor_readings"

    reading_id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(64), ForeignKey("devices.device_id"), nullable=False, index=True)
    soil_moisture = Column(Float, nullable=False)  # 0.0 to 100.0 %
    temperature = Column(Float, nullable=False)    # degrees Celsius
    humidity = Column(Float, nullable=False)       # 0.0 to 100.0 %
    light_level = Column(Float, nullable=False, default=50.0)  # 0.0 to 100.0 %
    water_tank_level = Column(Float, nullable=True, default=85.0)  # 0.0 to 100.0 %
    timestamp = Column(DateTime, default=get_utc_now, index=True)

    # Relationships
    device = relationship("Device", back_populates="readings")


class WateringEvent(Base):
    """Audit log of watering actions executed automatically by cloud logic or manually by user."""
    __tablename__ = "watering_events"

    event_id = Column(String(64), primary_key=True, default=generate_uuid)
    device_id = Column(String(64), ForeignKey("devices.device_id"), nullable=False, index=True)
    trigger_type = Column(String(20), nullable=False)  # AUTOMATIC or MANUAL
    moisture_before = Column(Float, nullable=False)
    moisture_after = Column(Float, nullable=True)
    duration_seconds = Column(Integer, nullable=False, default=5)
    timestamp = Column(DateTime, default=get_utc_now, index=True)

    # Relationships
    device = relationship("Device", back_populates="watering_events")


class Alert(Base):
    """System-generated alert notifications regarding plant health or device status."""
    __tablename__ = "alerts"

    alert_id = Column(String(64), primary_key=True, default=generate_uuid)
    device_id = Column(String(64), ForeignKey("devices.device_id"), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)  # LOW_SOIL_MOISTURE, HIGH_TEMPERATURE, LOW_WATER_TANK, DEVICE_OFFLINE
    severity = Column(String(20), nullable=False, default="WARNING")  # INFO, WARNING, CRITICAL
    message = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")  # ACTIVE, ACKNOWLEDGED, RESOLVED
    created_at = Column(DateTime, default=get_utc_now, index=True)

    # Relationships
    device = relationship("Device", back_populates="alerts")
