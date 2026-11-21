from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from app.modules.knowledge.master_publication_bridge import (
    DOCUMENT_KEY_PREFIX,
    build_master_review_packet,
    get_all_master_review_packets,
    publish_reviewed_master_guide,
)


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


def test_all_ten_master_guides_have_review_packets():
    packets = get_all_master_review_packets()

    assert len(packets) == 10

    assert len(
        {packet.draft.document_key for packet in packets}
    ) == 10


def test_birth_guide_contains_its_own_content():
    packet = build_master_review_packet(
        "birth_registration_new"
    )

    assert packet.guide_key == "birth_registration_new"

    assert packet.draft.document_key == (
        DOCUMENT_KEY_PREFIX
        + "birth_registration_new"
    )

    assert packet.draft.title == "নতুন জন্মনিবন্ধন"

    assert "০–৪৫ দিন" in packet.draft.content
    assert "৫ বছরের বেশি" in packet.draft.content


def test_each_guide_has_separate_review_requirements():
    packets = get_all_master_review_packets()

    for packet in packets:
        assert len(packet.required_evidence) == 5

        assert (
            packet.draft.review_flags
            == packet.required_evidence
        )

        assert any(
            "required documents" in flag
            for flag in packet.required_evidence
        )

        assert any(
            "fees and charges" in flag
            for flag in packet.required_evidence
        )


def test_review_packets_are_unpublished_research():
    packets = get_all_master_review_packets()

    for packet in packets:
        assert "RESEARCH — NOT VERIFIED" in (
            packet.draft.content
        )


def test_unknown_guide_is_rejected():
    with pytest.raises(
        ValueError,
        match="Unknown master service guide",
    ):
        build_master_review_packet(
            "nonexistent_service"
        )


async def test_publication_rejects_wrong_review_key():
    service = SimpleNamespace(
        publish=AsyncMock()
    )

    review = SimpleNamespace(
        document_key="wrong-document-key"
    )

    with pytest.raises(
        ValueError,
        match="does not match",
    ):
        await publish_reviewed_master_guide(
            service=service,
            guide_key="trade_license",
            review=review,
            reviewer=SimpleNamespace(id=1),
            approved_content="Test approved content",
            evidence=(object(),),
        )

    service.publish.assert_not_awaited()


async def test_missing_evidence_blocks_publication():
    service = SimpleNamespace(
        publish=AsyncMock()
    )

    packet = build_master_review_packet(
        "trade_license"
    )

    review = SimpleNamespace(
        document_key=packet.draft.document_key
    )

    with pytest.raises(
        ValueError,
        match="evidence is required",
    ):
        await publish_reviewed_master_guide(
            service=service,
            guide_key="trade_license",
            review=review,
            reviewer=SimpleNamespace(id=1),
            approved_content="Test approved content",
            evidence=(),
        )

    service.publish.assert_not_awaited()


async def test_valid_handoff_uses_existing_publisher():
    service = SimpleNamespace(
        publish=AsyncMock(
            return_value={
                "document_key": (
                    "bd-master-trade_license"
                ),
                "chunk_count": 2,
                "is_published": True,
            }
        )
    )

    packet = build_master_review_packet(
        "trade_license"
    )

    review = SimpleNamespace(
        document_key=packet.draft.document_key
    )

    reviewer = SimpleNamespace(id=1)

    evidence = (object(),)

    result = await publish_reviewed_master_guide(
        service=service,
        guide_key="trade_license",
        review=review,
        reviewer=reviewer,
        approved_content=(
            "Synthetic approved content for handoff testing."
        ),
        evidence=evidence,
    )

    assert result["chunk_count"] == 2

    service.publish.assert_awaited_once()

    arguments = service.publish.await_args.kwargs

    assert arguments["draft"].document_key == (
        "bd-master-trade_license"
    )
    assert arguments["review"] is review
    assert arguments["reviewer"] is reviewer
    assert arguments["evidence"] is evidence
