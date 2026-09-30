"""
Device Management & Irrigation Control REST API Routes
Provides full CRUD, configuration management, and irrigation trigger endpoints.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from cloud.database_service import get_db
from backend.models.db_models import Device, WateringEvent
from backend.models.schemas import (
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse,
    ThresholdUpdateRequest,
    WateringRequest,
    WateringEventResponse,
    SensorReadingResponse
)
from backend.services.device_service import DeviceService
from backend.services.sensor_service import SensorService
from automation.watering_engine import WateringEngine

router = APIRouter(prefix="/api/devices", tags=["Devices & Irrigation"])


@router.get("", response_model=List[DeviceResponse])
def list_devices(db: Session = Depends(get_db)):
    """List all registered plant monitoring nodes with online and health status."""
    return DeviceService.get_all_devices(db)


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def register_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    """Register a new IoT plant monitoring node."""
    existing = db.query(Device).filter(Device.device_id == payload.device_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Device '{payload.device_id}' is already registered."
        )
    dev = DeviceService.create_device(db, payload)
    return DeviceService.get_device_by_id(db, dev.device_id)


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: str, db: Session = Depends(get_db)):
    """Retrieve detailed metadata and live operational state for a specific device."""
    dev = DeviceService.get_device_by_id(db, device_id)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return dev


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(device_id: str, payload: DeviceUpdate, db: Session = Depends(get_db)):
    """Update plant name, species type, location, or automated watering toggle."""
    dev = db.query(Device).filter(Device.device_id == device_id).first()
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    if payload.plant_name is not None:
        dev.plant_name = payload.plant_name
    if payload.plant_type is not None:
        dev.plant_type = payload.plant_type
    if payload.location is not None:
        dev.location = payload.location
    if payload.moisture_threshold is not None:
        dev.moisture_threshold = payload.moisture_threshold
    if payload.auto_water_enabled is not None:
        dev.auto_water_enabled = payload.auto_water_enabled

    db.commit()
    return DeviceService.get_device_by_id(db, device_id)


@router.get("/{device_id}/latest", response_model=Optional[SensorReadingResponse])
def get_latest_reading(device_id: str, db: Session = Depends(get_db)):
    """Retrieve the most recent telemetry reading captured from the plant node."""
    reading = SensorService.get_latest_reading(db, device_id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No telemetry readings found for device {device_id}."
        )
    return reading


@router.get("/{device_id}/history", response_model=List[SensorReadingResponse])
def get_reading_history(
    device_id: str,
    limit: int = Query(50, ge=5, le=500, description="Max readings to retrieve"),
    db: Session = Depends(get_db)
):
    """Retrieve chronologically ordered time-series telemetry records for plotting graphs."""
    return SensorService.get_reading_history(db, device_id, limit=limit)


@router.put("/{device_id}/threshold", response_model=DeviceResponse)
def update_moisture_threshold(
    device_id: str,
    payload: ThresholdUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update moisture trigger threshold used by the automated watering engine."""
    dev = DeviceService.update_threshold(db, device_id, payload.moisture_threshold)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return DeviceService.get_device_by_id(db, device_id)


@router.post("/{device_id}/water")
def trigger_manual_watering(
    device_id: str,
    payload: Optional[WateringRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Manually actuate the virtual or physical water pump from the cloud dashboard.
    Enforces safe duration bounds and records an audit watering event.
    """
    dev = db.query(Device).filter(Device.device_id == device_id).first()
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    duration = payload.duration_seconds if payload else 5
    success, cmd, metadata = WateringEngine.trigger_manual_water(db, dev, duration_seconds=duration)

    return {
        "status": "success",
        "pump_command": cmd,
        "device_id": device_id,
        "details": metadata
    }


@router.get("/{device_id}/watering-history", response_model=List[WateringEventResponse])
def get_watering_history(
    device_id: str,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieve historical log of automatic and manual watering cycles."""
    events = db.query(WateringEvent).filter(
        WateringEvent.device_id == device_id
    ).order_by(WateringEvent.timestamp.desc()).limit(limit).all()
    return events
