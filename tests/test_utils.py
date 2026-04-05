import unittest

from refine.utils import clean_text, remove_noise_markers, remove_timestamps


class TestUtils(unittest.TestCase):
    def test_remove_timestamps(self):
        raw = "00:01 Bom dia\n[01:23] tudo bem\n02:34:56 teste"
        self.assertEqual(remove_timestamps(raw), "Bom dia\ntudo bem\nteste")

    def test_remove_noise_markers(self):
        raw = "[Música] Olá (risos) mundo [aplausos]"
        self.assertEqual(remove_noise_markers(raw), "Olá mundo")

    def test_clean_text_normalizes_spacing_and_punctuation(self):
        raw = "Olá  ,   mundo !\n\n\nLinha   dois  ."
        self.assertEqual(clean_text(raw), "Olá, mundo!\n\nLinha dois.")

    def test_clean_text_preserves_paragraphs(self):
        raw = "Primeiro bloco.\n\nSegundo bloco."
        self.assertEqual(clean_text(raw), "Primeiro bloco.\n\nSegundo bloco.")


if __name__ == "__main__":
    unittest.main()
