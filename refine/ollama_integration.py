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
    
    # Apply minimal corrections to preserve original speech structure
    corrected_text = bp_system.enhance_academic_structure(text)

    # Use Ollama for refinement
    try:
        prompt = f"""
INSTRUÇÕES CRÍTICAS: Você deve fazer APENAS correções mínimas de termos e ortografia. NÃO altere a estrutura, não reorganize, não adicione conteúdo.

TAREFA: Corrija apenas erros de digitação, ortografia e termos filosóficos específicos. Mantenha EXATAMENTE a mesma estrutura e conteúdo.

REGRAS ABSOLUTAS:
1. NÃO mude a ordem das palavras, frases ou parágrafos
2. NÃO adicione ou remova qualquer ideia ou informação
3. NÃO crie transições ou conexões entre ideias
4. NÃO altere o tom oral da aula
5. NÃO reorganize o conteúdo de forma alguma
6. APENAS corrija erros óbvios de ortografia e termos específicos

CORREÇÕES PERMITIDAS:
- Corrija erros de digitação óbvios
- Corrija termos filosóficos incorretos para formas padrão
- Corrija pontuação quando claramente errada
- Corrija erros gramaticais evidentes

NÃO ALTERE:
- Estrutura de frases e parágrafos
- Ordem e sequência de ideias
- Tom e estilo oral original
- Repetições ou ênfases da fala
- Qualquer aspecto da estrutura original

TEXTO A PROCESSAR (faça apenas correções mínimas):
{corrected_text}

SAÍDA: Texto com apenas correções mínimas de ortografia e termos, mantendo EXATAMENTE a mesma estrutura:
"""
        
        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'system', 'content': 'Você é um corretor ortográfico e terminológico. Sua tarefa é fazer APENAS correções mínimas de ortografia, pontuação e termos específicos. NÃO altere a estrutura, conteúdo ou ordem das ideias de forma alguma.'},
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
