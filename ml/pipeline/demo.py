from __future__ import annotations

import math
from random import Random

from ml.pipeline.anomaly import AnomalyEvent, GLOFRiskClassifier
from ml.pipeline.types import LakeSensorReading


class DemoScenarioGenerator:
    def __init__(self, seed: int = 42) -> None:
        self.random = Random(seed)
        self.classifier = GLOFRiskClassifier()

    def next_frame(self, frame_index: int, anomaly_profile: str) -> tuple[list, list, list[AnomalyEvent], list[dict]]:
        reading = self.next_reading(frame_index, anomaly_profile)
        events = self.classifier.classify_reading(reading)
        points = self.risk_surface(reading)
        return [], [], events, points

    def next_reading(self, frame_index: int, anomaly_profile: str) -> LakeSensorReading:
        phase = frame_index / 16.0
        surge_start = 48 if anomaly_profile == "monsoon_breach" else 82
        surge = max(0.0, frame_index - surge_start)
        surge_curve = min(1.0, surge / 52.0)
        jitter = self.random.uniform(-0.25, 0.25)

        rainfall_boost = 20.0 if anomaly_profile in {"monsoon_breach", "extreme"} else 8.0
        seismic_boost = 2.6 if anomaly_profile in {"moraine_failure", "extreme"} else 1.1

        return LakeSensorReading(
            lake_level_m=41.8 + math.sin(phase) * 0.35 + surge_curve * 5.1 + jitter,
            level_rise_cm_hr=6.0 + surge_curve * 43.0 + max(0, math.sin(phase * 1.7)) * 4,
            rainfall_mm_hr=5.0 + max(0, math.sin(phase * 0.8)) * rainfall_boost + surge_curve * 18.0,
            air_temp_c=4.0 + max(0, math.sin(phase * 0.5)) * 9.5,
            snowmelt_index=min(1.0, 0.24 + max(0, math.sin(phase * 0.6)) * 0.45 + surge_curve * 0.34),
            moraine_stability=max(0.12, 0.82 - surge_curve * 0.58 - max(0, math.sin(phase * 1.2)) * 0.08),
            seismic_tremor=0.9 + surge_curve * seismic_boost + max(0, math.sin(phase * 2.4)) * 1.3,
            satellite_ndwi_delta=0.03 + surge_curve * 0.2,
            downstream_flow_cms=180.0 + surge_curve * 570.0 + max(0, math.sin(phase * 1.3)) * 80.0,
            timestamp_index=frame_index,
        )

    def risk_surface(self, reading: LakeSensorReading) -> list[dict]:
        risk_features = self.classifier._risk_features(reading)
        risk_score = self.classifier._weighted_risk_score(risk_features)
        lake_pressure = max(risk_features["lake_level"], risk_features["level_rise"])
        breach_pressure = max(risk_features["moraine_instability"], risk_features["seismic_tremor"])
        downstream_pressure = max(risk_features["downstream_flow"], risk_score)

        return [
            {"x": 0.2, "y": 0.22, "intensity": round(lake_pressure, 3), "label": "Lake basin"},
            {"x": 0.43, "y": 0.39, "intensity": round(breach_pressure, 3), "label": "Moraine dam"},
            {"x": 0.58, "y": 0.58, "intensity": round(downstream_pressure, 3), "label": "River channel"},
            {"x": 0.74, "y": 0.74, "intensity": round(min(1.0, downstream_pressure * 0.86), 3), "label": "Village zone"},
        ]
