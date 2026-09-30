"""
Sensor Telemetry REST API Routes
Provides endpoints for IoT nodes (virtual or hardware) to transmit telemetry.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from cloud.database_service import get_db
from cloud.auth_service import verify_device_api_key
from backend.models.schemas import SensorReadingCreate, SensorReadingResponse, SensorIngestResponse
from backend.services.sensor_service import SensorService

router = APIRouter(prefix="/api/sensors", tags=["Sensors & Telemetry"])


@router.post("/data", response_model=SensorIngestResponse, status_code=status.HTTP_201_CREATED)
def ingest_sensor_data(
    payload: SensorReadingCreate,
    db: Session = Depends(get_db),
    _authorized: bool = Depends(verify_device_api_key)
):
    """
    Ingest real-time sensor telemetry from a physical ESP32 or Python sensor simulator.
    Validates payload, records reading, evaluates threshold watering logic, checks alerts,
    and returns immediate pump actuation commands.
    """
    try:
        result = SensorService.ingest_sensor_data(db, payload)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Telemetry ingestion failed: {str(e)}"
        )
