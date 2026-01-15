import unittest

from refine.term_matching import find_best_match, normalize_text


class TestTermMatching(unittest.TestCase):
    def test_normalize_text(self):
        self.assertEqual(normalize_text("Árvore São"), "arvore sao")

    def test_find_best_match_exact(self):
        result = find_best_match("Aristóteles", "philosophers_ancient_medieval")
        self.assertEqual(result, "aristoteles")

    def test_find_best_match_fuzzy(self):
        result = find_best_match("aristotels", "philosophers_ancient_medieval", cutoff=0.7)
        self.assertEqual(result, "aristoteles")

    def test_find_best_match_invalid_category(self):
        result = find_best_match("Aristóteles", "unknown")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
