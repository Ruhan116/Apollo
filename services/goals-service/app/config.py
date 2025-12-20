"""Goals Service Configuration"""
import os
import sys
from pathlib import Path

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from shared.config import BaseConfig


class GoalsServiceConfig(BaseConfig):
    """Configuration for Goals Service"""

    def __init__(self):
        super().__init__(service_name="goals-service")

        # Service-specific config
        self.PORT = int(os.getenv("GOALS_SERVICE_PORT", "8002"))

        # Gemini API
        self.GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
        self.GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# Global settings instance
settings = GoalsServiceConfig()
