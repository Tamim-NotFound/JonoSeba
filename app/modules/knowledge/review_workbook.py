from pathlib import Path
from app.modules.knowledge.bangladesh_demo_pack import (
    DraftKnowledgeGuide,
    get_draft_guides,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "docs"
    / "knowledge"
    / "bangladesh_source_review.md"
)


def build_review_workbook(
    guides: tuple[DraftKnowledgeGuide, ...],
) -> str:
    """
    Create a human-review worksheet from unpublished
    Bangladesh municipal knowledge drafts.

    This does not verify, approve, ingest, or publish
    any knowledge.
    """

    lines = [
        "# JonoSeba — Bangladesh Knowledge Source Review",
        "",
        "**Status:** PENDING HUMAN VERIFICATION",
        "",
        "**Project:** JonoSeba municipal service demo",
        "",
        "This document contains unverified research drafts.",
        "It is NOT an official government publication.",
        "",
        "## Review instructions",
        "",
        "For each guide:",
        "",
        "1. Find the specific official webpage or PDF.",
        "2. Record the issuing authority and source URL.",
        "3. Copy an exact excerpt supporting each claim.",
        "4. Record the applicable date and municipality.",
        "5. Mark unsupported claims for removal or revision.",
        "6. Keep the guide unpublished until reviewed.",
        "",
        "Do not treat a government-looking URL alone "
        "as evidence.",
        "",
        "---",
        "",
    ]

    for index, guide in enumerate(guides, start=1):
        lines.extend(
            [
                f"## {index}. {guide.title}",
                "",
                f"**Document key:** `{guide.document_key}`",
                "",
                "**Review status:** PENDING",
                "",
                "### Current research draft",
                "",
                guide.content.strip(),
                "",
                "### Claims requiring verification",
                "",
            ]
        )

        for flag in guide.review_flags:
            lines.append(f"- [ ] {flag}")

        lines.extend(
            [
                "",
                "### Source evidence",
                "",
                "- Official source URL: NOT COLLECTED",
                "- Issuing authority: NOT CONFIRMED",
                "- Source document title: NOT COLLECTED",
                "- Relevant source excerpt: NOT COLLECTED",
                "- Publication/effective date: NOT CONFIRMED",
                "- Applicable municipality: NOT CONFIRMED",
                "",
                "### Reviewer decision",
                "",
                "- [ ] Supported by evidence",
                "- [ ] Needs revision",
                "- [ ] Unsupported claim removed",
                "",
                "**Approved content:** NOT PREPARED",
                "",
                "---",
                "",
            ]
        )

    return "\n".join(lines) + "\n"


def save_review_workbook(
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> Path:
    """
    Write the review worksheet to disk.

    The output is documentation only and does not
    change the RAG database.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    content = build_review_workbook(
        get_draft_guides()
    )

    output_path.write_text(
        content,
        encoding="utf-8",
    )

    return output_path


def main() -> None:
    output_path = save_review_workbook()

    print("Knowledge review workbook created:")
    print(output_path)
    print("Status: PENDING HUMAN VERIFICATION")
    print(
        "Guides:",
        len(get_draft_guides()),
    )


if __name__ == "__main__":
    main()
