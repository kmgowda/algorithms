import itertools
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def run_bubble(a):
    p = []
    r = ex.bubble_sort(list(a), p)
    return len(p), r["comparisons"]


class TestChapter04Solutions(unittest.TestCase):
    def test_passes_follow_larger_before(self) -> None:          # Thinking Problem 1
        self.assertEqual(sol.larger_before(sol.PILE), [0, 1, 0, 3, 1, 3, 1, 5, 3])
        self.assertEqual(run_bubble(sol.PILE), (6, 33))
        self.assertEqual(run_bubble([2, 3, 4, 5, 1]), (4, 10))
        for n in range(2, 7):
            for t in itertools.product(range(4), repeat=n):
                self.assertEqual(run_bubble(t)[0], min(n - 1, max(sol.larger_before(list(t))) + 1))

    def test_predict_small(self) -> None:          # Thinking Problem 2
        self.assertEqual(sol.predict_bubble_passes([]), (0, 0))
        self.assertEqual(sol.predict_bubble_passes([7]), (0, 0))
        self.assertEqual(sol.predict_bubble_passes([1, 2]), (1, 1))
        self.assertEqual(sol.predict_bubble_passes([2, 1]), (1, 1))
        self.assertEqual(sol.predict_bubble_passes([5, 5, 5]), (1, 2))
        self.assertEqual(sol.predict_bubble_passes(sol.PILE), (6, 33))

    def test_predict_random(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            a = [rng.randint(0, 9) for _ in range(rng.randint(0, 30))]
            self.assertEqual(sol.predict_bubble_passes(a), run_bubble(a) if len(a) > 1 else (0, 0))

    def test_predict_mixup(self) -> None:          # Section 7.8's far-moved books
        rng = random.Random(1)
        n = 5000
        for _ in range(5):
            i = rng.randrange(n - 1)
        far = list(range(n))
        for _ in range(5):
            far.append(far.pop(rng.randrange(n // 10)))
        self.assertEqual(sol.predict_bubble_passes(far)[1], ex.bubble_sort(list(far))["comparisons"])

    def test_two_and_three_sorted(self) -> None:          # Thinking Problem 3
        self.assertTrue(sol.is_h_sorted([2, 1, 4, 3], 2) and sol.is_h_sorted([2, 1, 4, 3], 3))
        rng = random.Random(2)
        for _ in range(300):
            a = [rng.randint(0, 20) for _ in range(rng.randint(0, 25))]
            ex.shell_sort(a, [3, 2])
            self.assertTrue(sol.is_h_sorted(a, 2) and sol.is_h_sorted(a, 3))
            self.assertLessEqual(inversions(a), len(a) // 2)
            self.assertLessEqual(ex.shell_sort(a, [1])["shifts"], len(a) // 2)


if __name__ == "__main__":
    unittest.main()
