"""
Example configuration file for the Text Refinement Program

Copy this file to 'config.py' and modify the settings according to your needs.
"""

# Default Ollama model to use
DEFAULT_MODEL = "gemma:2b"

# Chunk processing settings
MAX_WORDS_PER_CHUNK = 800      # Maximum words per chunk
MIN_WORDS_PER_CHUNK = 400      # Minimum words per chunk (for fallback)
CHUNK_OVERLAP_WORDS = 50       # Overlap between chunks (not currently used)

# Text processing settings
MAX_RETRIES = 3                # Maximum retry attempts for failed chunks
RETRY_DELAY_SECONDS = 2        # Delay between retries
CONTENT_LOSS_THRESHOLD = 0.7   # If refined text is shorter than 70% of original, retry

# File encoding
DEFAULT_ENCODING = "utf-8"

# Output settings
OUTPUT_PREFIX = "refined_"     # Prefix for output files
OUTPUT_SEPARATOR = "\n\n"      # Separator between chunks in output

# Custom prompt templates
# You can modify these prompts to better suit your specific content type

PHILOSOPHY_REFINEMENT_PROMPT = """Você é um especialista em filosofia medieval e escolástica, com profundo conhecimento da língua portuguesa e da obra de Olavo de Carvalho.

Sua tarefa é refinar a seguinte transcrição de uma aula de filosofia, mantendo a fidelidade absoluta ao conteúdo original e ao estilo do professor, mas corrigindo:

1. Erros gramaticais óbvios do português
2. Palavras mal transcritas ou incompletas
3. Frases quebradas ou mal estruturadas
4. Termos filosóficos incorretos

IMPORTANTE:
- NÃO resuma, condense ou omita conteúdo
- Mantenha TODAS as ideias filosóficas originais
- Preserve o estilo coloquial e didático do professor
- Corrija apenas erros óbvios de transcrição
- Mantenha a estrutura e fluxo da argumentação original

Transcrição a refinar (parte {chunk_num} de {total_chunks}):

{chunk}

Refine esta transcrição mantendo a fidelidade absoluta ao original:"""

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

# Add your own custom prompt templates here
CUSTOM_REFINEMENT_PROMPT = """Você é um especialista em [SEU DOMÍNIO].

Sua tarefa é refinar a seguinte transcrição, mantendo a fidelidade absoluta ao conteúdo original, mas corrigindo:

1. Erros gramaticais óbvios
2. Palavras mal transcritas ou incompletas
3. Frases quebradas ou mal estruturadas
4. Termos técnicos incorretos específicos do domínio

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
        "best": ["mistral:7b", "llama2:7b", "gemma:7b"],
        "fast": ["gemma:2b", "llama2:3b"],
        "balanced": ["llama2:7b", "gemma:7b"]
    },
    "general": {
        "best": ["mistral:7b", "llama2:7b"],
        "fast": ["gemma:2b", "llama2:3b"],
        "balanced": ["llama2:7b", "gemma:7b"]
    },
    # Add your own content types here
    "technical": {
        "best": ["mistral:7b", "llama2:7b"],
        "fast": ["gemma:2b", "llama2:3b"],
        "balanced": ["llama2:7b", "gemma:7b"]
    }
}

# Content type detection keywords
# Add keywords specific to your content types
CONTENT_TYPE_KEYWORDS = {
    "philosophy": [
        "filosofia", "escolástica", "medieval", "aristóteles", "platão", "santo tomás",
        "são boaventura", "pedro abelardo", "universais", "realismo", "nominalismo",
        "metafísica", "ontologia", "epistemologia", "lógica", "ética", "teologia"
    ],
    "technical": [
        "programação", "software", "hardware", "algoritmo", "código", "sistema",
        "tecnologia", "computador", "internet", "dados", "banco de dados"
    ]
    # Add more content types as needed
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

# Custom settings for your use case
# Uncomment and modify as needed:

# CUSTOM_CHUNK_SIZE = 600  # Smaller chunks for better quality
# CUSTOM_RETRY_COUNT = 5   # More retries for difficult content
# CUSTOM_ENCODING = "latin-1"  # Different encoding if needed
