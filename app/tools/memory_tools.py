from sqlalchemy.orm import Session

from app.models.memory import Memory

def search_memories(
    db: Session,
    user_id: int,
    query: str
):
    """
    Search the user's memories
    using title and content.
    """

    memories = (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id,
            (
                Memory.title.ilike(
                    f"%{query}%"
                )
                |
                Memory.content.ilike(
                    f"%{query}%"
                )
            )
        )
        .order_by(
            Memory.created_at.desc()
        )
        .limit(10)
        .all()
    )
    return memories

def get_goals(
    db: Session,
    user_id: int
):
    """
    Return all goal memories
    belonging to the current user.
    """

    goals = (
        db.query(Memory)
        .filter(
            Memory.user_id == user_id,
            Memory.memory_type == "goal"
        )
        .order_by(
            Memory.created_at.desc()
        )
        .all()
    )

    return goals