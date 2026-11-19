from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.models import User
from app.modules.complaints.repositories import (
    ComplaintRepository,
)
from app.modules.complaints.services import (
    ComplaintService,
)


async def get_my_complaint_status(
    db: AsyncSession,
    complaint_id: int,
    current_user: User,
) -> dict:
    """
    Return a complaint's current status from PostgreSQL.

    Reuses ComplaintService.get_by_id() so existing
    citizen ownership and admin permissions apply.

    Never trust a citizen_id supplied by the AI model.
    The authenticated user must come from the backend.
    """

    if complaint_id <= 0:
        return {
            "found": False,
            "message": "Complaint ID must be a positive integer.",
        }

    service = ComplaintService(db)

    try:
        complaint = await service.get_by_id(
            complaint_id=complaint_id,
            current_user=current_user,
        )

    except Exception as error:
        from app.core.exceptions import NotFoundError

        if not isinstance(error, NotFoundError):
            raise

        return {
            "found": False,
            "message": (
                "Complaint not found or you do not "
                "have permission to view it."
            ),
        }

    return {
        "found": True,
        "complaint": {
            "id": complaint.id,
            "title": complaint.title,
            "status": complaint.status.value,
            "priority": complaint.priority.value,
            "department_id": complaint.department_id,
            "created_at": complaint.created_at.isoformat(),
            "updated_at": complaint.updated_at.isoformat(),
        },
    }
