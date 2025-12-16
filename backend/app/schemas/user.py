from pydantic import BaseModel
import datetime

class User(BaseModel):
    id: str 
    user_name: str 
    email: str
    created_at: datetime   

