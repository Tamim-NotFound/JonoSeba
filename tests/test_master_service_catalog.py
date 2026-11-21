from app.modules.knowledge.master_service_catalog import (
    COMPLAINT_ROUTING_RESEARCH,
    build_master_research_document,
    get_service_guide,
    get_service_guides,
    render_service_guide,
    save_master_research_document,
)


def test_ten_service_guides_exist():
    assert len(get_service_guides()) == 10


def test_all_document_keys_are_unique():
    keys = [
        guide.key
        for guide in get_service_guides()
    ]

    assert len(keys) == len(set(keys))


def test_all_guides_have_complete_sections():
    for guide in get_service_guides():
        assert guide.title_bn.strip()
        assert guide.department_bn.strip()
        assert guide.documents
        assert guide.fees
        assert guide.process
        assert guide.source_status == "research_pending"


def test_birth_registration_has_age_specific_documents():
    guide = get_service_guide(
        "birth_registration_new"
    )

    assert guide is not None

    text = " ".join(guide.documents)

    assert "০–৪৫ দিন" in text
    assert "৪৬ দিন–৫ বছর" in text
    assert "৫ বছরের বেশি" in text


def test_lost_birth_certificate_does_not_require_gd():
    guide = get_service_guide(
        "birth_certificate_reprint"
    )

    assert guide is not None

    text = render_service_guide(guide)

    assert "পুনঃমুদ্রণ" in text
    assert "GD-সংক্রান্ত কোনো বাধ্যতামূলক" in text


def test_rendered_guides_remain_unverified():
    for guide in get_service_guides():
        content = render_service_guide(guide)

        assert "RESEARCH — NOT VERIFIED" in content
        assert guide.department_bn in content
        assert "প্রয়োজনীয় কাগজপত্র" in content


def test_complaint_routing_is_research_only():
    assert len(COMPLAINT_ROUTING_RESEARCH) == 8

    content = build_master_research_document()

    assert "active departments" in content
    assert "জমা হয়েছে বলে জানানো যাবে না" in content
    assert "OTP" in content


def test_master_document_can_be_saved(tmp_path):
    output = tmp_path / "knowledge" / "master.md"

    result = save_master_research_document(
        output
    )

    assert result == output
    assert output.exists()

    content = output.read_text(
        encoding="utf-8"
    )

    assert "JonoSeba" in content
    assert "UNPUBLISHED" in content
    assert "ট্রেড লাইসেন্স" in content
    assert "হোল্ডিং" in content
