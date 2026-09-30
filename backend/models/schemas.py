"""
Pydantic Schemas for Request Validation and Response Serialization
Ensures strict type-checking and data contracts across all REST API endpoints.
"""

from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SensorReadingCreate(BaseModel):
    """Payload sent by simulated sensor node or physical ESP32."""
    device_id: str = Field(..., description="Unique hardware or virtual device identifier", examples=["PLANT-001"])
    soil_moisture: float = Field(..., ge=0.0, le=100.0, description="Volumetric soil moisture percentage (0-100%)")
    temperature: float = Field(..., ge=-20.0, le=70.0, description="Ambient temperature in degrees Celsius")
    humidity: float = Field(..., ge=0.0, le=100.0, description="Relative humidity percentage (0-100%)")
    light_level: Optional[float] = Field(50.0, ge=0.0, le=100.0, description="Ambient light intensity percentage")
    water_tank_level: Optional[float] = Field(80.0, ge=0.0, le=100.0, description="Water reservoir fill level percentage")
    timestamp: Optional[datetime] = Field(default_factory=get_utc_now, description="ISO8601 reading timestamp")

    @field_validator("device_id")
    @classmethod
    def validate_device_id(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Device ID cannot be empty")
        return v


class SensorReadingResponse(BaseModel):
    """Serialized sensor telemetry reading."""
    reading_id: int
    device_id: str
    soil_moisture: float
    temperature: float
    humidity: float
    light_level: float
    water_tank_level: Optional[float] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceCreate(BaseModel):
    """Payload to register a new plant monitoring node."""
    device_id: str = Field(..., min_length=2, max_length=64, examples=["PLANT-002"])
    plant_name: str = Field(..., min_length=2, max_length=100, examples=["Basil Herb"])
    plant_type: str = Field("HERB", examples=["HERB", "TOMATO", "SUCCULENT", "INDOOR PLANT"])
    location: Optional[str] = Field("Living Room Window", max_length=100)
    moisture_threshold: Optional[float] = Field(35.0, ge=5.0, le=80.0)
    auto_water_enabled: Optional[bool] = Field(True)


class DeviceUpdate(BaseModel):
    """Payload to update device settings."""
    plant_name: Optional[str] = None
    plant_type: Optional[str] = None
    location: Optional[str] = None
    moisture_threshold: Optional[float] = Field(None, ge=5.0, le=80.0)
    auto_water_enabled: Optional[bool] = None


class ThresholdUpdateRequest(BaseModel):
    """Payload to modify soil moisture threshold."""
    moisture_threshold: float = Field(..., ge=5.0, le=80.0, description="Moisture threshold percentage to trigger watering")


class DeviceResponse(BaseModel):
    """Device metadata and current operational state."""
    device_id: str
    plant_name: str
    plant_type: str
    location: str
    moisture_threshold: float
    auto_water_enabled: bool
    pump_status: str
    is_online: bool
    plant_health_status: str  # "Healthy", "Needs Water", "Overheated", "Offline"
    last_seen: Optional[datetime] = None
    last_watered_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WateringRequest(BaseModel):
    """Payload to manually trigger or schedule a watering cycle."""
    duration_seconds: Optional[int] = Field(5, ge=1, le=30, description="Duration in seconds to run pump")


class WateringEventResponse(BaseModel):
    """Record of an automated or manual watering cycle."""
    event_id: str
    device_id: str
    trigger_type: str
    moisture_before: float
    moisture_after: Optional[float] = None
    duration_seconds: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertResponse(BaseModel):
    """System alert notification item."""
    alert_id: str
    device_id: str
    alert_type: str
    severity: str
    message: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertAcknowledgeRequest(BaseModel):
    """Acknowledge or dismiss an alert."""
    status: str = Field("ACKNOWLEDGED", examples=["ACKNOWLEDGED", "RESOLVED"])


class AnalyticsSummaryResponse(BaseModel):
    """Computed analytical KPIs and statistical aggregates."""
    device_id: str
    total_readings: int
    avg_soil_moisture: float
    min_soil_moisture: float
    max_soil_moisture: float
    avg_temperature: float
    avg_humidity: float
    total_watering_events: int
    watering_count_today: int
    estimated_water_used_liters: float
    uptime_percentage: float
    current_health_status: str


class SensorIngestResponse(BaseModel):
    """Response returned upon successful sensor data ingestion."""
    status: str = "success"
    message: str
    reading_id: int
    pump_command: str  # "ON" or "OFF"
    watering_triggered: bool
    current_moisture: float
    threshold: float
    decision_metadata: Optional[dict] = None
