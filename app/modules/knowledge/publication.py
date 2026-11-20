import hashlib
from dataclasses import dataclass, replace
from urllib.parse import urlsplit
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.models import User
from app.modules.knowledge.bangladesh_demo_pack import (
    DraftKnowledgeGuide,
)
from app.modules.knowledge.embeddings import (
    GeminiEmbeddingService,
)
from app.modules.knowledge.evidence_matching import (
    excerpt_occurs_in_source,
)
from app.modules.knowledge.ingestion import (
    KnowledgeIngestionService,
)
from app.modules.knowledge.models import (
    KnowledgePublicationAudit,
)
from app.modules.knowledge.source_review import (
    KnowledgeSourceReview,
    prepare_reviewed_document,
)


@dataclass(frozen=True)
class ClaimEvidence:
    """
    Reviewer-supplied evidence for one review requirement.

    source_text is copied from a source document.
    source_excerpt must occur within that source_text.

    This is not independent government-source
    authentication.
    """

    review_flag: str
    source_url: str
    source_excerpt: str
    source_text: str


class KnowledgePublicationService:
    def __init__(
        self,
        db: AsyncSession,
        embedding_service: GeminiEmbeddingService,
    ) -> None:
        self.db = db

        self.ingestion = KnowledgeIngestionService(
            db=db,
            embedding_service=embedding_service,
        )

    async def publish(
        self,
        *,
        draft: DraftKnowledgeGuide,
        review: KnowledgeSourceReview,
        reviewer: User,
        approved_content: str,
        evidence: tuple[ClaimEvidence, ...],
    ) -> dict:
        """
        Publish reviewed knowledge and audit atomically.

        Must be called from a trusted admin workflow
        using a dedicated database session.

        Reviewers must independently check the actual
        source, effective date and factual accuracy.
        """

        document = prepare_reviewed_document(
            draft=draft,
            review=review,
            reviewer=reviewer,
        )

        if (
            not isinstance(approved_content, str)
            or len(approved_content.strip()) < 60
        ):
            raise ValueError(
                "Approved content must contain at least "
                "60 characters."
            )

        cleaned_content = approved_content.strip()

        if cleaned_content == draft.content.strip():
            raise ValueError(
                "Approved content must be independently "
                "reviewed and rewritten from the draft."
            )

        if (
            "review-pending" in cleaned_content.lower()
            or "খসড়া তথ্য" in cleaned_content
        ):
            raise ValueError(
                "Remove draft-review notices from "
                "approved content."
            )

        path = urlsplit(document.source_url).path

        if path in {"", "/"}:
            raise ValueError(
                "Use a specific official source page, "
                "not the website homepage."
            )

        if (
            not isinstance(evidence, tuple)
            or not evidence
        ):
            raise ValueError(
                "Supporting evidence is required."
            )

        flags = [
            item.review_flag
            for item in evidence
        ]

        if (
            len(flags) != len(set(flags))
            or set(flags) != set(draft.review_flags)
        ):
            raise ValueError(
                "Provide exactly one supporting excerpt "
                "for every draft review flag."
            )

        # All evidence must pass before database writes.
        evidence_records = []

        for item in evidence:
            if item.source_url != document.source_url:
                raise ValueError(
                    "Evidence source URL must match "
                    "the approved document source URL."
                )

            if (
                not isinstance(item.source_excerpt, str)
                or len(item.source_excerpt.strip()) < 25
            ):
                raise ValueError(
                    "Each evidence excerpt must contain "
                    "at least 25 characters."
                )

            if (
                not isinstance(item.source_text, str)
                or len(item.source_text.strip()) < 30
            ):
                raise ValueError(
                    "Each source text must contain "
                    "at least 30 characters."
                )

            if not excerpt_occurs_in_source(
                item.source_text,
                item.source_excerpt,
            ):
                raise ValueError(
                    "Evidence excerpt was not found "
                    "in the supplied source text."
                )

            evidence_records.append(
                {
                    "review_flag": item.review_flag,
                    "source_url": item.source_url,
                    "source_excerpt": (
                        item.source_excerpt.strip()
                    ),
                    "source_text_sha256": (
                        hashlib.sha256(
                            item.source_text.encode("utf-8")
                        ).hexdigest()
                    ),
                }
            )

        approved_document = replace(
            document,
            content=cleaned_content,
        )

        content_hash = hashlib.sha256(
            cleaned_content.encode("utf-8")
        ).hexdigest()

        audit = KnowledgePublicationAudit(
            document_key=approved_document.document_key,
            document_title=approved_document.document_title,
            reviewer_id=reviewer.id,
            source_url=approved_document.source_url,
            source_name=approved_document.source_name,
            reviewed_at=approved_document.verified_at,
            approved_content_sha256=content_hash,
            claim_evidence=evidence_records,
        )

        try:
            result = await self.ingestion.ingest_document(
                approved_document,
                commit=False,
            )

            self.db.add(audit)

            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

        return result
