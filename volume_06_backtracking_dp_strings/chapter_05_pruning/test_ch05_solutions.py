import itertools
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


def brute_split(values):
    total = sum(values)
    return total % 2 == 0 and any(sum(c) * 2 == total for k in range(len(values) + 1)
                                  for c in itertools.combinations(values, k))


class TestChapter05Solutions(unittest.TestCase):
    def test_equal_split(self) -> None:
        self.assertEqual(sol.equal_split([]), ([], 0))
        self.assertEqual(sol.equal_split([3]), (None, 0))
        self.assertEqual(sol.equal_split([4])[0], None)
        self.assertEqual(sol.equal_split([5, 5])[0], [5])
        self.assertIsNone(sol.equal_split(ex.VOUCHERS)[0])          # total 115 is odd
        pile, _ = sol.equal_split(ex.VOUCHERS + [5])
        self.assertEqual(sum(pile), 60)
        r = random.Random(5)
        for _ in range(300):
            v = [r.randint(1, 15) for _ in range(r.randint(0, 8))]
            pile, _ = sol.equal_split(v)
            self.assertEqual(pile is not None, brute_split(v))
            if pile is not None:
                self.assertEqual(sum(pile) * 2, sum(v))

    def test_thinking_problems(self) -> None:
        self.assertEqual(ex.subset_sum([2, 1, 2], 3, True, False)[1], 3)
        self.assertEqual(ex.subset_sum([2, 1, 2], 3, True, True)[1], 5)
        self.assertEqual(sol.max_reach_bug(ex.VOUCHERS, 50), (None, 1))
        self.assertEqual(ex.subset_sum(ex.VOUCHERS, 50, True, False)[0], [3, 34, 4, 9])


if __name__ == "__main__":
    unittest.main()
