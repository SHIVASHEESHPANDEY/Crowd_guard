from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from app.core.auth import create_access_token, verify_password
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.repositories import authority_repository


router = APIRouter(tags=["auth"])


@router.post("/token", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    user = authority_repository.get_by_username(request.username)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(
        subject=user.username,
        expires_delta=timedelta(minutes=30),
    )
    return TokenResponse(access_token=token)
