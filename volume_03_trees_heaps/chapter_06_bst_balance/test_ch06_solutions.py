import itertools
import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestChapter06Solutions(unittest.TestCase):
    def test_depths_small(self) -> None:
        self.assertEqual(sol.depths_without_building([]), (-1, 0))
        self.assertEqual(sol.depths_without_building([5]), (0, 0))
        self.assertEqual(sol.depths_without_building([5, 3]), (1, 1))
        rows = [range(1, 101), range(100, 0, -1), [4, 2, 6, 1, 3, 5, 7], [1, 7, 2, 6, 3, 5, 4],
                [47, 12, 25, 31, 58, 63, 70]]
        for keys in rows:
            self.assertEqual(sol.depths_without_building(keys), ex.insert_all(keys))

    def test_depths_random(self) -> None:
        rng = random.Random(6)
        for _ in range(300):
            keys = rng.sample(range(1000), rng.randrange(0, 60))
            self.assertEqual(sol.depths_without_building(keys), ex.insert_all(keys))
        self.assertEqual(sol.depths_without_building(range(100_000)), (99_999, 4_999_950_000))

    def test_perfect_orders(self) -> None:
        self.assertEqual([sol.perfect_orders(k) for k in range(1, 5)], [1, 2, 80, 21_964_800])
        for k in (1, 2, 3):
            n = 2 ** k - 1
            count = sum(ex.insert_all(p)[0] == k - 1 for p in itertools.permutations(range(n)))
            self.assertEqual(count, sol.perfect_orders(k))

    def test_root_only_balance(self) -> None:
        self.assertEqual(sol.middle_then_sorted(1), [0])
        self.assertEqual(ex.insert_all(sol.middle_then_sorted(7)), (3, 12))
        self.assertEqual(ex.insert_all(sol.middle_then_sorted(1001))[0], 500)


if __name__ == "__main__":
    unittest.main()
