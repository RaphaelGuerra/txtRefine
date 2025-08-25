"""Simple Ollama integration for BP philosophical text refinement."""

import ollama
from .bp_philosophy import BPPhilosophySystem


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
        return [model['name'] for model in response.get('models', [])]
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
        prompt = f"""Refine este texto filosófico brasileiro mantendo a integridade do conteúdo:

INSTRUÇÕES:
- Corrija erros gramaticais e ortográficos
- Preserve termos filosóficos e conceitos originais  
- Mantenha o estilo acadêmico brasileiro
- Não altere o significado ou argumentos filosóficos
- Preserve expressões como "quer dizer", "ou seja"

TEXTO:
{corrected_text}

TEXTO REFINADO:"""
        
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.3}
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
