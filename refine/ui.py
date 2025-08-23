"""User interface functions for txtRefine."""

from typing import List, Dict, Any
from pathlib import Path


def show_header():
    """Display the program header."""
    print("=" * 60)
    print("🎯 txtRefine - Interactive Transcription Refinement")
    print("=" * 60)
    print("📚 Specialized in philosophy and academic content")
    print()


def show_models_menu(models: List[Dict[str, Any]]) -> str:
    """Display the models menu and return selected model."""
    print("🤖 Available Models:")
    print("-" * 40)

    # Sort models by recommended order for philosophy
    recommended_order = [
        'llama3.2:latest',  # Default - good balance
        'neural-chat:latest',  # Highest quality
        'openchat:latest',  # High quality
        'dolphin-phi:latest',  # Good balance
        'gemma:2b'  # Fastest
    ]

    # Sort models by recommendation, then alphabetically
    def sort_key(model):
        name = model['name']
        if name in recommended_order:
            return (recommended_order.index(name), name)
        else:
            return (len(recommended_order), name)

    sorted_models = sorted(models, key=sort_key)

    for i, model in enumerate(sorted_models, 1):
        marker = "⭐" if model['name'] == 'llama3.2:latest' else "  "
        print(f"{marker} {i}. {model['name']} ({model['size']})")

    print()
    print("⭐ = Recommended default model")
    print()

    while True:
        try:
            choice = input("Choose a model (number) or press Enter for default [1]: ").strip()

            if not choice:  # Default to llama3.2:latest
                default_model = next((m for m in sorted_models if m['name'] == 'llama3.2:latest'), sorted_models[0])
                return default_model['name']

            choice_num = int(choice)
            if 1 <= choice_num <= len(sorted_models):
                return sorted_models[choice_num - 1]['name']
            else:
                print(f"❌ Choose a number between 1 and {len(sorted_models)}")
        except ValueError:
            print("❌ Enter a valid number")


def show_files_menu(files: List[str]) -> List[str]:
    """Display the files menu and return selected files."""
    if not files:
        print("❌ No .txt files found in 'input' folder")
        print("💡 Place your .txt files in the 'input' folder and try again")
        return []

    print("📁 Available Files:")
    print("-" * 40)

    for i, file in enumerate(files, 1):
        file_path = Path("input") / file
        try:
            size = file_path.stat().st_size
            size_kb = f"{size / 1024:.1f} KB"
        except:
            size_kb = "? KB"

        print(f"   {i}. {file} ({size_kb})")

    print(f"   {len(files) + 1}. All files")
    print()

    while True:
        try:
            choice = input("Choose file(s) (number, list or 'all'): ").strip().lower()

            if choice in ['todos', 'all', str(len(files) + 1)]:
                return files

            if ',' in choice:
                # Multiple files
                choices = [int(x.strip()) for x in choice.split(',')]
                selected_files = []
                for c in choices:
                    if 1 <= c <= len(files):
                        selected_files.append(files[c - 1])
                if selected_files:
                    return selected_files
                else:
                    print("❌ Invalid numbers")
            else:
                # Single file
                choice_num = int(choice)
                if 1 <= choice_num <= len(files):
                    return [files[choice_num - 1]]
                else:
                    print(f"❌ Choose a number between 1 and {len(files) + 1}")
        except ValueError:
            print("❌ Enter a valid number or 'all'")


def show_options_menu() -> int:
    """Display processing options menu."""
    print("⚙️  Processing Options:")
    print("-" * 40)
    print("   1. Process now")
    print("   2. Compare with multiple models")
    print("   3. View file statistics")
    print("   4. Advanced settings")
    print()

    while True:
        try:
            choice = input("Choose an option [1]: ").strip()

            if not choice:
                return 1

            choice_num = int(choice)
            if 1 <= choice_num <= 4:
                return choice_num
            else:
                print("❌ Choose a number between 1 and 4")
        except ValueError:
            print("❌ Enter a valid number")


def show_file_stats(files: List[str]) -> None:
    """Show statistics about the selected files."""
    print("📊 File Statistics:")
    print("-" * 40)

    total_size = 0
    total_words = 0

    for file in files:
        file_path = Path("input") / file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            size = len(content)
            words = len(content.split())
            total_size += size
            total_words += words

            print(f"📄 {file}:")
            print(f"   📏 {size:,} characters")
            print(f"   📝 {words:,} words")
            print(f"   ⏱️  Estimated time: {words // 100:.1f}-{words // 50:.1f} seconds")
            print()

        except Exception as e:
            print(f"❌ Error reading {file}: {e}")

    if len(files) > 1:
        print("📊 Total:")
        print(f"   📏 {total_size:,} characters")
        print(f"   📝 {total_words:,} words")
        print(f"   ⏱️  Total estimated time: {total_words // 100:.1f}-{total_words // 50:.1f} seconds")

    print()
    input("Press Enter to continue...")


def show_processing_start(model_name: str, files: List[str]) -> None:
    """Show processing start message."""
    print(f"🚀 Starting processing with {model_name}")
    print("=" * 60)


def show_file_processing(file: str, current: int, total: int) -> None:
    """Show file processing message."""
    print(f"\n📦 Processing file {current}/{total}: {file}")
    print("-" * 40)


def show_processing_complete(file: str) -> None:
    """Show file processing completion message."""
    print(f"✅ {file} processed successfully!")


def show_processing_error(file: str, error: str) -> None:
    """Show file processing error message."""
    print(f"❌ Failed to process {file}: {error}")


def show_processing_summary(successful: int, failed: int, total_files: int) -> None:
    """Show processing summary."""
    print(f"\n{'='*60}")
    print("📊 PROCESSING SUMMARY")
    print("=" * 60)

    print(f"📁 Total files: {total_files}")
    print(f"✅ Successfully processed: {successful}")
    print(f"❌ Failures: {failed}")


def show_success_message(output_files: List[str]) -> None:
    """Show success message with output files."""
    if output_files:
        print(f"\n✅ Refined files saved in 'output/' folder:")
        for file in output_files:
            print(f"   📄 {file}")


def show_exit_message() -> None:
    """Show program exit message."""
    print("\n🎉 Thank you for using txtRefine!")


def show_interrupted_message() -> None:
    """Show program interrupted message."""
    print("\n\n👋 Program interrupted by user. Goodbye!")


def show_error_message(error: str) -> None:
    """Show general error message."""
    print(f"\n❌ Unexpected error: {error}")
    print("💡 Try again or report the issue")


def show_warning_message(message: str) -> None:
    """Show warning message."""
    print(f"⚠️  {message}")


def show_info_message(message: str) -> None:
    """Show info message."""
    print(f"ℹ️  {message}")


def confirm_action(message: str, default: bool = False) -> bool:
    """Get user confirmation for an action."""
    default_text = "s/n" if not default else "S/n"
    response = input(f"{message} [{default_text}]: ").strip().lower()

    if not response:
        return default

    return response in ['s', 'sim', 'y', 'yes']


def get_user_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default value."""
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    else:
        return input(f"{prompt}: ").strip()


def show_progress(current: int, total: int, prefix: str = "Progresso") -> None:
    """Show progress bar."""
    percentage = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    print(f"\r{prefix}: |{bar}| {percentage:.1f}% ({current}/{total})", end="", flush=True)

    if current == total:
        print()  # New line when complete
