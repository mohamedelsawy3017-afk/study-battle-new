# schemas/task.py - Task request/response schemas
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    estimated_minutes: float = Field(default=25.0, ge=1, le=480)  # 1min - 8hrs


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    estimated_minutes: Optional[float] = Field(None, ge=1, le=480)


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    estimated_minutes: float
    is_done: bool
    completed_at: Optional[datetime]
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}
