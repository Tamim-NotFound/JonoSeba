from dataclasses import dataclass, replace
from typing import Any
from app.modules.knowledge.bangladesh_demo_pack import (
    DraftKnowledgeGuide,
    get_draft_guides,
)
from app.modules.knowledge.master_service_catalog import (
    SERVICE_GUIDES,
    get_service_guide,
    render_service_guide,
)
from app.modules.knowledge.publication import (
    ClaimEvidence,
    KnowledgePublicationService,
)
from app.modules.knowledge.source_review import (
    KnowledgeSourceReview,
)


DOCUMENT_KEY_PREFIX = "bd-master-"


@dataclass(frozen=True)
class MasterReviewPacket:
    """
    An unpublished master guide prepared for
    the existing knowledge publication workflow.

    Building a packet never writes to the database.
    """

    guide_key: str
    draft: DraftKnowledgeGuide
    required_evidence: tuple[str, ...]


def _review_flags(guide_key: str) -> tuple[str, ...]:
    """
    Each flag requires separate supporting evidence.

    These are verification requirements, not
    statements that the claims are already proven.
    """
    return (
        f"{guide_key}: responsible department",
        f"{guide_key}: required documents",
        f"{guide_key}: fees and charges",
        f"{guide_key}: application procedure",
        f"{guide_key}: local applicability and exceptions",
    )


def build_master_review_packet(
    guide_key: str,
) -> MasterReviewPacket:
    """
    Convert a research guide into the project's
    existing DraftKnowledgeGuide structure.

    No knowledge is published at this stage.
    """

    if not isinstance(guide_key, str):
        raise ValueError(
            "Guide key must be a string."
        )

    guide = get_service_guide(guide_key.strip())

    if guide is None:
        raise ValueError(
            f"Unknown master service guide: {guide_key}"
        )

    if guide.source_status != "research_pending":
        raise ValueError(
            "Unexpected research source status."
        )

    templates = get_draft_guides()

    if not templates:
        raise RuntimeError(
            "No draft knowledge template available."
        )

    # Reuse the existing Bengali draft's dataclass
    # structure, but replace all guide-specific
    # identity, text and review requirements.
    template = templates[0]

    flags = _review_flags(guide.key)

    draft = replace(
        template,
        document_key=(
            f"{DOCUMENT_KEY_PREFIX}{guide.key}"
        ),
        title=guide.title_bn,
        content=render_service_guide(guide),
        review_flags=flags,
    )

    return MasterReviewPacket(
        guide_key=guide.key,
        draft=draft,
        required_evidence=flags,
    )


def get_all_master_review_packets(
) -> tuple[MasterReviewPacket, ...]:
    """
    Prepare all ten guides without publishing them.
    """
    return tuple(
        build_master_review_packet(guide.key)
        for guide in SERVICE_GUIDES
    )


async def publish_reviewed_master_guide(
    *,
    service: KnowledgePublicationService,
    guide_key: str,
    review: KnowledgeSourceReview,
    reviewer: Any,
    approved_content: str,
    evidence: tuple[ClaimEvidence, ...],
) -> dict:
    """
    Send one reviewed guide through the existing
    audited, atomic publication service.

    This function does not bypass source review,
    evidence matching, admin authorization or
    the existing PostgreSQL transaction checks.

    The caller must independently establish that
    the cited government material is authentic,
    current and applicable before requesting
    publication.
    """

    packet = build_master_review_packet(
        guide_key
    )

    if review.document_key != packet.draft.document_key:
        raise ValueError(
            "Review document key does not match "
            "the selected master service guide."
        )

    if not isinstance(evidence, tuple) or not evidence:
        raise ValueError(
            "Reviewed source evidence is required "
            "before publication."
        )

    if (
        not isinstance(approved_content, str)
        or not approved_content.strip()
    ):
        raise ValueError(
            "Approved content is required "
            "before publication."
        )

    # The existing publication service performs
    # further checks and owns the database commit.
    return await service.publish(
        draft=packet.draft,
        review=review,
        reviewer=reviewer,
        approved_content=approved_content,
        evidence=evidence,
    )
