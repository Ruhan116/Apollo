"""Auth Service Configuration"""
import os
import sys
from pathlib import Path

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from shared.config import BaseConfig


class AuthServiceConfig(BaseConfig):
    """Configuration for Auth Service"""

    def __init__(self):
        super().__init__(service_name="auth-service")

        # Service-specific config
        self.PORT = int(os.getenv("AUTH_SERVICE_PORT", "8001"))


# Global settings instance
settings = AuthServiceConfig()
