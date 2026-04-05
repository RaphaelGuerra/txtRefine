"""Transcript-oriented deterministic cleanup helpers."""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from .term_matching import CORRECTIONS_MAP, find_best_match as _tm_find_best_match
from .utils import get_global_cache

WORD_CHARS = r"A-Za-zÀ-ÿ0-9"


class TranscriptRefinementSystem:
    """Apply conservative deterministic cleanup before LLM refinement."""

    def __init__(self) -> None:
        self._phrase_patterns = self._build_phrase_patterns()
        self._connector_patterns = self._build_connector_patterns()
        self._duplicate_phrase_patterns = self._build_duplicate_phrase_patterns()

    def _build_phrase_patterns(self) -> List[Tuple[str, str, re.Pattern[str]]]:
        patterns: List[Tuple[str, str, re.Pattern[str]]] = []
        for original, replacement in sorted(
            CORRECTIONS_MAP.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            pattern = re.compile(
                rf"(?<![{WORD_CHARS}]){re.escape(original)}(?![{WORD_CHARS}])",
                re.IGNORECASE,
            )
            patterns.append((original, replacement, pattern))
        return patterns

    def _build_connector_patterns(self) -> List[Tuple[str, re.Pattern[str]]]:
        connectors = [
            "a",
            "as",
            "da",
            "das",
            "de",
            "do",
            "dos",
            "e",
            "na",
            "nas",
            "no",
            "nos",
            "o",
            "os",
            "para",
            "pra",
            "que",
        ]
        return [
            (
                connector,
                re.compile(
                    rf"\b({connector})\s+\1\b",
                    re.IGNORECASE,
                ),
            )
            for connector in connectors
        ]

    def _build_duplicate_phrase_patterns(self) -> List[re.Pattern[str]]:
        return [
            re.compile(
                rf"\b(?P<phrase>[{WORD_CHARS}]{{2,}}(?:\s+[{WORD_CHARS}]{{2,}}){{1,3}})\s+(?P=phrase)\b",
                re.IGNORECASE,
            )
        ]

    def _preserve_case(self, original: str, replacement: str) -> str:
        if " " in replacement:
            return replacement
        if original.isupper():
            return replacement.upper()
        if original.istitle():
            return replacement.capitalize()
        return replacement

    def _apply_targeted_corrections(self, text: str, corrections: List[Dict[str, object]]) -> str:
        updated_text = text
        for _, replacement, pattern in self._phrase_patterns:
            def repl(match: re.Match[str]) -> str:
                matched = match.group(0)
                corrected = self._preserve_case(matched, replacement)
                corrections.append(
                    {
                        "original": matched,
                        "corrected": corrected,
                        "position": match.start(),
                    }
                )
                return corrected

            updated_text = pattern.sub(repl, updated_text)
        return updated_text

    def _apply_duplicate_phrase_cleanup(self, text: str, corrections: List[Dict[str, object]]) -> str:
        updated_text = text
        for pattern in self._duplicate_phrase_patterns:
            while True:
                match = pattern.search(updated_text)
                if not match:
                    break
                phrase = match.group("phrase")
                corrections.append(
                    {
                        "original": match.group(0),
                        "corrected": phrase,
                        "position": match.start(),
                    }
                )
                updated_text = updated_text[: match.start()] + phrase + updated_text[match.end() :]
        return updated_text

    def _apply_connector_cleanup(self, text: str, corrections: List[Dict[str, object]]) -> str:
        updated_text = text
        for connector, pattern in self._connector_patterns:
            while True:
                match = pattern.search(updated_text)
                if not match:
                    break
                corrected = match.group(1)
                corrections.append(
                    {
                        "original": match.group(0),
                        "corrected": corrected,
                        "position": match.start(),
                    }
                )
                updated_text = updated_text[: match.start()] + corrected + updated_text[match.end() :]
        return updated_text

    def find_and_correct_terms(self, text: str) -> Tuple[str, List[Dict[str, object]]]:
        """Apply transcript-focused deterministic cleanup with caching."""
        cache = get_global_cache()
        cached_result = cache.get_transcript_corrections(text)
        if cached_result:
            return cached_result["corrected_text"], cached_result["corrections"]

        corrections: List[Dict[str, object]] = []
        corrected_text = text
        corrected_text = self._apply_targeted_corrections(corrected_text, corrections)
        corrected_text = self._apply_duplicate_phrase_cleanup(corrected_text, corrections)
        corrected_text = self._apply_connector_cleanup(corrected_text, corrections)

        cache.set_transcript_corrections(text, corrected_text, corrections)

        from .utils import get_performance_monitor

        get_performance_monitor().record_transcript_corrections(len(corrections))
        return corrected_text, corrections

    def find_best_match(self, term: str, category: str, cutoff: float = 0.8) -> Optional[str]:
        return _tm_find_best_match(term, category, cutoff)

    def __len__(self) -> int:
        return len(CORRECTIONS_MAP)


# Compatibility aliases for the previous philosophy-oriented names.
OptimizedBPPhilosophySystem = TranscriptRefinementSystem
BPPhilosophySystem = TranscriptRefinementSystem
