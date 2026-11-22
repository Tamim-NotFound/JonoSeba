from typing import Annotated, Any
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    ValidationError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.llm.tools.complaints import (
    get_my_complaint_status,
)
from app.integrations.llm.tools.departments import (
    list_departments,
)
from app.integrations.llm.tools.knowledge import (
    search_published_knowledge,
)
from app.modules.auth.models import User


class ListDepartmentsArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    search: str | None = Field(
        default=None,
        max_length=100,
    )


class ComplaintStatusArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    complaint_id: int = Field(
        strict=True,
        gt=0,
    )


class KnowledgeSearchArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=2000,
        ),
    ]

    include_research: bool = Field(
        default=False,
        strict=True,
    )


async def execute_ai_tool(
    *,
    tool_name: str,
    arguments: dict[str, Any],
    db: AsyncSession,
    current_user: User,
) -> dict[str, Any]:
    """
    Execute only approved JonoSeba tools.

    Database session and authenticated user come
    from the backend, never from Gemini.
    """

    if not isinstance(arguments, dict):
        return {
            "success": False,
            "error": (
                "Tool arguments must be a JSON object."
            ),
        }

    if tool_name == "list_departments":
        try:
            validated = (
                ListDepartmentsArgs.model_validate(
                    arguments
                )
            )
        except ValidationError:
            return {
                "success": False,
                "error": (
                    "Invalid department search arguments."
                ),
            }

        result = await list_departments(
            db=db,
            search=validated.search,
        )

        return {
            "success": True,
            "data": result,
        }

    if tool_name == "get_my_complaint_status":
        try:
            validated = (
                ComplaintStatusArgs.model_validate(
                    arguments
                )
            )
        except ValidationError:
            return {
                "success": False,
                "error": (
                    "Invalid complaint ID arguments."
                ),
            }

        result = await get_my_complaint_status(
            db=db,
            complaint_id=validated.complaint_id,
            current_user=current_user,
        )

        return {
            "success": True,
            "data": result,
        }

    if tool_name == "search_published_knowledge":
        try:
            validated = (
                KnowledgeSearchArgs.model_validate(
                    arguments
                )
            )
        except ValidationError:
            return {
                "success": False,
                "error": (
                    "Invalid knowledge search arguments."
                ),
            }

        kwargs: dict[str, Any] = {
            "db": db,
            "query": validated.query,
        }

        if validated.include_research:
            kwargs["include_research"] = True

        result = await search_published_knowledge(
            **kwargs
        )

        return {
            "success": True,
            "data": result,
        }

    return {
        "success": False,
        "error": "Unknown or unauthorized AI tool.",
    }
