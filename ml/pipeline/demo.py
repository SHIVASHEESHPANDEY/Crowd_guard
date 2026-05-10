from __future__ import annotations

import math
from random import Random

from ml.pipeline.anomaly import AnomalyEvent
from ml.pipeline.types import Detection, TrackState


class DemoScenarioGenerator:
    def __init__(self, seed: int = 42) -> None:
        self.random = Random(seed)
        self._track_ids = [f"demo-{index}" for index in range(1, 9)]

    def next_frame(self, frame_index: int, anomaly_profile: str) -> tuple[list[Detection], list[TrackState], list[AnomalyEvent], list[dict]]:
        phase = frame_index / 12.0
        detections: list[Detection] = []
        tracks: list[TrackState] = []
        heatmap_points: list[dict] = []

        crowd_shift = 95 if frame_index > 20 else 0
        panic_multiplier = 2.6 if anomaly_profile == "panic" and frame_index > 14 else 1.0

        for idx, track_id in enumerate(self._track_ids):
            base_x = 120 + idx * 58
            x = base_x + math.sin(phase + idx) * 22 + crowd_shift
            y = 155 + (idx % 3) * 48 + math.cos(phase * 1.4 + idx) * 18
            velocity = abs(math.cos(phase + idx / 3.0)) * 11 * panic_multiplier

            bbox = (int(x), int(y), int(x + 36), int(y + 82))
            detections.append(Detection(class_name="person", confidence=0.88, bbox=bbox))
            tracks.append(
                TrackState(
                    track_id=track_id,
                    bbox=bbox,
                    center=(x + 18, y + 41),
                    velocity=velocity,
                    trajectory=[(x + 18 - velocity, y + 41 - velocity / 2), (x + 18, y + 41)],
                    class_name="person",
                    confidence=0.88,
                )
            )
            heatmap_points.append(
                {
                    "x": round(min(max((x + 18) / 800, 0.05), 0.95), 3),
                    "y": round(min(max((y + 41) / 450, 0.05), 0.95), 3),
                    "intensity": round(min(1.0, 0.42 + velocity / 20), 3),
                }
            )

        events: list[AnomalyEvent] = []
        if frame_index == 8:
            events.append(
                AnomalyEvent(
                    anomaly_type="anomalous_position",
                    confidence=0.8,
                    description="Demo subject entered restricted zone near gate corridor",
                    metadata={"track_id": "demo-2", "zone": "north_gate"},
                )
            )
        if frame_index == 18:
            events.append(
                AnomalyEvent(
                    anomaly_type="anomalous_action",
                    confidence=0.86,
                    description="Dense fast group movement suggests panic near plaza",
                    metadata={"cluster_size": 6, "zone": "central_plaza"},
                )
            )
        if frame_index == 28:
            events.append(
                AnomalyEvent(
                    anomaly_type="anomalous_appearance",
                    confidence=0.74,
                    description="Unattended suitcase detected near monument perimeter",
                    metadata={"object_class": "suitcase", "zone": "monument"},
                )
            )

        return detections, tracks, events, heatmap_points
