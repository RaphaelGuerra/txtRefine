"""Utility functions for BP philosophical text refinement."""

import os
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from functools import lru_cache
import time


# Text processing functions
def remove_timestamps(text: str) -> str:
    """Remove timestamp patterns from text.

    Handles various timestamp formats commonly found in transcriptions:
    - M:SS format (e.g., "2:51", "15:30")
    - MM:SS format (e.g., "02:51", "15:30")
    - [Música] and other common markers
    """
    if not text:
        return ""

    # Remove timestamps in format M:SS or MM:SS at the beginning of lines
    # This pattern matches digits:digits at start of line, optionally followed by space or common markers
    text = re.sub(r'^(\d{1,2}:\d{2})\s*(\[.*?\])?\s*', '', text, flags=re.MULTILINE)

    # Remove standalone timestamps that might be on their own lines
    text = re.sub(r'^\s*(\d{1,2}:\d{2})\s*$', '', text, flags=re.MULTILINE)

    # Clean up any double spaces or excessive whitespace that might result
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\s+', '\n', text)

    return text.strip()


def clean_text(text: str) -> str:
    """Clean text while preserving paragraph structure.

    - Remove timestamps from transcriptions
    - Normalize line endings to \n
    - Repair hyphenated line-break splits (e.g., "pala-\n vra" -> "palavra")
    - Trim trailing spaces on each line
    - Collapse runs of 3+ blank lines to exactly one blank line
    """
    if not text:
        return ""

    # First, remove timestamps from transcriptions
    text = remove_timestamps(text)

    # Normalize Windows/Mac line endings to \n
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Fix broken words at line breaks: word-\n word -> wordword
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

    # Trim trailing spaces per line
    lines = [re.sub(r'\s+$', '', line) for line in text.split('\n')]
    text = '\n'.join(lines)

    # Collapse 3+ consecutive blank lines to a single blank line
    text = re.sub(r'(\n\s*){3,}', '\n\n', text)

    # Final trim while preserving first/last line boundaries
    return text.strip('\n')


def split_into_paragraphs(text: str) -> List[str]:
    """Split text into paragraphs while preserving structure."""
    # Handle different paragraph markers: double newlines, triple newlines, etc.
    paragraphs = re.split(r'\n\s*\n\s*|\n{3,}', text.strip())
    return [p.strip() for p in paragraphs if p.strip()]


# Note: All chunking helpers removed to simplify processing into single-pass


def reconstruct_with_paragraphs(paragraphs: List[str]) -> str:
    """Reassemble paragraphs with proper spacing for final output."""
    return '\n\n'.join(paragraphs)


def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def is_valid_text(text: str) -> bool:
    """Check if text is valid for processing."""
    return bool(text and text.strip() and len(text.strip()) > 10)


# File operations functions
def list_input_files(input_dir: str = "input") -> List[str]:
    """List all .txt files in the input folder."""
    input_folder = Path(input_dir)
    
    if not input_folder.exists():
        print(f"❌ Folder '{input_dir}' not found")
        return []
    
    txt_files = list(input_folder.glob("*.txt"))
    return [f.name for f in txt_files]


def list_output_files(output_dir: str = "output") -> List[str]:
    """List all files in the output folder."""
    output_folder = Path(output_dir)
    
    if not output_folder.exists():
        return []
    
    return [f.name for f in output_folder.iterdir() if f.is_file()]


def read_text_file(file_path: str, encoding: str = "utf-8") -> str:
    """Read text content from a file."""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return ""


def write_text_file(file_path: str, content: str, encoding: str = "utf-8") -> bool:
    """Write text content to a file."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error writing {file_path}: {e}")
        return False


def generate_output_filename(input_filename: str) -> str:
    """Generate output filename with 'refined_' prefix."""
    return f"refined_{input_filename}"


def ensure_directories(*dirs: str) -> None:
    """Ensure directories exist."""
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)


# Caching system for performance optimization
class TextProcessingCache:
    """LRU cache for text processing operations."""

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self._llm_cache: Dict[str, Dict[str, Any]] = {}
        self._bp_cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, float] = {}

    def _get_cache_key(self, text: str, operation: str, model: str = "") -> str:
        """Generate a cache key from text and operation."""
        content = f"{text}:{operation}:{model}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _cleanup_cache(self, cache_dict: Dict[str, Dict[str, Any]]) -> None:
        """Remove oldest entries if cache exceeds max size."""
        if len(cache_dict) >= self.max_size:
            # Remove oldest 20% of entries
            to_remove = int(self.max_size * 0.2)
            sorted_keys = sorted(self._access_times.items(), key=lambda x: x[1])
            for key, _ in sorted_keys[:to_remove]:
                if key in cache_dict:
                    del cache_dict[key]
                if key in self._access_times:
                    del self._access_times[key]

    def get_llm_response(self, text: str, model: str) -> Optional[str]:
        """Get cached LLM response if available."""
        key = self._get_cache_key(text, "llm", model)
        if key in self._llm_cache:
            self._access_times[key] = time.time()
            return self._llm_cache[key]['response']
        return None

    def set_llm_response(self, text: str, model: str, response: str) -> None:
        """Cache LLM response."""
        key = self._get_cache_key(text, "llm", model)
        self._cleanup_cache(self._llm_cache)
        self._llm_cache[key] = {
            'response': response,
            'timestamp': time.time()
        }
        self._access_times[key] = time.time()

    def get_bp_corrections(self, text: str) -> Optional[Dict[str, Any]]:
        """Get cached BP corrections if available."""
        key = self._get_cache_key(text, "bp")
        if key in self._bp_cache:
            self._access_times[key] = time.time()
            return self._bp_cache[key]
        return None

    def set_bp_corrections(self, text: str, corrected_text: str, corrections: List[Dict]) -> None:
        """Cache BP corrections."""
        key = self._get_cache_key(text, "bp")
        self._cleanup_cache(self._bp_cache)
        self._bp_cache[key] = {
            'corrected_text': corrected_text,
            'corrections': corrections,
            'timestamp': time.time()
        }
        self._access_times[key] = time.time()

    def clear_cache(self) -> None:
        """Clear all cached data."""
        self._llm_cache.clear()
        self._bp_cache.clear()
        self._access_times.clear()

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'llm_cache_size': len(self._llm_cache),
            'bp_cache_size': len(self._bp_cache),
            'total_cache_entries': len(self._llm_cache) + len(self._bp_cache)
        }


# Global cache instance
_text_cache = TextProcessingCache(max_size=200)


def get_global_cache() -> TextProcessingCache:
    """Get the global text processing cache."""
    return _text_cache


@lru_cache(maxsize=50)
def cached_clean_text(text: str) -> str:
    """Cached version of clean_text for repeated identical inputs."""
    return clean_text(text)


# Memory-efficient streaming processor for large files
class StreamingTextProcessor:
    """Process large text files in chunks to reduce memory usage."""

    def __init__(self, chunk_size: int = 100000):  # 100KB chunks by default
        self.chunk_size = chunk_size
        self.cache = get_global_cache()

    def process_large_file(self, file_path: str, model: str = "llama3.2:latest") -> str:
        """
        Process a large file by streaming it in chunks.
        This reduces memory usage for very large files.
        """
        print(f"📄 Processing large file: {os.path.basename(file_path)}")

        # Check if file is actually large enough to warrant streaming
        file_size = os.path.getsize(file_path)
        if file_size < self.chunk_size * 2:
            # File is small enough, use regular processing
            return read_text_file(file_path)

        print(f"📊 File size: {file_size / 1024:.1f} KB - using streaming mode")

        processed_chunks = []
        chunk_count = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                while True:
                    # Read chunk
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break

                    chunk_count += 1
                    print(f"   Processing chunk {chunk_count}...")

                    # Process the chunk
                    processed_chunk = self._process_chunk(chunk, model)
                    processed_chunks.append(processed_chunk)

                    # Show progress
                    print(f"   ✅ Chunk {chunk_count} completed")

            # Combine all processed chunks
            result = ''.join(processed_chunks)

            print(f"🎉 Streaming processing complete - {chunk_count} chunks processed")
            return result

        except Exception as e:
            print(f"⚠️  Streaming processing failed: {e}")
            # Fallback to regular processing
            print("🔄 Falling back to regular processing...")
            return read_text_file(file_path)

    def _process_chunk(self, chunk: str, model: str) -> str:
        """Process a single chunk with BP corrections and LLM refinement."""
        from .ollama_integration import single_pass_refine

        # Clean the chunk
        cleaned_chunk = cached_clean_text(chunk)

        # Process with the full pipeline
        refined_chunk = single_pass_refine(cleaned_chunk, model)

        return refined_chunk

    def should_use_streaming(self, file_path: str) -> bool:
        """Determine if streaming should be used for a file."""
        try:
            file_size = os.path.getsize(file_path)
            return file_size > self.chunk_size * 2  # Use streaming for files > 2 chunks
        except OSError:
            return False


# Global streaming processor instance
_streaming_processor = StreamingTextProcessor()


def get_streaming_processor() -> StreamingTextProcessor:
    """Get the global streaming processor."""
    return _streaming_processor


# Performance monitoring system
class PerformanceMonitor:
    """Monitor and track performance metrics for text processing operations."""

    def __init__(self):
        self.metrics = {
            'total_files_processed': 0,
            'total_processing_time': 0.0,
            'total_characters_processed': 0,
            'total_words_processed': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'streaming_files': 0,
            'regular_files': 0,
            'llm_calls': 0,
            'bp_corrections_applied': 0,
            'errors_encountered': 0
        }
        self.start_time = time.time()
        self.current_operation_start = None

    def start_operation(self, operation_name: str):
        """Start timing an operation."""
        self.current_operation_start = time.time()
        print(f"⏱️  Starting: {operation_name}")

    def end_operation(self, operation_name: str, **kwargs):
        """End timing an operation and record metrics."""
        if self.current_operation_start:
            duration = time.time() - self.current_operation_start
            print(f"✅ Completed: {operation_name} ({duration:.2f}s)")
            self.current_operation_start = None
            return duration
        return 0.0

    def record_file_processing(self, file_size: int, word_count: int, processing_time: float,
                             used_streaming: bool = False, used_cache: bool = False):
        """Record metrics for a processed file."""
        self.metrics['total_files_processed'] += 1
        self.metrics['total_processing_time'] += processing_time
        self.metrics['total_characters_processed'] += file_size
        self.metrics['total_words_processed'] += word_count

        if used_streaming:
            self.metrics['streaming_files'] += 1
        else:
            self.metrics['regular_files'] += 1

        if used_cache:
            self.metrics['cache_hits'] += 1
        else:
            self.metrics['cache_misses'] += 1

    def record_llm_call(self):
        """Record an LLM API call."""
        self.metrics['llm_calls'] += 1

    def record_bp_corrections(self, correction_count: int):
        """Record BP corrections applied."""
        self.metrics['bp_corrections_applied'] += correction_count

    def record_error(self):
        """Record an error."""
        self.metrics['errors_encountered'] += 1

    def get_summary(self) -> Dict[str, any]:
        """Get a summary of performance metrics."""
        total_runtime = time.time() - self.start_time
        avg_file_time = self.metrics['total_processing_time'] / max(self.metrics['total_files_processed'], 1)
        chars_per_second = self.metrics['total_characters_processed'] / max(total_runtime, 1)
        words_per_second = self.metrics['total_words_processed'] / max(total_runtime, 1)
        cache_hit_rate = (self.metrics['cache_hits'] / max(self.metrics['cache_hits'] + self.metrics['cache_misses'], 1)) * 100

        return {
            'total_runtime_seconds': round(total_runtime, 2),
            'files_processed': self.metrics['total_files_processed'],
            'avg_file_processing_time': round(avg_file_time, 2),
            'characters_per_second': round(chars_per_second, 2),
            'words_per_second': round(words_per_second, 2),
            'streaming_files': self.metrics['streaming_files'],
            'regular_files': self.metrics['regular_files'],
            'cache_hit_rate': round(cache_hit_rate, 1),
            'llm_calls': self.metrics['llm_calls'],
            'bp_corrections_applied': self.metrics['bp_corrections_applied'],
            'errors_encountered': self.metrics['errors_encountered']
        }

    def print_summary(self):
        """Print a formatted performance summary."""
        summary = self.get_summary()

        print("\n" + "=" * 60)
        print("📊 PERFORMANCE SUMMARY")
        print("=" * 60)
        print(f"Total runtime: {summary['total_runtime_seconds']}s")
        print(f"Files processed: {summary['files_processed']}")
        print(f"Average file time: {summary['avg_file_processing_time']}s")
        print(f"Processing speed: {summary['characters_per_second']} chars/sec")
        print(f"Word processing: {summary['words_per_second']} words/sec")
        print(f"Cache hit rate: {summary['cache_hit_rate']}%")
        print(f"LLM calls: {summary['llm_calls']}")
        print(f"BP corrections: {summary['bp_corrections_applied']}")
        if summary['streaming_files'] > 0:
            print(f"Streaming files: {summary['streaming_files']}")
        if summary['errors_encountered'] > 0:
            print(f"Errors encountered: {summary['errors_encountered']}")
        print("=" * 60)


# Global performance monitor instance
_performance_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor."""
    return _performance_monitor
