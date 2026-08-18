from datetime import date

from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.models.task import Task
from app.models.user import User


def build_user_context(
    db: Session,
    user_id: int
) -> str:

    # current user
    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    # task
    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status != "completed"
        )
        .order_by(
            Task.due_date.asc()
        )
        .limit(10)
        .all()
    )

    # memories
    memories = (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id
        )
        .order_by(
            Memory.created_at.desc()
        )
        .limit(10)
        .all()
    )

    # count task
    pending_task_count = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status != "completed"
        )
        .count()
    )

    # date of today
    today = date.today()

    # today's priorities
    priority_tasks = (
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

    context_parts = []

    # USER
    context_parts.append(
        "USER:"
    )

    if user:
        context_parts.append(
            f"- Name: {user.name}"
        )
    else:
        context_parts.append(
            "- Name: Unknown"
        )

    # TASK SUMMARY
    context_parts.append(
        "\nTASK SUMMARY:"
    )

    context_parts.append(
        f"Total pending tasks: "
        f"{pending_task_count}"
    )

    # TODAY'S PRIORITIES
    context_parts.append(
        "\nTODAY'S PRIORITIES:"
    )

    if priority_tasks:

        for task in priority_tasks:

            context_parts.append(
                f"- {task.title} "
                f"(due: {task.due_date}, "
                f"status: {task.status})"
            )

    else:

        context_parts.append(
            "- No high-priority tasks "
            "due today or overdue."
        )

    # CURRENT TASKS
    context_parts.append(
        "\nCURRENT TASKS:"
    )

    if tasks:

        for task in tasks:

            context_parts.append(
                f"- {task.title} "
                f"(priority: {task.priority}, "
                f"status: {task.status}, "
                f"due: {task.due_date})"
            )

    else:

        context_parts.append(
            "- No pending tasks."
        )

    # PERSONAL MEMORIES
    context_parts.append(
        "\nPERSONAL MEMORIES:"
    )

    if memories:

        for memory in memories:

            context_parts.append(
                f"- [{memory.memory_type}] "
                f"{memory.title}: "
                f"{memory.content}"
            )

    else:

        context_parts.append(
            "- No memories available."
        )

    return "\n".join(
        context_parts
    )