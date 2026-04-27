from app.models.domain import AlertRecord


class NotificationService:
    async def dispatch(self, alert: AlertRecord, escalated: bool = False) -> None:
        severity = "ESCALATED" if escalated else alert.severity.upper()
        message = f"[{severity}] {alert.anomaly_type}: {alert.description}"
        await self._send_sms_or_whatsapp(message)
        await self._send_push(message)
        if alert.severity == "info":
            await self._send_email_digest(message)

    async def _send_sms_or_whatsapp(self, message: str) -> None:
        _ = message

    async def _send_push(self, message: str) -> None:
        _ = message

    async def _send_email_digest(self, message: str) -> None:
        _ = message


notification_service = NotificationService()
