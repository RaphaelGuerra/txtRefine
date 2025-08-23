"""Model management functions for txtRefine."""

import ollama
import time
from typing import Optional, Dict, Any
from pathlib import Path


# Configuration constants
DEFAULT_MODEL = "llama3.2:latest"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
CONTENT_LOSS_THRESHOLD = 0.7

# Prompt template
PHILOSOPHY_REFINEMENT_PROMPT = """Você é um especialista em filosofia medieval e escolástica, com profundo conhecimento da língua portuguesa e da obra de Olavo de Carvalho.

Sua tarefa é refinar a seguinte transcrição de uma aula de filosofia, mantendo a fidelidade ABSOLUTA ao conteúdo original e ao estilo do professor, mas corrigindo APENAS:

1. Erros gramaticais óbvios do português
2. Palavras mal transcritas ou incompletas (ex: "Colássica" → "Escolástica")
3. Frases quebradas ou mal estruturadas
4. Termos filosóficos incorretos

REGRAS ESTRITAS:
- NÃO resuma, condense ou omita conteúdo
- NÃO adicione novas informações ou explicações
- NÃO mude o significado ou a estrutura das frases
- NÃO altere exemplos, citações ou referências
- Mantenha EXATAMENTE o mesmo comprimento e estrutura
- Preserve TODAS as ideias filosóficas originais
- Mantenha o estilo coloquial e didático do professor
- Corrija APENAS erros óbvios de transcrição
- Mantenha a estrutura e fluxo da argumentação original

Transcrição a refinar (parte {chunk_num} de {total_chunks}):

{chunk}

Refine esta transcrição mantendo a fidelidade ABSOLUTA ao original, corrigindo APENAS erros de transcrição:"""


def check_ollama_installation() -> bool:
    """Check if Ollama is installed and accessible."""
    try:
        response = ollama.list()
        return True
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        print("💡 Make sure Ollama is installed and running")
        return False


def list_available_models() -> list:
    """List all available Ollama models and return them."""
    try:
        response = ollama.list()
        models = response.models if hasattr(response, 'models') else []

        model_info = []
        if models:
            for model in models:
                model_name = getattr(model, 'model', 'Unknown')
                model_size = getattr(model, 'size', 'Unknown size')
                # Convert size to GB for readability
                if isinstance(model_size, int):
                    size_gb = f"{model_size / (1024**3):.1f} GB"
                else:
                    size_gb = str(model_size)
                model_info.append({
                    'name': model_name,
                    'size': size_gb,
                    'size_bytes': model_size if isinstance(model_size, int) else 0
                })

        return model_info

    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return []


def create_refinement_prompt(chunk: str, chunk_num: int, total_chunks: int) -> str:
    """Create refinement prompt for philosophical content."""
    return PHILOSOPHY_REFINEMENT_PROMPT.format(
        chunk=chunk,
        chunk_num=chunk_num,
        total_chunks=total_chunks
    )


def refine_chunk(
    chunk: str,
    model_name: str,
    chunk_num: int,
    total_chunks: int,
    max_retries: int = MAX_RETRIES
) -> str:
    """Refine a single chunk of text using the specified model."""
    prompt = create_refinement_prompt(chunk, chunk_num, total_chunks)

    for attempt in range(max_retries):
        try:
            response = ollama.generate(
                model=model_name,
                prompt=prompt,
                stream=False
            )

            refined_text = response['response'].strip()

            # Check for significant content loss
            original_length = len(chunk)
            refined_length = len(refined_text)

            if refined_length < original_length * CONTENT_LOSS_THRESHOLD:
                print(f"⚠️  Possible content loss detected (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    time.sleep(RETRY_DELAY_SECONDS)
                    continue
                else:
                    print("❌ Using original text due to content loss")
                    return chunk

            return refined_text

        except Exception as e:
            if "context length" in str(e).lower():
                print(f"⚠️  Chunk too long, splitting...")
                # Split chunk in half and process recursively
                mid_point = len(chunk) // 2
                # Find a good split point (sentence boundary)
                sentences = chunk.split('. ')
                if len(sentences) > 1:
                    mid_sentence = len(sentences) // 2
                    first_half = '. '.join(sentences[:mid_sentence]) + '.'
                    second_half = '. '.join(sentences[mid_sentence:])
                else:
                    first_half = chunk[:mid_point]
                    second_half = chunk[mid_point:]

                refined_first = refine_chunk(first_half, model_name, chunk_num, total_chunks, max_retries)
                refined_second = refine_chunk(second_half, model_name, chunk_num, total_chunks, max_retries)

                return refined_first + " " + refined_second
            else:
                print(f"❌ Error refining chunk {chunk_num}: {e}")
                if attempt < max_retries - 1:
                    print(f"🔄 Retrying in {RETRY_DELAY_SECONDS} seconds...")
                    time.sleep(RETRY_DELAY_SECONDS)
                else:
                    print("❌ Using original text after multiple attempts")
                    return chunk

    return chunk


def validate_model(model_name: str) -> bool:
    """Validate if a model is available and can be used."""
    available_models = list_available_models()
    model_names = [model['name'] for model in available_models]
    return model_name in model_names


def get_model_info(model_name: str) -> Optional[Dict[str, Any]]:
    """Get information about a specific model."""
    available_models = list_available_models()
    for model in available_models:
        if model['name'] == model_name:
            return model
    return None


def estimate_processing_time(word_count: int, model_name: str) -> float:
    """Estimate processing time in seconds based on word count and model."""
    # Rough estimates based on typical performance
    base_time_per_100_words = {
        'llama3.2:latest': 1.5,  # seconds per 100 words
        'neural-chat:latest': 2.0,
        'openchat:latest': 1.8,
        'dolphin-phi:latest': 1.2,
        'gemma:2b': 1.0
    }

    time_per_100 = base_time_per_100_words.get(model_name, 2.0)
    return (word_count / 100) * time_per_100
