from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import case

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.task import Task
from app.models.user import User

from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskStatsResponse,
    TaskUpdate
)

from app.services import task_service


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_service.create_task(
        db=db,
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date
    )


@router.get(
    "/",
    response_model=list[TaskResponse]
)
def get_tasks(
    status_filter: str | None = Query(
        default=None,
        pattern="^(pending|in_progress|completed)$"
    ),
    priority: str | None = Query(
        default=None,
        pattern="^(low|medium|high)$"
    ),
    search: str | None = None,
    due_today: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = (
        db.query(Task)
        .filter(
            Task.user_id == current_user.id
        )
    )

    if status_filter:
        query = query.filter(
            Task.status == status_filter
        )

    if priority:
        query = query.filter(
            Task.priority == priority
        )

    if search:
        query = query.filter(
            Task.title.ilike(
                f"%{search}%"
            )
        )

    if due_today:
        query = query.filter(
            Task.due_date == date.today()
        )

    return (
        query
        .order_by(Task.created_at.desc())
        .all()
    )

@router.get(
    "/today/focus",
    response_model=list[TaskResponse]
)
def todays_focus(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    priority_order = case(
        (Task.priority == "high", 1),
        (Task.priority == "medium", 2),
        (Task.priority == "low", 3),
        else_ = 4
    )

    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == current_user.id,
            Task.status != "completed"
        )
        .order_by(
            Task.priority.desc(),
            Task.due_date.asc()
        )
        .all()
    )

    return tasks[:5]

@router.get(
    "/stats",
    response_model=TaskStatsResponse
)
def task_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == current_user.id
        )
        .all()
    )

    total_tasks = len(tasks)

    completed_tasks = sum(
        task.status == "completed"
        for task in tasks
    )

    pending_tasks = sum(
        task.status == "pending"
        for task in tasks
    )

    in_progress_tasks = sum(
        task.status == "in_progress"
        for task in tasks
    )

    overdue_tasks = sum(
        task.due_date is not None
        and task.due_date < date.today()
        and task.status != "completed"
        for task in tasks
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "overdue_tasks": overdue_tasks
    }

@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = task_service.get_task(
        db=db,
        user_id=current_user.id,
        task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = task_service.get_task(
        db=db,
        user_id=current_user.id,
        task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    return task_service.update_task(
        db=db,
        task=task,
        update_data=update_data
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = task_service.get_task(
        db=db,
        user_id=current_user.id,
        task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task_service.delete_task(
        db=db,
        task=task
    )

    return None


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse
)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = task_service.get_task(
        db=db,
        user_id=current_user.id,
        task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task_service.complete_task(
        db=db,
        task=task
    )