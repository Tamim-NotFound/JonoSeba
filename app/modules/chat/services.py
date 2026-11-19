import logging
from fastapi import HTTPException
from google.genai.errors import APIError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.integrations.llm.tool_client import GeminiToolClient
from app.modules.auth.models import User
from app.modules.chat.schemas import ChatRequest, ChatResponse


logger = logging.getLogger(__name__)


class ChatService:
    async def chat(
        self,
        data: ChatRequest,
        db: AsyncSession,
        current_user: User,
    ) -> ChatResponse:
        client = GeminiToolClient()

        try:
            history = [
                {
                    "role": item.role,
                    "content": item.content,
                }
                for item in data.history
            ]

            reply = await client.generate_response(
                message=data.message,
                history=history,
                db=db,
                current_user=current_user,
            )

            return ChatResponse(
                reply=reply,
                model=settings.GEMINI_MODEL,
            )

        except APIError as error:
            status_code = error.code

            logger.warning(
                "Gemini API request failed with status %s",
                status_code,
            )

            if status_code in (429, 503):
                raise HTTPException(
                    status_code=503,
                    detail=(
                        "JonoSeba AI is temporarily unavailable. "
                        "Please try again later."
                    ),
                    headers={"Retry-After": "30"},
                ) from error

            raise HTTPException(
                status_code=502,
                detail=(
                    "JonoSeba AI could not complete the request. "
                    "Please try again later."
                ),
            ) from error

        except RuntimeError as error:
            logger.warning(
                "Gemini tool-calling failed: %s",
                type(error).__name__,
            )

            raise HTTPException(
                status_code=502,
                detail=(
                    "JonoSeba AI could not complete the request. "
                    "Please try again later."
                ),
            ) from error

        finally:
            await client.close()
