"""Simple Ollama integration for BP philosophical text refinement."""

import ollama
from .bp_philosophy_optimized import OptimizedBPPhilosophySystem as BPPhilosophySystem
from .utils import smart_chunk_text, reconstruct_with_paragraphs, split_into_paragraphs


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


def refine_text(text: str, model: str = "llama3.2:latest") -> str:
    """
    Refine philosophical text with BP corrections.
    
    Args:
        text: Text to refine
        model: Ollama model to use
    
    Returns:
        Refined text
    """
    # Initialize BP system
    bp_system = BPPhilosophySystem()

    # Apply BP term corrections first
    corrected_text, corrections = bp_system.find_and_correct_terms(text)

    if corrections:
        print(f"✅ Applied {len(corrections)} BP corrections")

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
            print("⚠️  Content loss detected, using corrected text")
            return corrected_text

        return refined_text
        
    except Exception as e:
        print(f"⚠️  Model processing failed: {e}")
        return corrected_text


def validate_model(model_name: str) -> bool:
    """Check if model is available."""
    models = get_available_models()
    return model_name in models


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
    # Initialize BP system for terminology corrections
    bp_system = BPPhilosophySystem()

    # Split into smart chunks that respect paragraph boundaries
    chunks = smart_chunk_text(text, max_words=chunk_size)

    if len(chunks) == 1 and len(chunks[0].split()) <= chunk_size:
        # Single chunk - process directly
        return _process_single_chunk(chunks[0], bp_system, model)

    # Multiple chunks - process each and reassemble
    refined_chunks = []
    total_corrections = 0

    for i, chunk in enumerate(chunks, 1):
        print(f"   Processing chunk {i}/{len(chunks)} ({len(chunk.split())} words)...")
        refined_chunk = _process_single_chunk(chunk, bp_system, model)

        # Extract correction count from the chunk processing
        # (We'll need to modify _process_single_chunk to return this info)

        refined_chunks.append(refined_chunk)

    # Reassemble with proper paragraph formatting
    final_text = reconstruct_with_paragraphs(refined_chunks)

    print(f"✅ Completed hybrid paragraph processing: {len(chunks)} chunks processed")
    return final_text


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
