from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user
from app.schemas.alert import AlertListResponse
from app.services.alert_service import alert_service


router = APIRouter(tags=["alerts"])


@router.get("/alerts", response_model=AlertListResponse)
async def list_alerts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    severity: str | None = None,
    anomaly_type: str | None = None,
    resolved: bool | None = None,
    _: str = Depends(get_current_user),
) -> AlertListResponse:
    return alert_service.list_alerts(
        page=page,
        page_size=page_size,
        severity=severity,
        anomaly_type=anomaly_type,
        resolved=resolved,
    )
