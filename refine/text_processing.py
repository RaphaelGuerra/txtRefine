"""Text processing functions for txtRefine."""

import re
from typing import List


def clean_text(text: str) -> str:
    """Clean and preprocess text before chunking."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Fix broken words at line breaks
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    # Remove extra newlines but preserve paragraph breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def split_into_chunks(text: str, max_words: int = 800) -> List[str]:
    """Split text into chunks - simple and fast."""
    words = text.split()

    if len(words) <= max_words:
        return [text]

    chunks = []
    for i in range(0, len(words), max_words):
        chunk_words = words[i:i + max_words]
        chunks.append(' '.join(chunk_words))

    return chunks


def detect_content_type(text: str) -> str:
    """Detect content type from text."""
    # All texts are philosophical for this program
    return "philosophy"


def merge_chunks(chunks: List[str]) -> str:
    """Merge refined chunks back into a single text."""
    return ' '.join(chunks)


def calculate_word_count(text: str) -> int:
    """Calculate word count in text."""
    return len(text.split())


def validate_text(text: str, min_length: int = 10) -> bool:
    """Validate text content before processing."""
    if not text or not text.strip():
        return False
    if len(text.strip()) < min_length:
        return False
    return True
