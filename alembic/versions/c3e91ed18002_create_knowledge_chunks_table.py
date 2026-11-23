"""create knowledge chunks table

Revision ID: c3e91ed18002
Revises: 06c6b7b005b8
Create Date: 2026-11-20 15:12:38.410415
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# Revision identifiers used by Alembic.
revision: str = "c3e91ed18002"

down_revision: Union[str, Sequence[str], None] = (
    "06c6b7b005b8"
)

branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    """Create the RAG knowledge chunks table."""

    op.create_table(
        "knowledge_chunks",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "document_key",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "document_title",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "language",
            sa.Enum(
                "bn",
                "en",
                name="knowledge_language",
            ),
            nullable=False,
        ),
        sa.Column(
            "source_url",
            sa.String(length=2048),
            nullable=True,
        ),
        sa.Column(
            "source_name",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "verified_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "is_published",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "embedding",
            Vector(768),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "document_key",
            "chunk_index",
            name="uq_knowledge_document_chunk",
        ),
    )

    op.create_index(
        "ix_knowledge_chunks_id",
        "knowledge_chunks",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_knowledge_document_key",
        "knowledge_chunks",
        ["document_key"],
        unique=False,
    )

    op.create_index(
        "ix_knowledge_language_published",
        "knowledge_chunks",
        ["language", "is_published"],
        unique=False,
    )


def downgrade() -> None:
    """Remove the RAG knowledge chunks table."""

    op.drop_index(
        "ix_knowledge_language_published",
        table_name="knowledge_chunks",
    )

    op.drop_index(
        "ix_knowledge_document_key",
        table_name="knowledge_chunks",
    )

    op.drop_index(
        "ix_knowledge_chunks_id",
        table_name="knowledge_chunks",
    )

    op.drop_table("knowledge_chunks")

    # PostgreSQL enum types are independent database objects.
    # Remove the enum after its table has been dropped.
    sa.Enum(
        name="knowledge_language",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )