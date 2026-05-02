# services/task_service.py - Task business logic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from models.task import Task
from models.user import User
from schemas.task import TaskCreate, TaskUpdate
from services.user_service import update_user_score
from typing import Optional


async def create_task(db: AsyncSession, user_id: int, data: TaskCreate) -> Task:
    """Create a new study task for a user."""
    task = Task(
        user_id=user_id,
        title=data.title,
        description=data.description,
        estimated_minutes=data.estimated_minutes,
        is_done=False,
    )
    db.add(task)
    await db.flush()
    return task


async def get_tasks_for_user(db: AsyncSession, user_id: int) -> list[Task]:
    """Get all tasks for a user, ordered by creation time (newest first)."""
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    return result.scalars().all()


async def get_task_by_id(db: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    """Get a specific task, ensuring it belongs to the user."""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def update_task(db: AsyncSession, task: Task, data: TaskUpdate) -> Task:
    """Partial update a task's fields."""
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.estimated_minutes is not None:
        task.estimated_minutes = data.estimated_minutes
    await db.flush()
    return task


async def complete_task(db: AsyncSession, task: Task, user: User) -> Task:
    """Mark a task as done and award study score to the user."""
    if task.is_done:
        return task  # Already done, no double-counting

    task.is_done = True
    task.completed_at = datetime.now(timezone.utc)
    await db.flush()

    # Award score: estimated study minutes
    await update_user_score(db, user, task.estimated_minutes)
    return task


async def delete_task(db: AsyncSession, task: Task) -> None:
    """Delete a task (and optionally reverse score if completed)."""
    await db.delete(task)
    await db.flush()
