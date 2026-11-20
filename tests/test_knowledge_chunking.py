import pytest
from app.modules.knowledge.chunking import (
    chunk_document,
    normalize_document_text,
)


def test_normalize_document_text():
    text = "  Hello   world  \r\n\r\n\r\n  Next paragraph  "

    result = normalize_document_text(text)

    assert result == "Hello world\n\nNext paragraph"


def test_empty_document_returns_no_chunks():
    assert chunk_document("") == []
    assert chunk_document("   \n\n   ") == []


def test_short_document_returns_single_chunk():
    text = "Birth registration requires an application."

    result = chunk_document(
        text,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert result == [text]


def test_bangla_document_is_supported():
    text = (
        "জন্ম নিবন্ধনের জন্য প্রয়োজনীয় তথ্য জানতে "
        "সংশ্লিষ্ট কর্তৃপক্ষের নির্দেশনা অনুসরণ করুন। "
    ) * 10

    chunks = chunk_document(
        text,
        chunk_size=120,
        chunk_overlap=20,
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert chunk
        assert len(chunk) <= 120


def test_long_document_is_split():
    text = "Municipal service information. " * 100

    chunks = chunk_document(
        text,
        chunk_size=150,
        chunk_overlap=30,
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert len(chunk) <= 150


def test_chunk_overlap_preserves_context():
    text = "abcdefghijklmnopqrstuvwxyz" * 10

    chunks = chunk_document(
        text,
        chunk_size=50,
        chunk_overlap=10,
    )

    assert len(chunks) > 1

    # Character-only text forces fixed-width splitting.
    assert chunks[0][-10:] == chunks[1][:10]


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        chunk_document(
            "Hello",
            chunk_size=0,
            chunk_overlap=0,
        )


def test_invalid_chunk_overlap():
    with pytest.raises(ValueError):
        chunk_document(
            "Hello",
            chunk_size=100,
            chunk_overlap=100,
        )


def test_non_string_document_is_rejected():
    with pytest.raises(TypeError):
        chunk_document(None)
