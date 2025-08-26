"""Simple Ollama integration for BP philosophical text refinement."""

import ollama
from .bp_philosophy_optimized import OptimizedBPPhilosophySystem as BPPhilosophySystem


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
