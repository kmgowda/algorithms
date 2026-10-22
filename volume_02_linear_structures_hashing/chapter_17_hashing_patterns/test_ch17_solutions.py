import itertools
import random
import unittest

import ch17_examples as ex
import ch17_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.count_pairs_for_card([], 30), 0)
        self.assertEqual(sol.count_pairs_for_card([15], 30), 0)
        self.assertEqual(sol.count_pairs_for_card([15, 15], 30), 1)
        self.assertEqual(sol.count_pairs_for_card([10, 20], 30), 1)

    def test_worked_trace(self) -> None:
        self.assertEqual(sol.count_pairs_for_card([15, 12, 15, 18, 15], 30), 4)
        self.assertEqual(sol.count_pairs_for_card([15] * 5, 30), 10)

    def test_against_brute_force(self) -> None:
        rng = random.Random(17)
        for _ in range(400):
            prices = [rng.randint(0, 20) for _ in range(rng.randint(0, 12))]
            card = rng.randint(0, 40)
            brute = sum(a + b == card for a, b in itertools.combinations(prices, 2))
            self.assertEqual(sol.count_pairs_for_card(prices, card), brute)
            self.assertEqual(brute > 0, ex.pair_for_card(prices, card) is not None)

    def test_letter_sum_signature_merges_non_anagrams(self) -> None:
        groups = sol.group_by_letter_sum(["cat", "act", "gap"])
        self.assertEqual(list(groups.values()), [["cat", "act", "gap"]])
        self.assertEqual(len(ex.group_anagrams(["cat", "act", "gap"])), 2)
        self.assertEqual(sol.group_by_letter_sum([]), {})


if __name__ == "__main__":
    unittest.main()
