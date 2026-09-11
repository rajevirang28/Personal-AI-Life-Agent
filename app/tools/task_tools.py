from datetime import date
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.task import Task

def get_pending_tasks(
        db: Session,
        user_id: int
):
    """
    Return all unfinished tasks
    belonging to the current user.
    """

    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status != "completed"
        )
        .order_by(
            Task.due_date.asc()
        )
        .all()
    )
    return tasks

def get_today_priorities(
    db: Session,
    user_id: int
):
    """
    Return high-priority unfinished tasks
    that are due today or overdue.
    """

    today = date.today()

    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.priority == "high",
            Task.status != "completed",
            Task.due_date <= today
        )
        .order_by(
            Task.due_date.asc()
        )
        .all()
    )

    return tasks

def get_task_statistics(
    db: Session,
    user_id: int
):
    """
    Return task statistics for the current user.
    """

    total = (
        db.query(Task)
        .filter(
            Task.user_id == user_id
        )
        .count()
    )

    completed = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status == "completed"
        )
        .count()
    )

    pending = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status == "pending"
        )
        .count()
    )

    in_progress = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status == "in_progress"
        )
        .count()
    )

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "in_progress": in_progress
    }

def create_task(
    db: Session,
    user_id: int,
    title: str,
    description: str,
    priority: str,
    due_date: date = None
):
    task = Task(
        user_id = user_id,
        title = title,
        description = description,
        priority = priority,
        due_date = due_date,
        status = "pending"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "success": True,
        "message": "Task created successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "due_date": str(task.due_date) if task.due_date else None
        }
    }