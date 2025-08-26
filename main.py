#!/usr/bin/env python3
"""
txtRefine - Interactive Transcription Refinement

A modularized tool for refining philosophy lecture transcriptions.
Specialized for Brazilian Portuguese content with English UI.

Usage:
    python main.py              # Interactive mode
    python main.py --input file.txt --output refined.txt  # Direct processing
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Import from our optimized modules
from refine import (
    # Utility functions (merged text + file processing)
    clean_text, split_into_chunks, merge_chunks, word_count, is_valid_text,
    list_input_files, read_text_file, write_text_file, generate_output_filename, ensure_directories,
    # Ollama integration (simplified)
    check_ollama, get_available_models, refine_text, validate_model,
    refine_text_with_paragraphs,
    # Core BP functionality
    BPPhilosophySystem,
    # Minimal UI
    show_header, show_error_message, show_processing_complete, show_success_message, show_exit_message, show_interrupted_message, get_user_input
)

# Configuration constants
DEFAULT_MODEL = "llama3.2:latest"
DEFAULT_ENCODING = "utf-8"


def process_file(input_path: str, output_path: str, model_name: str, use_paragraphs: bool = True, chunk_size: int = 800) -> bool:
    """Process a single file with the specified model and processing method."""
    try:
        # Validate input file
        if not os.path.exists(input_path):
            show_error_message(f"Input file not found: {input_path}")
            return False

        # Read input file
        print(f"📖 Processing: {os.path.basename(input_path)}")
        original_text = read_text_file(input_path, DEFAULT_ENCODING)

        if not original_text or not original_text.strip():
            print("❌ Empty file")
            return False

        # Validate text content
        if not is_valid_text(original_text):
            print("❌ Text too short or invalid")
            return False

        print("📚 Processing as BP philosophical text")

        # Clean and prepare text
        cleaned_text = clean_text(original_text)

        # Choose processing method
        if use_paragraphs:
            print(f"   🧠 Using hybrid paragraph-aware processing ({chunk_size} words/chunk)")
            from refine.ollama_integration import refine_text_with_paragraphs
            refined_text = refine_text_with_paragraphs(cleaned_text, model_name, chunk_size)
        else:
            print("   📝 Using traditional word-based processing")
            from refine.ollama_integration import refine_text
            refined_text = refine_text(cleaned_text, model_name)

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            ensure_directories(output_dir)

        # Write output file
        success = write_text_file(output_path, refined_text, DEFAULT_ENCODING)
        if not success:
            print(f"❌ Failed to save file: {output_path}")
            return False

        # Statistics
        original_words = word_count(original_text)
        refined_words = word_count(refined_text)

        print("\n✅ Refinement completed!")
        print("📊 Statistics:")
        print(f"   Original words: {original_words}")
        print(f"   Refined words: {refined_words}")
        print(f"   Difference: {refined_words - original_words:+}")
        print(f"📁 Saved to: {output_path}")

        return True

    except Exception as e:
        show_error_message(f"Processing error: {e}")
        return False


def interactive_mode():
    """Run in interactive mode."""
    while True:
        show_header()

        # Check if Ollama is available
        if not check_ollama():
            show_error_message("Ollama not available")
            print("💡 Install with: pip install ollama")
            print("💡 Make sure Ollama service is running")
            return

        # Get available models
        models = get_available_models()
        if not models:
            show_error_message("No models found")
            print("💡 Install models with: ollama pull llama3.2:latest")
            return

        # Select model
        print("🤖 Available Models:")
        print("-" * 40)
        for i, model in enumerate(models, 1):
            marker = "⭐" if model == 'llama3.2:latest' else "  "
            print(f"{marker} {i}. {model}")
        print()
        print("⭐ = Recommended for BP philosophy")
        print()

        choice = get_user_input("Choose model (number) or Enter for default [1]: ").strip()
        if not choice:
            selected_model = 'llama3.2:latest'
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(models):
                    selected_model = models[index]
                else:
                    selected_model = 'llama3.2:latest'
            except ValueError:
                selected_model = 'llama3.2:latest'

        print(f"✅ Selected model: {selected_model}\n")

        # Select files
        print("🎯 Step 2: Choose files")
        available_files = list_input_files()

        if not available_files:
            print("❌ No .txt files found in input/")
            return

        for i, file in enumerate(available_files, 1):
            print(f"  {i}. {file}")

        print()
        choice = get_user_input("Choose file (number): ").strip()

        try:
            index = int(choice) - 1
            if 0 <= index < len(available_files):
                selected_files = [available_files[index]]
            else:
                show_error_message("Invalid choice")
                return
        except ValueError:
            show_error_message("Invalid choice")
            return

        print(f"✅ Selected file: {selected_files[0]}\n")

        # Process the file directly
        print("🎯 Processing file...")

        # Ensure output directory exists
        ensure_directories("output")

        file = selected_files[0]
        input_path = os.path.join("input", file)
        output_filename = generate_output_filename(file)
        output_path = os.path.join("output", output_filename)

        try:
            if process_file(input_path, output_path, selected_model, use_paragraphs=True, chunk_size=800):
                show_processing_complete(file)
                show_success_message([file])
            else:
                show_error_message("Processing failed")
        except Exception as e:
            show_error_message(str(e))

        # Ask if user wants to process more files
        print("\n" + "=" * 60)
        choice = get_user_input("✨ Process another file? [y/N]: ").strip().lower()

        if choice not in ['y', 'yes', 's', 'sim']:
            show_exit_message()
            break

        print()


def main():
    """Main function with command-line argument support."""
    if len(sys.argv) > 1:
        # Command-line mode
        import argparse

        parser = argparse.ArgumentParser(description='txtRefine - Transcription Refinement')
        parser.add_argument('--input', '-i', help='Input file path')
        parser.add_argument('--output', '-o', help='Output file path')
        parser.add_argument('--model', '-m', default=DEFAULT_MODEL, help='Model to use')
        parser.add_argument('--list-models', action='store_true', help='List available models')
        parser.add_argument('--no-paragraphs', action='store_true', help='Use traditional word-based processing instead of paragraph-aware')
        parser.add_argument('--chunk-size', type=int, default=800, help='Maximum words per chunk (default: 800, recommended: 600-1000)')

        args = parser.parse_args()

        if args.list_models:
            models = get_available_models()
            if models:
                print("Available models:")
                for model in models:
                    print(f"  - {model}")
            else:
                print("No models found. Make sure Ollama is running.")
            return

        if args.input and args.output:
            if not os.path.exists(args.input):
                print(f"❌ Input file not found: {args.input}")
                return

            # Determine processing method
            use_paragraphs = not args.no_paragraphs
            chunk_size = args.chunk_size

            if use_paragraphs:
                print(f"🧠 Using hybrid paragraph-aware processing (chunk size: {chunk_size} words)")
            else:
                print("📝 Using traditional word-based processing")

            success = process_file(args.input, args.output, args.model, use_paragraphs, chunk_size)
            if success:
                print(f"\n✅ Successfully processed {args.input} → {args.output}")
            else:
                print(f"\n❌ Failed to process {args.input}")
        else:
            print("❌ Please specify both --input and --output files")
            parser.print_help()
    else:
        # Interactive mode
        interactive_mode()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        show_interrupted_message()
    except Exception as e:
        show_error_message(str(e))
        print("💡 Try again or report the issue")
