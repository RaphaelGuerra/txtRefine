"""txtRefine - Intelligent Text Refinement Package

This package provides intelligent refinement of philosophy lecture transcriptions.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Import functions from modules to make them available at package level
from .text_processing import (
    clean_text,
    split_into_chunks,
    detect_content_type,
    merge_chunks,
    calculate_word_count,
    validate_text
)

from .model_manager import (
    check_ollama_installation,
    list_available_models,
    create_refinement_prompt,
    refine_chunk,
    validate_model,
    get_model_info,
    estimate_processing_time
)

from .file_manager import (
    list_input_files,
    list_output_files,
    validate_file_path,
    read_text_file,
    write_text_file,
    get_file_info,
    get_file_stats,
    create_backup_file,
    cleanup_old_backups,
    generate_output_filename,
    ensure_directories,
    validate_directory
)

from .ui import (
    show_header,
    show_models_menu,
    show_files_menu,
    show_options_menu,
    show_file_stats,
    show_processing_start,
    show_file_processing,
    show_processing_complete,
    show_processing_error,
    show_processing_summary,
    show_success_message,
    show_exit_message,
    show_interrupted_message,
    show_error_message,
    show_warning_message,
    show_info_message,
    confirm_action,
    get_user_input,
    show_progress
)

from .exceptions import (
    TxtRefineError,
    ModelError,
    ModelNotFoundError,
    ModelUnavailableError,
    OllamaConnectionError,
    FileError,
    FileNotFoundError,
    FileReadError,
    FileWriteError,
    DirectoryError,
    DirectoryNotFoundError,
    DirectoryAccessError,
    ProcessingError,
    TextProcessingError,
    ContentLossError,
    ChunkError,
    ChunkTooLargeError,
    ValidationError,
    TextValidationError,
    ConfigurationError,
    ConfigValidationError,
    ConfigFileError,
    NetworkError,
    TimeoutError,
    RetryExhaustedError
)

# Define what's available when importing the package
__all__ = [
    # Text processing
    'clean_text',
    'split_into_chunks',
    'detect_content_type',
    'merge_chunks',
    'calculate_word_count',
    'validate_text',

    # Model management
    'check_ollama_installation',
    'list_available_models',
    'create_refinement_prompt',
    'refine_chunk',
    'validate_model',
    'get_model_info',
    'estimate_processing_time',

    # File management
    'list_input_files',
    'list_output_files',
    'validate_file_path',
    'read_text_file',
    'write_text_file',
    'get_file_info',
    'get_file_stats',
    'create_backup_file',
    'cleanup_old_backups',
    'generate_output_filename',
    'ensure_directories',
    'validate_directory',

    # UI functions
    'show_header',
    'show_models_menu',
    'show_files_menu',
    'show_options_menu',
    'show_file_stats',
    'show_processing_start',
    'show_file_processing',
    'show_processing_complete',
    'show_processing_error',
    'show_processing_summary',
    'show_success_message',
    'show_exit_message',
    'show_interrupted_message',
    'show_error_message',
    'show_warning_message',
    'show_info_message',
    'confirm_action',
    'get_user_input',
    'show_progress',

    # Exceptions
    'TxtRefineError',
    'ModelError',
    'ModelNotFoundError',
    'ModelUnavailableError',
    'OllamaConnectionError',
    'FileError',
    'FileNotFoundError',
    'FileReadError',
    'FileWriteError',
    'DirectoryError',
    'DirectoryNotFoundError',
    'DirectoryAccessError',
    'ProcessingError',
    'TextProcessingError',
    'ContentLossError',
    'ChunkError',
    'ChunkTooLargeError',
    'ValidationError',
    'TextValidationError',
    'ConfigurationError',
    'ConfigValidationError',
    'ConfigFileError',
    'NetworkError',
    'TimeoutError',
    'RetryExhaustedError'
]
