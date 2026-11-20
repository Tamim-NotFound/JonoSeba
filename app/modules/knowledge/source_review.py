from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlsplit
from app.modules.auth.models import User, UserRole
from app.modules.knowledge.bangladesh_demo_pack import (
    DraftKnowledgeGuide,
)
from app.modules.knowledge.ingestion import (
    KnowledgeDocumentInput,
)
from app.modules.knowledge.models import KnowledgeLanguage


@dataclass(frozen=True)
class KnowledgeSourceReview:
    document_key: str
    source_url: str
    source_name: str
    reviewed_at: datetime
    reviewed_flags: tuple[str, ...]
    evidence_notes: str


def prepare_reviewed_document(
    *,
    draft: DraftKnowledgeGuide,
    review: KnowledgeSourceReview,
    reviewer: User,
) -> KnowledgeDocumentInput:
    """
    Prepare an admin-reviewed knowledge document.

    Does not write to the database or publish anything
    directly. The human reviewer is responsible for
    verifying the source and every factual claim.
    """

    if (
        reviewer.role != UserRole.ADMIN
        or not reviewer.is_active
    ):
        raise PermissionError(
            "Only an active admin can approve knowledge."
        )

    if review.document_key != draft.document_key:
        raise ValueError(
            "Review document key does not match the draft."
        )

    source_url = _validate_official_url(
        review.source_url
    )

    if (
        not isinstance(review.source_name, str)
        or not review.source_name.strip()
        or len(review.source_name.strip()) > 255
    ):
        raise ValueError(
            "A valid source_name is required."
        )

    if not isinstance(review.reviewed_at, datetime):
        raise ValueError(
            "reviewed_at must be a datetime."
        )

    if (
        review.reviewed_at.tzinfo is None
        or review.reviewed_at.utcoffset() is None
    ):
        raise ValueError(
            "reviewed_at must include a timezone."
        )

    if review.reviewed_at > datetime.now(timezone.utc):
        raise ValueError(
            "reviewed_at cannot be in the future."
        )

    if not draft.review_flags:
        raise ValueError(
            "Draft must contain review requirements."
        )

    if (
        not isinstance(review.reviewed_flags, tuple)
        or len(review.reviewed_flags)
        != len(set(review.reviewed_flags))
        or set(review.reviewed_flags)
        != set(draft.review_flags)
    ):
        raise ValueError(
            "Every draft review flag must be checked."
        )

    if (
        not isinstance(review.evidence_notes, str)
        or len(review.evidence_notes.strip()) < 30
    ):
        raise ValueError(
            "Evidence notes must contain at least "
            "30 characters."
        )

    if not isinstance(draft.content, str) or not draft.content.strip():
        raise ValueError(
            "Draft content cannot be empty."
        )

    return KnowledgeDocumentInput(
        document_key=draft.document_key,
        document_title=draft.title,
        content=draft.content,
        language=KnowledgeLanguage.BANGLA,
        source_url=source_url,
        source_name=review.source_name.strip(),
        verified_at=review.reviewed_at,
        is_published=True,
    )


def _validate_official_url(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            "An official source URL is required."
        )

    url = value.strip()

    if (
        len(url) > 2048
        or any(char.isspace() for char in url)
    ):
        raise ValueError(
            "Invalid official source URL."
        )

    try:
        parsed = urlsplit(url)
        hostname = (parsed.hostname or "").lower()
        port = parsed.port
    except ValueError as exc:
        raise ValueError(
            "Invalid official source URL."
        ) from exc

    if (
        parsed.scheme != "https"
        or port is not None
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError(
            "Official source must use HTTPS "
            "without credentials or custom ports."
        )

    if not (
        hostname == "gov.bd"
        or hostname.endswith(".gov.bd")
    ):
        raise ValueError(
            "Official source must use a gov.bd domain."
        )

    return url
