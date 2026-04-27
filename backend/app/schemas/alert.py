from datetime import datetime

from pydantic import BaseModel, Field


class AlertItem(BaseModel):
    id: str
    stream_id: str
    anomaly_type: str
    severity: str
    confidence: float
    description: str
    timestamp: datetime
    resolved: bool
    source_name: str = ""
    metadata: dict = Field(default_factory=dict)


class AlertListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[AlertItem]
