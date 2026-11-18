from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.departments.models import Department
from app.modules.departments.repositories import DepartmentRepository
from app.core.exceptions import ConflictError, NotFoundError
from app.modules.departments.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
)

class DepartmentNotFoundError(NotFoundError):
    pass

class DepartmentAlreadyExistsError(ConflictError):
    pass


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = DepartmentRepository(db)

    async def create(
        self,
        data: DepartmentCreate,
    ) -> Department:
        existing = await self.repository.get_by_name(data.name)

        if existing is not None:
            raise DepartmentAlreadyExistsError(
                "A department with this name already exists."
            )

        try:
            department = await self.repository.create(data)
            await self.db.commit()
            return department
        except IntegrityError as exc:
            await self.db.rollback()
            raise DepartmentAlreadyExistsError(
                "A department with this name already exists."
            ) from exc
        except Exception:
            await self.db.rollback()
            raise

    async def get_by_id(
        self,
        department_id: int,
    ) -> Department:
        department = await self.repository.get_by_id(
            department_id
        )

        if department is None:
            raise DepartmentNotFoundError(
                "Department not found."
            )

        return department

    async def get_all(
        self,
        search: str | None = None,
        is_active: bool | None = None,
    ) -> list[Department]:
        return await self.repository.get_all(
            search=search,
            is_active=is_active,
        )

    async def update(
        self,
        department_id: int,
        data: DepartmentUpdate,
    ) -> Department:
        department = await self.get_by_id(department_id)

        if data.name is not None and data.name != department.name:
            existing = await self.repository.get_by_name(
                data.name
            )

            if existing is not None:
                raise DepartmentAlreadyExistsError(
                    "A department with this name already exists."
                )

        try:
            department = await self.repository.update(
                department,
                data,
            )
            await self.db.commit()
            return department
        except IntegrityError as exc:
            await self.db.rollback()
            raise DepartmentAlreadyExistsError(
                "A department with this name already exists."
            ) from exc
        except Exception:
            await self.db.rollback()
            raise

    async def delete(
        self,
        department_id: int,
    ) -> None:
        department = await self.get_by_id(department_id)

        try:
            await self.repository.delete(department)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
