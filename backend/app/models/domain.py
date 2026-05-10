from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AuthorityUser:
    username: str
    hashed_password: str
    role: str = "authority"


@dataclass
class AlertRecord:
    id: str
    stream_id: str
    anomaly_type: str
    severity: str
    confidence: float
    description: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved: bool = False
    source_name: str = ""
    metadata: dict = field(default_factory=dict)
