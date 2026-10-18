import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestDynamicArray(unittest.TestCase):
    def test_doubling(self) -> None:
        stats = ex.simulate_appends(1024)
        self.assertEqual(stats["copies"], 1023)              # 1 + 2 + 4 + ... + 512
        self.assertEqual(stats["resizes"], 10)
        self.assertEqual(stats["worst_single_append"], 513)  # one write + copying 512 items
        for n in (10, 1000, 100_000):
            self.assertLess(ex.amortized_cost_per_append(n), 3)

    def test_adding_constant_is_quadratic(self) -> None:
        small = ex.simulate_appends(10_000, "add")["copies"]
        big = ex.simulate_appends(20_000, "add")["copies"]
        self.assertAlmostEqual(big / small, 4, delta=0.1)
        self.assertGreater(ex.amortized_cost_per_append(100_000, "add"), 1000)

    def test_accounting(self) -> None:
        self.assertTrue(ex.accounting_bank_never_negative(100_000))
        self.assertFalse(ex.accounting_bank_never_negative(100_000, charge=2))

    def test_real_list_overallocates(self) -> None:
        points = ex.python_list_resize_points(1000)
        self.assertGreater(len(points), 3)
        self.assertLess(len(points), 100)                    # far fewer resizes than appends


class TestCounterAndBuffers(unittest.TestCase):
    def test_counter(self) -> None:
        bits: list[int] = []
        for value in range(1, 300):
            ex.increment_flips(bits)
            self.assertEqual(sum(bit << i for i, bit in enumerate(bits)), value)
        total, worst = ex.total_flips_counting_to(1_000_000)
        self.assertLess(total, 2 * 1_000_000)
        self.assertEqual(worst, 20)

    def test_buffer(self) -> None:
        amortized, worst = ex.buffered_writes(10_000, 500)
        self.assertAlmostEqual(amortized, 1.2)
        self.assertEqual(worst, 101)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertLess(sol.copies_with_factor(100_000, 1.5), 3 * 100_000)
        self.assertLess(sol.copies_with_factor(100_000, 2), 2 * 100_000)
        self.assertGreater(sol.thrashing_cost(1000, 0.5), 10 * sol.thrashing_cost(1000, 0.25) + 100)
        # a full truck (1000) lasts 25 days at 40 per day -> refills on days 25, 50, ..., 350 = 14 trucks
        self.assertAlmostEqual(sol.restock_amortized(365, 40, 1000, 500), 14 * 500 / 365, places=6)
        worst, amortized = sol.worst_vs_amortized(1_000_000)
        self.assertGreater(worst, 500_000)
        self.assertLess(amortized, 3)


if __name__ == "__main__":
    unittest.main()
