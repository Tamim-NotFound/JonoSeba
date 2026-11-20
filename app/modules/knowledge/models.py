from datetime import datetime
from enum import Enum
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


# We will use a 768-dimensional embedding model.
# The embedding generation service must use this exact dimension.
EMBEDDING_DIMENSIONS = 768


class KnowledgeLanguage(str, Enum):
    BANGLA = "bn"
    ENGLISH = "en"


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    __table_args__ = (
        UniqueConstraint(
            "document_key",
            "chunk_index",
            name="uq_knowledge_document_chunk",
        ),
        Index(
            "ix_knowledge_document_key",
            "document_key",
        ),
        Index(
            "ix_knowledge_language_published",
            "language",
            "is_published",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    document_key: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    document_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    language: Mapped[KnowledgeLanguage] = mapped_column(
        SQLEnum(
            KnowledgeLanguage,
            name="knowledge_language",
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
        ),
        nullable=False,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )

    source_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_published: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(EMBEDDING_DIMENSIONS),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
