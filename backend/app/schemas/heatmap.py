from pydantic import BaseModel, Field


class HeatmapPoint(BaseModel):
    x: float
    y: float
    intensity: float


class HeatmapResponse(BaseModel):
    generated_at: str
    points: list[HeatmapPoint] = Field(default_factory=list)
    active_streams: int = 0
