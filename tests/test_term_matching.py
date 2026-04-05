import unittest

from refine.term_matching import find_best_match, normalize_text


class TestTermMatching(unittest.TestCase):
    def test_normalize_text(self):
        self.assertEqual(normalize_text("Áudio São"), "audio sao")

    def test_find_best_match_exact(self):
        result = find_best_match("Microsoft Teams", "platform_terms")
        self.assertEqual(result, "microsoft teams")

    def test_find_best_match_fuzzy(self):
        result = find_best_match("microsof teams", "platform_terms", cutoff=0.7)
        self.assertEqual(result, "microsoft teams")

    def test_find_best_match_invalid_category(self):
        result = find_best_match("Microsoft Teams", "unknown")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
