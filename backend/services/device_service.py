"""
Device Management & Heartbeat Service
Handles device registration, configuration updates, botanical profile mapping,
and active heartbeat / offline node detection.
"""

from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.models.db_models import Device, SensorReading, Alert
from backend.models.schemas import DeviceCreate, DeviceUpdate
from backend.utils.logger import logger

# Offline threshold: if no telemetry received within this timeframe, flag as offline
OFFLINE_HEARTBEAT_THRESHOLD_SECONDS = 90


class DeviceService:
    """Service layer managing plant monitor devices and heartbeat health."""

    @staticmethod
    def evaluate_online_status(device: Device) -> bool:
        """Determines if device is actively transmitting telemetry."""
        if not device.last_seen:
            return False
        now = datetime.now(timezone.utc)
        last_seen = device.last_seen
        if last_seen.tzinfo is None:
            last_seen = last_seen.replace(tzinfo=timezone.utc)
        return (now - last_seen).total_seconds() <= OFFLINE_HEARTBEAT_THRESHOLD_SECONDS

    @classmethod
    def get_plant_health(cls, db: Session, device: Device) -> str:
        """Computes human-readable operational health status."""
        is_online = cls.evaluate_online_status(device)
        if not is_online:
            return "Offline"

        if device.pump_status == "ON":
            return "Watering Active"

        latest_reading = db.query(SensorReading).filter_by(device_id=device.device_id).order_by(
            SensorReading.timestamp.desc()
        ).first()

        if not latest_reading:
            return "No Data"

        if latest_reading.temperature > 35.0:
            return "Heat Stress"
        elif latest_reading.soil_moisture < device.moisture_threshold:
            return "Needs Water"
        else:
            return "Healthy"

    @classmethod
    def check_and_alert_offline_devices(cls, db: Session) -> List[Device]:
        """
        Background health checker scanning for offline IoT devices.
        Creates an alert if a device has gone dark.
        """
        devices = db.query(Device).all()
        now = datetime.now(timezone.utc)
        offline_devices = []

        for dev in devices:
            is_online = cls.evaluate_online_status(dev)
            if not is_online:
                offline_devices.append(dev)
                # Check if offline alert already active
                existing = db.query(Alert).filter(
                    Alert.device_id == dev.device_id,
                    Alert.alert_type == "DEVICE_OFFLINE",
                    Alert.status == "ACTIVE"
                ).first()

                if not existing:
                    alert = Alert(
                        device_id=dev.device_id,
                        alert_type="DEVICE_OFFLINE",
                        severity="WARNING",
                        message=f"Device {dev.device_id} ({dev.plant_name}) has stopped sending heartbeat signals. Status: OFFLINE.",
                        status="ACTIVE",
                        created_at=now
                    )
                    db.add(alert)
                    logger.warning(f"[{dev.device_id}] HEARTBEAT LOST: Device marked OFFLINE.")
            else:
                # Resolve offline alert if device has come back online
                active_offline_alerts = db.query(Alert).filter(
                    Alert.device_id == dev.device_id,
                    Alert.alert_type == "DEVICE_OFFLINE",
                    Alert.status == "ACTIVE"
                ).all()
                for a in active_offline_alerts:
                    a.status = "RESOLVED"
                    logger.info(f"[{dev.device_id}] Heartbeat restored. Alert {a.alert_id} resolved.")

        db.commit()
        return offline_devices

    @classmethod
    def get_all_devices(cls, db: Session) -> List[Dict[str, Any]]:
        """Return list of all registered devices with computed status fields."""
        cls.check_and_alert_offline_devices(db)
        devices = db.query(Device).all()
        result = []
        for dev in devices:
            result.append({
                "device_id": dev.device_id,
                "plant_name": dev.plant_name,
                "plant_type": dev.plant_type,
                "location": dev.location,
                "moisture_threshold": dev.moisture_threshold,
                "auto_water_enabled": dev.auto_water_enabled,
                "pump_status": dev.pump_status,
                "is_online": cls.evaluate_online_status(dev),
                "plant_health_status": cls.get_plant_health(db, dev),
                "last_seen": dev.last_seen,
                "last_watered_at": dev.last_watered_at,
                "created_at": dev.created_at
            })
        return result

    @classmethod
    def get_device_by_id(cls, db: Session, device_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single device with enriched status."""
        dev = db.query(Device).filter(Device.device_id == device_id).first()
        if not dev:
            return None
        return {
            "device_id": dev.device_id,
            "plant_name": dev.plant_name,
            "plant_type": dev.plant_type,
            "location": dev.location,
            "moisture_threshold": dev.moisture_threshold,
            "auto_water_enabled": dev.auto_water_enabled,
            "pump_status": dev.pump_status,
            "is_online": cls.evaluate_online_status(dev),
            "plant_health_status": cls.get_plant_health(db, dev),
            "last_seen": dev.last_seen,
            "last_watered_at": dev.last_watered_at,
            "created_at": dev.created_at
        }

    @classmethod
    def create_device(cls, db: Session, data: DeviceCreate) -> Device:
        """Register a new plant monitor node."""
        dev = Device(
            device_id=data.device_id,
            plant_name=data.plant_name,
            plant_type=data.plant_type,
            location=data.location or "Garden",
            moisture_threshold=data.moisture_threshold or 30.0,
            auto_water_enabled=data.auto_water_enabled if data.auto_water_enabled is not None else True,
            pump_status="OFF",
            created_at=datetime.now(timezone.utc),
            last_seen=datetime.now(timezone.utc)
        )
        db.add(dev)
        db.commit()
        db.refresh(dev)
        logger.info(f"Registered new device: {dev.device_id} ({dev.plant_name})")
        return dev

    @classmethod
    def update_threshold(cls, db: Session, device_id: str, new_threshold: float) -> Optional[Device]:
        """Update soil moisture trigger threshold."""
        dev = db.query(Device).filter(Device.device_id == device_id).first()
        if dev:
            dev.moisture_threshold = new_threshold
            db.commit()
            db.refresh(dev)
            logger.info(f"[{device_id}] Moisture threshold updated to {new_threshold}%")
        return dev
