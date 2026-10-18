import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestText(unittest.TestCase):
    def test_basics(self) -> None:
        self.assertEqual(ex.code_points("Hi!"), [72, 105, 33])
        self.assertEqual(ex.utf8_bytes("hello"), 5)
        self.assertEqual(ex.utf8_bytes("🙂"), 4)
        self.assertEqual(ex.build_with_plus(25), ex.build_with_join(25))
        rng = random.Random(1)
        for _ in range(200):
            t = "".join(rng.choice("ab") for _ in range(rng.randint(0, 20)))
            p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 3)))
            self.assertEqual(ex.find_all_builtin(t, p), [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p])

    def test_examples(self) -> None:
        self.assertAlmostEqual(ex.gc_content("ATGCGCATTA"), 0.4)
        essay = "the quick brown fox jumps over the lazy dog near the river bank"
        self.assertEqual(ex.similarity(essay, essay), 1.0)
        self.assertLess(ex.similarity(essay, "a completely different sentence about cats and mice"), 0.1)
        self.assertTrue(sol.is_anagram("listen", "silent"))
        self.assertFalse(sol.is_anagram("rat", "car"))
        self.assertEqual(sol.reverse_complement("ATGC"), "GCAT")
        self.assertEqual(sol.most_common_word("Bob hit a ball, the hit BALL flew far after it was hit.", {"hit"}), "ball")


if __name__ == "__main__":
    unittest.main()
