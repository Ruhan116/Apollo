"""Rate limiting configuration"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],  # Global rate limit
    storage_uri="memory://",  # For MVP use in-memory (production: use Redis)
    strategy="fixed-window",
)
