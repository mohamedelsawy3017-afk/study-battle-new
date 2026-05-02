# routers/users.py - User profile and leaderboard endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.user import UserPublic, UserStats, LeaderboardEntry
from services.user_service import get_user_stats, get_leaderboard, get_user_by_username
from typing import Optional

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserPublic)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile."""
    return current_user


@router.get("/me/stats", response_model=UserStats)
async def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's full stats (score, level, tasks)."""
    stats = await get_user_stats(db, current_user.id)
    if not stats:
        raise HTTPException(status_code=404, detail="User not found")
    return stats


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard_endpoint(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),  # Auth required
):
    """Get top users ranked by study score."""
    return await get_leaderboard(db, min(limit, 50))


@router.get("/{username}", response_model=UserPublic)
async def get_user_profile(
    username: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),  # Auth required to view profiles
):
    """Get a user's public profile by username (for friend comparison)."""
    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{username}/stats", response_model=UserStats)
async def get_user_stats_endpoint(
    username: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Get another user's stats for comparison."""
    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await get_user_stats(db, user.id)
