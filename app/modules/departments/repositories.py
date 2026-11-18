from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.departments.models import Department
from app.modules.departments.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
)


class DepartmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        data: DepartmentCreate,
    ) -> Department:
        department = Department(**data.model_dump())

        self.db.add(department)
        await self.db.flush()
        await self.db.refresh(department)

        return department

    async def get_by_id(
        self,
        department_id: int,
    ) -> Department | None:
        return await self.db.get(
            Department,
            department_id,
        )

    async def get_by_name(
        self,
        name: str,
    ) -> Department | None:
        statement = select(Department).where(
            Department.name == name
        )

        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> list[Department]:
        statement = select(Department)

        if search:
            statement = statement.where(
                Department.name.ilike(f"%{search}%")
            )

        if is_active is not None:
            statement = statement.where(
                Department.is_active == is_active
            )

        statement = statement.order_by(Department.id)

        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def update(
        self,
        department: Department,
        data: DepartmentUpdate,
    ) -> Department:
        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(department, field, value)

        await self.db.flush()
        await self.db.refresh(department)

        return department

    async def delete(
        self,
        department: Department,
    ) -> None:
        await self.db.delete(department)
        await self.db.flush()
