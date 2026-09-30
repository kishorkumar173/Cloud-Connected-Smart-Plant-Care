"""
Alert & Anomaly Notification REST API Routes
Provides querying, filtering, and acknowledgment endpoints for system health alerts.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from cloud.database_service import get_db
from backend.models.schemas import AlertResponse, AlertAcknowledgeRequest
from backend.services.alert_service import AlertService

router = APIRouter(prefix="/api/alerts", tags=["Alerts & Notifications"])


@router.get("", response_model=List[AlertResponse])
def get_alerts(
    device_id: Optional[str] = Query(None, description="Filter alerts by device ID"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Retrieve system alerts (Low Moisture, Heat Stress, Low Reservoir, Device Offline)."""
    return AlertService.get_alerts(db, device_id=device_id, limit=limit)


@router.put("/{alert_id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(
    alert_id: str,
    payload: Optional[AlertAcknowledgeRequest] = None,
    db: Session = Depends(get_db)
):
    """Acknowledge or dismiss an alert notification."""
    status_val = payload.status if payload else "ACKNOWLEDGED"
    alert = AlertService.acknowledge_alert(db, alert_id, new_status=status_val)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert '{alert_id}' not found."
        )
    return alert
