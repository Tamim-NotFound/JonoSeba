from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
import pytest
from app.modules.auth.models import UserRole
from app.modules.knowledge.bangladesh_demo_pack import (
    get_draft_guides,
)
from app.modules.knowledge.source_review import (
    KnowledgeSourceReview,
    prepare_reviewed_document,
)


@pytest.fixture
def draft():
    return get_draft_guides()[0]


@pytest.fixture
def admin():
    return SimpleNamespace(
        id=1,
        role=UserRole.ADMIN,
        is_active=True,
    )


def make_review(draft, **overrides):
    values = {
        "document_key": draft.document_key,
        "source_url": "https://bdris.gov.bd/",
        "source_name": "Test Registration Authority",
        "reviewed_at": datetime.now(timezone.utc),
        "reviewed_flags": draft.review_flags,
        "evidence_notes": (
            "Reviewer checked the draft against "
            "the cited source before approval."
        ),
    }

    values.update(overrides)

    return KnowledgeSourceReview(**values)


def test_admin_can_prepare_reviewed_document(
    draft,
    admin,
):
    document = prepare_reviewed_document(
        draft=draft,
        review=make_review(draft),
        reviewer=admin,
    )

    assert document.is_published is True
    assert document.source_url == "https://bdris.gov.bd/"
    assert document.verified_at is not None
    assert document.document_key == draft.document_key


def test_citizen_cannot_approve(draft, admin):
    admin.role = UserRole.CITIZEN

    with pytest.raises(PermissionError):
        prepare_reviewed_document(
            draft=draft,
            review=make_review(draft),
            reviewer=admin,
        )


def test_inactive_admin_cannot_approve(draft, admin):
    admin.is_active = False

    with pytest.raises(PermissionError):
        prepare_reviewed_document(
            draft=draft,
            review=make_review(draft),
            reviewer=admin,
        )


def test_all_review_flags_are_required(draft, admin):
    review = make_review(
        draft,
        reviewed_flags=draft.review_flags[:-1],
    )

    with pytest.raises(
        ValueError,
        match="Every draft review flag",
    ):
        prepare_reviewed_document(
            draft=draft,
            review=review,
            reviewer=admin,
        )


def test_document_key_must_match(draft, admin):
    review = make_review(
        draft,
        document_key="wrong-document",
    )

    with pytest.raises(
        ValueError,
        match="does not match",
    ):
        prepare_reviewed_document(
            draft=draft,
            review=review,
            reviewer=admin,
        )


def test_evidence_notes_are_required(draft, admin):
    review = make_review(
        draft,
        evidence_notes="Checked",
    )

    with pytest.raises(
        ValueError,
        match="Evidence notes",
    ):
        prepare_reviewed_document(
            draft=draft,
            review=review,
            reviewer=admin,
        )


@pytest.mark.parametrize(
    "url",
    [
        "https://example.org/guide",
        "http://bdris.gov.bd/",
        "https://bdris.gov.bd.evil.com/",
    ],
)
def test_invalid_official_urls_rejected(
    draft,
    admin,
    url,
):
    review = make_review(
        draft,
        source_url=url,
    )

    with pytest.raises(ValueError):
        prepare_reviewed_document(
            draft=draft,
            review=review,
            reviewer=admin,
        )


def test_future_review_date_rejected(draft, admin):
    review = make_review(
        draft,
        reviewed_at=(
            datetime.now(timezone.utc)
            + timedelta(days=1)
        ),
    )

    with pytest.raises(
        ValueError,
        match="future",
    ):
        prepare_reviewed_document(
            draft=draft,
            review=review,
            reviewer=admin,
        )


def test_review_date_requires_timezone(draft, admin):
    review = make_review(
        draft,
        reviewed_at=datetime(2026, 1, 1),
    )

    with pytest.raises(
        ValueError,
        match="timezone",
    ):
        prepare_reviewed_document(
            draft=draft,
            review=review,
            reviewer=admin,
        )
