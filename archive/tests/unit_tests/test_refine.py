#!/usr/bin/env python3
"""
Unit tests for txtRefine core functionality.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from refine import (
    clean_text, split_into_chunks, detect_content_type,
    create_refinement_prompt, refine_chunk, refine_transcription
)


class TestTextProcessing(unittest.TestCase):
    """Test text processing functions."""

    def test_clean_text_basic(self):
        """Test basic text cleaning."""
        input_text = "Hello  \n\n\n  world   test"
        expected = "Hello world test"
        self.assertEqual(clean_text(input_text), expected)

    def test_clean_text_hyphenated_words(self):
        """Test hyphenated word fixing."""
        input_text = "escola-\n\nstica filosófica"
        expected = "escolástica filosófica"
        self.assertEqual(clean_text(input_text), expected)

    def test_split_into_chunks_small_text(self):
        """Test chunking small text."""
        text = " ".join(["word"] * 100)  # 100 words
        chunks = split_into_chunks(text, 200)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], text)

    def test_split_into_chunks_large_text(self):
        """Test chunking large text."""
        text = " ".join(["word"] * 1000)  # 1000 words
        chunks = split_into_chunks(text, 400)
        self.assertTrue(len(chunks) > 1)
        # Verify all chunks combined equal original
        reconstructed = " ".join(chunks)
        self.assertEqual(reconstructed, text)

    def test_detect_content_type(self):
        """Test content type detection."""
        text = "A filosofia escolástica é importante"
        self.assertEqual(detect_content_type(text), "philosophy")


class TestPromptGeneration(unittest.TestCase):
    """Test prompt generation functions."""

    def test_create_refinement_prompt(self):
        """Test refinement prompt creation."""
        chunk = "Este é um texto de teste."
        prompt = create_refinement_prompt(chunk, 1, 3)

        self.assertIn("Este é um texto de teste.", prompt)
        self.assertIn("parte 1 de 3", prompt)
        self.assertIn("escolástica", prompt)  # Philosophy-specific content


class TestRefinement(unittest.TestCase):
    """Test refinement functionality."""

    @patch('ollama.generate')
    def test_refine_chunk_success(self, mock_generate):
        """Test successful chunk refinement."""
        mock_response = {'response': 'Texto refinado com sucesso.'}
        mock_generate.return_value = mock_response

        result = refine_chunk("Texto original", "llama3.2:latest", 1, 1)
        self.assertEqual(result, "Texto refinado com sucesso.")

    @patch('ollama.generate')
    def test_refine_chunk_content_loss(self, mock_generate):
        """Test content loss detection."""
        # Very short response compared to input
        mock_response = {'response': 'Sim'}
        mock_generate.return_value = mock_response

        result = refine_chunk("Este é um texto muito longo de teste", "llama3.2:latest", 1, 1)
        # Should return original text due to content loss
        self.assertEqual(result, "Este é um texto muito longo de teste")

    @patch('refine.open', new_callable=mock_open, read_data="Test content")
    @patch('pathlib.Path.mkdir')
    @patch('refine.refine_chunk')
    def test_refine_transcription_success(self, mock_refine, mock_mkdir, mock_file):
        """Test successful transcription refinement."""
        mock_refine.return_value = "Refined content"

        from pathlib import Path
        input_path = Path("input/test.txt")
        output_path = Path("output/refined_test.txt")

        result = refine_transcription(input_path, output_path, "llama3.2:latest")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
