"""Auth schemas"""
from pydantic import BaseModel


class UserCreate(BaseModel):
    user_name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str
