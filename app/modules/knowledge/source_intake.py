from dataclasses import dataclass
from datetime import datetime, timezone
from ipaddress import ip_address
from urllib.parse import urlsplit


MIN_CONTENT_LENGTH = 30

PLACEHOLDER_DOMAINS = {
    "example.com",
    "example.org",
    "example.net",
    "localhost",
}


@dataclass(frozen=True)
class KnowledgeSourceCandidate:
    document_key: str
    title: str
    authority: str
    source_url: str
    content: str
    collected_at: datetime


def prepare_source_candidate(
    candidate: KnowledgeSourceCandidate,
) -> dict:
    """
    Validate collected source metadata before human review.

    This function DOES NOT approve, verify, publish,
    or ingest a document.
    """

    document_key = _required_text(
        candidate.document_key,
        "document_key",
        150,
    )

    title = _required_text(
        candidate.title,
        "title",
        255,
    )

    authority = _required_text(
        candidate.authority,
        "authority",
        255,
    )

    content = _required_text(
        candidate.content,
        "content",
        100_000,
    )

    if len(content) < MIN_CONTENT_LENGTH:
        raise ValueError(
            "Source content must contain at least "
            f"{MIN_CONTENT_LENGTH} characters."
        )

    source_url, hostname = _validate_source_url(
        candidate.source_url
    )

    collected_at = candidate.collected_at

    if not isinstance(collected_at, datetime):
        raise ValueError(
            "collected_at must be a datetime."
        )

    if (
        collected_at.tzinfo is None
        or collected_at.utcoffset() is None
    ):
        raise ValueError(
            "collected_at must include a timezone."
        )

    if collected_at > datetime.now(timezone.utc):
        raise ValueError(
            "collected_at cannot be in the future."
        )

    government_domain_candidate = (
        hostname == "gov.bd"
        or hostname.endswith(".gov.bd")
    )

    return {
        "document_key": document_key,
        "title": title,
        "authority": authority,
        "source_url": source_url,
        "content": content,
        "collected_at": collected_at.isoformat(),
        "government_domain_candidate": (
            government_domain_candidate
        ),
        "review_status": "pending",
        "is_published": False,
        "notice": (
            "This source has not been independently "
            "verified or approved. A government-looking "
            "domain does not prove that the content "
            "is accurate, current, or applicable."
        ),
    }


def _required_text(
    value: str,
    field_name: str,
    max_length: int,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"{field_name} cannot be empty."
        )

    cleaned = value.strip()

    if len(cleaned) > max_length:
        raise ValueError(
            f"{field_name} cannot exceed "
            f"{max_length} characters."
        )

    return cleaned


def _validate_source_url(
    value: str,
) -> tuple[str, str]:
    url = _required_text(value, "source_url", 2048)

    try:
        parsed = urlsplit(url)
        hostname = (parsed.hostname or "").lower()
        port = parsed.port
    except ValueError as exc:
        raise ValueError(
            "Invalid source URL."
        ) from exc

    if parsed.scheme.lower() != "https":
        raise ValueError(
            "Source URL must use HTTPS."
        )

    if not hostname or port is not None:
        raise ValueError(
            "Source URL must have a valid hostname "
            "without a custom port."
        )

    if parsed.username is not None or parsed.password is not None:
        raise ValueError(
            "Source URL cannot contain credentials."
        )

    if any(character.isspace() for character in url):
        raise ValueError(
            "Source URL cannot contain whitespace."
        )

    if (
        hostname in PLACEHOLDER_DOMAINS
        or any(
            hostname.endswith("." + domain)
            for domain in PLACEHOLDER_DOMAINS
        )
    ):
        raise ValueError(
            "Placeholder or local URLs are not allowed."
        )

    try:
        ip_address(hostname)
    except ValueError:
        pass
    else:
        raise ValueError(
            "IP-address source URLs are not allowed."
        )

    return url, hostname
