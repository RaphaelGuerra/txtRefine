import unittest
from unittest.mock import patch

from refine.ollama_integration import SYSTEM_PROMPT, build_refinement_prompt, single_pass_refine
from refine.utils import get_global_cache


class TestOllamaIntegration(unittest.TestCase):
    def setUp(self):
        get_global_cache().clear_cache()

    @patch("refine.ollama_integration.ollama")
    def test_prompt_targets_readable_transcript_cleanup(self, mock_ollama):
        mock_ollama.chat.return_value = {
            "message": {
                "content": "Texto revisado com pontuação."
            }
        }

        single_pass_refine("texto bruto", model="llama3.2:latest")

        call = mock_ollama.chat.call_args
        self.assertIn("readable transcript", call.kwargs["messages"][1]["content"])
        self.assertIn("voice memos", SYSTEM_PROMPT)

    @patch("refine.ollama_integration.ollama")
    def test_fallback_returns_deterministic_cleanup_on_failure(self, mock_ollama):
        mock_ollama.chat.side_effect = RuntimeError("offline")

        refined = single_pass_refine("vamos abrir no microsof teams", model="llama3.2:latest")

        self.assertEqual(refined, "vamos abrir no Microsoft Teams")

    @patch("refine.ollama_integration.ollama")
    def test_content_loss_guard_keeps_deterministic_text(self, mock_ollama):
        mock_ollama.chat.return_value = {
            "message": {
                "content": "Resumo curto"
            }
        }

        refined = single_pass_refine(
            "Essa é uma transcrição longa o suficiente para validar a proteção contra perda de conteúdo.",
            model="llama3.2:latest",
        )

        self.assertEqual(
            refined,
            "Essa é uma transcrição longa o suficiente para validar a proteção contra perda de conteúdo.",
        )

    def test_build_refinement_prompt_mentions_rules(self):
        prompt = build_refinement_prompt("texto")
        self.assertIn("Do not summarize", prompt)
        self.assertIn("cleaned transcript", prompt)


if __name__ == "__main__":
    unittest.main()
