from app.modules.knowledge.bangladesh_demo_pack import (
    get_draft_guides,
)
from app.modules.knowledge.review_workbook import (
    build_review_workbook,
    save_review_workbook,
)


def test_workbook_contains_all_ten_guides():
    content = build_review_workbook(
        get_draft_guides()
    )

    for guide in get_draft_guides():
        assert guide.document_key in content
        assert guide.title in content


def test_every_review_flag_is_included():
    content = build_review_workbook(
        get_draft_guides()
    )

    for guide in get_draft_guides():
        for flag in guide.review_flags:
            assert f"- [ ] {flag}" in content


def test_workbook_has_pending_review_status():
    content = build_review_workbook(
        get_draft_guides()
    )

    assert (
        "PENDING HUMAN VERIFICATION"
        in content
    )

    assert (
        content.count(
            "**Review status:** PENDING"
        ) == 10
    )


def test_workbook_does_not_claim_verified_sources():
    content = build_review_workbook(
        get_draft_guides()
    )

    assert "NOT COLLECTED" in content
    assert "NOT CONFIRMED" in content
    assert "NOT PREPARED" in content


def test_workbook_includes_original_draft_text():
    content = build_review_workbook(
        get_draft_guides()
    )

    for guide in get_draft_guides():
        assert guide.content.strip() in content


def test_workbook_saves_to_selected_path(tmp_path):
    output = (
        tmp_path
        / "review"
        / "knowledge_review.md"
    )

    result = save_review_workbook(output)

    assert result == output
    assert output.exists()

    saved_text = output.read_text(
        encoding="utf-8"
    )

    assert "JonoSeba" in saved_text
    assert "PENDING HUMAN VERIFICATION" in saved_text
