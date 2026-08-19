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
