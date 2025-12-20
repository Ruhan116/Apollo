"""User schemas"""
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    user_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
