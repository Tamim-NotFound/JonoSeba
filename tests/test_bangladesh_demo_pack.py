from app.modules.knowledge.models import KnowledgeLanguage
from app.modules.knowledge.bangladesh_demo_pack import (
    get_draft_guides,
)


def test_pack_contains_ten_guides():
    assert len(get_draft_guides()) == 10


def test_document_keys_are_unique():
    guides = get_draft_guides()

    keys = [guide.document_key for guide in guides]

    assert len(keys) == len(set(keys))


def test_all_guides_are_unpublished():
    for guide in get_draft_guides():
        document = guide.to_ingestion_input()

        assert document.is_published is False
        assert document.verified_at is None
        assert document.source_url is None


def test_all_guides_use_bangla():
    for guide in get_draft_guides():
        document = guide.to_ingestion_input()

        assert document.language == KnowledgeLanguage.BANGLA


def test_all_guides_have_review_flags():
    for guide in get_draft_guides():
        assert guide.review_flags
        assert all(guide.review_flags)


def test_guides_have_meaningful_content():
    for guide in get_draft_guides():
        assert guide.title.strip()
        assert len(guide.content) >= 100


def test_lost_certificate_guide_flags_gd_rule():
    guide = next(
        guide
        for guide in get_draft_guides()
        if guide.document_key == "bd-lost-birth-certificate"
    )

    assert "GD" in guide.content
    assert any(
        "GD" in flag
        for flag in guide.review_flags
    )


def test_fee_guide_requires_review():
    guide = next(
        guide
        for guide in get_draft_guides()
        if guide.document_key
        == "bd-birth-death-registration-fees"
    )

    assert "২৫" in guide.content
    assert "৫০" in guide.content
    assert "যাচাই" in guide.content

    assert any(
        "fee" in flag.lower()
        for flag in guide.review_flags
    )
