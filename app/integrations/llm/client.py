from google import genai
from google.genai import types
from app.core.config import settings


SYSTEM_PROMPT = """
You are JonoSeba AI, a helpful municipal citizen-service assistant
for people in Bangladesh.

Your responsibilities:
1. Help citizens understand municipal services.
2. Explain how to submit and track complaints.
3. Provide clear, polite, practical guidance.
4. Respond in Bangla when the user writes in Bangla.
5. Respond in English when the user writes in English.
6. If the user mixes Bangla and English, respond naturally
   in the same language style.
7. Never invent complaint statuses, department records,
   government rules, or official service information.
8. If verified information is unavailable, clearly say so.
9. Never claim that a complaint was submitted or updated
   unless the application confirms that action.
10. Never request passwords, API keys, or JWT tokens.
11. Use previous conversation messages to understand follow-up
    questions and maintain context.

You are an assistant, not a government official.
"""


class GeminiLLMClient:
    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Please configure it in your .env file."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        self.model = settings.GEMINI_MODEL

    def generate_response(
        self,
        message: str,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        if not message.strip():
            raise ValueError("Message cannot be empty.")

        contents: list[types.Content] = []

        if history:
            for item in history:
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

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_OUTPUT_TOKENS,
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()

    def close(self) -> None:
        self.client.close()
