"""
Cloud Database Service
Manages database connection pooling, table schemas, initialization, and session lifetimes.
Seamlessly switches between local SQLite (zero-config student setup) and managed cloud
databases (PostgreSQL, Supabase, Neon, AWS RDS, Google Cloud SQL).
"""

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.models.db_models import Base, User, Device, SensorReading, WateringEvent, Alert

# Resolve base project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Cloud or local Database URL
# Example SQLite: sqlite:///./smart_plant.db
# Example Cloud Postgres: postgresql+psycopg2://user:pass@db.supabase.co:5432/postgres
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'smart_plant.db'}")

# SQLite requires check_same_thread=False for multi-threaded FastAPI workers
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a transactional database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(seed_demo: bool = True) -> None:
    """
    Creates database tables and seeds initial sample records for placement-ready demonstrations.
    """
    Base.metadata.create_all(bind=engine)

    if not seed_demo:
        return

    db = SessionLocal()
    try:
        # Check if default user exists
        user = db.query(User).filter_by(email="gardener@cloudplants.io").first()
        if not user:
            user = User(
                user_id="USER-001",
                name="Alex Cloud Gardener",
                email="gardener@cloudplants.io",
                created_at=datetime.now(timezone.utc) - timedelta(days=7)
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Check if primary demo device exists
        device = db.query(Device).filter_by(device_id="PLANT-001").first()
        if not device:
            device = Device(
                device_id="PLANT-001",
                user_id=user.user_id,
                plant_name="Roma Tomato Plant",
                plant_type="TOMATO",
                location="Balcony Greenzone",
                moisture_threshold=30.0,
                auto_water_enabled=True,
                pump_status="OFF",
                last_seen=datetime.now(timezone.utc),
                last_watered_at=datetime.now(timezone.utc) - timedelta(hours=4),
                created_at=datetime.now(timezone.utc) - timedelta(days=5)
            )
            db.add(device)
            db.commit()

            # Seed a second device for multi-device demonstration
            device2 = Device(
                device_id="PLANT-002",
                user_id=user.user_id,
                plant_name="Aloe Vera Succulent",
                plant_type="SUCCULENT",
                location="Study Desk",
                moisture_threshold=20.0,
                auto_water_enabled=True,
                pump_status="OFF",
                last_seen=datetime.now(timezone.utc) - timedelta(minutes=1),
                last_watered_at=datetime.now(timezone.utc) - timedelta(days=2),
                created_at=datetime.now(timezone.utc) - timedelta(days=5)
            )
            db.add(device2)
            db.commit()

        # Seed realistic historical readings if table is empty
        readings_count = db.query(SensorReading).count()
        if readings_count == 0:
            now = datetime.now(timezone.utc)
            sample_readings = []
            # Generate 24 historical data points (last 12 hours, 30 min intervals)
            for i in range(24, 0, -1):
                t = now - timedelta(minutes=i * 30)
                # Simulated daytime sine-like temperature and declining moisture
                hour_fraction = (t.hour + t.minute / 60.0) / 24.0
                temp = 22.0 + 8.0 * (0.5 - abs(hour_fraction - 0.5) * 2) + (i % 3) * 0.4
                humidity = 75.0 - (temp - 20.0) * 1.8
                light = max(5.0, 90.0 * max(0.0, 1.0 - abs(hour_fraction - 0.5) * 2.8))
                # Moisture declining towards 32%
                moisture = 48.0 - (24 - i) * 0.7
                if moisture < 28.0:
                    moisture = 28.0

                sample_readings.append(SensorReading(
                    device_id="PLANT-001",
                    soil_moisture=round(moisture, 1),
                    temperature=round(temp, 1),
                    humidity=round(humidity, 1),
                    light_level=round(light, 1),
                    water_tank_level=82.0,
                    timestamp=t
                ))

            db.bulk_save_objects(sample_readings)

            # Seed past watering event
            past_event = WateringEvent(
                device_id="PLANT-001",
                trigger_type="AUTOMATIC",
                moisture_before=28.5,
                moisture_after=52.0,
                duration_seconds=5,
                timestamp=now - timedelta(hours=4)
            )
            db.add(past_event)

            # Seed an informational alert
            info_alert = Alert(
                device_id="PLANT-001",
                alert_type="SYSTEM_INITIALIZED",
                severity="INFO",
                message="Smart Plant Care Cloud Node connected and telemetry activated.",
                status="RESOLVED",
                created_at=now - timedelta(hours=12)
            )
            db.add(info_alert)
            db.commit()

    finally:
        db.close()
