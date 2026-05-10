from __future__ import annotations

from dataclasses import dataclass

from ml.pipeline.types import Detection, LakeSensorReading, TrackState


@dataclass
class AnomalyEvent:
    anomaly_type: str
    confidence: float
    description: str
    metadata: dict


class GLOFRiskClassifier:
    """Interpretable early-warning rules for glacier lake outburst flood risk."""

    def __init__(self, geofences: list[list[float]] | None = None) -> None:
        self.geofences = geofences or []
        self._last_risk_score = 0.0

    def classify_reading(self, reading: LakeSensorReading) -> list[AnomalyEvent]:
        features = self._risk_features(reading)
        risk_score = self._weighted_risk_score(features)
        self._last_risk_score = risk_score

        events: list[AnomalyEvent] = []
        if risk_score >= 0.82:
            events.append(
                AnomalyEvent(
                    anomaly_type="evacuation_trigger",
                    confidence=risk_score,
                    description="Critical GLOF probability: rapid lake rise, heavy precipitation, and moraine instability align.",
                    metadata={"risk_score": round(risk_score, 3), "features": features, "stage": "evacuate"},
                )
            )
        elif risk_score >= 0.68:
            events.append(
                AnomalyEvent(
                    anomaly_type="high_glof_risk",
                    confidence=risk_score,
                    description="High outburst risk detected; downstream warning sirens and field verification should be activated.",
                    metadata={"risk_score": round(risk_score, 3), "features": features, "stage": "prepare"},
                )
            )
        elif risk_score >= 0.55:
            events.append(
                AnomalyEvent(
                    anomaly_type="watch_condition",
                    confidence=risk_score,
                    description="Watch condition: lake level and melt indicators are trending above baseline.",
                    metadata={"risk_score": round(risk_score, 3), "features": features, "stage": "watch"},
                )
            )

        events.extend(self._threshold_events(reading, features))
        return events

    def classify(
        self,
        detections: list[Detection],
        tracks: list[TrackState],
    ) -> list[AnomalyEvent]:
        return []

    @staticmethod
    def _risk_features(reading: LakeSensorReading) -> dict[str, float]:
        return {
            "lake_level": _clamp((reading.lake_level_m - 41.5) / 5.0),
            "level_rise": _clamp(reading.level_rise_cm_hr / 42.0),
            "rainfall": _clamp(reading.rainfall_mm_hr / 38.0),
            "temperature": _clamp((reading.air_temp_c - 2.0) / 14.0),
            "snowmelt": _clamp(reading.snowmelt_index),
            "moraine_instability": _clamp(1.0 - reading.moraine_stability),
            "seismic_tremor": _clamp(reading.seismic_tremor / 7.0),
            "satellite_change": _clamp(abs(reading.satellite_ndwi_delta) / 0.22),
            "downstream_flow": _clamp(reading.downstream_flow_cms / 720.0),
        }

    @staticmethod
    def _weighted_risk_score(features: dict[str, float]) -> float:
        weights = {
            "lake_level": 0.16,
            "level_rise": 0.2,
            "rainfall": 0.12,
            "temperature": 0.08,
            "snowmelt": 0.1,
            "moraine_instability": 0.16,
            "seismic_tremor": 0.08,
            "satellite_change": 0.05,
            "downstream_flow": 0.05,
        }
        return round(sum(features[name] * weight for name, weight in weights.items()), 3)

    @staticmethod
    def _threshold_events(reading: LakeSensorReading, features: dict[str, float]) -> list[AnomalyEvent]:
        events: list[AnomalyEvent] = []
        if reading.level_rise_cm_hr >= 32:
            events.append(
                AnomalyEvent(
                    anomaly_type="rapid_lake_rise",
                    confidence=min(0.96, 0.55 + features["level_rise"] * 0.4),
                    description=f"Lake level rising at {reading.level_rise_cm_hr:.1f} cm/hr, above rapid-rise threshold.",
                    metadata={"level_rise_cm_hr": reading.level_rise_cm_hr, "sensor": "radar_gauge"},
                )
            )
        if reading.moraine_stability <= 0.38 and reading.seismic_tremor >= 3.8:
            events.append(
                AnomalyEvent(
                    anomaly_type="moraine_failure_signal",
                    confidence=min(0.94, 0.58 + features["moraine_instability"] * 0.24 + features["seismic_tremor"] * 0.16),
                    description="Moraine stability and micro-seismic tremor indicate possible breach initiation.",
                    metadata={
                        "moraine_stability": reading.moraine_stability,
                        "seismic_tremor": reading.seismic_tremor,
                    },
                )
            )
        if reading.satellite_ndwi_delta >= 0.16:
            events.append(
                AnomalyEvent(
                    anomaly_type="satellite_lake_expansion",
                    confidence=min(0.86, 0.5 + features["satellite_change"] * 0.34),
                    description="Satellite water-index change suggests rapid lake surface expansion.",
                    metadata={"satellite_ndwi_delta": reading.satellite_ndwi_delta, "sensor": "sentinel_ndwi"},
                )
            )
        return events


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)


CrowdAnomalyClassifier = GLOFRiskClassifier
