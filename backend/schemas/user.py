# schemas/user.py - User response schemas
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserPublic(BaseModel):
    """Public user info (safe to return in API responses)."""
    id: int
    username: str
    email: EmailStr
    study_score: float
    level: int
    badge: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserStats(BaseModel):
    """Extended stats for dashboard."""
    id: int
    username: str
    study_score: float
    level: int
    badge: str
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_rate: float  # 0-100%

    model_config = {"from_attributes": True}


class LeaderboardEntry(BaseModel):
    """Single leaderboard row."""
    rank: int
    id: int
    username: str
    study_score: float
    level: int
    badge: str
    completed_tasks: int

    model_config = {"from_attributes": True}
