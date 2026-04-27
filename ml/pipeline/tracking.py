from __future__ import annotations

from collections import defaultdict

from deep_sort_realtime.deepsort_tracker import DeepSort

from ml.pipeline.types import Detection, TrackState


class MultiObjectTracker:
    def __init__(self) -> None:
        self.tracker = DeepSort(max_age=20, n_init=2)
        self._history: dict[str, list[tuple[float, float]]] = defaultdict(list)

    def update(self, detections: list[Detection]) -> list[TrackState]:
        ds_detections = []
        for detection in detections:
            x1, y1, x2, y2 = detection.bbox
            ds_detections.append(([x1, y1, x2 - x1, y2 - y1], detection.confidence, detection.class_name))

        tracks = self.tracker.update_tracks(ds_detections, frame=None)
        states: list[TrackState] = []
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = str(track.track_id)
            x1, y1, x2, y2 = map(int, track.to_ltrb())
            center = ((x1 + x2) / 2, (y1 + y2) / 2)
            trajectory = self._history[track_id]
            trajectory.append(center)
            if len(trajectory) > 20:
                trajectory.pop(0)
            velocity = 0.0
            if len(trajectory) >= 2:
                prev = trajectory[-2]
                velocity = ((center[0] - prev[0]) ** 2 + (center[1] - prev[1]) ** 2) ** 0.5

            states.append(
                TrackState(
                    track_id=track_id,
                    bbox=(x1, y1, x2, y2),
                    center=center,
                    velocity=velocity,
                    trajectory=list(trajectory),
                    class_name=track.get_det_class() or "person",
                    confidence=track.det_conf if track.det_conf is not None else 0.0,
                )
            )
        return states
