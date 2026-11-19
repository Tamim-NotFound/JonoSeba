from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.modules.complaints.models import (
    ComplaintPriority,
    ComplaintStatus,
)


class ComplaintCreate(BaseModel):
    """Request schema for citizen complaint submission."""

    title: str = Field(
        min_length=5,
        max_length=200,
        description="Short title describing the complaint.",
    )

    description: str = Field(
        min_length=10,
        max_length=5000,
        description="Detailed explanation of the problem.",
    )

    location: str = Field(
        min_length=3,
        max_length=255,
        description="Location where the problem occurred.",
    )

    department_id: int = Field(
        gt=0,
        description="ID of the responsible department.",
    )


class ComplaintUpdate(BaseModel):
    """Admin-only request schema for complaint management."""

    status: ComplaintStatus | None = None
    priority: ComplaintPriority | None = None


class ComplaintResponse(BaseModel):
    """Public API response schema for a complaint."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    location: str
    status: ComplaintStatus
    priority: ComplaintPriority
    citizen_id: int
    department_id: int
    created_at: datetime
    updated_at: datetime
