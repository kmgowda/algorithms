import itertools
import random
import unittest

import ch18_examples as ex
import ch18_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertIsNone(sol.three_for_card([], 30))
        self.assertIsNone(sol.three_for_card([10, 20], 30))
        self.assertEqual(sol.three_for_card([10, 10, 10], 30), (10, 10, 10))

    def test_gift_shelf(self) -> None:
        self.assertEqual(sol.three_for_card([4, 9, 20, 6, 17, 13, 15], 30), (4, 6, 20))
        self.assertIsNone(sol.three_for_card([4, 9, 20], 30))

    def test_against_brute_force(self) -> None:
        rng = random.Random(18)
        for _ in range(400):
            prices = [rng.randint(0, 15) for _ in range(rng.randint(0, 9))]
            card = rng.randint(0, 40)
            got = sol.three_for_card(prices, card)
            exists = any(sum(t) == card for t in itertools.combinations(prices, 3))
            self.assertEqual(got is not None, exists)
            if got:
                self.assertEqual(sum(got), card)
                rest = list(prices)
                for x in got:
                    rest.remove(x)          # the three prices are three different books

    def test_moving_the_taller_end_is_wrong(self) -> None:
        self.assertEqual(sol.bookends_move_taller([1, 5, 5, 2]), 3)
        self.assertEqual(ex.best_bookends([1, 5, 5, 2])[0], 5)

    def test_read_minus_one_comparison_is_also_correct(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = sorted(rng.randint(0, 5) for _ in range(rng.randint(0, 10)))
            b = list(a)
            k = ex.dedupe_sorted(a)
            write = 1 if b else 0
            for read in range(1, len(b)):
                if b[read] != b[read - 1]:
                    b[write] = b[read]
                    write += 1
            self.assertEqual((a[:k], k), (b[:write], write))


if __name__ == "__main__":
    unittest.main()
