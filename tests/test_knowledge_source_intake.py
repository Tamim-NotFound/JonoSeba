from datetime import datetime, timedelta, timezone
import pytest
from app.modules.knowledge.source_intake import (
    KnowledgeSourceCandidate,
    prepare_source_candidate,
)


def make_candidate(**overrides):
    values = {
        "document_key": "birth-registration-guide",
        "title": "Birth Registration Guidance",
        "authority": "Relevant Registration Authority",
        "source_url": "https://bdris.gov.bd/",
        "content": (
            "This text represents a collected source "
            "excerpt for human review, not official guidance."
        ),
        "collected_at": datetime.now(timezone.utc),
    }

    values.update(overrides)

    return KnowledgeSourceCandidate(**values)


def test_government_domain_is_only_a_candidate():
    result = prepare_source_candidate(
        make_candidate()
    )

    assert result["government_domain_candidate"] is True
    assert result["review_status"] == "pending"
    assert result["is_published"] is False


def test_government_subdomain_is_recognized():
    result = prepare_source_candidate(
        make_candidate(
            source_url="https://everify.bdris.gov.bd/"
        )
    )

    assert result["government_domain_candidate"] is True


def test_external_domain_requires_review():
    result = prepare_source_candidate(
        make_candidate(
            source_url="https://www.wikipedia.org/"
        )
    )

    assert result["government_domain_candidate"] is False
    assert result["review_status"] == "pending"
    assert result["is_published"] is False


@pytest.mark.parametrize(
    "url",
    [
        "https://example.org/test-only",
        "http://bdris.gov.bd/",
        "https://localhost/test",
        "https://127.0.0.1/test",
        "https://user:pass@bdris.gov.bd/",
    ],
)
def test_unsafe_or_placeholder_urls_are_rejected(url):
    with pytest.raises(ValueError):
        prepare_source_candidate(
            make_candidate(source_url=url)
        )


def test_short_content_is_rejected():
    with pytest.raises(
        ValueError,
        match="at least",
    ):
        prepare_source_candidate(
            make_candidate(content="Short text")
        )


def test_missing_authority_is_rejected():
    with pytest.raises(
        ValueError,
        match="authority",
    ):
        prepare_source_candidate(
            make_candidate(authority="   ")
        )


def test_naive_collection_date_is_rejected():
    with pytest.raises(
        ValueError,
        match="timezone",
    ):
        prepare_source_candidate(
            make_candidate(
                collected_at=datetime(2026, 1, 1)
            )
        )


def test_future_collection_date_is_rejected():
    with pytest.raises(
        ValueError,
        match="future",
    ):
        prepare_source_candidate(
            make_candidate(
                collected_at=(
                    datetime.now(timezone.utc)
                    + timedelta(days=1)
                )
            )
        )


def test_oversized_document_key_is_rejected():
    with pytest.raises(
        ValueError,
        match="150 characters",
    ):
        prepare_source_candidate(
            make_candidate(
                document_key="A" * 151
            )
        )
