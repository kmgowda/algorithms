import itertools
import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


def brute_fewest(values, target):
    for k in range(len(values) + 1):
        for c in itertools.combinations(values, k):
            if sum(c) == target:
                return k
    return None


class TestChapter06Solutions(unittest.TestCase):
    def test_fewest_vouchers(self) -> None:
        self.assertEqual(sol.fewest_vouchers([], 0), ([], 1))
        self.assertEqual(sol.fewest_vouchers([], 5)[0], None)
        self.assertEqual(sol.fewest_vouchers([5], 5)[0], [5])
        got, _ = sol.fewest_vouchers(sol.VOUCHERS, 50)
        self.assertEqual((got, sol.fewest_vouchers(sol.VOUCHERS, 50)[1]), ([34, 12, 4], 17))
        r = random.Random(6)
        for _ in range(300):
            v = [r.randint(1, 20) for _ in range(r.randint(0, 8))]
            t = r.randint(0, 60)
            got, _ = sol.fewest_vouchers(v, t)
            want = brute_fewest(v, t)
            self.assertEqual(None if got is None else len(got), want)
            if got is not None:
                self.assertEqual(sum(got), t)

    def test_bound_bugs_and_gap(self) -> None:
        self.assertEqual(sol.unsorted_branch_and_bound(ex.BOOKS, 21), 16)
        self.assertEqual(ex.branch_and_bound(ex.BOOKS, 21)[0], 17)
        items = sorted(ex.BOOKS, key=lambda b: b[2] / b[1], reverse=True)
        for budget in range(0, 40):
            best = ex.branch_and_bound(ex.BOOKS, budget)[0]
            self.assertLessEqual(ex.fractional_bound(items, 0, budget), best + max(v for _, _, v in ex.BOOKS))
            self.assertGreaterEqual(ex.fractional_bound(items, 0, budget), best)


if __name__ == "__main__":
    unittest.main()
