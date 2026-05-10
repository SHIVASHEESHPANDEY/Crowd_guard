from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.tourist import (
    TouristRegistrationRequest,
    TouristRegistrationResponse,
    TouristVerificationResponse,
)
from app.services.tourist_service import tourist_service


router = APIRouter(tags=["tourist"])


@router.post("/tourist/register", response_model=TouristRegistrationResponse)
async def register_tourist(
    request: TouristRegistrationRequest,
    _: str = Depends(get_current_user),
) -> TouristRegistrationResponse:
    return tourist_service.register(request)


@router.get("/tourist/{tourist_id}/verify", response_model=TouristVerificationResponse)
async def verify_tourist(
    tourist_id: str,
    _: str = Depends(get_current_user),
) -> TouristVerificationResponse:
    tourist = tourist_service.verify(tourist_id)
    if tourist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tourist ID not found",
        )
    return tourist
