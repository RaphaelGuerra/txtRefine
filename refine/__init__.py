"""txtRefine core package for PT-BR transcript refinement."""

__version__ = "1.1.0"

# Merged utility functions
from .utils import (
    clean_text, word_count, is_valid_text,
    list_input_files, list_output_files, read_text_file, write_text_file,
    generate_output_filename, ensure_directories
)

# Ollama integration
from .ollama_integration import (
    check_ollama, get_available_models, single_pass_refine as refine_text, validate_model
)

# Core deterministic transcript cleanup
from .transcript_refinement import TranscriptRefinementSystem

# Backwards-compatible alias for older imports.
BPPhilosophySystem = TranscriptRefinementSystem

# Minimal UI
from .ui import show_header, show_error_message, show_processing_complete, show_success_message, show_exit_message, show_interrupted_message, get_user_input

__all__ = [
    # Utility functions
    'clean_text', 'word_count', 'is_valid_text',
    'list_input_files', 'list_output_files', 'read_text_file', 'write_text_file',
    'generate_output_filename', 'ensure_directories',
    # Ollama integration
    'check_ollama', 'get_available_models', 'refine_text', 'validate_model',
    # Core transcript functionality
    'TranscriptRefinementSystem',
    'BPPhilosophySystem',
    # Minimal UI
    'show_header', 'show_error_message', 'show_processing_complete',
    'show_success_message', 'show_exit_message', 'show_interrupted_message', 'get_user_input'
]
