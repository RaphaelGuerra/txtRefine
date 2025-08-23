"""Custom exceptions for txtRefine."""


class TxtRefineError(Exception):
    """Base exception for txtRefine errors."""
    pass


class ModelError(TxtRefineError):
    """Exception raised for model-related errors."""
    pass


class ModelNotFoundError(ModelError):
    """Exception raised when a specified model is not found."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        super().__init__(f"Model '{model_name}' not found. Please check if it's installed.")


class ModelUnavailableError(ModelError):
    """Exception raised when a model is not available."""

    def __init__(self, model_name: str, reason: str = ""):
        self.model_name = model_name
        self.reason = reason
        message = f"Model '{model_name}' is not available"
        if reason:
            message += f": {reason}"
        super().__init__(message)


class OllamaConnectionError(ModelError):
    """Exception raised when unable to connect to Ollama."""

    def __init__(self, message: str = "Unable to connect to Ollama"):
        super().__init__(message)


class FileError(TxtRefineError):
    """Exception raised for file-related errors."""
    pass


class FileNotFoundError(FileError):
    """Exception raised when a required file is not found."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        super().__init__(f"File not found: '{file_path}'")


class FileReadError(FileError):
    """Exception raised when unable to read a file."""

    def __init__(self, file_path: str, reason: str = ""):
        self.file_path = file_path
        self.reason = reason
        message = f"Unable to read file: '{file_path}'"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class FileWriteError(FileError):
    """Exception raised when unable to write to a file."""

    def __init__(self, file_path: str, reason: str = ""):
        self.file_path = file_path
        self.reason = reason
        message = f"Unable to write to file: '{file_path}'"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class DirectoryError(FileError):
    """Exception raised for directory-related errors."""
    pass


class DirectoryNotFoundError(DirectoryError):
    """Exception raised when a required directory is not found."""

    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        super().__init__(f"Directory not found: '{dir_path}'")


class DirectoryAccessError(DirectoryError):
    """Exception raised when unable to access a directory."""

    def __init__(self, dir_path: str, reason: str = ""):
        self.dir_path = dir_path
        self.reason = reason
        message = f"Unable to access directory: '{dir_path}'"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class ProcessingError(TxtRefineError):
    """Exception raised for text processing errors."""
    pass


class TextProcessingError(ProcessingError):
    """Exception raised when text processing fails."""

    def __init__(self, message: str = "Text processing failed"):
        super().__init__(message)


class ContentLossError(ProcessingError):
    """Exception raised when significant content loss is detected."""

    def __init__(self, original_length: int, refined_length: int):
        self.original_length = original_length
        self.refined_length = refined_length
        loss_percentage = (1 - refined_length / original_length) * 100
        super().__init__(
            f"Significant content loss detected: {loss_percentage:.1f}% "
            f"(original: {original_length}, refined: {refined_length})"
        )


class ChunkError(ProcessingError):
    """Exception raised for chunk processing errors."""
    pass


class ChunkTooLargeError(ChunkError):
    """Exception raised when a chunk is too large to process."""

    def __init__(self, chunk_size: int, max_size: int):
        self.chunk_size = chunk_size
        self.max_size = max_size
        super().__init__(
            f"Chunk too large: {chunk_size} characters (max: {max_size})"
        )


class ValidationError(TxtRefineError):
    """Exception raised for validation errors."""
    pass


class TextValidationError(ValidationError):
    """Exception raised when text validation fails."""

    def __init__(self, message: str = "Text validation failed"):
        super().__init__(message)


class ConfigurationError(TxtRefineError):
    """Exception raised for configuration errors."""
    pass


class ConfigValidationError(ConfigurationError):
    """Exception raised when configuration validation fails."""

    def __init__(self, key: str, value: str, reason: str = ""):
        self.key = key
        self.value = value
        self.reason = reason
        message = f"Configuration validation failed for '{key}': {value}"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class ConfigFileError(ConfigurationError):
    """Exception raised when configuration file operations fail."""

    def __init__(self, file_path: str, operation: str, reason: str = ""):
        self.file_path = file_path
        self.operation = operation
        self.reason = reason
        message = f"Configuration file {operation} failed: '{file_path}'"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class NetworkError(TxtRefineError):
    """Exception raised for network-related errors."""
    pass


class TimeoutError(NetworkError):
    """Exception raised when an operation times out."""

    def __init__(self, operation: str, timeout: float):
        self.operation = operation
        self.timeout = timeout
        super().__init__(f"Operation '{operation}' timed out after {timeout} seconds")


class RetryExhaustedError(TxtRefineError):
    """Exception raised when all retry attempts are exhausted."""

    def __init__(self, operation: str, attempts: int, last_error: str = ""):
        self.operation = operation
        self.attempts = attempts
        self.last_error = last_error
        message = f"All {attempts} attempts failed for operation '{operation}'"
        if last_error:
            message += f": {last_error}"
        super().__init__(message)
