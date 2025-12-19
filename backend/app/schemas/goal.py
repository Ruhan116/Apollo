from pydantic import BaseModel
import datetime

class GoalCreate(BaseModel):
    user_id: int  
    prompt: str

