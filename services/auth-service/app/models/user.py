"""User model"""
import sys
from pathlib import Path

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from shared.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
