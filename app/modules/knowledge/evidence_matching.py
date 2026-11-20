from dataclasses import dataclass
from urllib.parse import urlsplit
from app.modules.knowledge.research_claims import (
    RESEARCH_CLAIMS,
)


PRIORITY_CLAIM_IDS = (
    "BR-005",
    "BR-002",
    "BR-003",
    "BR-004",
    "FEE-001",
    "FEE-002",
)


@dataclass(frozen=True)
class SourceEvidence:
    """
    Reviewer-supplied source evidence.

    Source text must be copied from the actual document.
    This module does not fetch or authenticate websites.
    """

    claim_id: str
    source_url: str
    source_title: str
    source_text: str
    quoted_excerpt: str


@dataclass(frozen=True)
class EvidenceMatchResult:
    claim_id: str
    source_url: str
    excerpt_found: bool
    requires_human_review: bool
    notice: str


def _normalize_text(value: str) -> str:
    """
    Ignore whitespace differences while preserving
    wording and numeric values.
    """
    return " ".join(value.split())


def excerpt_occurs_in_source(
    source_text: str,
    quoted_excerpt: str,
) -> bool:
    """
    Check whether an excerpt appears in supplied source text.

    Whitespace differences are ignored, but words and
    numeric values must still match.

    Does not verify source authenticity or claim accuracy.
    """
    if not isinstance(source_text, str):
        return False

    if not isinstance(quoted_excerpt, str):
        return False

    source = _normalize_text(source_text)
    excerpt = _normalize_text(quoted_excerpt)

    if not source or not excerpt:
        return False

    return excerpt in source


def _required_text(
    value: str,
    field_name: str,
    minimum_length: int = 1,
) -> str:
    if not isinstance(value, str):
        raise ValueError(
            f"{field_name} must be text."
        )

    cleaned = value.strip()

    if len(cleaned) < minimum_length:
        raise ValueError(
            f"{field_name} must contain at least "
            f"{minimum_length} characters."
        )

    return cleaned


def _validate_official_url(value: str) -> str:
    url = _required_text(
        value,
        "source_url",
    )

    if (
        len(url) > 2048
        or any(char.isspace() for char in url)
    ):
        raise ValueError(
            "Invalid source URL."
        )

    try:
        parsed = urlsplit(url)
        hostname = (parsed.hostname or "").lower()
        port = parsed.port
    except ValueError as exc:
        raise ValueError(
            "Invalid source URL."
        ) from exc

    if (
        parsed.scheme != "https"
        or port is not None
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError(
            "Source must use a valid HTTPS URL."
        )

    if not (
        hostname == "gov.bd"
        or hostname.endswith(".gov.bd")
    ):
        raise ValueError(
            "Source must be from a gov.bd domain."
        )

    if parsed.path in {"", "/"}:
        raise ValueError(
            "Use a specific source page, "
            "not the website homepage."
        )

    return url


def match_source_evidence(
    evidence: SourceEvidence,
) -> EvidenceMatchResult:
    """
    Check whether a quoted excerpt occurs in the
    reviewer-supplied source text.

    This is a text-integrity check, not a factual
    correctness or government authenticity check.
    """

    known_claim_ids = {
        item.claim_id
        for item in RESEARCH_CLAIMS
    }

    if evidence.claim_id not in known_claim_ids:
        raise ValueError(
            "Unknown research claim ID."
        )

    source_url = _validate_official_url(
        evidence.source_url
    )

    _required_text(
        evidence.source_title,
        "source_title",
    )

    source_text = _required_text(
        evidence.source_text,
        "source_text",
        minimum_length=30,
    )

    excerpt = _required_text(
        evidence.quoted_excerpt,
        "quoted_excerpt",
        minimum_length=15,
    )

    excerpt_found = excerpt_occurs_in_source(
        source_text,
        excerpt,
    )

    return EvidenceMatchResult(
        claim_id=evidence.claim_id,
        source_url=source_url,
        excerpt_found=excerpt_found,
        requires_human_review=True,
        notice=(
            "Text match only. A human reviewer must "
            "confirm the issuing authority, effective "
            "date, scope, and whether this excerpt "
            "actually supports the claim."
        ),
    )


def get_priority_claims() -> tuple:
    """
    Return important birth-registration research
    claims that need official source verification.

    GD is intentionally excluded.
    """
    by_id = {
        item.claim_id: item
        for item in RESEARCH_CLAIMS
    }

    return tuple(
        by_id[claim_id]
        for claim_id in PRIORITY_CLAIM_IDS
    )
