from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from app.modules.departments.dependencies import get_department_service
from app.modules.departments.schemas import DepartmentResponse
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
    search: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=100,
            description="Search departments by name",
        ),
    ] = None,
    is_active: bool | None = None,
):
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
    return await service.get_by_id(department_id)
