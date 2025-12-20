"""Shared configuration utilities"""
import os
from pathlib import Path
from dotenv import load_dotenv


class BaseConfig:
    """Base configuration for all services"""

    def __init__(self, service_name: str):
        # Load environment variables
        env_path = Path.cwd() / '.env'
        load_dotenv(dotenv_path=env_path)

        # Service
        self.SERVICE_NAME: str = os.getenv("SERVICE_NAME", service_name)
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        self.DEBUG: bool = os.getenv("DEBUG", "True") == "True"

        # API
        self.API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
        self.API_PORT: int = int(os.getenv("API_PORT", "8000"))

        # Database
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "")

        # JWT
        self.JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_HOURS", "24"))

        # CORS
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        self.CORS_ORIGINS: list[str] = cors_origins.split(",")

        # Service URLs (for inter-service communication)
        self.AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
        self.GOALS_SERVICE_URL: str = os.getenv("GOALS_SERVICE_URL", "http://localhost:8002")

        # Service API Keys (for service-to-service auth)
        self.SERVICE_API_KEY: str = os.getenv("SERVICE_API_KEY", "")
        self.AUTH_SERVICE_API_KEY: str = os.getenv("AUTH_SERVICE_API_KEY", "")
        self.GOALS_SERVICE_API_KEY: str = os.getenv("GOALS_SERVICE_API_KEY", "")
