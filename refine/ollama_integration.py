"""Simple Ollama integration for BP philosophical text refinement.

Single-pass refinement only. All smart chunking has been removed to
avoid over-processing and preserve structure.
"""

import ollama
from typing import List, Dict
from .bp_philosophy_optimized import OptimizedBPPhilosophySystem as BPPhilosophySystem
from .utils import get_global_cache


def check_ollama() -> bool:
    """Check if Ollama is available."""
    try:
        ollama.list()
        return True
    except:
        return False


def get_available_models() -> list:
    """Get list of available models."""
    try:
        response = ollama.list()
        return [model.model for model in response.models]
    except:
        return []


def single_pass_refine(text: str, model: str = "llama3.2:latest") -> str:
    """
    Refine philosophical text with BP corrections.

    Args:
        text: Text to refine
        model: Ollama model to use

    Returns:
        Refined text
    """
    cache = get_global_cache()

    # Check cache first for LLM response
    cached_response = cache.get_llm_response(text, model)
    if cached_response:
        print("✅ Using cached LLM response")
        return cached_response

    # Initialize BP system
    bp_system = BPPhilosophySystem()

    # Apply BP term corrections first
    corrected_text, corrections = bp_system.find_and_correct_terms(text)

    if corrections:
        print(f"✅ Applied {len(corrections)} BP corrections")

    # Use Ollama for refinement
    try:
        prompt = f"""
CRITICAL INSTRUCTIONS: Make ONLY minimal corrections to terms and spelling. DO NOT alter structure, order, or content.

TASK: Correct only typos, spelling errors, and specific philosophical terms. Maintain EXACT structure and content.

ABSOLUTE RULES:
1) Do not change the order of words, sentences, or paragraphs
2) Do not add or remove information
3) Do not create transitions
4) Preserve the oral lecture tone
5) Only correct obvious spelling, punctuation, and terminology

TEXT (apply minimal corrections only):
{corrected_text}

OUTPUT: Same text with minimal spelling/terminology fixes only.
"""

        # Record LLM call for performance monitoring
        from .utils import get_performance_monitor
        monitor = get_performance_monitor()
        monitor.record_llm_call()

        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'system', 'content': 'You are a spelling and terminology corrector. Your task is to make ONLY minimal corrections to spelling, punctuation, and specific terms. DO NOT alter the structure, content, or order of ideas in any way.'},
                {'role': 'user', 'content': prompt}
            ],
            options={'temperature': 0.1}
        )

        refined_text = response['message']['content'].strip()

        # Safety check - don't lose content
        if len(refined_text.split()) < len(corrected_text.split()) * 0.9:
            print("⚠️  Content loss detected, using corrected text")
            refined_text = corrected_text

        # Cache the LLM response
        cache.set_llm_response(text, model, refined_text)

        return refined_text

    except Exception as e:
        print(f"⚠️  Model processing failed: {e}")
        return corrected_text


def validate_model(model_name: str) -> bool:
    """Check if model is available."""
    models = get_available_models()
    return model_name in models

# Note: All smart chunking and paragraph-aware processing removed.


def smart_chunk_text(text: str, model: str = "llama3.2:latest", max_words: int = 800) -> List[str]:
    """
    Use LLM to intelligently segment text into logical paragraphs.

    This function analyzes the text for:
    - Topic shifts and thematic breaks
    - Rhetorical pauses and speaker transitions
    - Natural paragraph boundaries

    Args:
        text: Raw transcript text to segment
        model: Ollama model to use for analysis
        max_words: Maximum words per chunk (for fallback segmentation)

    Returns:
        List of paragraph strings
    """
    try:
        chunking_prompt = f"""You are a text processing expert specializing in academic transcripts. Your task is to segment a raw, unformatted transcript of a philosophy class into logical paragraphs.

Analyze the text to identify topic shifts, pauses, and rhetorical breaks, and divide the content accordingly.

The input will be a single block of text.
The output MUST be a JSON object containing a single key "paragraphs", which is a list of strings. Each string in the list is a distinct paragraph.

**Raw Transcript:**
{text}

**JSON Output:**
"""

        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'system', 'content': 'You are a text segmentation expert. Output only valid JSON.'},
                {'role': 'user', 'content': chunking_prompt}
            ],
            options={'temperature': 0.1}
        )

        result = response['message']['content'].strip()

        # Parse the JSON response
        import json
        try:
            parsed = json.loads(result)
            if 'paragraphs' in parsed and isinstance(parsed['paragraphs'], list):
                paragraphs = [p.strip() for p in parsed['paragraphs'] if p.strip()]
                print(f"✅ Smart chunking: Created {len(paragraphs)} logical paragraphs")
                return paragraphs
            else:
                print("⚠️  Smart chunking failed - invalid JSON structure, falling back to paragraph splitting")
                return [text]
        except json.JSONDecodeError as e:
            print(f"⚠️  Smart chunking JSON parsing failed: {e}, falling back to paragraph splitting")
            return [text]

    except Exception as e:
        print(f"⚠️  Smart chunking failed: {e}, falling back to paragraph splitting")
        return [text]


def _fallback_paragraph_split(text: str, max_words: int = 800) -> List[str]:
    """Deprecated: return full text as single chunk."""
    return [text]











def refine_text_with_paragraphs(text: str, model: str = "llama3.2:latest", chunk_size: int = 800) -> str:
    """
    Refine philosophical text using hybrid paragraph-aware chunking.

    This approach:
    1. Splits text into paragraphs (preserving semantic units)
    2. Intelligently combines paragraphs into optimal chunks
    3. Processes each chunk with BP corrections + Ollama refinement
    4. Reassembles with proper paragraph formatting

    Args:
        text: Text to refine
        model: Ollama model to use
        chunk_size: Maximum words per chunk (default 800 for optimal context)

    Returns:
        Refined text with preserved paragraph structure
    """
    # Single-pass path only
    return single_pass_refine(text, model)


def _process_single_chunk(chunk: str, bp_system: BPPhilosophySystem, model: str) -> str:
    """
    Process a single chunk with BP corrections and Ollama refinement.

    Args:
        chunk: Text chunk to process
        bp_system: Initialized BP philosophy system
        model: Ollama model name

    Returns:
        Refined chunk text
    """
    # Apply BP term corrections first
    corrected_text, corrections = bp_system.find_and_correct_terms(chunk)

    if corrections:
        print(f"     📚 Applied {len(corrections)} BP corrections")

    # Use Ollama for refinement
    try:
        prompt = f"""
CRITICAL INSTRUCTIONS: You must make ONLY minimal corrections to terms and spelling. DO NOT alter structure, reorganize, or add content.

TASK: Correct only typos, spelling errors, and specific philosophical terms. Maintain EXACTLY the same structure and content.

ABSOLUTE RULES:
1. DO NOT change the order of words, sentences, or paragraphs
2. DO NOT add or remove any ideas or information
3. DO NOT create transitions or connections between ideas
4. DO NOT alter the oral lecture tone
5. DO NOT reorganize the content in any way
6. ONLY correct obvious spelling errors and specific terms

ALLOWED CORRECTIONS:
- Fix obvious typos
- Correct incorrect philosophical terms to standard forms
- Fix punctuation when clearly wrong
- Correct obvious grammatical errors

DO NOT ALTER:
- Sentence and paragraph structure
- Order and sequence of ideas
- Original oral tone and style
- Speech repetitions or emphases
- Any aspect of the original structure

TEXT TO PROCESS (make only minimal corrections):
{corrected_text}

OUTPUT: Text with only minimal spelling and terminology corrections, maintaining EXACTLY the same structure:
"""

        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'system', 'content': 'You are a spelling and terminology corrector. Your task is to make ONLY minimal corrections to spelling, punctuation, and specific terms. DO NOT alter the structure, content, or order of ideas in any way.'},
                {'role': 'user', 'content': prompt}
            ],
            options={'temperature': 0.1}  # Very low temperature for minimal changes
        )

        refined_text = response['message']['content'].strip()

        # Safety check - don't lose content
        if len(refined_text.split()) < len(corrected_text.split()) * 0.8:
            print("     ⚠️  Content loss detected, using corrected text")
            return corrected_text

        return refined_text

    except Exception as e:
        print(f"     ⚠️  Model processing failed: {e}")
        return corrected_text


def refine_text(text: str, model: str = "llama3.2:latest") -> str:
    """
    Legacy function for backward compatibility.
    Use refine_text_with_paragraphs for better results.
    """
    return refine_text_with_paragraphs(text, model, chunk_size=1000)  # Use larger chunks for legacy behavior
