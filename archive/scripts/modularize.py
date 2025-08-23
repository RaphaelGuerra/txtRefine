#!/usr/bin/env python3
"""
Script to assist with modularization of txtRefine.
This script analyzes the current code structure and helps plan the modularization.
"""

import os
import re
import ast
from pathlib import Path
from collections import defaultdict

def analyze_current_structure():
    """Analyze the current structure of refine.py"""
    print("🔍 Analyzing current structure...")

    with open('refine.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all function definitions
    function_pattern = r'def\s+(\w+)\s*\([^)]*\):'
    functions = re.findall(function_pattern, content)

    # Find all class definitions
    class_pattern = r'class\s+(\w+)\s*:'
    classes = re.findall(class_pattern, content)

    # Find all import statements
    import_pattern = r'^(import\s+\w+|from\s+\w+\s+import\s+.*)$'
    imports = re.findall(import_pattern, content, re.MULTILINE)

    print(f"\n📊 Analysis Results:")
    print(f"   Functions: {len(functions)}")
    print(f"   Classes: {len(classes)}")
    print(f"   Imports: {len(imports)}")

    print(f"\n🔧 Functions Found:")
    for func in functions:
        print(f"   - {func}")

    print(f"\n🏗️  Classes Found:")
    for cls in classes:
        print(f"   - {cls}")

    return functions, classes, imports

def categorize_functions(functions):
    """Categorize functions by their purpose"""
    categories = {
        'text_processing': [],
        'model_management': [],
        'file_operations': [],
        'ui_interaction': [],
        'main_logic': [],
        'utilities': []
    }

    # Simple keyword-based categorization
    for func in functions:
        func_lower = func.lower()
        if any(word in func_lower for word in ['clean', 'chunk', 'split', 'text', 'process']):
            categories['text_processing'].append(func)
        elif any(word in func_lower for word in ['model', 'ollama', 'generate', 'refine']):
            categories['model_management'].append(func)
        elif any(word in func_lower for word in ['file', 'read', 'write', 'save', 'load']):
            categories['file_operations'].append(func)
        elif any(word in func_lower for word in ['show', 'menu', 'display', 'print', 'input']):
            categories['ui_interaction'].append(func)
        elif any(word in func_lower for word in ['main', 'transcription', 'process']):
            categories['main_logic'].append(func)
        else:
            categories['utilities'].append(func)

    return categories

def generate_module_structure():
    """Generate the proposed module structure"""
    structure = {
        'refine/': {
            '__init__.py': '# Main package for txtRefine',
            'text_processing.py': '# Text cleaning and chunking functions',
            'model_manager.py': '# Ollama model interaction',
            'file_manager.py': '# File I/O operations',
            'ui.py': '# User interface components',
            'exceptions.py': '# Custom exceptions',
            'logger.py': '# Logging configuration',
            'validation.py': '# Input validation',
            'config.py': '# Configuration management',
            'cache.py': '# Caching system',
            'metrics.py': '# Performance monitoring'
        }
    }
    return structure

def create_directory_structure():
    """Create the basic directory structure"""
    print("📁 Creating directory structure...")

    # Create refine package directory
    os.makedirs('refine', exist_ok=True)

    # Create __init__.py
    with open('refine/__init__.py', 'w') as f:
        f.write('''"""txtRefine - Intelligent Text Refinement Package

This package provides intelligent refinement of philosophy lecture transcriptions.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .text_processing import *
from .model_manager import *
from .file_manager import *

__all__ = [
    'clean_text',
    'split_into_chunks',
    'refine_chunk',
    'process_transcription'
]
''')

    print("✅ Created refine/ package structure")

def create_sample_module():
    """Create a sample module to demonstrate the structure"""
    print("📝 Creating sample text_processing.py module...")

    sample_content = '''"""Text processing functions for txtRefine."""

import re
from typing import List


def clean_text(text: str) -> str:
    """Clean and preprocess text before chunking."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Fix broken words at line breaks
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    # Remove extra newlines but preserve paragraph breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def split_into_chunks(text: str, max_words: int = 800) -> List[str]:
    """Split text into chunks - simple and fast."""
    words = text.split()

    if len(words) <= max_words:
        return [text]

    chunks = []
    for i in range(0, len(words), max_words):
        chunk_words = words[i:i + max_words]
        chunks.append(' '.join(chunk_words))

    return chunks


def detect_content_type(text: str) -> str:
    """Detect content type from text."""
    # All texts are philosophical for this program
    return "philosophy"
'''

    with open('refine/text_processing.py', 'w') as f:
        f.write(sample_content)

    print("✅ Created sample text_processing.py module")

def main():
    """Main function to run the modularization assistant"""
    print("🚀 txtRefine Modularization Assistant")
    print("=" * 50)

    # Analyze current structure
    functions, classes, imports = analyze_current_structure()

    # Categorize functions
    categories = categorize_functions(functions)

    print(f"\n📈 Function Categories:")
    for category, funcs in categories.items():
        if funcs:
            print(f"   {category}: {len(funcs)} functions")
            for func in funcs:
                print(f"      - {func}")

    # Generate structure
    structure = generate_module_structure()

    print(f"\n🏗️  Proposed Module Structure:")
    for dir_path, files in structure.items():
        print(f"   {dir_path}")
        for file_path, description in files.items():
            print(f"      {file_path} - {description}")

    # Ask user if they want to proceed
    response = input(f"\n🤔 Create directory structure? (y/n): ").strip().lower()

    if response in ['y', 'yes']:
        create_directory_structure()
        create_sample_module()
        print(f"\n🎉 Modularization structure created!")
        print(f"   Next steps:")
        print(f"   1. Move functions from refine.py to appropriate modules")
        print(f"   2. Update imports in main script")
        print(f"   3. Test functionality")
    else:
        print("❌ Operation cancelled. Run again when ready.")

if __name__ == '__main__':
    main()
