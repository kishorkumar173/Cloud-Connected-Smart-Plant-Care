"""
Alert Management Service
Monitors environmental bounds, generates classified notifications, tracks resolution status,
and dispatches simulated notification webhooks.
"""

from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.db_models import Alert, Device, SensorReading
from backend.utils.logger import logger

TEMP_CRITICAL_HIGH = 38.0  # °C
TEMP_WARNING_HIGH = 33.0   # °C
MOISTURE_CRITICAL_LOW = 15.0  # %


class AlertService:
    """Detects anomalies and manages system alerts."""

    @staticmethod
    def evaluate_telemetry_alerts(db: Session, device: Device, reading: SensorReading) -> List[Alert]:
        """
        Scans incoming sensor data against critical safety thresholds.
        Emits new alerts if conditions breached and not currently active.
        """
        now = datetime.now(timezone.utc)
        new_alerts = []

        # 1. Check Critical Low Soil Moisture
        if reading.soil_moisture < MOISTURE_CRITICAL_LOW:
            existing = db.query(Alert).filter(
                Alert.device_id == device.device_id,
                Alert.alert_type == "LOW_SOIL_MOISTURE",
                Alert.status == "ACTIVE"
            ).first()

            if not existing:
                alert = Alert(
                    device_id=device.device_id,
                    alert_type="LOW_SOIL_MOISTURE",
                    severity="CRITICAL",
                    message=f"{device.plant_name} soil moisture is critically low at {reading.soil_moisture:.1f}% (Threshold: {device.moisture_threshold}%). Immediate watering required!",
                    status="ACTIVE",
                    created_at=now
                )
                db.add(alert)
                new_alerts.append(alert)
                logger.warning(f"[{device.device_id}] ALERT TRIGGERED: {alert.message}")

        # 2. Check High Ambient Temperature
        if reading.temperature >= TEMP_CRITICAL_HIGH:
            existing = db.query(Alert).filter(
                Alert.device_id == device.device_id,
                Alert.alert_type == "HIGH_TEMPERATURE",
                Alert.status == "ACTIVE"
            ).first()

            if not existing:
                alert = Alert(
                    device_id=device.device_id,
                    alert_type="HIGH_TEMPERATURE",
                    severity="CRITICAL",
                    message=f"Dangerous heat detected: {reading.temperature:.1f}°C exceeds heat stress threshold ({TEMP_CRITICAL_HIGH}°C)!",
                    status="ACTIVE",
                    created_at=now
                )
                db.add(alert)
                new_alerts.append(alert)
                logger.warning(f"[{device.device_id}] ALERT TRIGGERED: {alert.message}")
        elif reading.temperature >= TEMP_WARNING_HIGH:
            existing = db.query(Alert).filter(
                Alert.device_id == device.device_id,
                Alert.alert_type == "HIGH_TEMPERATURE",
                Alert.status == "ACTIVE"
            ).first()

            if not existing:
                alert = Alert(
                    device_id=device.device_id,
                    alert_type="HIGH_TEMPERATURE",
                    severity="WARNING",
                    message=f"Elevated temperature detected: {reading.temperature:.1f}°C for {device.plant_name}.",
                    status="ACTIVE",
                    created_at=now
                )
                db.add(alert)
                new_alerts.append(alert)

        # 3. Check Water Tank Level (if sensor provided)
        if reading.water_tank_level is not None and reading.water_tank_level < 15.0:
            existing = db.query(Alert).filter(
                Alert.device_id == device.device_id,
                Alert.alert_type == "LOW_WATER_TANK",
                Alert.status == "ACTIVE"
            ).first()

            if not existing:
                alert = Alert(
                    device_id=device.device_id,
                    alert_type="LOW_WATER_TANK",
                    severity="WARNING",
                    message=f"Reservoir tank level low ({reading.water_tank_level:.1f}%). Refill soon.",
                    status="ACTIVE",
                    created_at=now
                )
                db.add(alert)
                new_alerts.append(alert)

        # Auto-resolve moisture alerts if moisture has recovered
        if reading.soil_moisture >= device.moisture_threshold:
            active_moisture_alerts = db.query(Alert).filter(
                Alert.device_id == device.device_id,
                Alert.alert_type == "LOW_SOIL_MOISTURE",
                Alert.status == "ACTIVE"
            ).all()
            for a in active_moisture_alerts:
                a.status = "RESOLVED"
                logger.info(f"[{device.device_id}] Soil moisture recovered. Alert {a.alert_id} marked RESOLVED.")

        if new_alerts:
            db.commit()

        return new_alerts

    @staticmethod
    def get_alerts(db: Session, device_id: Optional[str] = None, limit: int = 50) -> List[Alert]:
        """Fetch alert history, optionally filtered by device."""
        query = db.query(Alert)
        if device_id:
            query = query.filter(Alert.device_id == device_id)
        return query.order_by(Alert.created_at.desc()).limit(limit).all()

    @staticmethod
    def acknowledge_alert(db: Session, alert_id: str, new_status: str = "ACKNOWLEDGED") -> Optional[Alert]:
        """Mark an alert as acknowledged or dismissed by the operator."""
        alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
        if alert:
            alert.status = new_status
            db.commit()
            db.refresh(alert)
        return alert
