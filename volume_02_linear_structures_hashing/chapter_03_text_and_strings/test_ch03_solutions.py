import itertools
import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_distinct_letters_never_overlap(self) -> None:
        rng = random.Random(3)
        for _ in range(300):
            word = "".join(rng.sample("abcd", rng.randint(1, 4)))
            text = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 15)))
            starts = ex.find_all(text, word)
            for a, b in zip(starts, starts[1:]):
                self.assertGreaterEqual(b - a, len(word))

    def test_aab_never_overlaps(self) -> None:
        for n in range(9):
            for letters in itertools.product("ab", repeat=n):
                starts = ex.find_all("".join(letters), "aab")
                self.assertTrue(all(b - a >= 3 for a, b in zip(starts, starts[1:])))

    def test_is_subsequence_smallest(self) -> None:
        self.assertTrue(sol.is_subsequence("", ""))
        self.assertTrue(sol.is_subsequence("", "MAP"))
        self.assertFalse(sol.is_subsequence("M", ""))
        self.assertTrue(sol.is_subsequence("M", "M"))

    def test_is_subsequence_examples(self) -> None:
        self.assertTrue(sol.is_subsequence("LIAR", "LIBRARY"))
        self.assertFalse(sol.is_subsequence("RAIL", "LIBRARY"))

    def test_is_subsequence_against_all_subsequences(self) -> None:
        rng = random.Random(30)
        for _ in range(200):
            text = "".join(rng.choice("ab") for _ in range(rng.randint(0, 7)))
            word = "".join(rng.choice("ab") for _ in range(rng.randint(0, 4)))
            self.assertEqual(sol.is_subsequence(word, text), word in ex.subsequences(text))

    def test_skipping_search_is_wrong(self) -> None:
        self.assertEqual(sol.find_all_skipping("CCAR", "CAR"), [])
        self.assertEqual(ex.find_all("CCAR", "CAR"), [1])
        self.assertEqual(sol.find_all_skipping("banana", "ana"), [1])
        self.assertEqual(sol.find_all_skipping("a map of maps", "map"), [2, 9])


if __name__ == "__main__":
    unittest.main()
