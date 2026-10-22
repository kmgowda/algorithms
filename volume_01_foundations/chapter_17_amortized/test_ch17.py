import unittest

import ch17_examples as ex


class TestChapter17(unittest.TestCase):
    def test_every_case(self) -> None:
        rows = {0: (0, 0), 1: (1, 1), 2: (3, 2), 3: (6, 3), 4: (7, 3), 5: (12, 5), 8: (15, 5), 9: (24, 9), 16: (31, 9),
                17: (48, 17), 1000: (2023, 513)}
        for n, (total, worst) in rows.items():
            c = ex.append_costs(n)
            self.assertEqual((sum(c), max(c) if c else 0), (total, worst))
        for n in range(1, 3000):
            self.assertLess(sum(ex.append_costs(n)) / n, 3)
        self.assertEqual([ex.copying_with_fixed_growth(n) for n in (10, 11, 100, 1000, 10000)],
                         [0, 10, 450, 49500, 4995000])

    def test_doubling(self) -> None:
        for n in range(1, 3000):
            costs = ex.append_costs(n)
            self.assertLess(sum(costs), 3 * n)
            self.assertLess(sum(costs) - n, 2 * n)
        c = ex.append_costs(33)
        self.assertEqual([i + 1 for i, x in enumerate(c) if x > 1], [2, 3, 5, 9, 17, 33])
        self.assertEqual(sum(c), 96)
        self.assertEqual(sum(ex.append_costs(16)), 31)
        self.assertEqual(sum(ex.append_costs(17)), 48)
        self.assertEqual(sum(ex.append_costs(10_000)) - 10_000, 16_383)

    def test_fixed_growth(self) -> None:
        self.assertEqual(ex.copying_with_fixed_growth(10_000), 4_995_000)

    def test_copies_bound(self) -> None:
        for n in range(1, 3000):
            copies = sum(ex.append_costs(n)) - n
            self.assertLess(copies, 2 * n)
            if n & (n - 1) == 0:
                self.assertEqual(copies, n - 1)
        self.assertEqual(sum(ex.append_costs(1000)) - 1000, 1023)

    def test_growth_factors(self) -> None:
        self.assertEqual(ex.copying_with_factor(10_000, 2), (16_383, 6_384))
        self.assertEqual(ex.copying_with_factor(10_000, 1.5), (24_284, 2_138))
        self.assertEqual(ex.copying_with_factor(10_000, 1.125), (88_035, 983))
        self.assertEqual(ex.copying_with_factor(20, 1.5, 2), (56, 8))
        self.assertEqual(ex.copying_with_factor(20, 2, 2), (30, 12))
        self.assertEqual(ex.copying_with_factor(0, 2), (0, 1))
        self.assertEqual(ex.copying_with_factor(1, 2), (0, 0))

    def test_counter(self) -> None:
        self.assertEqual(ex.counter_flips(0), [])
        self.assertEqual(ex.counter_flips(1), [1])
        self.assertEqual(ex.counter_flips(8), [1, 2, 1, 3, 1, 2, 1, 4])
        self.assertEqual((sum(ex.counter_flips(8)), sum(ex.counter_flips(16)), sum(ex.counter_flips(1000, bits=16))),
                         (15, 31, 1994))
        self.assertEqual(sum(ex.counter_flips(1000, bits=16)), 2 * 1000 - bin(1000).count("1"))
        for n in range(1, 2000):
            self.assertLess(sum(ex.counter_flips(n, bits=12)), 2 * n)
        self.assertEqual(ex.counter_flips(16)[-1], 5)
        self.assertEqual(set(ex.counter_amortized(255)), {2})
        self.assertEqual(ex.array_amortized(1), [2])
        self.assertEqual(set(ex.array_amortized(1000)[1:]), {3})


if __name__ == "__main__":
    unittest.main()
