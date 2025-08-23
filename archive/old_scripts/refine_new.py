#!/usr/bin/env python3
"""
txtRefine - Refinamento Inteligente de Transcrições (Modularized Version)

This program refines transcriptions of philosophy classes in Brazilian Portuguese.
It provides an interactive menu system for choosing models, files, and options.
"""

import sys
import os
from pathlib import Path
from tqdm import tqdm

# Add the refine package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'refine'))

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
    estimate_processing_time,

    # File management
    list_input_files,
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

    # Exceptions
    TxtRefineError,
    FileNotFoundError,
    ModelUnavailableError
)

# Configuration constants (will be moved to config.py later)
DEFAULT_MODEL = "llama3.2:latest"
DEFAULT_ENCODING = "utf-8"


def refine_transcription(input_path: str, output_path: str, model_name: str) -> bool:
    """Main function to refine a transcription file using modularized functions."""
    try:
        # Validate input file
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

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

        # Process chunks with progress bar
        refined_chunks = []
        with tqdm(total=len(chunks), desc="Refining chunks", unit="chunk") as pbar:
            for i, chunk in enumerate(chunks, 1):
                refined_chunk = refine_chunk(chunk, model_name, i, len(chunks))
                refined_chunks.append(refined_chunk)
                pbar.update(1)

        # Combine refined chunks
        refined_text = merge_chunks(refined_chunks)

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            ensure_directories(output_dir)

        # Write output file
        success = write_text_file(output_path, refined_text, DEFAULT_ENCODING)
        if not success:
            print(f"❌ Falha ao salvar arquivo: {output_path}")
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

    except FileNotFoundError as e:
        print(f"❌ {e}")
        return False
    except ModelUnavailableError as e:
        print(f"❌ {e}")
        return False
    except TxtRefineError as e:
        print(f"❌ Processing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def process_files(files: list, model_name: str) -> dict:
    """Process the selected files with the selected model."""
    show_processing_start(model_name, files)

    # Ensure output directory exists
    ensure_directories("output")

    results = []

    for i, file in enumerate(files, 1):
        show_file_processing(file, i, len(files))

        input_path = os.path.join("input", file)
        output_filename = generate_output_filename(file)
        output_path = os.path.join("output", output_filename)

        try:
            success = refine_transcription(input_path, output_path, model_name)

            if success:
                show_processing_complete(file)
                results.append({"file": file, "success": True})
            else:
                show_processing_error(file, "Falha no processamento")
                results.append({"file": file, "success": False})

        except Exception as e:
            show_processing_error(file, str(e))
            results.append({"file": file, "success": False, "error": str(e)})

    # Summary
    show_processing_summary(
        sum(1 for r in results if r.get('success')),
        len(results) - sum(1 for r in results if r.get('success')),
        len(files)
    )

    successful_files = [r["file"] for r in results if r.get('success')]
    if successful_files:
        output_files = [generate_output_filename(f) for f in successful_files]
        show_success_message(output_files)

    return results


def main():
    """Main interactive function using modularized components."""
    while True:
        show_header()

        # Check if Ollama is available
        if not check_ollama_installation():
            show_error_message("Ollama não está disponível")
            print("💡 Install with: pip install ollama")
            print("💡 And make sure the Ollama service is running")
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
            process_files(selected_files, selected_model)

        elif option == 2:
            # Compare models (placeholder)
            print("🔍 Model Comparison")
            print("=" * 60)
            print("💡 For detailed comparison, use: python3 compare_models.py")
            input("Press Enter to continue...")

        elif option == 3:
            # Show file statistics
            show_file_stats(selected_files)
            continue

        elif option == 4:
            # Advanced settings (placeholder)
            print("⚙️  Advanced settings (in development)")
            input("Press Enter to continue...")
            continue

        # Ask if user wants to process more files
        print("\n" + "=" * 60)
        print("✨ Process more files? [y/n]: ", end="")
        continue_choice = input().strip().lower()

        if continue_choice not in ['s', 'sim', 'y', 'yes']:
            show_exit_message()
            break

        print()  # Add some space before next iteration


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        show_interrupted_message()
    except Exception as e:
        show_error_message(str(e))
        print("💡 Try again or report the issue")
