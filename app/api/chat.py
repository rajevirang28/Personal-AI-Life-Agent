from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db

from app.models.user import User

from app.schemas.chat import(
    ChatRequest,
    ChatResponse
)

from app.services.ai_service import generate_response
from app.services.context_service import build_user_context

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)

@router.post(
    "/",
    response_model=ChatResponse
)
def chat_with_ai(
    chat_data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    
    try:
        context = build_user_context(
            db=db,
            user_id=current_user.id
        )

        response = generate_response(
            user_message=chat_data.message,
            context=context
        )

        return{
            "response": response
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}"
        )