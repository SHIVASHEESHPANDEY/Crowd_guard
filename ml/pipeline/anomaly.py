from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

import numpy as np
from sklearn.ensemble import IsolationForest

from ml.pipeline.types import Detection, TrackState


@dataclass
class AnomalyEvent:
    anomaly_type: str
    confidence: float
    description: str
    metadata: dict


class CrowdAnomalyClassifier:
    def __init__(self, geofences: list[list[float]] | None = None) -> None:
        self.geofences = geofences or []
        self.unknown_detector = IsolationForest(contamination=0.08, random_state=42)
        self._baseline_fitted = False
        self._feature_buffer: list[list[float]] = []

    def classify(
        self,
        detections: list[Detection],
        tracks: list[TrackState],
    ) -> list[AnomalyEvent]:
        events: list[AnomalyEvent] = []
        events.extend(self._detect_position_anomalies(tracks))
        events.extend(self._detect_movement_anomalies(tracks))
        events.extend(self._detect_appearance_anomalies(detections))
        events.extend(self._detect_action_anomalies(tracks))
        events.extend(self._detect_affect_anomalies(tracks))
        events.extend(self._detect_unknown_anomalies(tracks))
        return events

    def _detect_position_anomalies(self, tracks: list[TrackState]) -> list[AnomalyEvent]:
        events = []
        for track in tracks:
            if self._inside_geofence(track.center):
                events.append(
                    AnomalyEvent(
                        anomaly_type="anomalous_position",
                        confidence=0.76,
                        description=f"Track {track.track_id} entered restricted zone",
                        metadata={"track_id": track.track_id, "center": track.center},
                    )
                )
        return events

    def _detect_movement_anomalies(self, tracks: list[TrackState]) -> list[AnomalyEvent]:
        events = []
        velocities = [track.velocity for track in tracks if track.class_name == "person"]
        average_velocity = mean(velocities) if velocities else 0.0
        for track in tracks:
            abrupt_turn = self._trajectory_turn_score(track.trajectory)
            if track.velocity > max(45.0, average_velocity * 2.5) or abrupt_turn > 0.7:
                confidence = min(0.9, 0.55 + (track.velocity / 100.0) + abrupt_turn / 3.0)
                events.append(
                    AnomalyEvent(
                        anomaly_type="anomalous_movement",
                        confidence=confidence,
                        description=f"Irregular movement detected for track {track.track_id}",
                        metadata={
                            "track_id": track.track_id,
                            "velocity": track.velocity,
                            "turn_score": round(abrupt_turn, 3),
                        },
                    )
                )
        return events

    def _detect_appearance_anomalies(self, detections: list[Detection]) -> list[AnomalyEvent]:
        unusual_classes = {"truck", "suitcase", "backpack"}
        events = []
        for detection in detections:
            if detection.class_name in unusual_classes and detection.confidence > 0.6:
                events.append(
                    AnomalyEvent(
                        anomaly_type="anomalous_appearance",
                        confidence=min(0.88, detection.confidence),
                        description=f"Unexpected {detection.class_name} detected",
                        metadata={"bbox": detection.bbox, "class_name": detection.class_name},
                    )
                )
        return events

    def _detect_action_anomalies(self, tracks: list[TrackState]) -> list[AnomalyEvent]:
        events = []
        if len(tracks) >= 5:
            centers = np.array([track.center for track in tracks])
            spread = centers.std(axis=0).mean() if len(centers) else 0.0
            group_speed = mean([track.velocity for track in tracks]) if tracks else 0.0
            if spread < 40 and group_speed > 15:
                events.append(
                    AnomalyEvent(
                        anomaly_type="anomalous_action",
                        confidence=0.82,
                        description="Fast dense group movement suggests panic or stampede",
                        metadata={"spread": float(spread), "group_speed": float(group_speed)},
                    )
                )
        return events

    def _detect_affect_anomalies(self, tracks: list[TrackState]) -> list[AnomalyEvent]:
        events = []
        high_velocity_people = [track for track in tracks if track.class_name == "person" and track.velocity > 30]
        if len(high_velocity_people) >= 4:
            events.append(
                AnomalyEvent(
                    anomaly_type="anomalous_affect",
                    confidence=0.7,
                    description="Collective panic-like motion inferred from pose surrogate features",
                    metadata={"affected_tracks": [track.track_id for track in high_velocity_people]},
                )
            )
        return events

    def _detect_unknown_anomalies(self, tracks: list[TrackState]) -> list[AnomalyEvent]:
        if not tracks:
            return []
        features = [[track.center[0], track.center[1], track.velocity, len(track.trajectory)] for track in tracks]
        self._feature_buffer.extend(features)
        if len(self._feature_buffer) >= 20 and not self._baseline_fitted:
            self.unknown_detector.fit(self._feature_buffer[:100])
            self._baseline_fitted = True

        if not self._baseline_fitted:
            return []

        predictions = self.unknown_detector.predict(features)
        scores = self.unknown_detector.decision_function(features)
        events = []
        for idx, prediction in enumerate(predictions):
            if prediction == -1:
                confidence = min(0.92, 0.5 + abs(float(scores[idx])))
                events.append(
                    AnomalyEvent(
                        anomaly_type="unknown_anomaly",
                        confidence=confidence,
                        description=f"Novel anomaly pattern detected for track {tracks[idx].track_id}",
                        metadata={"track_id": tracks[idx].track_id, "score": float(scores[idx])},
                    )
                )
        return events

    def _inside_geofence(self, center: tuple[float, float]) -> bool:
        for zone in self.geofences:
            if len(zone) != 4:
                continue
            x1, y1, x2, y2 = zone
            if x1 <= center[0] <= x2 and y1 <= center[1] <= y2:
                return True
        return False

    @staticmethod
    def _trajectory_turn_score(trajectory: list[tuple[float, float]]) -> float:
        if len(trajectory) < 3:
            return 0.0
        p1 = np.array(trajectory[-3])
        p2 = np.array(trajectory[-2])
        p3 = np.array(trajectory[-1])
        v1 = p2 - p1
        v2 = p3 - p2
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            return 0.0
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return float((1 - np.clip(cos_theta, -1.0, 1.0)) / 2)
