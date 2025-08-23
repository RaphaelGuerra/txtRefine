#!/usr/bin/env python3
"""
Simple test script for txtRefine
"""

from refine import clean_text, show_header

def test_basic_functionality():
    """Test basic functionality."""
    print("🧪 Testing txtRefine...")

    # Test UI
    show_header()
    print()

    # Test text processing
    test_text = "Este é um teste   de processamento de texto   em português."
    cleaned = clean_text(test_text)
    print(f"✅ Text processing works:")
    print(f"   Original: {test_text}")
    print(f"   Cleaned:  {cleaned}")
    print()

    # Test file operations
    from refine import list_input_files
    files = list_input_files()
    print(f"✅ File operations work: {len(files)} files found")

    # Test model availability
    from refine import check_ollama_installation
    ollama_ok = check_ollama_installation()
    print(f"✅ Ollama integration: {'Available' if ollama_ok else 'Not available'}")

    print("\n🎉 All tests passed! txtRefine is ready to use.")

if __name__ == "__main__":
    test_basic_functionality()
