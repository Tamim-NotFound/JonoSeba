from fastapi import APIRouter, Query, status
from app.modules.auth.dependencies import CurrentUserDep
from app.modules.auth.permissions import AdminUserDep
from app.modules.complaints.dependencies import ComplaintServiceDep
from app.modules.complaints.models import (
    ComplaintPriority,
    ComplaintStatus,
)
from app.modules.complaints.schemas import (
    ComplaintCreate,
    ComplaintResponse,
    ComplaintUpdate,
)


router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"],
)


@router.post(
    "",
    response_model=ComplaintResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_complaint(
    data: ComplaintCreate,
    service: ComplaintServiceDep,
    current_user: CurrentUserDep,
):
    """Submit a complaint as an authenticated user."""

    return await service.create(
        data=data,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=list[ComplaintResponse],
    status_code=status.HTTP_200_OK,
)
async def list_complaints(
    service: ComplaintServiceDep,
    current_user: CurrentUserDep,
    search: str | None = Query(default=None),
    status_filter: ComplaintStatus | None = Query(
        default=None,
        alias="status",
    ),
    priority: ComplaintPriority | None = Query(default=None),
    department_id: int | None = Query(default=None, gt=0),
):
    """List complaints visible to the authenticated user."""

    return await service.get_all(
        current_user=current_user,
        search=search,
        status=status_filter,
        priority=priority,
        department_id=department_id,
    )


@router.get(
    "/{complaint_id}",
    response_model=ComplaintResponse,
    status_code=status.HTTP_200_OK,
)
async def get_complaint(
    complaint_id: int,
    service: ComplaintServiceDep,
    current_user: CurrentUserDep,
):
    """Get a complaint if the user is its owner or an admin."""

    return await service.get_by_id(
        complaint_id=complaint_id,
        current_user=current_user,
    )


@router.patch(
    "/{complaint_id}",
    response_model=ComplaintResponse,
    status_code=status.HTTP_200_OK,
)
async def update_complaint(
    complaint_id: int,
    data: ComplaintUpdate,
    service: ComplaintServiceDep,
    admin: AdminUserDep,
):
    """Update complaint status and priority. Admin only."""

    return await service.update(
        complaint_id=complaint_id,
        data=data,
        current_user=admin,
    )


@router.delete(
    "/{complaint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_complaint(
    complaint_id: int,
    service: ComplaintServiceDep,
    admin: AdminUserDep,
):
    """Delete a complaint. Admin only."""

    await service.delete(
        complaint_id=complaint_id,
        current_user=admin,
    )
