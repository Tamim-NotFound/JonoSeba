from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import (
    DateTime,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ComplaintStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class ComplaintPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Complaint(Base):
    __tablename__ = "complaints"

    __table_args__ = (
        Index("ix_complaints_citizen_status", "citizen_id", "status"),
        Index("ix_complaints_department_status", "department_id", "status"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[ComplaintStatus] = mapped_column(
        SQLAlchemyEnum(
            ComplaintStatus,
            name="complaint_status",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        default=ComplaintStatus.PENDING,
        nullable=False,
    )

    priority: Mapped[ComplaintPriority] = mapped_column(
        SQLAlchemyEnum(
            ComplaintPriority,
            name="complaint_priority",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        default=ComplaintPriority.MEDIUM,
        nullable=False,
    )

    citizen_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    citizen = relationship(
        "User",
        foreign_keys=[citizen_id],
    )

    department = relationship(
        "Department",
        foreign_keys=[department_id],
    )
