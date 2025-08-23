#!/usr/bin/env python3
"""
txtRefine - Interactive Transcription Refinement

A modularized tool for refining philosophy lecture transcriptions.
Specialized for Brazilian Portuguese content with English UI.

Usage:
    python txtrefine.py              # Interactive mode
    python txtrefine.py --input file.txt --output refined.txt  # Direct processing
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Import from our modularized packages
from refine import (
    # Text processing
    clean_text,
    split_into_chunks,
    merge_chunks,
    calculate_word_count,
    validate_text,

    # Model management
    check_ollama_installation,
    list_available_models,
    refine_chunk,
    validate_model,

    # File management
    read_text_file,
    write_text_file,
    generate_output_filename,
    ensure_directories,
    get_file_info,

    # UI functions
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
    confirm_action,
    get_user_input
)

# Configuration constants
DEFAULT_MODEL = "llama3.2:latest"
DEFAULT_ENCODING = "utf-8"


def process_file(input_path: str, output_path: str, model_name: str) -> bool:
    """Process a single file with the specified model."""
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
        if not validate_text(original_text):
            print("❌ Text too short or invalid")
            return False

        print("📚 Processing as philosophical text")

        # Clean and prepare text
        cleaned_text = clean_text(original_text)

        # Split into chunks
        chunks = split_into_chunks(cleaned_text)
        print(f"📝 Divided into {len(chunks)} chunks for processing")

        # Process chunks
        refined_chunks = []
        for i, chunk in enumerate(chunks, 1):
            print(f"   Processing chunk {i}/{len(chunks)}...")
            refined_chunk = refine_chunk(chunk, model_name, i, len(chunks))
            refined_chunks.append(refined_chunk)

        # Combine refined chunks
        refined_text = merge_chunks(refined_chunks)

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
        original_words = calculate_word_count(original_text)
        refined_words = calculate_word_count(refined_text)

        print("\n✅ Refinement completed!")
        print("📊 Statistics:")
        print(f"   Original words: {original_words:,}")
        print(f"   Refined words: {refined_words:,}")
        print(f"   Difference: {refined_words - original_words:+,}")
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
        if not check_ollama_installation():
            show_error_message("Ollama not available")
            print("💡 Install with: pip install ollama")
            print("💡 Make sure Ollama service is running")
            return

        # Get available models
        models = list_available_models()
        if not models:
            show_error_message("No models found")
            print("💡 Install models with: ollama pull llama3.2:latest")
            return

        # Select model
        print("🎯 Step 1: Choose model")
        selected_model = show_models_menu(models)
        print(f"✅ Selected model: {selected_model}\n")

        # Select files
        print("🎯 Step 2: Choose files")
        from refine import list_input_files
        available_files = list_input_files()
        selected_files = show_files_menu(available_files)

        if not selected_files:
            show_error_message("No files selected")
            input("Press Enter to exit...")
            return

        print(f"✅ Selected file(s): {', '.join(selected_files)}\n")

        # Select processing option
        print("🎯 Step 3: Choose action")
        option = show_options_menu()

        if option == 1:
            # Process files
            show_processing_start(selected_model, selected_files)

            # Ensure output directory exists
            ensure_directories("output")

            successful = 0
            failed = 0

            for i, file in enumerate(selected_files, 1):
                show_file_processing(file, i, len(selected_files))

                input_path = os.path.join("input", file)
                output_filename = generate_output_filename(file)
                output_path = os.path.join("output", output_filename)

                try:
                    if process_file(input_path, output_path, selected_model):
                        show_processing_complete(file)
                        successful += 1
                    else:
                        show_processing_error(file, "Processing failed")
                        failed += 1

                except Exception as e:
                    show_processing_error(file, str(e))
                    failed += 1

            # Summary
            show_processing_summary(successful, failed, len(selected_files))

            if successful > 0:
                output_files = [generate_output_filename(f) for f in selected_files if f not in [f for i, f in enumerate(selected_files) if i < successful]]
                show_success_message(output_files)

        elif option == 2:
            print("🔍 Model Comparison - Feature coming soon")
            input("Press Enter to continue...")

        elif option == 3:
            show_file_stats(selected_files)
            continue

        elif option == 4:
            print("⚙️ Advanced settings - Feature coming soon")
            input("Press Enter to continue...")
            continue

        # Ask if user wants to process more files
        print("\n" + "=" * 60)
        print("✨ Process more files? [y/n]: ", end="")
        continue_choice = input().strip().lower()

        if continue_choice not in ['s', 'sim', 'y', 'yes']:
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

        args = parser.parse_args()

        if args.list_models:
            models = list_available_models()
            if models:
                print("Available models:")
                for model in models:
                    print(f"  - {model['name']} ({model['size']})")
            else:
                print("No models found. Make sure Ollama is running.")
            return

        if args.input and args.output:
            if not os.path.exists(args.input):
                print(f"❌ Input file not found: {args.input}")
                return

            success = process_file(args.input, args.output, args.model)
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
