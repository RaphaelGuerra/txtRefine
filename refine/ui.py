"""Simplified UI functions for transcript refinement."""

from typing import List


def show_header():
    """Display the program header."""
    print("=" * 60)
    print("🎯 txtRefine - PT-BR Transcript Refinement")
    print("=" * 60)
    print("🇧🇷 Readable cleanup for Brazilian Portuguese voice-memo transcripts")
    print()


def show_error_message(message: str):
    """Show error message."""
    print(f"❌ {message}")


def show_processing_complete(filename: str):
    """Show processing completion."""
    print(f"✅ {filename} processed successfully")


def show_success_message(files: List[str]):
    """Show success message."""
    print(f"\\n🎉 Processing complete! Output files:")
    for file in files:
        print(f"  📁 output/refined_{file}")


def show_exit_message():
    """Show exit message."""
    print("\\n👋 Obrigado por usar txtRefine!")
    print("🇧🇷 Transcrições mais claras, sem perder a voz original")


def show_interrupted_message():
    """Show message when user interrupts the program."""
    print("\\n\\n⚠️  Operation interrupted by user (Ctrl+C)")
    print("👋 Obrigado por usar txtRefine!")
    print("🇧🇷 Até a próxima!")


def get_user_input(prompt: str) -> str:
    """Get user input."""
    return input(prompt).strip()
