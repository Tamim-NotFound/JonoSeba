import asyncio
import logging
from google import genai
from google.genai import types
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.integrations.llm.client import SYSTEM_PROMPT
from app.integrations.llm.tools.declarations import (
    JONOSEBA_GEMINI_TOOLS,
)
from app.integrations.llm.tools.executor import (
    execute_ai_tool,
)
from app.modules.auth.models import User


logger = logging.getLogger(__name__)


class GeminiToolClient:
    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing from .env."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    async def generate_response(
        self,
        *,
        message: str,
        history: list[dict[str, str]] | None,
        db: AsyncSession,
        current_user: User,
    ) -> str:
        if not message.strip():
            raise ValueError("Message cannot be empty.")

        contents: list[types.Content] = []

        for item in history or []:
            role = item.get("role")
            text = item.get("content", "")

            if role not in {"user", "model"}:
                raise ValueError(
                    "History role must be 'user' or 'model'."
                )

            if not text.strip():
                raise ValueError(
                    "History messages cannot be empty."
                )

            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(text=text)
                    ],
                )
            )

        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=message)
                ],
            )
        )

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=settings.GEMINI_TEMPERATURE,
            max_output_tokens=settings.GEMINI_MAX_OUTPUT_TOKENS,
            tools=JONOSEBA_GEMINI_TOOLS,
            automatic_function_calling=(
                types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            ),
        )

        for _ in range(3):
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=contents,
                config=config,
            )

            function_calls = response.function_calls or []

            if not function_calls:
                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return response.text.strip()

            if response.candidates:
                candidate_content = (
                    response.candidates[0].content
                )

                if candidate_content is not None:
                    contents.append(candidate_content)

            tool_parts: list[types.Part] = []

            for function_call in function_calls:
                tool_name = function_call.name or ""
                arguments = dict(
                    function_call.args or {}
                )

                logger.info(
                    "Gemini requested tool: %s",
                    tool_name,
                )

                result = await execute_ai_tool(
                    tool_name=tool_name,
                    arguments=arguments,
                    db=db,
                    current_user=current_user,
                )

                tool_parts.append(
                    types.Part.from_function_response(
                        name=tool_name,
                        response=result,
                    )
                )

            contents.append(
                types.Content(
                    role="user",
                    parts=tool_parts,
                )
            )

        raise RuntimeError(
            "Gemini exceeded the maximum tool-call rounds."
        )

    async def close(self) -> None:
        await self.client.aio.aclose()
