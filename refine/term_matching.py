"""Normalization and term matching utilities for transcript refinement.

This module provides:
- ``normalize_text`` for robust comparisons across accents and casing
- ``REFINED_DICT`` with small transcript-focused canonical term groups
- ``CORRECTIONS_MAP`` for common PT-BR ASR/product-name corrections
- ``find_best_match`` to support exact/fuzzy matching within a group
"""

from difflib import get_close_matches
from typing import List, Optional
import unicodedata


def normalize_text(text: str) -> str:
    """Lowercase, trim, and strip accents/diacritics for robust matching."""
    if not text:
        return ""
    text = text.lower().strip()
    return "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )


REFINED_DICT = {
    "platform_terms": [
        "microsoft teams",
        "google meet",
        "google docs",
        "google drive",
        "whatsapp",
        "chatgpt",
        "ollama",
    ],
    "transcript_terms": [
        "transcricao",
        "voice memo",
        "nota de voz",
        "audio",
        "reuniao",
        "entrevista",
        "gravacao",
    ],
}


CORRECTIONS_MAP = {
    "microsof teams": "Microsoft Teams",
    "microsoft team": "Microsoft Teams",
    "microsoft time": "Microsoft Teams",
    "ms teams": "Microsoft Teams",
    "google meat": "Google Meet",
    "google met": "Google Meet",
    "google docis": "Google Docs",
    "google draive": "Google Drive",
    "whats app": "WhatsApp",
    "whatsapp": "WhatsApp",
    "chat gpt": "ChatGPT",
    "xat gpt": "ChatGPT",
    "olama": "Ollama",
    "olamma": "Ollama",
    "voice memo": "Voice Memo",
    "nota de vos": "nota de voz",
    "transcriçao": "transcrição",
    "transcrisao": "transcrição",
}

NORMALIZED_CORRECTIONS_MAP = {
    normalize_text(original): replacement
    for original, replacement in CORRECTIONS_MAP.items()
}


def find_best_match(term: str, category: str, cutoff: float = 0.8) -> Optional[str]:
    """Return best normalized match from a category, or ``None``."""
    normalized_term = normalize_text(term)

    if not normalized_term or category not in REFINED_DICT:
        return None

    if normalized_term in NORMALIZED_CORRECTIONS_MAP:
        normalized_term = normalize_text(NORMALIZED_CORRECTIONS_MAP[normalized_term])

    if normalized_term in REFINED_DICT[category]:
        return normalized_term

    matches: List[str] = get_close_matches(
        normalized_term,
        REFINED_DICT[category],
        n=1,
        cutoff=cutoff,
    )
    return matches[0] if matches else None
