from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    user_name: str 
    email: str 
    password: str 

class UserLogin(BaseModel):
    email: str 
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    user_name: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
