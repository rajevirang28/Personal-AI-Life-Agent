from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.dependencies import get_current_user
from app.database.database import get_db

from app.models.user import User
from app.models.memory import Memory 

from app.schemas.memory import MemoryCreate, MemoryResponse, MemoryUpdate

from app.services import memory_service

router = APIRouter(
    prefix="/memories",
    tags=["Memories"]
)

@router.post(
    "/",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_memory(
    memory_data: MemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return memory_service.create_memory(
        db=db,
        user_id=current_user.id,
        title=memory_data.title,
        content=memory_data.content,
        memory_type=memory_data.memory_type
    )

@router.get(
    "/",
    response_model=list[MemoryResponse]
)
def get_memories(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return memory_service.get_memories(
        db=db,
        user_id=current_user.id
    )

@router.get(
    "/search",
    response_model=list[MemoryResponse]
)
def search_memories(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    memories = (
        db.query(Memory)
        .filter(
            Memory.user_id == current_user.id,
            or_(
                Memory.title.ilike(
                    f"%{q}%"
                ),
                Memory.content.ilike(
                    f"%{q}%"
                )
            )
        )
        .order_by(
            Memory.created_at.desc()
        )
        .all()
    )

    return memories

@router.get(
    "/stats/summary"
)
def memory_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    memories = (
        db.query(Memory)
        .filter(
            Memory.user_id == current_user.id
        )
        .all()
    )

    return {
        "total_memories": len(memories),
        "goals": sum(
            m.memory_type == "goal"
            for m in memories
        ),
        "preferences": sum(
            m.memory_type == "preference"
            for m in memories
        ),
        "ideas": sum(
            m.memory_type == "idea"
            for m in memories
        ),
        "important": sum(
            m.memory_type == "important"
            for m in memories
        ),
        "notes": sum(
            m.memory_type == "note"
            for m in memories
        )
    }

@router.get(
    "/{memory_id}",
    response_model=MemoryResponse
)
def get_memory(
    memory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    memory = memory_service.get_memories(
        db=db,
        user_id=current_user.id,
        memory_id=memory_id
    )

    if not memory:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )
    return memory

@router.put(
    "/{memory_id}",
    response_model=MemoryResponse
)
def update_memory(
    memory_id: int,
    memory_data: MemoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    memory = memory_service.get_memory(
        db=db,
        user_id=current_user.id,
        memory_id=memory_id
    )

    if not memory:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )
    
    update_data = memory_data.model_dump(
        exclude_unset=True
    )

    return memory_service.update_memory(
        db=db,
        memory=memory,
        update_data=update_data
    )

@router.delete(
    "/{memory_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_memory(
    memory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    memory = memory_service.get_memory(
        db=db,
        user_id=current_user.id,
        memory_id=memory_id
    )

    if not memory:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )
    
    memory_service.delete_memory(
        db=db,
        memory=memory
    )

    return None