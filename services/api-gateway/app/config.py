"""API Gateway Configuration"""
import os
import sys
from pathlib import Path

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from shared.config import BaseConfig


class GatewayConfig(BaseConfig):
    """API Gateway specific configuration"""

    def __init__(self):
        super().__init__(service_name="api-gateway")

        # Gateway specific settings
        self.PORT = int(os.getenv("GATEWAY_PORT", "8000"))

        # Backend service URLs
        self.AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
        self.GOALS_SERVICE_URL = os.getenv("GOALS_SERVICE_URL", "http://localhost:8002")

        # Service API Keys for service-to-service communication
        self.AUTH_SERVICE_API_KEY = os.getenv("AUTH_SERVICE_API_KEY", "auth-service-secret-key")
        self.GOALS_SERVICE_API_KEY = os.getenv("GOALS_SERVICE_API_KEY", "goals-service-secret-key")

        # JWT Settings (for token validation)
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key-apollo-2024")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

        # Public routes (no authentication required)
        self.PUBLIC_ROUTES = [
            "/api/auth/register",
            "/api/auth/login",
            "/health/live",
            "/health/ready",
            "/metrics",
            "/docs",
            "/openapi.json",
        ]


settings = GatewayConfig()
