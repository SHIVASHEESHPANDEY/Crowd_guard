from app.schemas.heatmap import HeatmapPoint, HeatmapResponse
from app.services.runtime_state import runtime_state


class HeatmapService:
    def get_live_heatmap(self) -> HeatmapResponse:
        snapshot = runtime_state.snapshot()
        return HeatmapResponse(
            generated_at=snapshot["generated_at"],
            points=[HeatmapPoint(**point) for point in snapshot["points"]],
            active_streams=snapshot["active_streams"],
        )


heatmap_service = HeatmapService()
