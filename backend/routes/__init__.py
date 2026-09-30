"""Routes package initialization."""
from backend.routes.sensors import router as sensors_router
from backend.routes.devices import router as devices_router
from backend.routes.alerts import router as alerts_router
from backend.routes.analytics import router as analytics_router

__all__ = ["sensors_router", "devices_router", "alerts_router", "analytics_router"]
