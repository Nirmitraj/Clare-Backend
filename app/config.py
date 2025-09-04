# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl
from typing import List, Optional

class Settings(BaseSettings):
    # existing
    GROQ_API_KEY: str = ""
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    BRAND: str = "#17B169"

    # Google OAuth / GBP
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[AnyUrl] = None
    GOOGLE_SCOPE: str = "https://www.googleapis.com/auth/business.manage"

    # 🔽 ADD THESE SMTP FIELDS
    smtp_host: Optional[str] = None      # maps to SMTP_HOST
    smtp_port: int = 587                 # maps to SMTP_PORT
    smtp_user: Optional[str] = None      # maps to SMTP_USER
    smtp_pass: Optional[str] = None      # maps to SMTP_PASS
    smtp_from: Optional[str] = None      # maps to SMTP_FROM
    smtp_to: Optional[str] = None        # maps to SMTP_TO

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,   # SMTP_HOST or smtp_host both OK
        extra="ignore",         # ignore env keys you don't declare
    )

settings = Settings()
