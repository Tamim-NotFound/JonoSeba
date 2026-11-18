from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.modules.departments.services import DepartmentService


def get_department_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DepartmentService:
    return DepartmentService(db)
