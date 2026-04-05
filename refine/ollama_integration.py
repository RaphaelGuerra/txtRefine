"""Ollama integration for readable transcript refinement."""

from __future__ import annotations

import json
from typing import Any, List

try:
    import ollama
except ImportError:  # pragma: no cover - exercised through function behavior
    ollama = None

from .transcript_refinement import TranscriptRefinementSystem
from .utils import get_global_cache

SYSTEM_PROMPT = (
    "You are a transcript editor for Brazilian Portuguese voice memos. "
    "Improve readability with punctuation, capitalization, paragraph breaks, "
    "and obvious ASR fixes, but preserve meaning, chronology, tone, and language. "
    "Do not summarize, translate, invent content, or rewrite the transcript into essay prose."
)


def check_ollama() -> bool:
    """Check if Ollama is available."""
    if ollama is None:
        return False
    try:
        ollama.list()
        return True
    except Exception:
        return False


def get_available_models() -> list:
    """Get list of available models."""
    if ollama is None:
        return []
    try:
        response = ollama.list()
        return [model.model for model in response.models]
    except Exception:
        return []


def build_refinement_prompt(text: str) -> str:
    """Build the user prompt for transcript refinement."""
    return f"""
TASK: Rewrite this raw transcript as a readable transcript.

GOALS:
1) Fix obvious spelling and ASR mistakes
2) Improve punctuation, capitalization, and paragraph breaks
3) Remove accidental duplicate fragments and repeated connector words
4) Preserve the original meaning, chronology, and spoken tone

STRICT RULES:
- Do not summarize
- Do not translate
- Do not add speaker labels unless already present
- Do not invent missing information
- Do not turn it into polished article prose

TEXT:
{text}

OUTPUT:
Return only the cleaned transcript.
""".strip()


def single_pass_refine(text: str, model: str = "llama3.2:latest") -> str:
    """Refine transcript text into a readable transcript."""
    cache = get_global_cache()
    cached_response = cache.get_llm_response(text, model)
    if cached_response:
        print("✅ Using cached LLM response")
        return cached_response

    transcript_system = TranscriptRefinementSystem()
    corrected_text, corrections = transcript_system.find_and_correct_terms(text)

    if corrections:
        print(f"✅ Applied {len(corrections)} transcript corrections")

    if ollama is None:
        return corrected_text

    try:
        from .utils import get_performance_monitor

        get_performance_monitor().record_llm_call()
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_refinement_prompt(corrected_text)},
            ],
            options={"temperature": 0.1},
        )

        refined_text = response["message"]["content"].strip()
        if len(refined_text.split()) < len(corrected_text.split()) * 0.9:
            print("⚠️  Content loss detected, using deterministic transcript cleanup")
            refined_text = corrected_text

        cache.set_llm_response(text, model, refined_text)
        return refined_text

    except Exception as exc:
        print(f"⚠️  Model processing failed: {exc}")
        return corrected_text


def validate_model(model_name: str) -> bool:
    """Check if model is available."""
    return model_name in get_available_models()


def smart_chunk_text(text: str, model: str = "llama3.2:latest", max_words: int = 800) -> List[str]:
    """Optionally ask the model to suggest paragraph boundaries for a transcript."""
    if ollama is None:
        return [text]

    try:
        chunking_prompt = f"""You segment raw voice-memo transcripts into readable paragraphs.

Return only valid JSON with the shape {{"paragraphs": ["..."]}}.

Transcript:
{text}
"""
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are a transcript segmentation expert. Output only valid JSON."},
                {"role": "user", "content": chunking_prompt},
            ],
            options={"temperature": 0.1},
        )

        parsed = json.loads(response["message"]["content"].strip())
        paragraphs = parsed.get("paragraphs")
        if isinstance(paragraphs, list):
            cleaned = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
            return cleaned or [text]
        return [text]
    except Exception:
        return [text]


def refine_text_with_paragraphs(text: str, model: str = "llama3.2:latest", chunk_size: int = 800) -> str:
    """Compatibility wrapper for the single-pass refinement path."""
    return single_pass_refine(text, model)


def _process_single_chunk(chunk: str, transcript_system: TranscriptRefinementSystem, model: str) -> str:
    """Process a single chunk with deterministic cleanup and readable transcript polishing."""
    corrected_text, _ = transcript_system.find_and_correct_terms(chunk)
    if ollama is None:
        return corrected_text
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_refinement_prompt(corrected_text)},
            ],
            options={"temperature": 0.1},
        )
        return response["message"]["content"].strip()
    except Exception:
        return corrected_text
