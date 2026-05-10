from datetime import datetime

from pydantic import BaseModel, EmailStr


class TouristRegistrationRequest(BaseModel):
    full_name: str
    passport_number: str
    nationality: str
    email: EmailStr


class TouristRegistrationResponse(BaseModel):
    tourist_id: str
    blockchain_hash: str
    issued_at: datetime


class TouristVerificationResponse(BaseModel):
    tourist_id: str
    valid: bool
    blockchain_hash: str
    full_name: str
    nationality: str
    issued_at: datetime
