"""Add knowledge publication audit records.

Revision ID: d8a4f6b21903
Revises: c3e91ed18002
"""

from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB


revision: str = "d8a4f6b21903"
down_revision: str | None = "c3e91ed18002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "knowledge_publication_audits",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
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
            "reviewer_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "source_url",
            sa.String(length=2048),
            nullable=False,
        ),
        sa.Column(
            "source_name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "reviewed_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "approved_content_sha256",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "claim_evidence",
            JSONB(),
            nullable=False,
        ),
        sa.Column(
            "published_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["reviewer_id"],
            ["users.id"],
            ondelete="RESTRICT",
        ),
    )

    op.create_index(
        "ix_knowledge_audit_document_key",
        "knowledge_publication_audits",
        ["document_key"],
    )

    op.create_index(
        "ix_knowledge_audit_reviewer_id",
        "knowledge_publication_audits",
        ["reviewer_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_knowledge_audit_reviewer_id",
        table_name="knowledge_publication_audits",
    )

    op.drop_index(
        "ix_knowledge_audit_document_key",
        table_name="knowledge_publication_audits",
    )

    op.drop_table("knowledge_publication_audits")
