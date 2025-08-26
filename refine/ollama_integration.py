"""Simple Ollama integration for BP philosophical text refinement."""

import ollama
from typing import List, Dict
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


def smart_chunk_text(text: str, model: str = "llama3.2:latest") -> List[str]:
    """
    Use LLM to intelligently segment text into logical paragraphs.

    This function analyzes the text for:
    - Topic shifts and thematic breaks
    - Rhetorical pauses and speaker transitions
    - Natural paragraph boundaries

    Args:
        text: Raw transcript text to segment
        model: Ollama model to use for analysis

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
                return _fallback_paragraph_split(text)
        except json.JSONDecodeError as e:
            print(f"⚠️  Smart chunking JSON parsing failed: {e}, falling back to paragraph splitting")
            return _fallback_paragraph_split(text)

    except Exception as e:
        print(f"⚠️  Smart chunking failed: {e}, falling back to paragraph splitting")
        return _fallback_paragraph_split(text)


def _fallback_paragraph_split(text: str) -> List[str]:
    """Fallback method to split text into paragraphs if smart chunking fails."""
    import re
    # Use the existing paragraph splitting logic
    from .utils import split_into_paragraphs
    return split_into_paragraphs(text)


def advanced_correction_review(text: str, model: str = "llama3.2:latest") -> List[Dict]:
    """
    Perform advanced, context-aware correction review using LLM.

    This function catches complex errors that dictionary-based approaches can't handle:
    - Transcription stutters (repeated words/phrases)
    - Grammatical errors requiring context
    - Contextually wrong phrases
    - Awkward phrasing from transcription errors

    Args:
        text: Semi-corrected text to review
        model: Ollama model to use

    Returns:
        List of correction objects with original, corrected, reason, and type
    """
    try:
        correction_prompt = f"""You are an expert academic editor with a specialization in philosophy, particularly scholasticism and modern thought, in Brazilian Portuguese. You will be given a paragraph from a class transcription that has already been partially corrected by a dictionary-based script.

Your task is to identify and correct any remaining errors. Pay close attention to:
1.  **Transcription Stutters:** Repeated words or phrases (e.g., "de Aquino de Aquino").
2.  **Grammatical Errors:** Incorrect prepositions or agreement (e.g., "período de medieval").
3.  **Contextual Phrase Errors:** Phrases that are phonetically similar but contextually wrong (e.g., "Dias César" instead of "Dai a César").
4.  **Awkward Phrasing:** Sentences that are grammatically valid but unnatural due to transcription errors.

**CRITICAL RULE:** Do NOT "simplify" or change correct philosophical terms (like 'tomista', 'cultura sacra', 'neotomismo'). Your job is to fix transcription errors, not to rewrite the content or the speaker's style.

The output MUST be a JSON list of correction objects. Each object must have four keys:
- "original": The exact text snippet to be replaced.
- "corrected": The corrected text snippet.
- "reason": A brief explanation of why the change was made.
- "type": The category of the error ('stutter', 'grammar', 'contextual', 'phrasing').

If no corrections are needed, return an empty list `[]`.

**Text to Analyze:**
{text}

**JSON Output:**
"""

        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'system', 'content': 'You are an academic editor specializing in philosophy. Output only valid JSON correction objects.'},
                {'role': 'user', 'content': correction_prompt}
            ],
            options={'temperature': 0.1}
        )

        result = response['message']['content'].strip()

        # Parse the JSON response
        import json
        try:
            corrections = json.loads(result)
            if isinstance(corrections, list):
                # Validate each correction object
                valid_corrections = []
                for correction in corrections:
                    if (isinstance(correction, dict) and
                        'original' in correction and
                        'corrected' in correction and
                        'reason' in correction and
                        'type' in correction and
                        correction['type'] in ['stutter', 'grammar', 'contextual', 'phrasing']):
                        valid_corrections.append(correction)

                print(f"✅ Advanced correction: Found {len(valid_corrections)} complex corrections")
                return valid_corrections
            else:
                print("⚠️  Advanced correction: Invalid response format, returning empty list")
                return []
        except json.JSONDecodeError as e:
            print(f"⚠️  Advanced correction JSON parsing failed: {e}, returning empty list")
            return []

    except Exception as e:
        print(f"⚠️  Advanced correction failed: {e}, returning empty list")
        return []


def apply_advanced_corrections(text: str, corrections: List[Dict]) -> str:
    """
    Apply the advanced corrections to the text, handling overlaps carefully.

    Args:
        text: Original text to apply corrections to
        corrections: List of correction objects from advanced_correction_review

    Returns:
        Text with advanced corrections applied
    """
    if not corrections:
        return text

    # Sort corrections by position in text (to handle overlaps correctly)
    corrections_with_positions = []
    for correction in corrections:
        original = correction['original']
        pos = text.find(original)
        if pos != -1:
            corrections_with_positions.append({
                **correction,
                'position': pos,
                'length': len(original)
            })

    # Sort by position (reverse to avoid position shifts)
    corrections_with_positions.sort(key=lambda x: x['position'], reverse=True)

    # Apply corrections
    result = text
    applied_count = 0

    for correction in corrections_with_positions:
        original = correction['original']
        corrected = correction['corrected']
        pos = result.find(original)

        if pos != -1:
            result = result[:pos] + corrected + result[pos + len(original):]
            applied_count += 1
            print(f"    Applied: '{original}' → '{corrected}' ({correction['type']})")

    print(f"✅ Applied {applied_count} advanced corrections")
    return result


def refine_text_comprehensive(text: str, model: str = "llama3.2:latest", use_smart_chunking: bool = True, chunk_size: int = 800) -> str:
    """
    Comprehensive three-step text refinement workflow.

    Step 1: Smart Chunking - Use LLM to segment into logical paragraphs
    Step 2: Initial Correction - Apply dictionary-based BP corrections
    Step 3: Advanced Correction - Use LLM for context-aware fixes

    This addresses the limitations of dictionary-only approaches by:
    - Handling transcription stutters (e.g., "Tomás de Aquino de Aquino")
    - Fixing grammatical errors requiring context (e.g., "período de medieval")
    - Correcting contextually wrong phrases (e.g., "Dias César" → "Dai a César")
    - Improving awkward phrasing from transcription errors

    Args:
        text: Raw transcript text to refine
        model: Ollama model to use for smart chunking and advanced correction
        use_smart_chunking: Whether to use LLM-based chunking (fallback to paragraph splitting if False)
        chunk_size: Maximum words per processing chunk

    Returns:
        Fully refined text with both simple and complex corrections applied
    """
    print("🎯 Starting comprehensive text refinement...")

    # Step 1: Smart Chunking
    print("\n📋 Step 1: Smart Chunking")
    if use_smart_chunking:
        print("   🧠 Using LLM-based intelligent segmentation...")
        paragraphs = smart_chunk_text(text, model)
    else:
        print("   📝 Using fallback paragraph splitting...")
        paragraphs = _fallback_paragraph_split(text)

    print(f"   📊 Segmented into {len(paragraphs)} logical paragraphs")

    # Step 2: Initial Correction (Dictionary-based)
    print("\n📚 Step 2: Initial Dictionary Corrections")
    bp_system = BPPhilosophySystem()
    corrected_paragraphs = []
    total_bp_corrections = 0

    for i, paragraph in enumerate(paragraphs, 1):
        print(f"   Processing paragraph {i}/{len(paragraphs)} ({len(paragraph.split())} words)")
        corrected_para, bp_corrections = bp_system.find_and_correct_terms(paragraph)
        corrected_paragraphs.append(corrected_para)
        total_bp_corrections += len(bp_corrections)

    print(f"   ✅ Applied {total_bp_corrections} dictionary-based corrections")

    # Step 3: Advanced Correction (Context-aware)
    print("\n🔍 Step 3: Advanced Context-Aware Corrections")
    final_paragraphs = []
    total_advanced_corrections = 0

    for i, corrected_para in enumerate(corrected_paragraphs, 1):
        print(f"   Reviewing paragraph {i}/{len(corrected_paragraphs)}...")
        advanced_corrections = advanced_correction_review(corrected_para, model)
        final_para = apply_advanced_corrections(corrected_para, advanced_corrections)
        final_paragraphs.append(final_para)
        total_advanced_corrections += len(advanced_corrections)

    # Reassemble with proper paragraph formatting
    final_text = '\n\n'.join(final_paragraphs)

    print("\n🎉 Comprehensive refinement completed!")
    print("📊 Summary:")
    print(f"   📋 Paragraphs processed: {len(paragraphs)}")
    print(f"   📚 Dictionary corrections: {total_bp_corrections}")
    print(f"   🔍 Advanced corrections: {total_advanced_corrections}")
    print(f"   📈 Total improvements: {total_bp_corrections + total_advanced_corrections}")

    return final_text


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
