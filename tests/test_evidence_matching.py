import pytest
from app.modules.knowledge.evidence_matching import (
    SourceEvidence,
    excerpt_occurs_in_source,
    get_priority_claims,
    match_source_evidence,
)

TEST_SOURCE_TEXT = (
    "This is a synthetic official-looking test document. "
    "It contains a sample sentence for matching. "
    "No real government requirements are verified here."
)


def make_evidence(**overrides):
    values = {
        "claim_id": "BR-005",
        "source_url": (
            "https://bdris.gov.bd/br/correction"
        ),
        "source_title": (
            "Synthetic Birth Registration Test Source"
        ),
        "source_text": TEST_SOURCE_TEXT,
        "quoted_excerpt": (
            "It contains a sample sentence for matching."
        ),
    }

    values.update(overrides)

    return SourceEvidence(**values)


def test_exact_excerpt_is_found():
    result = match_source_evidence(
        make_evidence()
    )

    assert result.excerpt_found is True
    assert result.requires_human_review is True


def test_whitespace_difference_is_accepted():
    result = match_source_evidence(
        make_evidence(
            quoted_excerpt=(
                "It contains  a sample sentence\n"
                "for matching."
            )
        )
    )

    assert result.excerpt_found is True


def test_modified_statement_is_not_matched():
    result = match_source_evidence(
        make_evidence(
            quoted_excerpt=(
                "It contains a different sentence "
                "for matching."
            )
        )
    )

    assert result.excerpt_found is False


def test_unknown_claim_is_rejected():
    with pytest.raises(
        ValueError,
        match="Unknown",
    ):
        match_source_evidence(
            make_evidence(
                claim_id="UNKNOWN-999"
            )
        )


@pytest.mark.parametrize(
    "url",
    [
        "https://example.org/guide",
        "http://bdris.gov.bd/br/correction",
        "https://bdris.gov.bd.evil.com/guide",
        "https://bdris.gov.bd/",
    ],
)
def test_invalid_source_url_is_rejected(url):
    with pytest.raises(ValueError):
        match_source_evidence(
            make_evidence(
                source_url=url
            )
        )


def test_short_excerpt_is_rejected():
    with pytest.raises(
        ValueError,
        match="15 characters",
    ):
        match_source_evidence(
            make_evidence(
                quoted_excerpt="Too short"
            )
        )


def test_short_source_text_is_rejected():
    with pytest.raises(
        ValueError,
        match="30 characters",
    ):
        match_source_evidence(
            make_evidence(
                source_text="Short"
            )
        )


def test_priority_claims_exclude_gd():
    claims = get_priority_claims()

    ids = {
        item.claim_id
        for item in claims
    }

    assert "BR-005" in ids
    assert "FEE-001" in ids
    assert "FEE-002" in ids

    assert "BL-003" not in ids


def test_priority_claims_are_unverified():
    for item in get_priority_claims():
        assert item.verified is False
        assert item.source_url is None


def test_shared_matcher_rejects_empty_excerpt():
    assert excerpt_occurs_in_source(
        "A synthetic source document.",
        "",
    ) is False

    assert excerpt_occurs_in_source(
        "A synthetic source document.",
        "source document",
    ) is True

    assert excerpt_occurs_in_source(
        "Fee amount is 25 BDT.",
        "Fee amount is 50 BDT.",
    ) is False
