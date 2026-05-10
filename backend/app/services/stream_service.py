from __future__ import annotations

import asyncio
import sys
import threading
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from app.schemas.stream import StreamRequest
from app.services.alert_service import alert_service
from app.services.runtime_state import runtime_state
from ml.pipeline.orchestrator import GLOFEarlyWarningPipeline


class StreamService:
    def __init__(self) -> None:
        self._pipelines: dict[str, GLOFEarlyWarningPipeline] = {}
        self._threads: dict[str, threading.Thread] = {}

    async def register_stream(self, request: StreamRequest) -> str:
        stream_id = f"stream-{uuid.uuid4().hex[:10]}"
        source_name = request.source_name or request.rtsp_url or "unknown-source"
        runtime_state.register_stream(stream_id, source_name, request.source_type)
        if request.source_type == "demo":
            runtime_state.set_heatmap(
                stream_id=stream_id,
                points=[
                    {"x": 0.22, "y": 0.34, "intensity": 0.62},
                    {"x": 0.43, "y": 0.39, "intensity": 0.48},
                    {"x": 0.58, "y": 0.58, "intensity": 0.52},
                    {"x": 0.74, "y": 0.74, "intensity": 0.36},
                ],
                tracks=[],
            )
            await alert_service.raise_alert(
                stream_id=stream_id,
                anomaly_type="monitoring_started",
                confidence=0.61,
                description="GLOF monitoring activated for the demo basin. Sensor fusion and risk scoring are live.",
                source_name=source_name,
                metadata={"mode": "demo"},
            )
        pipeline = GLOFEarlyWarningPipeline(
            stream_id=stream_id,
            source_name=source_name,
            source_type=request.source_type,
            geofences=request.geofences,
            alert_callback=alert_service.raise_alert,
            telemetry_callback=self._telemetry_callback,
            frame_limit=request.frame_limit,
            anomaly_profile=request.anomaly_profile,
        )
        self._pipelines[stream_id] = pipeline
        thread = threading.Thread(
            target=self._run_pipeline,
            args=(pipeline, request.rtsp_url),
            daemon=True,
            name=f"glof-sentinel-{stream_id}",
        )
        self._threads[stream_id] = thread
        thread.start()
        alert_service.start_escalation_loop()
        return stream_id

    async def _telemetry_callback(self, stream_id: str, points: list[dict], tracks: list[dict]) -> None:
        runtime_state.set_heatmap(stream_id=stream_id, points=points, tracks=tracks)

    def _run_pipeline(self, pipeline: CrowdGuardPipeline, source: str | None) -> None:
        asyncio.run(pipeline.run(source))


stream_service = StreamService()
