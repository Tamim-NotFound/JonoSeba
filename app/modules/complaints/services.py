from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import (
    ForbiddenError,
    NotFoundError,
)
from app.modules.auth.models import User, UserRole
from app.modules.complaints.models import (
    Complaint,
    ComplaintPriority,
    ComplaintStatus,
)
from app.modules.complaints.repositories import ComplaintRepository
from app.modules.complaints.schemas import (
    ComplaintCreate,
    ComplaintUpdate,
)
from app.modules.departments.repositories import DepartmentRepository


class ComplaintService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = ComplaintRepository(db)
        self.department_repository = DepartmentRepository(db)

    async def create(
        self,
        data: ComplaintCreate,
        current_user: User,
    ) -> Complaint:
        """Create a complaint for the authenticated user."""

        department = await self.department_repository.get_by_id(
            data.department_id
        )

        if department is None:
            raise NotFoundError("Department not found.")

        if not department.is_active:
            raise ForbiddenError(
                "Cannot submit a complaint to an inactive department."
            )

        try:
            complaint = await self.repository.create(
                data=data,
                citizen_id=current_user.id,
            )

            await self.db.commit()
            return complaint

        except Exception:
            await self.db.rollback()
            raise

    async def get_all(
        self,
        current_user: User,
        search: str | None = None,
        status: ComplaintStatus | None = None,
        priority: ComplaintPriority | None = None,
        department_id: int | None = None,
    ) -> list[Complaint]:
        """List complaints based on the user's role."""

        citizen_id = None

        if current_user.role != UserRole.ADMIN:
            citizen_id = current_user.id

        return await self.repository.get_all(
            search=search,
            status=status,
            priority=priority,
            department_id=department_id,
            citizen_id=citizen_id,
        )

    async def get_by_id(
        self,
        complaint_id: int,
        current_user: User,
    ) -> Complaint:
        """Return a complaint if the user has access."""

        complaint = await self.repository.get_by_id(
            complaint_id
        )

        if complaint is None:
            raise NotFoundError("Complaint not found.")

        if (
            current_user.role != UserRole.ADMIN
            and complaint.citizen_id != current_user.id
        ):
            raise NotFoundError("Complaint not found.")

        return complaint

    async def update(
        self,
        complaint_id: int,
        data: ComplaintUpdate,
        current_user: User,
    ) -> Complaint:
        """Allow admins to update complaint status and priority."""

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenError("Admin access is required.")

        complaint = await self.repository.get_by_id(
            complaint_id
        )

        if complaint is None:
            raise NotFoundError("Complaint not found.")

        try:
            updated_complaint = await self.repository.update(
                complaint=complaint,
                data=data,
            )

            await self.db.commit()
            return updated_complaint

        except Exception:
            await self.db.rollback()
            raise

    async def delete(
        self,
        complaint_id: int,
        current_user: User,
    ) -> None:
        """Allow admins to delete a complaint."""

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenError("Admin access is required.")

        complaint = await self.repository.get_by_id(
            complaint_id
        )

        if complaint is None:
            raise NotFoundError("Complaint not found.")

        try:
            await self.repository.delete(complaint)
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise
