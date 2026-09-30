"""
Analytics, Botanical Profiles, and Cloud Health Routes
Exposes analytical aggregations, botanical species profiles, and system health checks.
"""

from typing import List, Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from cloud.database_service import get_db
from backend.models.schemas import AnalyticsSummaryResponse
from backend.services.sensor_service import SensorService
from automation.plant_profiles import list_available_profiles

router = APIRouter(prefix="/api", tags=["Analytics & System"])


@router.get("/devices/{device_id}/analytics", response_model=AnalyticsSummaryResponse)
def get_device_analytics(device_id: str, db: Session = Depends(get_db)):
    """Fetch statistical analytics: averages, min/max, watering frequency, and water consumption."""
    try:
        return SensorService.compute_analytics(db, device_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute analytics: {str(e)}"
        )


@router.get("/plant-profiles", response_model=List[Dict[str, Any]])
def get_botanical_plant_profiles():
    """Retrieve all preconfigured agronomic plant species profiles with recommended thresholds."""
    return list_available_profiles()


@router.get("/health")
def cloud_health_check(db: Session = Depends(get_db)):
    """
    Cloud liveness and readiness probe for container orchestrators (Kubernetes, AWS ECS, GCP Cloud Run).
    Verifies database connectivity and service availability.
    """
    try:
        # Perform lightweight DB ping
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "service": "Cloud-Connected Smart Plant Care & Watering System",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
        "environment": "cloud-production-ready"
    }
