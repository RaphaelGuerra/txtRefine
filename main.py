#!/usr/bin/env python3
"""
txtRefine - Interactive Transcript Refinement

A modularized tool for turning raw voice-memo transcripts into readable text.
Specialized for Brazilian Portuguese content with English UI.

Usage:
    python main.py              # Interactive mode
    python main.py --input file.txt --output refined.txt  # Direct processing
"""

import sys
import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from typing import List, Dict, Any, Optional
import time

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Import from our optimized modules
from refine import (
    # Utility functions
    clean_text, word_count, is_valid_text,
    list_input_files, read_text_file, write_text_file, generate_output_filename, ensure_directories,
    # Ollama integration
    get_available_models, get_ollama_status, DETERMINISTIC_ONLY_MODEL, refine_text, validate_model,
    # Minimal UI
    show_header, show_error_message, show_processing_complete, show_success_message, show_exit_message, show_interrupted_message, get_user_input
)

# Configuration constants
DEFAULT_MODEL = "llama3.2:latest"
DEFAULT_ENCODING = "utf-8"


def _parse_bool(value: Any) -> Optional[bool]:
    """Parse loose boolean values from config/env."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    return None


def load_runtime_config() -> Dict[str, Any]:
    """Load config from disk and environment variables."""
    config: Dict[str, Any] = {}
    env_config_path = os.getenv("TXTREFINE_CONFIG")
    config_paths = []
    if env_config_path:
        config_paths.append(Path(env_config_path).expanduser())
    config_paths.extend([
        Path.cwd() / "txtrefine.json",
        Path.home() / ".config" / "txtrefine" / "config.json",
    ])

    for path in config_paths:
        if path.is_file():
            try:
                with path.open("r", encoding="utf-8") as handle:
                    data = json.load(handle)
                if isinstance(data, dict):
                    config.update(data)
                else:
                    print(f"⚠️  Ignoring config file (expected JSON object): {path}")
            except Exception as exc:
                print(f"⚠️  Failed to load config {path}: {exc}")
            break

    env_model = os.getenv("TXTREFINE_MODEL")
    if env_model:
        config["model"] = env_model

    env_no_streaming = os.getenv("TXTREFINE_NO_STREAMING")
    parsed_no_streaming = _parse_bool(env_no_streaming)
    if parsed_no_streaming is not None:
        config["no_streaming"] = parsed_no_streaming

    env_max_workers = os.getenv("TXTREFINE_MAX_WORKERS")
    if env_max_workers:
        try:
            config["max_workers"] = int(env_max_workers)
        except ValueError:
            print("⚠️  TXTREFINE_MAX_WORKERS must be an integer.")

    env_input = os.getenv("TXTREFINE_INPUT")
    if env_input:
        config["input"] = env_input

    env_output = os.getenv("TXTREFINE_OUTPUT")
    if env_output:
        config["output"] = env_output

    return config


def describe_ollama_status() -> Dict[str, Any]:
    """Print a friendly status message and return Ollama availability details."""
    status = get_ollama_status()
    if status["server_reachable"]:
        return status

    if not status["python_package_installed"]:
        print("⚠️  Ollama Python package not installed in this interpreter")
        print("💡 Recommended: run `./txtrefine` to auto-bootstrap `.venv`")
        print("💡 Manual setup: python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -r requirements.txt")
    else:
        print("⚠️  Ollama app/server not reachable from the project")
        print("💡 If the Ollama app is open, wait a few seconds and try again")
        print("💡 You can still continue in deterministic-only mode")

    return status


def process_file(input_path: str, output_path: str, model_name: str, **kwargs) -> bool:
    """Process a single file with the specified model using single-pass refinement."""
    from refine.utils import get_performance_monitor, get_streaming_processor
    monitor = get_performance_monitor()
    streaming_processor = get_streaming_processor()

    file_start_time = time.time()
    used_streaming = False
    used_cache = False

    try:
        # Validate input file
        if not os.path.exists(input_path):
            show_error_message(f"Input file not found: {input_path}")
            monitor.record_error()
            return False

        # Read input file
        print(f"📖 Processing: {os.path.basename(input_path)}")

        # Check if file should use streaming (unless disabled)
        no_streaming = kwargs.get('no_streaming', False)
        if not no_streaming and streaming_processor.should_use_streaming(input_path):
            original_text = streaming_processor.process_large_file(input_path, model_name)
            used_streaming = True
        else:
            original_text = read_text_file(input_path, DEFAULT_ENCODING)

        if not original_text or not original_text.strip():
            print("❌ Empty file")
            return False

        # Validate text content
        if not is_valid_text(original_text):
            print("❌ Text too short or invalid")
            return False

        print("📚 Processing as readable PT-BR transcript")

        # Clean and prepare text
        cleaned_text = clean_text(original_text)

        # Single-pass refinement
        print("   📝 Using single-pass readable transcript refinement")
        from refine.ollama_integration import single_pass_refine as single_refine

        # Check if we have cached LLM response
        from refine.utils import get_global_cache
        cache = get_global_cache()
        if cache.get_llm_response(cleaned_text, model_name):
            used_cache = True

        refined_text = single_refine(cleaned_text, model_name)

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            ensure_directories(output_dir)

        # Write output file
        success = write_text_file(output_path, refined_text, DEFAULT_ENCODING)
        if not success:
            print(f"❌ Failed to save file: {output_path}")
            monitor.record_error()
            return False

        # Statistics and performance monitoring
        original_words = word_count(original_text)
        refined_words = word_count(refined_text)
        file_size = len(original_text)
        processing_time = time.time() - file_start_time

        # Record performance metrics
        monitor.record_file_processing(
            file_size=file_size,
            word_count=original_words,
            processing_time=processing_time,
            used_streaming=used_streaming,
            used_cache=used_cache
        )

        print("\n✅ Refinement completed!")
        print("📊 Statistics:")
        print(f"   Original words: {original_words}")
        print(f"   Refined words: {refined_words}")
        print(f"   Difference: {refined_words - original_words:+}")
        print(f"   Processing time: {processing_time:.2f}s")
        if used_streaming:
            print("   Mode: Streaming")
        if used_cache:
            print("   Cache: Hit")
        print(f"📁 Saved to: {output_path}")

        return True

    except Exception as e:
        show_error_message(f"Processing error: {e}")
        monitor.record_error()
        return False


def process_files_concurrent(input_paths: List[str], output_paths: List[str], model_name: str, max_workers: int = None, no_streaming: bool = False) -> Dict[str, bool]:
    """Process multiple files concurrently with ThreadPoolExecutor."""
    if len(input_paths) != len(output_paths):
        print("❌ Input and output path lists must have the same length")
        return {}

    if max_workers is None:
        max_workers = min(len(input_paths), os.cpu_count() or 4)

    print(f"🚀 Starting concurrent processing with {max_workers} workers")
    print(f"📁 Processing {len(input_paths)} files...")

    results = {}
    start_time = time.time()

    # Create partial function with fixed parameters
    process_func = partial(process_file, model_name=model_name, no_streaming=no_streaming)

    # Create input-output pairs
    file_pairs = list(zip(input_paths, output_paths))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(process_func, input_path, output_path): (input_path, output_path)
            for input_path, output_path in file_pairs
        }

        # Process completed tasks with progress tracking
        completed = 0
        for future in as_completed(future_to_file):
            input_path, output_path = future_to_file[future]
            try:
                success = future.result()
                results[input_path] = success
                completed += 1

                filename = os.path.basename(input_path)
                status = "✅" if success else "❌"
                print(f"   {status} [{completed}/{len(input_paths)}] {filename}")

            except Exception as exc:
                print(f"   ❌ [{completed}/{len(input_paths)}] {os.path.basename(input_path)} - Error: {exc}")
                results[input_path] = False
                completed += 1

    elapsed_time = time.time() - start_time
    successful = sum(1 for result in results.values() if result)

    print("\n🎉 Concurrent processing complete!")
    print(f"⏱️  Total time: {elapsed_time:.2f}s")
    print(f"📊 Success rate: {successful}/{len(input_paths)} files")

    # Show performance summary if we processed multiple files
    from refine.utils import get_performance_monitor
    monitor = get_performance_monitor()
    if len(input_paths) > 1:
        monitor.print_summary()

    return results


def interactive_mode():
    """Run in interactive mode."""
    while True:
        show_header()

        status = describe_ollama_status()
        models = list(status["available_models"])

        if models:
            print("🤖 Available Models:")
            print("-" * 40)
            for i, model in enumerate(models, 1):
                marker = "⭐" if model == DEFAULT_MODEL else "  "
                print(f"{marker} {i}. {model}")
            print()
            print("⭐ = Recommended for PT-BR voice memos")
            print()

            choice = get_user_input("Choose model (number) or Enter for default [1]: ").strip()
            if not choice:
                selected_model = DEFAULT_MODEL
            else:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(models):
                        selected_model = models[index]
                    else:
                        selected_model = DEFAULT_MODEL
                except ValueError:
                    selected_model = DEFAULT_MODEL

            print(f"✅ Selected model: {selected_model}\n")
        else:
            selected_model = DETERMINISTIC_ONLY_MODEL
            print("🤖 Running in deterministic-only mode\n")

        # Select files
        print("🎯 Step 2: Choose files")
        available_files = list_input_files()

        if not available_files:
            print("❌ No .txt files found in input/")
            return

        for i, file in enumerate(available_files, 1):
            print(f"  {i}. {file}")

        print()
        print("💡 You can select multiple files (e.g., '1,3,5' or '1-3')")
        choice = get_user_input("Choose file(s): ").strip()

        selected_files = []
        try:
            if ',' in choice:
                # Multiple files by comma
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                selected_files = [available_files[i] for i in indices if 0 <= i < len(available_files)]
            elif '-' in choice:
                # Range of files
                start, end = [int(x.strip()) - 1 for x in choice.split('-')]
                selected_files = [available_files[i] for i in range(start, end + 1) if 0 <= i < len(available_files)]
            else:
                # Single file
                index = int(choice) - 1
                if 0 <= index < len(available_files):
                    selected_files = [available_files[index]]

            if not selected_files:
                show_error_message("No valid files selected")
                return

        except ValueError:
            show_error_message("Invalid choice format")
            return

        if len(selected_files) == 1:
            print(f"✅ Selected file: {selected_files[0]}\n")
        else:
            print(f"✅ Selected {len(selected_files)} files:")
            for file in selected_files:
                print(f"   📄 {file}")
            print()

        # Process files (concurrent if multiple, sequential if single)
        print("🎯 Processing files...")

        # Ensure output directory exists
        ensure_directories("output")

        # Prepare input and output paths
        input_paths = [os.path.join("input", file) for file in selected_files]
        output_paths = [os.path.join("output", generate_output_filename(file)) for file in selected_files]

        try:
            if len(selected_files) == 1:
                # Single file - use original method
                if process_file(input_paths[0], output_paths[0], selected_model):
                    show_processing_complete(selected_files[0])
                    show_success_message(selected_files)
                else:
                    show_error_message("Processing failed")
            else:
                # Multiple files - use concurrent processing
                results = process_files_concurrent(input_paths, output_paths, selected_model, no_streaming=False)

                successful_files = [file for file, success in zip(selected_files, results.values()) if success]
                if successful_files:
                    show_success_message(successful_files)

                failed_count = len(selected_files) - len(successful_files)
                if failed_count > 0:
                    print(f"⚠️  {failed_count} file(s) failed to process")

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
        parser.add_argument('--model', '-m', default=None, help='Model to use')
        parser.add_argument('--list-models', action='store_true', help='List available models')
        parser.add_argument('--process-all', action='store_true', help='Process all files in input directory concurrently')
        parser.add_argument('--max-workers', type=int, default=None, help='Maximum number of concurrent workers (default: CPU count)')
        parser.add_argument('--clear-cache', action='store_true', help='Clear all cached data')
        parser.add_argument('--cache-stats', action='store_true', help='Show cache statistics')
        parser.add_argument('--no-streaming', action='store_true', default=None, help='Disable streaming for large files')
        # Removed chunking options for simplified single-pass processing

        args = parser.parse_args()
        runtime_config = load_runtime_config()

        if args.model is None:
            config_model = runtime_config.get("model")
            args.model = config_model if isinstance(config_model, str) and config_model else DEFAULT_MODEL

        if args.input is None:
            args.input = runtime_config.get("input")
        if args.output is None:
            args.output = runtime_config.get("output")

        if args.max_workers is None and runtime_config.get("max_workers") is not None:
            args.max_workers = runtime_config.get("max_workers")

        if args.no_streaming is None:
            config_no_streaming = _parse_bool(runtime_config.get("no_streaming"))
            args.no_streaming = config_no_streaming if config_no_streaming is not None else False

        if args.list_models:
            status = describe_ollama_status()
            if not status["server_reachable"]:
                return
            models = get_available_models()
            if models:
                print("Available models:")
                for model in models:
                    print(f"  - {model}")
            else:
                print("No models found. Install one with: ollama pull llama3.2:latest")
            return

        if args.clear_cache:
            from refine.utils import get_global_cache
            cache = get_global_cache()
            cache.clear_cache()
            print("✅ Cache cleared successfully")
            return

        if args.cache_stats:
            from refine.utils import get_global_cache
            cache = get_global_cache()
            stats = cache.get_stats()
            print("📊 Cache Statistics:")
            print(f"   LLM responses cached: {stats['llm_cache_size']}")
            print(f"   Transcript corrections cached: {stats['transcript_cache_size']}")
            print(f"   Total cache entries: {stats['total_cache_entries']}")
            return

        if args.process_all:
            status = describe_ollama_status()
            selected_model = args.model if status["server_reachable"] else DETERMINISTIC_ONLY_MODEL
            # Process all files in input directory concurrently
            available_files = list_input_files()
            if not available_files:
                print("❌ No .txt files found in input/")
                return

            print(f"🚀 Processing all {len(available_files)} files concurrently")
            print("📝 Using single-pass readable transcript refinement")

            # Prepare input and output paths
            input_paths = [os.path.join("input", file) for file in available_files]
            output_paths = [os.path.join("output", generate_output_filename(file)) for file in available_files]

            # Ensure output directory exists
            ensure_directories("output")

            results = process_files_concurrent(input_paths, output_paths, selected_model, args.max_workers, args.no_streaming)

            successful = sum(1 for result in results.values() if result)
            print(f"\n📊 Batch processing complete: {successful}/{len(available_files)} files successful")

        elif args.input and args.output:
            status = describe_ollama_status()
            if not os.path.exists(args.input):
                print(f"❌ Input file not found: {args.input}")
                return

            print("📝 Using single-pass readable transcript refinement")
            selected_model = args.model if status["server_reachable"] else DETERMINISTIC_ONLY_MODEL
            success = process_file(args.input, args.output, selected_model, no_streaming=args.no_streaming)
            if success:
                print(f"\n✅ Successfully processed {args.input} → {args.output}")
            else:
                print(f"\n❌ Failed to process {args.input}")
        else:
            print("❌ Please specify both --input and --output files (or use --process-all)")
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
