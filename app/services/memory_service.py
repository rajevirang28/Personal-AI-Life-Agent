from sqlalchemy.orm import Session

from app.models.memory import Memory

def create_memory(
    db: Session,
    user_id: int,
    title: str,
    content: str,
    memory_type: str 
):
    memory = Memory(
        user_id=user_id,
        title=title,
        content=content,
        memory_type=memory_type
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory

def get_memories(
    db: Session,
    user_id: int
):
    
    return(
        db.query(Memory)
        .filter(
            Memory.user_id == user_id
        )
        .order_by(
            Memory.created_at.desc()
        )
        .all()
    )

def get_memory(
    db: Session,
    user_id: int,
    memory_id: int
):
    return(
        db.query(Memory)
        .filter(
            Memory.id == memory_id,
            Memory.user_id == user_id
        )
        .first()
    )

def update_memory(
    db: Session,
    memory: Memory,
    update_data: dict
):
    for key, value in update_data.items():
        setattr(memory, key, value)

    db.commit()
    db.refresh(memory)

    return memory

def delete_memory(
        db: Session,
        memory: Memory
):
    db.delete(memory)
    db.commit()