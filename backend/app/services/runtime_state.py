from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone


class RuntimeState:
    def __init__(self) -> None:
        self._heatmap_points: list[dict] = []
        self._active_streams: dict[str, dict] = {}
        self._track_snapshots: dict[str, list[dict]] = defaultdict(list)

    def register_stream(self, stream_id: str, source_name: str, source_type: str) -> None:
        self._active_streams[stream_id] = {
            "stream_id": stream_id,
            "source_name": source_name,
            "source_type": source_type,
            "started_at": datetime.now(timezone.utc).isoformat(),
        }

    def set_heatmap(self, stream_id: str, points: list[dict], tracks: list[dict] | None = None) -> None:
        self._heatmap_points = points
        if tracks is not None:
            self._track_snapshots[stream_id] = tracks

    def snapshot(self) -> dict:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "points": list(self._heatmap_points),
            "active_streams": len(self._active_streams),
        }

    def stream_snapshot(self) -> list[dict]:
        return list(self._active_streams.values())


runtime_state = RuntimeState()
