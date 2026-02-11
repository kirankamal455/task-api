from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    user_id = Column(String, index=True)
    
    # New fields
    due_date = Column(DateTime, nullable=True)
    priority = Column(String, default="Medium")
    category = Column(String, default="Work")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
