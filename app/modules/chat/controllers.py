from fastapi import APIRouter
from app.db.session import get_db
from app.modules.auth.dependencies import CurrentUserDep
from app.modules.chat.schemas import ChatRequest, ChatResponse
from app.modules.chat.services import ChatService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    summary="Chat with JonoSeba AI",
)
async def chat_with_ai(
    data: ChatRequest,
    current_user: CurrentUserDep,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ChatResponse:
    service = ChatService()

    return await service.chat(
        data=data,
        db=db,
        current_user=current_user,
    )
