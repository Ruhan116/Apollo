"""Goal schemas"""
from pydantic import BaseModel
from typing import Optional


class GoalCreate(BaseModel):
    user_id: Optional[int] = None
    prompt: str
