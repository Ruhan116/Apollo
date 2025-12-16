from app.models.base import Base 
from sqlalchemy import Column, Integer, String
from app.models.base import Base 
import datetime 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(Integer, unique=True, nullable=False) 
    email = Column(str, unique=True, index=True, nullable= False) 
    hashed_pass = Column(str, nullable=False) 
    created_at = Column(datetime, nullable=False)

