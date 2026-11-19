from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from app.modules.auth.permissions import AdminUserDep
from app.modules.departments.dependencies import (
    get_department_service,
)
from app.modules.departments.schemas import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.modules.departments.services import DepartmentService

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


DepartmentServiceDep = Annotated[
    DepartmentService,
    Depends(get_department_service),
]


@router.get(
    "",
    response_model=list[DepartmentResponse],
    status_code=status.HTTP_200_OK,
)
async def list_departments(
    service: DepartmentServiceDep,
    search: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
):
    """List departments with optional filters."""

    return await service.get_all(
        search=search,
        is_active=is_active,
    )


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_department(
    department_id: int,
    service: DepartmentServiceDep,
):
    """Get a department by ID."""

    return await service.get_by_id(department_id)


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    data: DepartmentCreate,
    service: DepartmentServiceDep,
    admin: AdminUserDep,
):
    """Create a department. Admin only."""

    return await service.create(data)


@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
)
async def update_department(
    department_id: int,
    data: DepartmentUpdate,
    service: DepartmentServiceDep,
    admin: AdminUserDep,
):
    """Partially update a department. Admin only."""

    return await service.update(
        department_id,
        data,
    )


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_department(
    department_id: int,
    service: DepartmentServiceDep,
    admin: AdminUserDep,
):
    """Delete a department. Admin only."""

    await service.delete(department_id)