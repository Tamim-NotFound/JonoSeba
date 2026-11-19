from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.complaints.models import (
    Complaint,
    ComplaintPriority,
    ComplaintStatus,
)
from app.modules.complaints.schemas import (
    ComplaintCreate,
    ComplaintUpdate,
)


class ComplaintRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        data: ComplaintCreate,
        citizen_id: int,
    ) -> Complaint:
        """Add a new complaint to the current transaction."""

        complaint = Complaint(
            **data.model_dump(),
            citizen_id=citizen_id,
            status=ComplaintStatus.PENDING,
            priority=ComplaintPriority.MEDIUM,
        )

        self.db.add(complaint)
        await self.db.flush()
        await self.db.refresh(complaint)

        return complaint

    async def get_by_id(
        self,
        complaint_id: int,
    ) -> Complaint | None:
        """Find a complaint by its ID."""

        result = await self.db.execute(
            select(Complaint).where(
                Complaint.id == complaint_id
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
        search: str | None = None,
        status: ComplaintStatus | None = None,
        priority: ComplaintPriority | None = None,
        department_id: int | None = None,
        citizen_id: int | None = None,
    ) -> list[Complaint]:
        """List complaints with optional filters."""

        statement = select(Complaint)

        if search:
            statement = statement.where(
                or_(
                    Complaint.title.ilike(f"%{search}%"),
                    Complaint.description.ilike(f"%{search}%"),
                    Complaint.location.ilike(f"%{search}%"),
                )
            )

        if status is not None:
            statement = statement.where(
                Complaint.status == status
            )

        if priority is not None:
            statement = statement.where(
                Complaint.priority == priority
            )

        if department_id is not None:
            statement = statement.where(
                Complaint.department_id == department_id
            )

        if citizen_id is not None:
            statement = statement.where(
                Complaint.citizen_id == citizen_id
            )

        statement = statement.order_by(
            Complaint.created_at.desc(),
            Complaint.id.desc(),
        )

        result = await self.db.execute(statement)

        return list(result.scalars().all())

    async def update(
        self,
        complaint: Complaint,
        data: ComplaintUpdate,
    ) -> Complaint:
        """Update complaint fields in the current transaction."""

        update_data = data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for field, value in update_data.items():
            setattr(complaint, field, value)

        await self.db.flush()
        await self.db.refresh(complaint)

        return complaint

    async def delete(
        self,
        complaint: Complaint,
    ) -> None:
        """Delete a complaint in the current transaction."""

        await self.db.delete(complaint)
        await self.db.flush()
