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

    def test_creates_sentences_from_run_on_text(self):
        raw = (
            "hoje eu gravei esse áudio para revisar o projeto com calma mas antes disso "
            "eu queria alinhar os próximos passos depois a gente fecha os prazos"
        )
        corrected, _ = self.system.find_and_correct_terms(raw)
        self.assertIn("Hoje eu gravei esse áudio para revisar o projeto com calma.", corrected)
        self.assertIn("Mas antes disso eu queria alinhar os próximos passos.", corrected)
        self.assertIn("Depois a gente fecha os prazos.", corrected)

    def test_creates_paragraphs_from_long_transcript_block(self):
        raw = (
            "primeiro eu queria explicar o contexto da gravação e o que motivou essa revisão "
            "mas antes disso vale lembrar que a versão anterior estava muito confusa "
            "depois a gente organiza os próximos passos para a equipe "
            "agora eu quero fechar com o que precisa entrar na próxima entrega"
        )
        corrected, _ = self.system.find_and_correct_terms(raw)
        self.assertIn("\n\n", corrected)


if __name__ == "__main__":
    unittest.main()
