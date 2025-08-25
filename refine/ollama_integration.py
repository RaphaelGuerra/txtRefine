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
        prompt = f"""
Você é um assistente de refinamento para transcrições de aulas de filosofia em Português Brasileiro.
Seu objetivo é melhorar clareza e ortografia SEM alterar o sentido do texto.

REGRAS ESTRITAS (OBRIGATÓRIAS):
- NÃO resuma, NÃO reordene, NÃO omita conteúdo do original
- NÃO invente nomes, datas ou referências; mantenha estritamente o original
- Preserve fielmente nomes próprios, títulos de obras e citações
- Corrija apenas erros evidentes de transcrição, digitação e acentuação
- Mantenha o estilo oral/acadêmico do professor ("quer dizer", "ou seja", etc.)
- Preserve termos filosóficos e suas grafias consagradas em PB

ORIENTAÇÕES ADICIONAIS:
- Preferir pontuação simples e períodos claros
- Unificar espaços, remover quebras incorretas
- Não converter oralidade em prosa literária; manter tom de aula

TEXTO A REFINAR (já com correções terminológicas aplicadas):
{corrected_text}

TEXTO REFINADO (apenas ajustes mínimos, mantendo o conteúdo integral):
"""
        
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
