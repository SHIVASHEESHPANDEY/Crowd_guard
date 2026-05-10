import uuid

from app.models.domain import TouristIdentity
from app.schemas.tourist import (
    TouristRegistrationRequest,
    TouristRegistrationResponse,
    TouristVerificationResponse,
)
from app.services.blockchain_service import blockchain_service
from app.services.repositories import tourist_repository


class TouristService:
    def register(self, request: TouristRegistrationRequest) -> TouristRegistrationResponse:
        tourist_id = f"TID-{uuid.uuid4().hex[:12].upper()}"
        payload = request.model_dump()
        blockchain_hash = blockchain_service.anchor_identity(payload)
        tourist = TouristIdentity(
            tourist_id=tourist_id,
            blockchain_hash=blockchain_hash,
            **payload,
        )
        tourist_repository.save(tourist)
        return TouristRegistrationResponse(
            tourist_id=tourist_id,
            blockchain_hash=blockchain_hash,
            issued_at=tourist.created_at,
        )

    def verify(self, tourist_id: str) -> TouristVerificationResponse | None:
        tourist = tourist_repository.get(tourist_id)
        if tourist is None:
            return None
        payload = {
            "full_name": tourist.full_name,
            "passport_number": tourist.passport_number,
            "nationality": tourist.nationality,
            "email": tourist.email,
        }
        return TouristVerificationResponse(
            tourist_id=tourist.tourist_id,
            valid=blockchain_service.verify_hash(payload, tourist.blockchain_hash),
            blockchain_hash=tourist.blockchain_hash,
            full_name=tourist.full_name,
            nationality=tourist.nationality,
            issued_at=tourist.created_at,
        )


tourist_service = TouristService()
