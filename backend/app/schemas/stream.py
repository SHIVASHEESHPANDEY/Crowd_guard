from pydantic import BaseModel, Field


class StreamRequest(BaseModel):
    rtsp_url: str | None = None
    source_name: str | None = None
    source_type: str = Field(default="cctv")
    geofences: list[list[float]] = Field(default_factory=list)
    frame_limit: int = Field(default=180, ge=30, le=3600)
    anomaly_profile: str = Field(default="balanced")
    metadata: dict = Field(default_factory=dict)


class StreamResponse(BaseModel):
    stream_id: str
    status: str
