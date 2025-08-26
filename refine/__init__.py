"""txtRefine - BP Philosophical Text Refinement

Core functionality for Brazilian Portuguese philosophical transcription refinement.
"""

__version__ = "1.0.0"

# Merged utility functions
from .utils import (
    clean_text, split_into_chunks, merge_chunks, word_count, is_valid_text,
    list_input_files, list_output_files, read_text_file, write_text_file,
    generate_output_filename, ensure_directories
)

# Ollama integration
from .ollama_integration import check_ollama, get_available_models, refine_text, validate_model

# Core BP functionality (optimized version)
from .bp_philosophy_optimized import OptimizedBPPhilosophySystem as BPPhilosophySystem

# Minimal UI
from .ui import show_header, show_error_message, show_processing_complete, show_success_message, show_exit_message, show_interrupted_message, get_user_input

__all__ = [
    # Utility functions
    'clean_text', 'split_into_chunks', 'merge_chunks', 'word_count', 'is_valid_text',
    'list_input_files', 'list_output_files', 'read_text_file', 'write_text_file',
    'generate_output_filename', 'ensure_directories',
    # Ollama integration
    'check_ollama', 'get_available_models', 'refine_text', 'validate_model',
    # Core BP functionality
    'BPPhilosophySystem',
    # Minimal UI
    'show_header', 'show_error_message', 'show_processing_complete',
    'show_success_message', 'show_exit_message', 'show_interrupted_message', 'get_user_input'
]
