import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def brute_close(a, d):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if abs(a[i] - a[j]) <= d)


class TestChapter01Solutions(unittest.TestCase):
    def test_close_pairs_small(self) -> None:
        self.assertEqual(sol.count_close_pairs([], 5), 0)
        self.assertEqual(sol.count_close_pairs([7], 0), 0)
        self.assertEqual(sol.count_close_pairs([7, 7], 0), 1)
        self.assertEqual(sol.count_close_pairs([1, 5], 3), 0)
        self.assertEqual(sol.count_close_pairs(sol.PILE, 10), 4)

    def test_close_pairs_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 50) for _ in range(rng.randint(0, 20))]
            d = rng.randint(0, 12)
            self.assertEqual(sol.count_close_pairs(a, d), brute_close(a, d))

    def test_displacement_bounds(self) -> None:          # half the displacement <= inversions <= displacement
        self.assertEqual((sol.total_displacement(sol.PILE), len(ex.inversions(sol.PILE))), (26, 17))
        self.assertEqual((sol.total_displacement([3, 2, 1]), len(ex.inversions([3, 2, 1]))), (4, 3))
        rng = random.Random(2)
        for _ in range(300):
            a = rng.sample(range(100), rng.randint(0, 12))
            d, i = sol.total_displacement(a), len(ex.inversions(a))
            self.assertLessEqual(d, 2 * i)
            self.assertLessEqual(i, d)

    def test_long_swap_removes_odd_number(self) -> None:          # Thinking Problem 1
        a = list(sol.PILE)
        a[2], a[7] = a[7], a[2]
        self.assertEqual(len(ex.inversions(a)), 10)
        rng = random.Random(3)
        for _ in range(300):
            b = rng.sample(range(100), rng.randint(2, 12))
            i, j = sorted(rng.sample(range(len(b)), 2))
            if b[i] > b[j]:
                before = len(ex.inversions(b))
                b[i], b[j] = b[j], b[i]
                drop = before - len(ex.inversions(b))
                self.assertEqual(drop % 2, 1)


if __name__ == "__main__":
    unittest.main()
