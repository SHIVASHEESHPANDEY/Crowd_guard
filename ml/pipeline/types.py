from dataclasses import dataclass, field

import numpy as np


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
