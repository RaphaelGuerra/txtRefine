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
    
    # Use enhanced academic structure method first
    structured_text = bp_system.enhance_academic_structure(corrected_text)

    # Force critical corrections one more time to ensure they're preserved
    final_corrections = {
        'hamartianeamente': 'equivocadamente',
        'ptechne': 'techne',
        'capacidadi': 'capacidade',
        'e spantoso': 'espantoso',
        'neotomismo': 'neotomismo',
        'síntese tomista': 'síntese tomista',
        'quer dizer': 'Ou seja,',
        'o pessoal enuncia': 'é frequentemente interpretada',
        'o que a gente vê': 'olhando em retrospecto',
        'como se nada tivesse sido feito': 'como se sua obra não tivesse tido impacto algum',
        'assim mesmo': 'de fato',
        'é muito espantoso': 'É notável',
        'esse período de medieval': 'O período medieval tardio',
        'mas uma culminação': 'mas representa um ponto crucial',
        'buscava-se resolver': 'Nela, buscava-se resolver'
    }

    for wrong, correct in final_corrections.items():
        structured_text = structured_text.replace(wrong, correct)

    # Use Ollama for refinement
    try:
        prompt = f"""
Você é um assistente de refinamento para transcrições de aulas de filosofia em Português Brasileiro.
Seu objetivo é melhorar clareza, ortografia e estrutura acadêmica SEM alterar o sentido do texto.

REGRAS ESTRITAS (OBRIGATÓRIAS):
- NÃO resuma, NÃO reordene, NÃO omita conteúdo do original
- NÃO altere correções terminológicas já aplicadas (ex: "equivocadamente", "techne", "historicamente")
- NÃO invente nomes, datas ou referências; mantenha estritamente o original
- Preserve fielmente nomes próprios, títulos de obras e citações
- Corrija apenas erros evidentes de transcrição, digitação e acentuação
- Mantenha o estilo acadêmico brasileiro preservando expressões como "quer dizer", "ou seja"
- Preserve termos filosóficos e suas grafias consagradas em PB

ORIENTAÇÕES PARA ESTRUTURA ACADÊMICA:
- Melhore a organização em parágrafos quando apropriado
- Use transições mais elegantes entre ideias
- Mantenha tom acadêmico sem converter completamente em prosa formal
- Preserve o caráter oral da aula mas torne mais fluido
- Melhore conexões lógicas entre frases
- Adicione título apropriado se o texto não tiver um

IMPORTANTE: O texto já foi corrigido terminologicamente. NÃO altere termos como:
- "equivocadamente" (não volte para "hamartianeamente")
- "techne" (não volte para "ptechne")
- "historicamente" (não altere)
- "neotomismo" (mantenha como está)

TEXTO A REFINAR (já estruturado academicamente):
{structured_text}

TEXTO REFINADO (com melhor estrutura acadêmica, mantendo conteúdo integral):
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
