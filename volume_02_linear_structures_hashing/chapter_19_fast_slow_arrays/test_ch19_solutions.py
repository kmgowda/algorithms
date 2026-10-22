import random
import unittest

import ch19_examples as ex
import ch19_solutions as sol


def brute_tail_loop(a, start):
    first, i, k = {}, start, 0
    while i not in first:
        first[i] = k
        i, k = a[i], k + 1
    return first[i], k - first[i]


class TestTailAndLoop(unittest.TestCase):
    def test_smallest(self) -> None:
        self.assertEqual(sol.tail_and_loop([0]), (0, 1))
        self.assertEqual(sol.tail_and_loop([1, 1]), (1, 1))
        self.assertEqual(sol.tail_and_loop([1, 0]), (0, 2))

    def test_lockers(self) -> None:
        self.assertEqual(sol.tail_and_loop([3, 1, 3, 4, 2]), (1, 3))
        self.assertEqual(sol.tail_and_loop([3, 1, 3, 4, 2], 4), (0, 3))
        self.assertEqual(sol.tail_and_loop([3, 1, 3, 4, 2], 1), (0, 1))

    def test_random(self) -> None:
        rng = random.Random(19)
        for _ in range(2000):
            n = rng.randint(1, 40)
            a = [rng.randrange(n) for _ in range(n)]
            s = rng.randrange(n)
            self.assertEqual(sol.tail_and_loop(a, s), brute_tail_loop(a, s))


class TestMixedBug(unittest.TestCase):
    def test_never_meets_on_lockers(self) -> None:
        self.assertIsNone(sol.find_duplicate_mixed([3, 1, 3, 4, 2]))
        self.assertEqual(ex.find_duplicate([3, 1, 3, 4, 2]), 3)

    def test_works_only_for_loop_of_one(self) -> None:
        self.assertEqual(sol.find_duplicate_mixed([1, 1]), 1)
        self.assertEqual(sol.find_duplicate_mixed([2, 2, 2]), 2)


class TestHappyStops(unittest.TestCase):
    def test_bound(self) -> None:
        for d in range(4, 30):
            self.assertLess(81 * d, 10 ** (d - 1))
        self.assertEqual(max(ex.digit_square_sum(n) for n in range(1, 1000)), 243)


if __name__ == "__main__":
    unittest.main()
