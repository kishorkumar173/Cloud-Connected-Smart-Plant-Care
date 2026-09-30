"""
Automated Watering Logic & Decision Engine
Evaluates real-time sensor metrics against agronomic plant rules, hysteresis boundaries,
water reservoir levels, and anti-oscillation cooldowns.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from backend.models.db_models import Device, SensorReading, WateringEvent, Alert
from backend.utils.logger import logger
from automation.plant_profiles import get_plant_profile

# Safety and automation constants
MIN_WATER_TANK_LEVEL_PERCENT = 10.0   # Below this, disable pump to prevent dry run
DEFAULT_COOLDOWN_SECONDS = 60          # Minimum seconds between successive watering cycles
MAX_SINGLE_WATERING_SECONDS = 15      # Hard safety cutoff against stuck relays / flooding


class WateringEngine:
    """Core intelligence engine deciding when and how much to irrigate."""

    @staticmethod
    def evaluate_reading(
        db: Session,
        device: Device,
        reading: SensorReading
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Evaluates incoming telemetry and determines if an automated irrigation command is required.
        Returns: (should_water: bool, pump_command: "ON"|"OFF", metadata: dict)
        """
        now = datetime.now(timezone.utc)
        threshold = device.moisture_threshold
        current_moisture = reading.soil_moisture
        tank_level = reading.water_tank_level if reading.water_tank_level is not None else 100.0

        # Check 1: Auto-watering feature toggle
        if not device.auto_water_enabled:
            return False, "OFF", {"reason": "Automated watering is disabled by user"}

        # Check 2: Water reservoir safety check
        if tank_level < MIN_WATER_TANK_LEVEL_PERCENT:
            logger.warning(
                f"[{device.device_id}] Watering blocked: Water reservoir depleted ({tank_level}% < {MIN_WATER_TANK_LEVEL_PERCENT}%)"
            )
            # Create low reservoir alert if not already active
            existing_alert = db.query(Alert).filter(
                Alert.device_id == device.device_id,
                Alert.alert_type == "LOW_WATER_TANK",
                Alert.status == "ACTIVE"
            ).first()

            if not existing_alert:
                alert = Alert(
                    device_id=device.device_id,
                    alert_type="LOW_WATER_TANK",
                    severity="CRITICAL",
                    message=f"Water reservoir critically low ({tank_level:.1f}%). Refill tank immediately.",
                    status="ACTIVE",
                    created_at=now
                )
                db.add(alert)
                db.commit()

            return False, "OFF", {"reason": "Low water reservoir level"}

        # Check 3: Is soil dry enough to trigger watering? (Hysteresis rule)
        if current_moisture < threshold:
            # Check 4: Anti-Rapid-Cycling Cooldown Period
            if device.last_watered_at:
                # Ensure timezone compatibility
                last_watered = device.last_watered_at
                if last_watered.tzinfo is None:
                    last_watered = last_watered.replace(tzinfo=timezone.utc)

                elapsed_seconds = (now - last_watered).total_seconds()
                if elapsed_seconds < DEFAULT_COOLDOWN_SECONDS:
                    remaining = int(DEFAULT_COOLDOWN_SECONDS - elapsed_seconds)
                    return False, "OFF", {
                        "reason": f"Cooldown active. Waiting {remaining}s for soil absorption before re-watering."
                    }

            # Retrieve species profile for tailored duration
            profile = get_plant_profile(device.plant_type)
            duration = min(profile.get("watering_duration_seconds", 5), MAX_SINGLE_WATERING_SECONDS)

            # Trigger automated watering event
            device.pump_status = "ON"
            device.last_watered_at = now
            device.pump_active_until = now + timedelta(seconds=duration)

            event = WateringEvent(
                device_id=device.device_id,
                trigger_type="AUTOMATIC",
                moisture_before=current_moisture,
                duration_seconds=duration,
                timestamp=now
            )
            db.add(event)
            db.commit()

            logger.info(
                f"[{device.device_id}] AUTO-WATER TRIGGERED: Moisture {current_moisture}% < Threshold {threshold}%. "
                f"Actuating pump for {duration} seconds."
            )

            return True, "ON", {
                "reason": f"Soil moisture {current_moisture}% dropped below {threshold}% threshold.",
                "duration_seconds": duration,
                "event_id": event.event_id
            }

        # If moisture is sufficient and pump is currently ON from an expired cycle, shut it OFF
        if device.pump_status == "ON":
            device.pump_status = "OFF"
            # Update latest watering event with post-irrigation moisture
            latest_event = db.query(WateringEvent).filter_by(device_id=device.device_id).order_by(
                WateringEvent.timestamp.desc()
            ).first()
            if latest_event and latest_event.moisture_after is None:
                latest_event.moisture_after = current_moisture
            db.commit()

        return False, "OFF", {"reason": f"Soil moisture {current_moisture}% is healthy (Threshold: {threshold}%)"}

    @staticmethod
    def trigger_manual_water(
        db: Session,
        device: Device,
        duration_seconds: int = 5
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Executes an immediate manual watering command initiated from the cloud dashboard.
        """
        now = datetime.now(timezone.utc)
        safe_duration = min(max(duration_seconds, 1), MAX_SINGLE_WATERING_SECONDS)

        # Get latest moisture reading
        latest_reading = db.query(SensorReading).filter_by(device_id=device.device_id).order_by(
            SensorReading.timestamp.desc()
        ).first()

        moisture_before = latest_reading.soil_moisture if latest_reading else device.moisture_threshold

        device.pump_status = "ON"
        device.last_watered_at = now
        device.pump_active_until = now + timedelta(seconds=safe_duration)

        event = WateringEvent(
            device_id=device.device_id,
            trigger_type="MANUAL",
            moisture_before=moisture_before,
            duration_seconds=safe_duration,
            timestamp=now
        )
        db.add(event)
        db.commit()

        logger.info(f"[{device.device_id}] MANUAL WATER TRIGGERED: Actuating pump for {safe_duration}s.")
        return True, "ON", {
            "message": f"Manual watering cycle initiated for {safe_duration} seconds.",
            "duration_seconds": safe_duration,
            "event_id": event.event_id
        }
