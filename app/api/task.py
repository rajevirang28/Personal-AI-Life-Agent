from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# Temporary user ID
# Authentication will be added later.
CURRENT_USER_ID = 1

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    task = Task(
        user_id=CURRENT_USER_ID,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

@router.get(
    "/",
    response_model=list[TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db)
):
    tasks = (
        db.query(Task)
        .filter(Task.user_id == CURRENT_USER_ID)
        .order_by(Task.created_at.desc())
        .all()
    )

    return tasks

@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == CURRENT_USER_ID
        )
        .first()
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
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == CURRENT_USER_ID
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    update_data = task_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

@router.patch(
        "/{task_id}/complete",
        response_model=TaskResponse
)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == CURRENT_USER_ID
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task.status = "completed"
    db.commit()
    db.refresh(task)

    return task

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == CURRENT_USER_ID
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    db.delete(task)
    db.commit()

    return None