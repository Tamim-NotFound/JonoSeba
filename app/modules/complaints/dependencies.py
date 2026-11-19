from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.modules.complaints.services import ComplaintService


async def get_complaint_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ComplaintService:
    """Provide ComplaintService with a database session."""

    return ComplaintService(db)


ComplaintServiceDep = Annotated[
    ComplaintService,
    Depends(get_complaint_service),
]
