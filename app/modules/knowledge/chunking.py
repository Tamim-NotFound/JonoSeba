import re

DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 120


def normalize_document_text(text: str) -> str:
    """
    Normalize whitespace while preserving paragraphs.
    Supports Unicode text, including Bangla and English.
    """

    if not isinstance(text, str):
        raise TypeError("Document text must be a string.")

    # Normalize Windows and old Mac line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove unnecessary spaces within each line.
    lines = [
        re.sub(r"[ \t]+", " ", line).strip()
        for line in text.split("\n")
    ]

    text = "\n".join(lines)

    # Keep paragraph boundaries but remove excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_document(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """
    Split a document into overlapping chunks.

    Rules:
    - Empty documents return an empty list.
    - Each chunk has at most chunk_size characters.
    - Adjacent chunks share up to chunk_overlap characters.
    - Prefer breaking at paragraph, sentence, or word boundaries.
    - Fall back to character splitting for very long words.
    """

    if not isinstance(chunk_size, int) or isinstance(
        chunk_size, bool
    ):
        raise ValueError("chunk_size must be an integer.")

    if not isinstance(chunk_overlap, int) or isinstance(
        chunk_overlap, bool
    ):
        raise ValueError("chunk_overlap must be an integer.")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be >= 0 and < chunk_size."
        )

    normalized_text = normalize_document_text(text)

    if not normalized_text:
        return []

    if len(normalized_text) <= chunk_size:
        return [normalized_text]

    chunks: list[str] = []

    start = 0
    text_length = len(normalized_text)

    while start < text_length:
        max_end = min(start + chunk_size, text_length)

        if max_end == text_length:
            chunk = normalized_text[start:max_end].strip()

            if chunk:
                chunks.append(chunk)

            break

        segment = normalized_text[start:max_end]

        # Prefer natural boundaries in the last 30% of a chunk.
        minimum_break = max(
            1,
            int(len(segment) * 0.7),
        )

        boundary_candidates = [
            segment.rfind("\n\n", minimum_break),
            segment.rfind("\n", minimum_break),
            segment.rfind("।", minimum_break),
            segment.rfind(".", minimum_break),
            segment.rfind("!", minimum_break),
            segment.rfind("?", minimum_break),
            segment.rfind(" ", minimum_break),
        ]

        best_boundary = max(boundary_candidates)

        if best_boundary >= minimum_break:
            end = start + best_boundary + 1
        else:
            end = max_end

        chunk = normalized_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Keep overlapping context.
        next_start = max(0, end - chunk_overlap)

        # Prevent infinite loops when a short boundary is found.
        if next_start <= start:
            next_start = end

        start = next_start

    return chunks
