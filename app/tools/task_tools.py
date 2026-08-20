from datetime import date

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