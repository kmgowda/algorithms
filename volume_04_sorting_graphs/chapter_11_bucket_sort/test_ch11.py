import random
import unittest

import ch11_examples as ex


class TestChapter17(unittest.TestCase):
    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.uniform(0, 100) for _ in range(rng.randint(0, 40))]
            self.assertEqual(ex.bucket_sort(a, 0, 100, rng.randint(1, 12)), sorted(a))

    def test_every_case(self) -> None:
        rows = [(ex.PILE, [[12, 25, 31], [47, 58, 63], [70, 84, 91]], 7),
                (sorted(ex.PILE, reverse=True), [[12, 25, 31], [47, 58, 63], [70, 84, 91]], 9),
                ([47] * 9, [[], [47] * 9, []], 8), ([5, 8, 2, 9, 1, 7, 3, 6, 4], [list(range(1, 10)), [], []], 26),
                ([47, 47, 12, 12, 91], [[12, 12], [47, 47], [91]], 2), ([47], [[], [47], []], 0)]
        for a, buckets, comps in rows:
            log = {}
            self.assertEqual(ex.bucket_sort(a, 0, 100, 3, log), sorted(a))
            self.assertEqual((log["buckets"], log["comparisons"]), (buckets, comps))
        self.assertEqual(ex.bucket_sort([], 0, 100, 3), [])

    def test_even_beats_bunched(self) -> None:
        r = ex.experiment(n=2000)
        self.assertLess(r["even"][0] * 10, r["bunched"][0])

    def test_stable(self) -> None:
        recs = [(30, "a"), (10, "b"), (30, "c"), (10, "d")]

        class K:
            def __init__(self, r): self.r = r
            def __sub__(self, o): return self.r[0] - o
            def __le__(self, o): return self.r[0] <= o.r[0]
        out = ex.bucket_sort([K(r) for r in recs], 0, 100, 2)
        self.assertEqual([k.r[1] for k in out], ["b", "d", "a", "c"])

    def test_figure_samples(self) -> None:
        sizes = ex.bucket_sizes(ex.SAMPLE, 10)
        self.assertEqual(sizes, [1, 0, 1, 1, 2, 0, 1, 3, 1, 0])
        self.assertEqual(sum(s * s for s in sizes), 18)
        log = {}
        self.assertEqual(ex.bucket_sort(ex.SHELF_KEYS, 0, 1, 10, log), sorted(ex.SHELF_KEYS))
        self.assertEqual(log["comparisons"], 4)
        self.assertEqual([len(b) for b in log["buckets"]], [0, 2, 3, 1, 0, 0, 1, 1, 1, 1])
        self.assertEqual(ex.bucket_sizes([], 3), [0, 0, 0])

    def test_expected_square(self) -> None:
        self.assertEqual(ex.expected_square(0), 0.0)
        self.assertEqual(ex.expected_square(1), 1.0)            # one bucket always holds the one key
        self.assertAlmostEqual(ex.expected_square(10_000), 1.9999)
        self.assertEqual(ex.sum_of_squares(1, random.Random(1)), 1)
        self.assertEqual(ex.sum_of_squares(0, random.Random(1)), 0)
        for n in (2, 10, 1000):
            self.assertAlmostEqual(ex.average_sum_of_squares(n, 400) / (2 * n - 1), 1.0, delta=0.05)


if __name__ == "__main__":
    unittest.main()
