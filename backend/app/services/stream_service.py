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
from ml.pipeline.orchestrator import CrowdGuardPipeline


class StreamService:
    def __init__(self) -> None:
        self._pipelines: dict[str, CrowdGuardPipeline] = {}
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
                    {"x": 0.38, "y": 0.47, "intensity": 0.75},
                    {"x": 0.51, "y": 0.41, "intensity": 0.58},
                    {"x": 0.66, "y": 0.53, "intensity": 0.81},
                ],
                tracks=[],
            )
            await alert_service.raise_alert(
                stream_id=stream_id,
                anomaly_type="system_bootstrap",
                confidence=0.61,
                description="Demo monitoring activated. Live anomaly simulation is now running.",
                source_name=source_name,
                metadata={"mode": "demo"},
            )
        pipeline = CrowdGuardPipeline(
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
            name=f"crowdguard-{stream_id}",
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
