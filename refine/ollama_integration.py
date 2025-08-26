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
Você é um assistente de refinamento acadêmico para textos filosóficos em Português Brasileiro.
Seu objetivo é transformar transcrições em textos acadêmicos claros e bem estruturados SEM alterar o conteúdo fundamental.

REGRAS ESTRITAS (OBRIGATÓRIAS):
- PRESERVE todo o conteúdo original - não omita ideias, exemplos ou argumentos
- NÃO altere correções terminológicas já aplicadas (ex: "equivocadamente", "techne", "historicamente")
- NÃO invente informações, nomes, datas ou referências
- Preserve termos filosóficos e expressões acadêmicas brasileiras
- Mantenha a essência do pensamento filosófico original

ORIENTAÇÕES PARA TRANSFORMAÇÃO ACADÊMICA:
- REORGANIZE em parágrafos lógicos e coesos (4-6 parágrafos principais)
- Use transições suaves entre ideias e parágrafos
- Seja conciso mas completo - elimine repetições desnecessárias
- Melhore a clareza e precisão da linguagem acadêmica
- Mantenha tom acadêmico acessível, não excessivamente formal
- Adicione uma conclusão resumindo os pontos principais
- Adicione título apropriado se necessário

ESTRUTURA DESEJADA:
1. Introdução ao período e obra de Tomás de Aquino
2. Análise da síntese tomista e suas interpretações
3. Impacto histórico e influência limitada
4. Problemas da cultura sacra/mundana e função da Igreja
5. Conclusão sobre a oportunidade perdida

IMPORTANTE: O texto base já foi corrigido terminologicamente. NÃO altere:
- "equivocadamente" (mantém esta correção)
- "techne" (mantém esta correção)
- "historicamente" (mantém)
- "neotomismo" (mantém)

TEXTO A TRANSFORMAR (já corrigido terminologicamente):
{structured_text}

TEXTO ACADÊMICO FINAL (bem estruturado, claro e conciso, mantendo todo conteúdo):
"""
        
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.3}
        )

        refined_text = response['message']['content'].strip()

        # FORCE preservation of critical corrections after Ollama processing
        final_force_corrections = {
            'hamartianeamente': 'equivocadamente',
            'ptechne': 'techne',
            'capacidadi': 'capacidade',
            'e spantoso': 'espantoso',
            'neotomismo': 'neotomismo',
            'historicamnete': 'historicamente',
            'historicamente inute': 'historicamente ineficaz',
            'maior ptechne': 'maior capacidade',
            'cuja maior ptechne': 'cuja maior capacidade'
        }

        for wrong, correct in final_force_corrections.items():
            refined_text = refined_text.replace(wrong, correct)

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
