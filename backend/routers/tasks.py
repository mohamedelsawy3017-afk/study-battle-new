# routers/tasks.py - Study task CRUD endpoints
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from core.dependencies import get_current_user
from models.user import User
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from services.task_service import (
    create_task, get_tasks_for_user, get_task_by_id,
    update_task, complete_task, delete_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_study_task(
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new study task."""
    task = await create_task(db, current_user.id, data)
    return task


@router.get("/", response_model=list[TaskResponse])
async def list_my_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all tasks for the current user."""
    return await get_tasks_for_user(db, current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific task by ID."""
    task = await get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_study_task(
    task_id: int,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update task fields (title, description, minutes)."""
    task = await get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.is_done:
        raise HTTPException(status_code=400, detail="Cannot edit a completed task")
    return await update_task(db, task, data)


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_complete(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a task as done and award score to the user."""
    task = await get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await complete_task(db, task, current_user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_study_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a study task."""
    task = await get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await delete_task(db, task)
