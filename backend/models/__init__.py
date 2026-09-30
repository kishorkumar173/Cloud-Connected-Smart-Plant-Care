"""Models package exports."""
from backend.models.db_models import Base, User, Device, SensorReading, WateringEvent, Alert
from backend.models.schemas import (
    SensorReadingCreate,
    SensorReadingResponse,
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse,
    ThresholdUpdateRequest,
    WateringRequest,
    WateringEventResponse,
    AlertResponse,
    AlertAcknowledgeRequest,
    AnalyticsSummaryResponse,
    SensorIngestResponse,
)

__all__ = [
    "Base",
    "User",
    "Device",
    "SensorReading",
    "WateringEvent",
    "Alert",
    "SensorReadingCreate",
    "SensorReadingResponse",
    "DeviceCreate",
    "DeviceUpdate",
    "DeviceResponse",
    "ThresholdUpdateRequest",
    "WateringRequest",
    "WateringEventResponse",
    "AlertResponse",
    "AlertAcknowledgeRequest",
    "AnalyticsSummaryResponse",
    "SensorIngestResponse",
]
