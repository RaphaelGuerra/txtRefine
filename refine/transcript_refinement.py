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
        self._sentence_break_markers = [
            ("mas",),
            ("porém",),
            ("então",),
            ("depois",),
            ("agora",),
            ("daí",),
            ("no", "entanto"),
            ("só", "que"),
            ("por", "isso"),
            ("nesse", "ponto"),
            ("além", "disso"),
            ("por", "outro", "lado"),
        ]
        self._paragraph_start_markers = {
            "agora",
            "além disso",
            "daí",
            "depois",
            "nesse ponto",
            "no entanto",
            "por outro lado",
            "por isso",
        }

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

    def _match_marker(self, tokens: List[str], index: int) -> Optional[Tuple[str, int]]:
        for marker_tokens in self._sentence_break_markers:
            end_index = index + len(marker_tokens)
            if end_index > len(tokens):
                continue
            normalized = [
                re.sub(rf"^[^{WORD_CHARS}]+|[^{WORD_CHARS}]+$", "", token).lower()
                for token in tokens[index:end_index]
            ]
            if tuple(normalized) == marker_tokens:
                return (" ".join(marker_tokens), len(marker_tokens))
        return None

    def _infer_sentence_breaks(self, text: str) -> str:
        paragraph = re.sub(r"\s+", " ", text).strip()
        if not paragraph:
            return ""
        if re.search(r"[.!?]", paragraph):
            return paragraph

        tokens = paragraph.split(" ")
        rebuilt: List[str] = []
        words_since_break = 0

        for index, token in enumerate(tokens):
            marker_match = self._match_marker(tokens, index)
            if (
                marker_match
                and rebuilt
                and words_since_break >= 8
                and not rebuilt[-1].endswith((".", "!", "?"))
            ):
                rebuilt[-1] = rebuilt[-1].rstrip(",;:") + "."
                words_since_break = 0

            rebuilt.append(token)
            if re.search(rf"[{WORD_CHARS}]", token):
                words_since_break += 1
            if token.endswith((".", "!", "?")):
                words_since_break = 0

        if rebuilt and not rebuilt[-1].endswith((".", "!", "?")):
            rebuilt[-1] = rebuilt[-1].rstrip(",;:") + "."

        return " ".join(rebuilt)

    def _capitalize_sentences(self, text: str) -> str:
        capitalized = re.sub(
            r"(^|(?<=[.!?]\s))([a-zà-ÿ])",
            lambda match: match.group(1) + match.group(2).upper(),
            text,
            flags=re.IGNORECASE,
        )
        return capitalized.strip()

    def _split_sentences(self, text: str) -> List[str]:
        return [
            sentence.strip()
            for sentence in re.findall(r"[^.!?]+[.!?]?", text)
            if sentence.strip()
        ]

    def _format_paragraphs(self, text: str) -> str:
        source_paragraphs = [
            paragraph.strip()
            for paragraph in re.split(r"\n\s*\n+", text.strip())
            if paragraph.strip()
        ] or [text.strip()]

        formatted_paragraphs: List[str] = []
        for source_paragraph in source_paragraphs:
            inferred = self._infer_sentence_breaks(source_paragraph)
            capitalized = self._capitalize_sentences(inferred)
            sentences = self._split_sentences(capitalized)

            if len(sentences) <= 2:
                formatted_paragraphs.append(" ".join(sentences).strip())
                continue

            current_sentences: List[str] = []
            current_words = 0

            for sentence in sentences:
                normalized_sentence = sentence.strip()
                lower_sentence = normalized_sentence.lower().rstrip(".!?")
                sentence_words = len(normalized_sentence.split())
                should_split = bool(
                    current_sentences and (
                        len(current_sentences) >= 2
                        or current_words >= 55
                        or lower_sentence in self._paragraph_start_markers
                    )
                )
                if should_split:
                    formatted_paragraphs.append(" ".join(current_sentences).strip())
                    current_sentences = []
                    current_words = 0

                current_sentences.append(normalized_sentence)
                current_words += sentence_words

            if current_sentences:
                formatted_paragraphs.append(" ".join(current_sentences).strip())

        return "\n\n".join(paragraph for paragraph in formatted_paragraphs if paragraph).strip()

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
        structured_text = self._format_paragraphs(corrected_text)
        if structured_text != corrected_text:
            corrections.append(
                {
                    "original": corrected_text,
                    "corrected": structured_text,
                    "position": 0,
                }
            )
            corrected_text = structured_text

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
