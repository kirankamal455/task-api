from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

T = TypeVar('T')

class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Category(str, Enum):
    WORK = "Work"
    PERSONAL = "Personal"
    HEALTH = "Health"
    FINANCE = "Finance"
    EDUCATION = "Education"
    SHOPPING = "Shopping"
    TRAVEL = "Travel"
    OTHERS = "Others"

class ResponseModel(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None
    total: Optional[int] = None

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = Priority.MEDIUM
    category: Optional[Category] = Category.WORK

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
