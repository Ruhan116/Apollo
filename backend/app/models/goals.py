from enum import Enum
from app.models.base import Base 
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum 
from datetime import datetime

class GoalStatus(Enum):
    active = "Active"
    completed = "Completed"

class SubgoalCategory(Enum):
    skill = "Skill"
    mental = "Mental"
    communication = "Communication"

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # foreign key referencing users table 
    title = Column(String, nullable=False) 
    description = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(SQLAlchemyEnum(GoalStatus), nullable=False, default=GoalStatus.completed)

class SubGoal(Base):
    __tablename__ = "subgoals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    goal_id = Column(Integer, nullable=False)  # foreign key referencing goals table 
    title = Column(String, nullable=False) 
    description = Column(String)
    category = Column(SQLAlchemyEnum(SubgoalCategory), nullable=False)

class Actions(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subgoal_id = Column(Integer, nullable=False) # foreign key referencing subgoals table 
    description = Column(String)


