import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


def brute(a):
    return [sum(1 for q in range(p + 1, len(a)) if a[q] < a[p]) for p in range(len(a))]


class TestChapter5Solutions(unittest.TestCase):
    def test_smaller_to_the_right(self) -> None:
        self.assertEqual(sol.smaller_to_the_right([]), [])
        self.assertEqual(sol.smaller_to_the_right([7]), [0])
        self.assertEqual(sol.smaller_to_the_right([2, 1]), [1, 0])
        self.assertEqual(sol.smaller_to_the_right([5, 5, 5]), [0, 0, 0])
        self.assertEqual(sol.smaller_to_the_right(sol.PILE), [4, 1, 6, 0, 3, 1, 2, 0, 0])
        self.assertEqual(sum(sol.smaller_to_the_right(sol.PILE)), 17)
        rng = random.Random(3)
        for _ in range(300):
            a = [rng.randint(0, 9) for _ in range(rng.randint(0, 30))]
            self.assertEqual(sol.smaller_to_the_right(a), brute(a))

    def test_bottom_up_bug(self) -> None:
        self.assertEqual(sol.bottom_up_buggy(sol.PILE), [12, 25, 31, 47, 58, 70, 84, 91, 63])
        self.assertEqual(sol.bottom_up_buggy(sol.PILE[:8]), sorted(sol.PILE[:8]))   # powers of two hide the bug
        rng = random.Random(4)
        for _ in range(300):
            a = [rng.randint(0, 50) for _ in range(rng.randint(0, 40))]
            self.assertEqual(sol.bottom_up(a), sorted(a))
        for a in ([], [1], [2, 1], [3, 1, 2]):
            self.assertEqual(sol.bottom_up(a), sorted(a))

    def test_lower_bound_tight_on_sorted(self) -> None:          # Thinking Problem 1 and the formal proof
        for k in range(11):
            n = 2 ** k
            c = {"comparisons": 0}
            ex.merge_sort(list(range(n)), c)
            self.assertEqual(c["comparisons"], n * k // 2)
        rng = random.Random(5)
        for n in (2, 3, 9, 100, 257):
            a = [rng.random() for _ in range(n)]
            c = {"comparisons": 0}
            ex.merge_sort(a, c)
            self.assertLessEqual(c["comparisons"], n * (n - 1).bit_length())


if __name__ == "__main__":
    unittest.main()
