"""
AI Customer Support Agent - Configuration Module

Manages application settings with environment variable support.
"""
from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass, field

from dotenv import load_dotenv

# Load .env file
load_dotenv()


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    # OpenAI
    openai_api_key: str = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", "")
    )
    openai_base_url: str = field(
        default_factory=lambda: os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )
    )
    openai_model_name: str = field(
        default_factory=lambda: os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    )

    # Application
    app_host: str = field(default_factory=lambda: os.getenv("APP_HOST", "0.0.0.0"))
    app_port: int = field(default_factory=lambda: int(os.getenv("APP_PORT", "8000")))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Session
    max_session_history: int = field(
        default_factory=lambda: int(os.getenv("MAX_SESSION_HISTORY", "50"))
    )

    @property
    def is_api_key_set(self) -> bool:
        """Check if a valid API key has been configured."""
        return bool(self.openai_api_key) and self.openai_api_key != "sk-your-api-key-here"


# Global singleton
settings = Settings()
