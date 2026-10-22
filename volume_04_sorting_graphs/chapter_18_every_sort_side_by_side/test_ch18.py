import random
import unittest

import ch18_examples as ex

CASES = [ex.PILE, sorted(ex.PILE), sorted(ex.PILE, reverse=True), [47] * 9, [58, 25, 58, 12, 25, 47, 58, 12, 47], [47], []]
MATRIX = {"selection": [36, 36, 36, 36, 36, 0, 0], "insertion": [23, 8, 36, 8, 23, 0, 0],
          "bubble": [33, 8, 36, 8, 35, 0, 0], "merge": [21, 13, 16, 13, 20, 0, 0], "heap": [29, 35, 30, 21, 29, 0, 0],
          "Timsort (teaching)": [27, 8, 8, 8, 23, 0, 0], "odd-even network": [28, 28, 28, 28, 28, 0, 0]}


class TestChapter21(unittest.TestCase):
    def test_all_sort_correctly(self) -> None:
        rng = random.Random(1)
        for _ in range(20):
            data = [rng.randrange(500) for _ in range(rng.randint(0, 120))]
            ex.run_all(data)                    # run_all asserts every result is sorted

    def test_every_case_matrix(self) -> None:
        for name, row in MATRIX.items():
            got = [ex.SORTS[name](list(a))[1] for a in CASES]
            self.assertEqual(got, row, name)

    def test_quadratic_counts(self) -> None:
        rng = random.Random(1)
        data = [rng.randrange(1_000_000) for _ in range(500)]
        r = ex.run_all(data)
        self.assertEqual(r["selection"][0], 500 * 499 // 2)
        self.assertLess(r["merge"][0], r["insertion"][0])


    def test_sorting_network_sizes(self) -> None:
        self.assertEqual(ex.sorting_network(0), [])
        self.assertEqual(ex.sorting_network(1), [])
        self.assertEqual(ex.sorting_network(2), [(0, 1)])
        self.assertEqual(ex.sorting_network(4), [(0, 1), (2, 3), (0, 2), (1, 3), (1, 2)])
        for n, size, depth in [(2, 1, 1), (4, 5, 3), (8, 19, 6), (9, 28, 9), (16, 63, 10)]:
            net = ex.sorting_network(n)
            self.assertEqual((len(net), len(ex.stages(net))), (size, depth))
        for p in range(1, 6):          # (p^2 - p + 4) 2^(p-2) - 1 comparators, p(p+1)/2 stages, for n = 2^p
            net = ex.sorting_network(2 ** p)
            self.assertEqual(4 * len(net) + 4, (p * p - p + 4) * 2 ** p)
            self.assertEqual(len(ex.stages(net)), p * (p + 1) // 2)

    def test_sorting_network_sorts(self) -> None:
        rng = random.Random(8)
        for n in range(0, 11):
            net = ex.sorting_network(n)
            self.assertTrue(ex.sorts_all_01(net, n))
            for _ in range(50):
                a = [rng.randint(0, 9) for _ in range(n)]
                self.assertEqual(ex.apply_network(net, a), sorted(a))
        self.assertEqual(ex.apply_network([], []), [])
        self.assertEqual(ex.apply_network([], [47]), [47])
        self.assertEqual(ex.apply_network([(0, 1)], [70, 12]), [12, 70])
        self.assertFalse(ex.sorts_all_01([(0, 1), (1, 2)], 3))

    def test_network_trace(self) -> None:
        a, rows = [58, 25, 91, 12, 70, 47, 84, 31], []
        for layer in ex.stages(ex.sorting_network(8)):
            a = ex.apply_network(layer, a)
            rows.append(a)
        self.assertEqual(rows, [[25, 58, 12, 91, 47, 70, 31, 84], [12, 58, 25, 91, 31, 70, 47, 84],
                                [12, 25, 58, 84, 31, 47, 70, 91], [12, 25, 58, 84, 31, 47, 70, 91],
                                [12, 25, 31, 47, 58, 84, 70, 91], [12, 25, 31, 47, 58, 70, 84, 91]])
        self.assertEqual(ex.apply_network(ex.sorting_network(4), [70, 12, 47, 25]), [12, 25, 47, 70])


if __name__ == "__main__":
    unittest.main()
