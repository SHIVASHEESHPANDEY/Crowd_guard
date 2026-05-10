from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.stream import StreamRequest, StreamResponse
from app.services.stream_service import stream_service


router = APIRouter(tags=["stream"])


@router.post("/stream", response_model=StreamResponse)
async def ingest_stream(
    request: StreamRequest,
    _: str = Depends(get_current_user),
) -> StreamResponse:
    if not request.rtsp_url and not request.source_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either a telemetry source URL or source_name is required",
        )
    stream_id = await stream_service.register_stream(request)
    return StreamResponse(stream_id=stream_id, status="accepted")
