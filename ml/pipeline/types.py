from dataclasses import dataclass, field

import numpy as np


@dataclass
class LakeSensorReading:
    lake_level_m: float
    level_rise_cm_hr: float
    rainfall_mm_hr: float
    air_temp_c: float
    snowmelt_index: float
    moraine_stability: float
    seismic_tremor: float
    satellite_ndwi_delta: float
    downstream_flow_cms: float
    timestamp_index: int = 0


@dataclass
class Detection:
    class_name: str
    confidence: float
    bbox: tuple[int, int, int, int]


@dataclass
class TrackState:
    track_id: str
    bbox: tuple[int, int, int, int]
    center: tuple[float, float]
    velocity: float
    trajectory: list[tuple[float, float]] = field(default_factory=list)
    class_name: str = "person"
    confidence: float = 0.0


@dataclass
class FrameContext:
    frame_index: int
    frame: np.ndarray
    detections: list[Detection]
    tracks: list[TrackState]
