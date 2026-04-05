import unittest

from refine.transcript_refinement import TranscriptRefinementSystem


class TestTranscriptRefinementSystem(unittest.TestCase):
    def setUp(self):
        self.system = TranscriptRefinementSystem()

    def test_common_asr_corrections(self):
        raw = "Vamos revisar no microsof teams e abrir no chat gpt."
        corrected, corrections = self.system.find_and_correct_terms(raw)
        self.assertIn("Microsoft Teams", corrected)
        self.assertIn("ChatGPT", corrected)
        self.assertGreaterEqual(len(corrections), 2)

    def test_duplicate_phrase_cleanup(self):
        raw = "O plano de ação plano de ação ficou melhor."
        corrected, _ = self.system.find_and_correct_terms(raw)
        self.assertEqual(corrected, "O plano de ação ficou melhor.")

    def test_repeated_connector_cleanup(self):
        raw = "Eu acho que que a gente pode seguir."
        corrected, _ = self.system.find_and_correct_terms(raw)
        self.assertEqual(corrected, "Eu acho que a gente pode seguir.")

    def test_conservative_when_no_change_needed(self):
        raw = "A gravação ficou clara e fácil de revisar."
        corrected, corrections = self.system.find_and_correct_terms(raw)
        self.assertEqual(corrected, raw)
        self.assertEqual(corrections, [])


if __name__ == "__main__":
    unittest.main()
