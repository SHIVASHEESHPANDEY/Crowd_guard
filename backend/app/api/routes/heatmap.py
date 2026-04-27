from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.heatmap import HeatmapResponse
from app.services.heatmap_service import heatmap_service


router = APIRouter(tags=["heatmap"])


@router.get("/heatmap/live", response_model=HeatmapResponse)
async def live_heatmap(_: str = Depends(get_current_user)) -> HeatmapResponse:
    return heatmap_service.get_live_heatmap()
