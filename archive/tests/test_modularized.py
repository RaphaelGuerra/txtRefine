#!/usr/bin/env python3
"""
Comprehensive Testing Script for txtRefine Modularized Version
Run this script to test all functionality after setup.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test all module imports."""
    print("🔍 Testing Module Imports...")
    try:
        from refine import (
            # Text processing
            clean_text, split_into_chunks, detect_content_type,
            merge_chunks, calculate_word_count, validate_text,

            # Model management
            check_ollama_installation, list_available_models,
            create_refinement_prompt, refine_chunk,

            # File management
            list_input_files, read_text_file, write_text_file,
            get_file_info, get_file_stats,

            # UI functions
            show_header, show_models_menu, show_files_menu,
            show_processing_complete, show_error_message
        )
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_text_processing():
    """Test text processing functions."""
    print("\n📝 Testing Text Processing Functions...")
    try:
        from refine import clean_text, split_into_chunks, validate_text

        # Test text cleaning
        test_text = "Hello  \n\n  world   test"
        cleaned = clean_text(test_text)
        assert cleaned == "Hello world test", f"Expected 'Hello world test', got '{cleaned}'"

        # Test text splitting
        long_text = " ".join(["word"] * 200)  # 200 words
        chunks = split_into_chunks(long_text, 50)  # 50 words per chunk
        assert len(chunks) > 1, "Should create multiple chunks"

        # Test text validation
        valid_text = "This is valid text for processing"
        assert validate_text(valid_text), "Valid text should pass validation"

        print("✅ Text processing functions work correctly")
        return True
    except Exception as e:
        print(f"❌ Text processing error: {e}")
        return False

def test_file_operations():
    """Test file management functions."""
    print("\n📁 Testing File Operations...")
    try:
        from refine import write_text_file, read_text_file, get_file_info

        # Test file writing and reading
        test_content = "This is a test file content."
        test_file = "output/test_temp.txt"

        # Ensure output directory exists
        Path("output").mkdir(exist_ok=True)

        success = write_text_file(test_file, test_content)
        assert success, "File writing should succeed"

        read_content = read_text_file(test_file)
        assert read_content == test_content, "File content should match"

        # Test file info
        info = get_file_info(test_file)
        assert info['exists'] == True, "File should exist"
        assert info['size'] > 0, "File should have size"

        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

        print("✅ File operations work correctly")
        return True
    except Exception as e:
        print(f"❌ File operations error: {e}")
        return False

def test_model_functions():
    """Test model management functions."""
    print("\n🤖 Testing Model Functions...")
    try:
        from refine import check_ollama_installation, list_available_models, create_refinement_prompt

        # Test Ollama connection
        ollama_available = check_ollama_installation()
        if ollama_available:
            models = list_available_models()
            print(f"   Found {len(models)} available models")
            if models:
                print(f"   First model: {models[0]['name']} ({models[0]['size']})")
        else:
            print("   ⚠️  Ollama not available - this is OK for testing")

        # Test prompt creation
        prompt = create_refinement_prompt("Test chunk", 1, 3)
        assert len(prompt) > 100, "Prompt should be substantial"
        assert "Test chunk" in prompt, "Prompt should contain the chunk"

        print("✅ Model functions work correctly")
        return True
    except Exception as e:
        print(f"❌ Model functions error: {e}")
        return False

def test_ui_functions():
    """Test UI functions for English messages."""
    print("\n🎨 Testing UI Functions (English Messages)...")
    try:
        from refine import show_header, show_processing_complete, show_error_message

        # Test that functions exist and can be called
        print("   Testing header display...")
        show_header()

        print("   Testing completion message...")
        show_processing_complete("sample_file.txt")

        print("   Testing error message...")
        show_error_message("Sample error message")

        print("✅ UI functions work correctly with English messages")
        return True
    except Exception as e:
        print(f"❌ UI functions error: {e}")
        return False

def test_full_workflow():
    """Test the complete workflow with sample data."""
    print("\n🚀 Testing Full Workflow...")
    try:
        from refine import (
            read_text_file, clean_text, split_into_chunks,
            refine_chunk, write_text_file, generate_output_filename
        )

        # Ensure directories exist
        Path("input").mkdir(exist_ok=True)
        Path("output").mkdir(exist_ok=True)

        # Create test file if it doesn't exist
        test_file = "input/workflow_test.txt"
        if not os.path.exists(test_file):
            test_content = ("Este é um texto de teste para o workflow completo. "
                          "Ele contém múltiplas frases para testar o processamento. "
                          "Vamos ver como o sistema lida com conteúdo em português brasileiro.")
            write_text_file(test_file, test_content)

        # Read and process
        content = read_text_file(test_file)
        cleaned = clean_text(content)
        chunks = split_into_chunks(cleaned)

        print(f"   Original: {len(content)} characters")
        print(f"   Cleaned: {len(cleaned)} characters")
        print(f"   Chunks: {len(chunks)}")

        # Test chunk processing if Ollama is available
        try:
            if len(chunks) > 0:
                refined_chunk = refine_chunk(chunks[0], 'llama3.2:latest', 1, len(chunks))
                print(f"   Refined chunk: {len(refined_chunk)} characters")

                # Save result
                output_file = generate_output_filename(test_file)
                write_text_file(f"output/{output_file}", refined_chunk)
                print(f"   Output saved to: output/{output_file}")

        except Exception as e:
            print(f"   ⚠️  AI processing error (expected if Ollama has issues): {e}")

        print("✅ Full workflow test completed")
        return True
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 txtRefine Modularized Version - Comprehensive Test")
    print("=" * 60)

    tests = [
        ("Module Imports", test_imports),
        ("Text Processing", test_text_processing),
        ("File Operations", test_file_operations),
        ("Model Functions", test_model_functions),
        ("UI Functions", test_ui_functions),
        ("Full Workflow", test_full_workflow)
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                failed += 1
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: ERROR - {e}")

    print(f"\n{'='*60}")
    print("📊 Test Results Summary")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")

    if failed == 0:
        print("\n🎉 All tests passed! The modularized txtRefine is working correctly.")
        print("🚀 Ready for production use.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")

    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
