from fastapi import APIRouter
from app.modules.auth.dependencies import CurrentUserDep
from app.modules.chat.schemas import ChatRequest, ChatResponse
from app.modules.chat.services import ChatService

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
) -> ChatResponse:
    service = ChatService()
    return await service.chat(data)
