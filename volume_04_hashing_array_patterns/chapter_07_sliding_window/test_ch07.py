import random
import unittest
from collections import Counter

import ch07_examples as ex
import ch07_solutions as sol


class TestWindows(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = [rng.randint(1, 9) for _ in range(rng.randint(1, 12))]
            k = rng.randint(1, len(v))
            self.assertEqual(ex.best_k_day_sales(v, k), max(sum(v[i:i + k]) for i in range(len(v) - k + 1)))
            t = rng.randint(1, 40)
            lengths = [j - i + 1 for i in range(len(v)) for j in range(i, len(v)) if sum(v[i:j + 1]) >= t]
            self.assertEqual(ex.shortest_run_reaching(v, t), min(lengths) if lengths else 0)
            s = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 12)))
            self.assertEqual(ex.longest_unique_run(s),
                             max([j - i for i in range(len(s) + 1) for j in range(i, len(s) + 1)
                                  if len(set(s[i:j])) == j - i] + [0]))
            trees = [rng.choice("xyz") for _ in range(rng.randint(0, 12))]
            self.assertEqual(ex.fruit_baskets(trees),
                             max([j - i for i in range(len(trees) + 1) for j in range(i, len(trees) + 1)
                                  if len(set(trees[i:j])) <= 2] + [0]))
        with self.assertRaises(ValueError):
            ex.best_k_day_sales([1], 2)

    def test_alerts(self) -> None:
        self.assertEqual(ex.error_alerts([1, 2, 3, 10, 11, 12, 13, 30], 5, 3), [13])
        self.assertEqual(ex.error_alerts([], 5, 3), [])


class TestSolutions(unittest.TestCase):
    def test_flips(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            b = [rng.randint(0, 1) for _ in range(rng.randint(0, 12))]
            k = rng.randint(0, 3)
            brute = max([j - i for i in range(len(b) + 1) for j in range(i, len(b) + 1) if b[i:j].count(0) <= k] + [0])
            self.assertEqual(sol.longest_ones_with_flips(b, k), brute)

    def test_anagrams_and_cover(self) -> None:
        self.assertEqual(sol.anagram_positions("cbaebabacd", "abc"), [0, 6])
        self.assertEqual(sol.anagram_positions("ab", "abc"), [])
        self.assertEqual(sol.smallest_covering_window("ADOBECODEBANC", "ABC"), "BANC")
        self.assertEqual(sol.smallest_covering_window("a", "aa"), "")
        rng = random.Random(3)
        for _ in range(200):
            text = "".join(rng.choice("abc") for _ in range(rng.randint(0, 10)))
            letters = "".join(rng.choice("abc") for _ in range(rng.randint(1, 3)))
            need = Counter(letters)
            covers = [text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1)
                      if not need - Counter(text[i:j])]
            got = sol.smallest_covering_window(text, letters)
            self.assertEqual(len(got), min(map(len, covers)) if covers else 0)
        self.assertAlmostEqual(sol.max_average([1, 12, -5, -6, 50, 3], 4), 12.75)


if __name__ == "__main__":
    unittest.main()
