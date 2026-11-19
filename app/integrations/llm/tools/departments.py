from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.departments.repositories import (
    DepartmentRepository,
)


async def list_departments(
    db: AsyncSession,
    search: str | None = None,
) -> dict:
    """
    Return active municipal departments from PostgreSQL.

    The result is structured for future Gemini tool calling.
    """

    repository = DepartmentRepository(db)

    departments = await repository.get_all(
        search=search,
        is_active=True,
    )

    return {
        "departments": [
            {
                "id": department.id,
                "name": department.name,
                "description": department.description,
            }
            for department in departments
        ],
        "count": len(departments),
    }
