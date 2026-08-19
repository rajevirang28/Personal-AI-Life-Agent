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