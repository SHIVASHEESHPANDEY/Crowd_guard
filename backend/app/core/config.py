from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    secret_key: str = Field(default="crowd-guard-secret-key")
    algorithm: str = Field(default="HS256")
    twilio_account_sid: str = Field(default="")
    twilio_auth_token: str = Field(default="")
    twilio_from_number: str = Field(default="")
    firebase_project_id: str = Field(default="")
    aws_bucket_name: str = Field(default="")
    escalation_seconds: int = Field(default=120)
    high_priority_threshold: float = Field(default=0.78)
    medium_priority_threshold: float = Field(default=0.55)


settings = Settings()
