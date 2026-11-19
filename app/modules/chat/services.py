import logging
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from google.genai.errors import APIError
from app.core.config import settings
from app.integrations.llm.client import GeminiLLMClient
from app.modules.chat.schemas import ChatRequest, ChatResponse


logger = logging.getLogger(__name__)


class ChatService:
    async def chat(self, data: ChatRequest) -> ChatResponse:
        client = GeminiLLMClient()

        try:
            history = [
                {
                    "role": item.role,
                    "content": item.content,
                }
                for item in data.history
            ]

            reply = await run_in_threadpool(
                client.generate_response,
                data.message,
                history,
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

        finally:
            client.close()
