import bisect
import itertools
import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


def buggy_binary_insertion(a, key):
    for i in range(1, len(a)):
        x = a[i]
        p = bisect.bisect_left([key(v) for v in a[:i]], key(x))          # first item >= x
        a[p + 1:i + 1] = a[p:i]
        a[p] = x
    return a


LOANS = [("Ben", 3), ("Ana", 1), ("Cai", 3), ("Dev", 2), ("Eva", 1)]


class TestChapter03Solutions(unittest.TestCase):
    def test_comparisons_never_exceed_selection(self) -> None:          # Thinking Problem 1
        tie = [84, 91, 70, 63, 58, 47, 31, 25, 12]
        self.assertEqual(ex.insertion_sort(list(tie)), {"comparisons": 36, "shifts": 35})
        for n in range(1, 8):
            ties = 0
            for p in itertools.permutations(range(n)):
                c = ex.insertion_sort(list(p))["comparisons"]
                self.assertLessEqual(c, n * (n - 1) // 2)
                ties += c == n * (n - 1) // 2
            self.assertEqual(ties, 2 ** (n - 1))

    def test_refresh_small(self) -> None:          # Thinking Problem 2
        self.assertEqual(sol.refresh_catalogue([], []), ([], 0))
        self.assertEqual(sol.refresh_catalogue([5], []), ([5], 0))
        self.assertEqual(sol.refresh_catalogue([], [3, 1]), ([1, 3], 1))
        self.assertEqual(sol.refresh_catalogue([1, 4, 9], [4])[0], [1, 4, 4, 9])

    def test_refresh_random(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            n, k = rng.randint(0, 40), rng.randint(0, 10)
            cat = sorted(rng.randint(0, 50) for _ in range(n))
            new = [rng.randint(0, 50) for _ in range(k)]
            out, c = sol.refresh_catalogue(cat, new)
            self.assertEqual(out, sorted(cat + new))
            self.assertLessEqual(c, k * (k - 1) // 2 + max(n + k - 1, 0))

    def test_refresh_catalogue_sizes(self) -> None:
        rng = random.Random(1)
        cat = sorted(rng.sample(range(200_000), 20_000))
        out, c = sol.refresh_catalogue(cat, [rng.randrange(200_000) for _ in range(50)])
        self.assertEqual(out, sorted(out))
        self.assertLessEqual(c, 1225 + 20_049)
        self.assertEqual(c, 20_600)          # the same data as nightly_catalogue(near_end=False)
        self.assertEqual(ex.nightly_catalogue(near_end=False)["comparisons"], 420_565)

    def test_binary_insertion_stability(self) -> None:          # Thinking Problem 3
        key = lambda r: r[1]
        self.assertEqual([n for n, _ in buggy_binary_insertion(list(LOANS), key)], ["Eva", "Ana", "Dev", "Cai", "Ben"])
        b = list(LOANS)
        sol.binary_insertion_sort(b, key)
        self.assertEqual([n for n, _ in b], ["Ana", "Eva", "Dev", "Ben", "Cai"])
        for a in ([], [1], [2, 1], [1, 1]):
            c = list(a)
            sol.binary_insertion_sort(c)
            self.assertEqual(c, sorted(a))
        rng = random.Random(2)
        for _ in range(200):
            a = [(i, rng.randint(0, 5)) for i in range(rng.randint(0, 20))]
            c = list(a)
            sol.binary_insertion_sort(c, key)
            self.assertEqual(c, sorted(a, key=key))          # Python's sorted is stable


if __name__ == "__main__":
    unittest.main()
