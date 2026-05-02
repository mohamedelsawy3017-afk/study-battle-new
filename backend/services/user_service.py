# services/user_service.py - User business logic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.user import User, compute_level_and_badge
from models.task import Task
from core.security import hash_password
from schemas.user import UserStats, LeaderboardEntry
from typing import Optional


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, email: str, password: str) -> User:
    """Create a new user with hashed password."""
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        study_score=0.0,
        level=1,
        badge="Rookie 🐣",
    )
    db.add(user)
    await db.flush()  # Get the ID without committing
    return user


async def update_user_score(db: AsyncSession, user: User, minutes_to_add: float) -> User:
    """Add study minutes to user score and recalculate level/badge."""
    user.study_score += minutes_to_add
    level, badge = compute_level_and_badge(user.study_score)
    user.level = level
    user.badge = badge
    await db.flush()
    return user


async def get_user_stats(db: AsyncSession, user_id: int) -> Optional[UserStats]:
    """Get full stats for a user including task counts."""
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    # Count tasks
    total_q = await db.execute(select(func.count(Task.id)).where(Task.user_id == user_id))
    total = total_q.scalar() or 0

    done_q = await db.execute(
        select(func.count(Task.id)).where(Task.user_id == user_id, Task.is_done == True)
    )
    done = done_q.scalar() or 0
    pending = total - done
    rate = round((done / total * 100) if total > 0 else 0, 1)

    return UserStats(
        id=user.id,
        username=user.username,
        study_score=user.study_score,
        level=user.level,
        badge=user.badge,
        total_tasks=total,
        completed_tasks=done,
        pending_tasks=pending,
        completion_rate=rate,
    )


async def get_leaderboard(db: AsyncSession, limit: int = 10) -> list[LeaderboardEntry]:
    """Get top users ranked by study score."""
    result = await db.execute(
        select(User).order_by(User.study_score.desc()).limit(limit)
    )
    users = result.scalars().all()

    leaderboard = []
    for rank, user in enumerate(users, start=1):
        # Count completed tasks for this user
        done_q = await db.execute(
            select(func.count(Task.id)).where(Task.user_id == user.id, Task.is_done == True)
        )
        done = done_q.scalar() or 0

        leaderboard.append(LeaderboardEntry(
            rank=rank,
            id=user.id,
            username=user.username,
            study_score=user.study_score,
            level=user.level,
            badge=user.badge,
            completed_tasks=done,
        ))

    return leaderboard
