from __future__ import annotations

import asyncio
import threading
import uuid
from dataclasses import asdict
from datetime import datetime, timezone

from app.core.config import settings
from app.models.domain import AlertRecord
from app.schemas.alert import AlertItem, AlertListResponse
from app.services.notification_service import notification_service
from app.services.repositories import alert_repository
from app.services.websocket_manager import connection_manager


class AlertService:
    def __init__(self) -> None:
        self._escalation_thread: threading.Thread | None = None

    def start_escalation_loop(self) -> None:
        if self._escalation_thread is None:
            self._escalation_thread = threading.Thread(
                target=self._run_escalation_loop,
                daemon=True,
                name="crowdguard-escalation",
            )
            self._escalation_thread.start()

    async def raise_alert(
        self,
        stream_id: str,
        anomaly_type: str,
        confidence: float,
        description: str,
        source_name: str,
        metadata: dict | None = None,
    ) -> AlertRecord:
        severity = self._severity_from_confidence(confidence)
        alert = AlertRecord(
            id=str(uuid.uuid4()),
            stream_id=stream_id,
            anomaly_type=anomaly_type,
            severity=severity,
            confidence=confidence,
            description=description,
            source_name=source_name,
            metadata=metadata or {},
        )
        alert_repository.add(alert)
        await connection_manager.broadcast_json(
            {
                "event": "alert.created",
                "data": AlertItem(**asdict(alert)).model_dump(mode="json"),
            }
        )
        await notification_service.dispatch(alert)
        return alert

    def list_alerts(
        self,
        page: int,
        page_size: int,
        severity: str | None,
        anomaly_type: str | None,
        resolved: bool | None,
    ) -> AlertListResponse:
        alerts = alert_repository.all()
        if severity is not None:
            alerts = [item for item in alerts if item.severity == severity]
        if anomaly_type is not None:
            alerts = [item for item in alerts if item.anomaly_type == anomaly_type]
        if resolved is not None:
            alerts = [item for item in alerts if item.resolved is resolved]

        total = len(alerts)
        start = (page - 1) * page_size
        end = start + page_size
        items = [AlertItem(**asdict(alert)) for alert in alerts[start:end]]
        return AlertListResponse(page=page, page_size=page_size, total=total, items=items)

    def _run_escalation_loop(self) -> None:
        asyncio.run(self._escalate_unresolved())

    async def _escalate_unresolved(self) -> None:
        while True:
            now = datetime.now(timezone.utc)
            for alert in alert_repository.unresolved():
                age = (now - alert.timestamp).total_seconds()
                if age >= settings.escalation_seconds and not alert.metadata.get("escalated"):
                    alert.metadata["escalated"] = True
                    await notification_service.dispatch(alert, escalated=True)
            await asyncio.sleep(10)

    @staticmethod
    def _severity_from_confidence(confidence: float) -> str:
        if confidence >= settings.high_priority_threshold:
            return "critical"
        if confidence >= settings.medium_priority_threshold:
            return "warning"
        return "info"


alert_service = AlertService()
