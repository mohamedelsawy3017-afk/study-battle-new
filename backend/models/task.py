# models/task.py - Study task database model
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, func
from database.session import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Task fields
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    estimated_minutes = Column(Float, default=25.0)  # Default: 1 Pomodoro

    # Status
    is_done = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Task '{self.title}' | Done: {self.is_done}>"
