"""
Configuration file for the Text Refinement Program
"""

# Default Ollama model to use
DEFAULT_MODEL = "llama3.2:latest"

# Chunk processing settings
MAX_WORDS_PER_CHUNK = 800
MIN_WORDS_PER_CHUNK = 400
CHUNK_OVERLAP_WORDS = 50

# Text processing settings
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
CONTENT_LOSS_THRESHOLD = 0.7  # If refined text is shorter than 70% of original, retry

# File encoding
DEFAULT_ENCODING = "utf-8"

# Output settings
OUTPUT_PREFIX = "refined_"
OUTPUT_SEPARATOR = "\n\n"

# Prompt templates
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

GENERAL_REFINEMENT_PROMPT = """Você é um especialista em língua portuguesa e transcrições.

Sua tarefa é refinar a seguinte transcrição, mantendo a fidelidade absoluta ao conteúdo original, mas corrigindo:

1. Erros gramaticais óbvios
2. Palavras mal transcritas ou incompletas
3. Frases quebradas ou mal estruturadas
4. Quebras de linha inadequadas

IMPORTANTE:
- NÃO resuma, condense ou omita conteúdo
- Mantenha o estilo e tom original
- Corrija apenas erros óbvios de transcrição
- Preserve a estrutura e fluxo original

Transcrição a refinar (parte {chunk_num} de {total_chunks}):

{chunk}

Refine esta transcrição mantendo a fidelidade absoluta ao original:"""

# Model recommendations for different content types
MODEL_RECOMMENDATIONS = {
    "philosophy": {
        "best": ["neural-chat:latest", "openchat:latest", "llama3.2:latest"],
        "fast": ["gemma:2b", "dolphin-phi:latest"],
        "balanced": ["openchat:latest", "llama3.2:latest"]
    },
    "general": {
        "best": ["neural-chat:latest", "openchat:latest", "llama3.2:latest"],
        "fast": ["gemma:2b", "dolphin-phi:latest"],
        "balanced": ["openchat:latest", "llama3.2:latest"]
    },
    "technical": {
        "best": ["neural-chat:latest", "openchat:latest"],
        "fast": ["gemma:2b", "dolphin-phi:latest"],
        "balanced": ["openchat:latest", "llama3.2:latest"]
    }
}

# Model descriptions and characteristics
MODEL_DESCRIPTIONS = {
    "neural-chat:latest": {
        "name": "Neural Chat",
        "description": "High-quality open-source model optimized for chat and instruction following",
        "size": "4.1 GB",
        "quality": "⭐⭐⭐⭐⭐",
        "speed": "⚡⚡",
        "best_for": "Philosophy, complex reasoning, high-quality output"
    },
    "openchat:latest": {
        "name": "OpenChat",
        "description": "Excellent open-source model with strong reasoning capabilities",
        "size": "4.1 GB",
        "quality": "⭐⭐⭐⭐⭐",
        "speed": "⚡⚡",
        "best_for": "Academic content, philosophy, detailed analysis"
    },
    "llama3.2:latest": {
        "name": "Llama 3.2",
        "description": "Meta's latest open-source model with strong performance",
        "size": "2.0 GB",
        "quality": "⭐⭐⭐⭐",
        "speed": "⚡⚡⚡",
        "best_for": "General purpose, good balance of quality and speed"
    },
    "dolphin-phi:latest": {
        "name": "Dolphin Phi",
        "description": "Microsoft's Phi model optimized for instruction following",
        "size": "1.6 GB",
        "quality": "⭐⭐⭐⭐",
        "speed": "⚡⚡⚡",
        "best_for": "Fast processing, good quality for size"
    },
    "gemma:2b": {
        "name": "Gemma 2B",
        "description": "Google's lightweight but capable model",
        "size": "1.7 GB",
        "quality": "⭐⭐⭐",
        "speed": "⚡⚡⚡⚡",
        "best_for": "Quick processing, basic refinement tasks"
    }
}

# Content type detection keywords
CONTENT_TYPE_KEYWORDS = {
    "philosophy": [
        "filosofia", "escolástica", "escolástico", "medieval", "aristóteles", "platão", "santo tomás",
        "são boaventura", "pedro abelardo", "universais", "realismo", "nominalismo",
        "metafísica", "ontologia", "epistemologia", "lógica", "ética", "teologia",
        "padres", "igreja", "cristã", "cristão", "religioso", "religiosa", "espiritual",
        "alma", "deus", "divino", "sagrado", "sagrada", "escritura", "evangelho",
        "academia", "intelectual", "intelectuais", "coletividade", "comunidade"
    ]
}

# Error messages in Portuguese
ERROR_MESSAGES = {
    "ollama_not_found": "❌ Erro: Ollama não está instalado ou acessível.",
    "ollama_install_url": "📥 Instale o Ollama em: https://ollama.com/download",
    "model_not_found": "❌ Erro: Modelo '{model}' não encontrado.",
    "model_pull_command": "📥 Baixe o modelo executando: ollama pull {model}",
    "input_folder_not_found": "❌ Erro: Pasta 'input' não encontrada.",
    "no_files_to_process": "❌ Nenhum arquivo .txt encontrado para processar.",
    "file_not_found": "⚠️  Arquivo não encontrado ou não é .txt: {filename}",
    "empty_file": "❌ Arquivo de entrada vazio",
    "connection_error": "❌ Erro: Não foi possível conectar ao Ollama. Verifique se está rodando.",
    "context_length_error": "⚠️  Chunk {chunk_num} muito longo, tentando dividir...",
    "unexpected_error": "❌ Erro inesperado no chunk {chunk_num}: {error}",
    "content_loss_warning": "⚠️  Aviso: Chunk {chunk_num} pode ter perdido conteúdo (tentativa {attempt})",
    "using_original": "⚠️  Usando texto original para chunk {chunk_num}",
    "processing_failed": "❌ Falha ao processar: {filename}"
}

# Success messages in Portuguese
SUCCESS_MESSAGES = {
    "using_model": "🤖 Usando modelo: {model}",
    "processing_file": "📖 Processando: {filename}",
    "chunks_created": "📝 Dividido em {count} chunks para processamento",
    "refinement_complete": "✅ Refinamento concluído: {filename}",
    "statistics": "📊 Estatísticas:",
    "original_chars": "   - Texto original: {count} caracteres",
    "refined_chars": "   - Texto refinado: {count} caracteres",
    "chunks_processed": "   - Chunks processados: {count}",
    "files_processing": "📁 Processando {count} arquivo(s)",
    "processing_complete": "🎉 Processamento concluído!"
}

# Progress bar settings
PROGRESS_BAR_DESC = "Refinando chunks"
PROGRESS_BAR_UNIT = "chunk"

# File patterns
TEXT_FILE_PATTERN = "*.txt"
