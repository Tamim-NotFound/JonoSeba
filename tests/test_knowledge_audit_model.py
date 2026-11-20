from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base
from app.modules.knowledge.models import (
    KnowledgeChunk,
    KnowledgePublicationAudit,
)


def test_audit_table_is_registered():
    assert (
        "knowledge_publication_audits"
        in Base.metadata.tables
    )


def test_existing_knowledge_table_is_preserved():
    assert KnowledgeChunk.__tablename__ == (
        "knowledge_chunks"
    )

    assert KnowledgeChunk.__table__.columns[
        "embedding"
    ].type.dim == 768


def test_audit_contains_required_columns():
    columns = {
        column.name
        for column in KnowledgePublicationAudit.__table__.columns
    }

    assert {
        "id",
        "document_key",
        "document_title",
        "reviewer_id",
        "source_url",
        "source_name",
        "reviewed_at",
        "approved_content_sha256",
        "claim_evidence",
        "published_at",
    }.issubset(columns)


def test_reviewer_has_user_foreign_key():
    column = KnowledgePublicationAudit.__table__.columns[
        "reviewer_id"
    ]

    assert column.nullable is False

    foreign_keys = list(column.foreign_keys)

    assert len(foreign_keys) == 1
    assert foreign_keys[0].target_fullname == "users.id"
    assert foreign_keys[0].ondelete == "RESTRICT"


def test_audit_stores_json_evidence():
    column = KnowledgePublicationAudit.__table__.columns[
        "claim_evidence"
    ]

    assert isinstance(column.type, JSONB)
    assert column.nullable is False


def test_audit_has_publication_timestamp():
    column = KnowledgePublicationAudit.__table__.columns[
        "published_at"
    ]

    assert column.nullable is False
    assert column.server_default is not None
