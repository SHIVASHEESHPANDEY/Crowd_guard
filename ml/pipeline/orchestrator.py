from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable

from ml.pipeline.anomaly import CrowdAnomalyClassifier
from ml.pipeline.demo import DemoScenarioGenerator
from ml.pipeline.preprocessing import VideoPreprocessor


AlertCallback = Callable[[str, str, float, str, str, dict | None], Awaitable[object]]
TelemetryCallback = Callable[[str, list[dict], list[dict]], Awaitable[object]]


class CrowdGuardPipeline:
    def __init__(
        self,
        stream_id: str,
        source_name: str,
        source_type: str,
        geofences: list[list[float]],
        alert_callback: AlertCallback,
        telemetry_callback: TelemetryCallback | None = None,
        frame_limit: int = 180,
        anomaly_profile: str = "balanced",
    ) -> None:
        self.stream_id = stream_id
        self.source_name = source_name
        self.source_type = source_type
        self.preprocessor = VideoPreprocessor()
        self.classifier = CrowdAnomalyClassifier(geofences=geofences)
        self.alert_callback = alert_callback
        self.telemetry_callback = telemetry_callback
        self.alert_threshold = 0.6
        self.frame_limit = frame_limit
        self.anomaly_profile = anomaly_profile
        self.detector = None
        self.tracker = None
        self.demo_generator = DemoScenarioGenerator()

    async def run(self, source: str | None) -> None:
        if self.source_type == "demo":
            await self._run_demo()
            return

        from ml.pipeline.detection import YOLODetector
        from ml.pipeline.tracking import MultiObjectTracker

        self.detector = YOLODetector()
        self.tracker = MultiObjectTracker()
        for frame_index, frame in self.preprocessor.extract_frames(source):
            detections = self.detector.detect(frame)
            tracks = self.tracker.update(detections)
            await self._emit_heatmap(tracks)
            events = self.classifier.classify(detections, tracks)
            for event in events:
                if event.confidence >= self.alert_threshold:
                    await self.alert_callback(
                        self.stream_id,
                        event.anomaly_type,
                        event.confidence,
                        event.description,
                        self.source_name,
                        {"frame_index": frame_index, **event.metadata},
                    )
            await asyncio.sleep(0)

    async def _run_demo(self) -> None:
        for frame_index in range(self.frame_limit):
            detections, tracks, events, heatmap_points = self.demo_generator.next_frame(
                frame_index=frame_index,
                anomaly_profile=self.anomaly_profile,
            )
            await self._emit_heatmap(tracks, heatmap_points=heatmap_points)
            if not events:
                events = self.classifier.classify(detections, tracks)
            for event in events:
                if event.confidence >= self.alert_threshold:
                    await self.alert_callback(
                        self.stream_id,
                        event.anomaly_type,
                        event.confidence,
                        event.description,
                        self.source_name,
                        {"frame_index": frame_index, **event.metadata},
                    )
            await asyncio.sleep(0.12)

    async def _emit_heatmap(self, tracks, heatmap_points: list[dict] | None = None) -> None:
        if self.telemetry_callback is None:
            return
        if heatmap_points is None:
            heatmap_points = [
                {
                    "x": round(track.center[0] / 1280, 3),
                    "y": round(track.center[1] / 720, 3),
                    "intensity": round(min(1.0, 0.35 + track.velocity / 60), 3),
                }
                for track in tracks
            ]
        track_payload = [
            {
                "track_id": track.track_id,
                "x": round(track.center[0], 2),
                "y": round(track.center[1], 2),
                "velocity": round(track.velocity, 2),
                "class_name": track.class_name,
            }
            for track in tracks
        ]
        await self.telemetry_callback(self.stream_id, heatmap_points, track_payload)
