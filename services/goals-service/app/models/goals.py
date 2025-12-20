"""Goals models"""
import sys
from pathlib import Path
from enum import Enum

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from shared.database import Base
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
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(SQLAlchemyEnum(GoalStatus), nullable=False, default=GoalStatus.active)


class SubGoal(Base):
    __tablename__ = "subgoals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    goal_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(SQLAlchemyEnum(SubgoalCategory), nullable=False)


class Actions(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subgoal_id = Column(Integer, nullable=False)
    description = Column(String)
