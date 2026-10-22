import random
import unittest

import ch14_examples as ex


class TestChapter20(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 30) for _ in range(rng.randint(1, 40))]
            k = rng.randint(1, len(a))
            want = sorted(a)[k - 1]
            self.assertEqual(ex.quickselect(a, k), want)
            self.assertEqual(ex.quickselect(a, k, rng=random.Random(k)), want)
            self.assertEqual(ex.median_of_medians(a, k), want)

    def test_every_case(self) -> None:
        p = ex.PILE
        rows = [(p, 1, 12, 13), (p, 9, 91, 10), (p, 3, 31, 12), (p, 5, 58, 13), (sorted(p), 5, 58, 30),
                (sorted(p, reverse=True), 5, 58, 36), ([47, 12, 47, 91, 12, 47, 58], 4, 47, 11), ([47] * 9, 5, 47, 30),
                ([47], 1, 47, 0)]
        for a, k, ans, comps in rows:
            c = {"comparisons": 0}
            self.assertEqual(ex.quickselect(a, k, c), ans)
            self.assertEqual(c["comparisons"], comps)
            self.assertEqual(ex.median_of_medians(a, k), ans)
        with self.assertRaises(ValueError):
            ex.quickselect(p, 10)

    def test_examples(self) -> None:
        log = []
        ex.quickselect(ex.PILE, 5, log=log)
        self.assertEqual([(x[0], x[1]) for x in log], [(63, 5), (31, 2), (58, 4)])
        self.assertEqual(ex.smallest_k_heap(ex.PILE, 3), [12, 25, 31])

    def test_median_of_medians_guarantee(self) -> None:
        a = [89, 42, 55, 93, 77, 13, 69, 41, 16, 30, 24, 57, 70, 92, 58, 79, 23, 86, 11, 37, 62, 45, 33, 59, 90]
        groups, pivot = ex.mom_pivot(a)
        self.assertEqual(pivot, 58)
        self.assertEqual([g[2] for g in groups], [77, 30, 58, 37, 59])
        self.assertEqual((sum(x < pivot for x in a), sum(x > pivot for x in a)), (13, 11))
        self.assertEqual(ex.guaranteed_side(0), 0)
        self.assertEqual(ex.guaranteed_side(25), 3)
        self.assertEqual(ex.guaranteed_side(100_000), 29_994)
        self.assertEqual(ex.mom_pivot([7]), ([[7]], 7))
        rng = random.Random(7)
        for _ in range(200):
            n = rng.randint(1, 300)
            b = rng.sample(range(10_000), n)
            _, p = ex.mom_pivot(b)
            self.assertGreaterEqual(min(sum(x < p for x in b), sum(x > p for x in b)), ex.guaranteed_side(n))

    def test_expected_quickselect(self) -> None:
        E = ex.expected_select(9)
        self.assertEqual((E[1][1], E[2][1]), (0.0, 1.0))
        self.assertAlmostEqual(E[3][2], 8 / 3)
        self.assertAlmostEqual(E[9][5], 16.646, places=3)
        rng, total = random.Random(3), 0
        for r in range(20_000):
            c = {"comparisons": 0}
            ex.quickselect(ex.PILE, 5, c, rng=rng)
            total += c["comparisons"]
        self.assertAlmostEqual(total / 20_000, E[9][5], delta=0.15)
        self.assertAlmostEqual(ex.average_median_comparisons(20_000, 200), 3.42, delta=0.01)


if __name__ == "__main__":
    unittest.main()
