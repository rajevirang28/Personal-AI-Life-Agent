from datetime import date

from sqlalchemy.orm import Session

from app.models.task import Task

def create_task(
    db: Session,
    user_id: int,
    title: str,
    description: str | None,
    priority: str,
    due_date: date | None
):
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_user_tasks(
        db: Session,
        user_id: int
):
    return(
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .all()
    )

def get_task(
        db: Session,
        user_id: int,
        task_id: int
):
    return(
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id
        )
        .first()
    )

def update_task(
    db: Session,
    task: Task,
    update_data: dict      
):
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task    

def delete_task(
    db: Session,
    task: Task
):
    db.delete(task)
    db.commit()

def complete_task(
    db: Session,
    task: Task
):
    task.status = "completed"

    db.commit()
    db.refresh(task)

    return task