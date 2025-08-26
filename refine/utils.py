"""Utility functions for BP philosophical text refinement."""

import os
import re
from pathlib import Path
from typing import List


# Text processing functions
def clean_text(text: str) -> str:
    """Clean text for BP philosophical processing."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Fix broken words at line breaks
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    # Normalize line breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def split_into_paragraphs(text: str) -> List[str]:
    """Split text into paragraphs while preserving structure."""
    import re
    # Handle different paragraph markers: double newlines, triple newlines, etc.
    paragraphs = re.split(r'\n\s*\n\s*|\n{3,}', text.strip())
    # Filter out empty paragraphs and clean whitespace
    return [p.strip() for p in paragraphs if p.strip()]


def split_into_chunks(text: str, max_words: int = 1000) -> List[str]:
    """Split text into manageable chunks."""
    words = text.split()
    if len(words) <= max_words:
        return [text]

    chunks = []
    for i in range(0, len(words), max_words):
        chunk = ' '.join(words[i:i + max_words])
        chunks.append(chunk)
    return chunks


def smart_chunk_text(text: str, max_words: int = 800) -> List[str]:
    """
    Hybrid approach: Split into paragraphs first, then combine intelligently.
    This preserves semantic units while ensuring optimal chunk sizes.
    """
    paragraphs = split_into_paragraphs(text)

    if not paragraphs:
        return [text]

    chunks = []
    current_chunk = []
    current_word_count = 0

    for para in paragraphs:
        para_words = len(para.split())

        # If adding this paragraph would exceed limit AND we have content
        if current_word_count + para_words > max_words and current_chunk:
            # Save current chunk
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_word_count = para_words
        else:
            # Add paragraph to current chunk
            current_chunk.append(para)
            current_word_count += para_words

    # Don't forget the last chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks


def merge_chunks(chunks: List[str]) -> str:
    """Merge chunks back into single text."""
    return ' '.join(chunks)


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
