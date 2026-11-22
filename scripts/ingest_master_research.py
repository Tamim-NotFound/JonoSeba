import argparse
import asyncio
from sqlalchemy import func, select
from app.db.session import AsyncSessionLocal, engine
from app.modules.knowledge.embeddings import GeminiEmbeddingService
from app.modules.knowledge.ingestion import (
    KnowledgeIngestionService,
)
from app.modules.knowledge.master_publication_bridge import (
    build_master_review_packet,
)
from app.modules.knowledge.master_service_catalog import (
    SERVICE_GUIDES,
)
from app.modules.knowledge.models import KnowledgeChunk


GUIDE_KEYS = tuple(
    guide.key for guide in SERVICE_GUIDES
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__
    )

    selection = parser.add_mutually_exclusive_group(
        required=True
    )

    selection.add_argument(
        "--guide",
        action="append",
        choices=GUIDE_KEYS,
        help=(
            "Guide key. May be supplied more than once."
        ),
    )

    selection.add_argument(
        "--all",
        action="store_true",
    )

    parser.add_argument(
        "--ingest",
        action="store_true",
        help=(
            "Write unpublished research chunks "
            "and embeddings to PostgreSQL."
        ),
    )

    return parser.parse_args()


async def run(
    args: argparse.Namespace,
) -> None:
    keys = (
        GUIDE_KEYS
        if args.all
        else tuple(dict.fromkeys(args.guide))
    )

    packets = [
        build_master_review_packet(key)
        for key in keys
    ]

    print("\n===== JONOSEBA SAVED RESEARCH =====")

    for packet in packets:
        print(
            packet.guide_key,
            "->",
            packet.draft.title,
        )

    if not args.ingest:
        print(
            "\nDRY RUN: No changes. "
            "Add --ingest to save drafts."
        )
        return

    embedding_service = GeminiEmbeddingService()

    try:
        async with AsyncSessionLocal() as db:
            ingestion = KnowledgeIngestionService(
                db,
                embedding_service,
            )

            for packet in packets:
                key = packet.draft.document_key

                already_published = await db.scalar(
                    select(func.count())
                    .select_from(KnowledgeChunk)
                    .where(
                        KnowledgeChunk.document_key
                        == key,
                        KnowledgeChunk.is_published.is_(
                            True
                        ),
                    )
                )

                if already_published:
                    print(
                        "SKIPPED published document:",
                        key,
                    )
                    continue

                result = await ingestion.ingest_document(
                    packet.draft.to_ingestion_input()
                )

                print(
                    "INGESTED:",
                    key,
                    "chunks:",
                    result["chunk_count"],
                )

    finally:
        await embedding_service.close()
        await engine.dispose()

    print(
        "\nAll ingested research remains "
        "UNPUBLISHED and UNVERIFIED."
    )


if __name__ == "__main__":
    asyncio.run(
        run(parse_args())
    )
