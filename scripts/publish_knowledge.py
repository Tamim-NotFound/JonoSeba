import argparse
import asyncio
from datetime import datetime
import json
from pathlib import Path
import sys
from sqlalchemy import select
from app.db.session import AsyncSessionLocal, engine
from app.modules.auth.models import User, UserRole
from app.modules.knowledge.embeddings import (
    GeminiEmbeddingService,
)
from app.modules.knowledge.master_publication_bridge import (
    build_master_review_packet,
    get_all_master_review_packets,
    publish_reviewed_master_guide,
)
from app.modules.knowledge.publication import (
    ClaimEvidence,
    KnowledgePublicationService,
)
from app.modules.knowledge.source_review import (
    KnowledgeSourceReview,
)


def required_text(data: dict, key: str) -> str:
    value = data.get(key)

    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"Missing or empty field: {key}"
        )

    return value.strip()


def create_template(
    guide_key: str,
    output: Path,
) -> None:
    packet = build_master_review_packet(
        guide_key
    )

    if output.exists():
        raise FileExistsError(
            f"File exists; refusing overwrite: {output}"
        )

    payload = {
        "guide_key": packet.guide_key,
        "source_url": "",
        "source_name": "",
        "reviewed_at": "",
        "evidence_notes": "",
        "approved_content": "",
        "evidence": [
            {
                "review_flag": flag,
                "source_excerpt": "",
                "source_text": "",
            }
            for flag in packet.required_evidence
        ],
    }

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(f"Created review template: {output}")
    print(
        "Nothing was published. "
        "Fill this template using real official evidence."
    )


def parse_review_payload(raw: object):
    if not isinstance(raw, dict):
        raise ValueError(
            "Review input must be a JSON object."
        )

    guide_key = required_text(
        raw,
        "guide_key",
    )

    packet = build_master_review_packet(
        guide_key
    )

    try:
        reviewed_at = datetime.fromisoformat(
            required_text(
                raw,
                "reviewed_at",
            ).replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError(
            "reviewed_at must be an ISO timestamp "
            "with timezone."
        ) from exc

    source_url = required_text(
        raw,
        "source_url",
    )

    raw_evidence = raw.get("evidence")

    if (
        not isinstance(raw_evidence, list)
        or not raw_evidence
    ):
        raise ValueError(
            "evidence must be a non-empty JSON array."
        )

    evidence = []

    for index, item in enumerate(
        raw_evidence,
        start=1,
    ):
        if not isinstance(item, dict):
            raise ValueError(
                f"evidence #{index} must be an object."
            )

        evidence.append(
            ClaimEvidence(
                review_flag=required_text(
                    item,
                    "review_flag",
                ),
                source_url=source_url,
                source_excerpt=required_text(
                    item,
                    "source_excerpt",
                ),
                source_text=required_text(
                    item,
                    "source_text",
                ),
            )
        )

    supplied_flags = [
        item.review_flag
        for item in evidence
    ]

    if (
        len(supplied_flags)
        != len(set(supplied_flags))
        or set(supplied_flags)
        != set(packet.required_evidence)
    ):
        raise ValueError(
            "Exactly one evidence item is required "
            "for each listed review_flag."
        )

    review = KnowledgeSourceReview(
        document_key=packet.draft.document_key,
        source_url=source_url,
        source_name=required_text(
            raw,
            "source_name",
        ),
        reviewed_at=reviewed_at,
        reviewed_flags=tuple(supplied_flags),
        evidence_notes=required_text(
            raw,
            "evidence_notes",
        ),
    )

    approved_content = required_text(
        raw,
        "approved_content",
    )

    return (
        guide_key,
        review,
        tuple(evidence),
        approved_content,
    )


async def publish(
    payload: object,
    admin_email: str,
    confirm_key: str,
) -> None:
    (
        guide_key,
        review,
        evidence,
        approved_content,
    ) = parse_review_payload(payload)

    if confirm_key != guide_key:
        raise ValueError(
            "--confirm-key must exactly match "
            "the reviewed guide_key."
        )

    admin_email = admin_email.strip().lower()

    if not admin_email:
        raise ValueError(
            "An existing admin email is required."
        )

    embeddings = None

    try:
        async with AsyncSessionLocal() as db:
            reviewer = await db.scalar(
                select(User).where(
                    User.email == admin_email
                )
            )

            if (
                reviewer is None
                or not reviewer.is_active
                or reviewer.role != UserRole.ADMIN
            ):
                raise PermissionError(
                    "An existing active admin account "
                    "is required in this database."
                )

            embeddings = GeminiEmbeddingService()

            service = KnowledgePublicationService(
                db=db,
                embedding_service=embeddings,
            )

            result = await publish_reviewed_master_guide(
                service=service,
                guide_key=guide_key,
                review=review,
                reviewer=reviewer,
                approved_content=approved_content,
                evidence=evidence,
            )

            print(
                "Publication committed successfully:"
            )

            print(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                )
            )

    finally:
        if embeddings is not None:
            await embeddings.close()

        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Review first; publish verified JonoSeba "
            "knowledge with an admin."
        )
    )

    action = parser.add_mutually_exclusive_group(
        required=True
    )

    action.add_argument(
        "--list",
        action="store_true",
        help="List reviewable master guides",
    )

    action.add_argument(
        "--template",
        metavar="GUIDE_KEY",
        help="Create an empty review JSON",
    )

    action.add_argument(
        "--publish",
        action="store_true",
        help="Publish reviewed JSON from stdin",
    )

    parser.add_argument(
        "--out",
        type=Path,
        help="Template output path",
    )

    parser.add_argument(
        "--admin-email",
        help="Existing active admin email",
    )

    parser.add_argument(
        "--confirm-key",
        help="Guide key confirmed for publication",
    )

    args = parser.parse_args()

    if args.list:
        for packet in get_all_master_review_packets():
            print(
                f"{packet.guide_key} | "
                f"{packet.draft.title} | "
                f"{len(packet.required_evidence)} "
                "evidence checks"
            )

        return

    if args.template:
        if args.out is None:
            parser.error(
                "--template requires --out"
            )

        create_template(
            args.template,
            args.out,
        )

        return

    if not args.admin_email or not args.confirm_key:
        parser.error(
            "--publish requires --admin-email "
            "and --confirm-key"
        )

    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON input: {exc}"
        ) from exc

    asyncio.run(
        publish(
            payload,
            args.admin_email,
            args.confirm_key,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (
        ValueError,
        PermissionError,
        FileExistsError,
    ) as exc:
        print(
            f"ERROR: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
