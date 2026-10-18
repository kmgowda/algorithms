import unittest

import ch12_examples as ex
import ch12_solutions as sol


class TestJob(unittest.TestCase):
    def test_versions_agree(self) -> None:
        orders = ex.load_orders(2000)
        vips = [f"cust{i}" for i in range(0, 200, 3)]
        self.assertEqual(ex.vip_customers_slow(orders, vips), ex.vip_customers_fast(orders, vips))
        self.assertEqual(ex.report_text_slow(orders), ex.report_text_fast(orders))
        self.assertEqual(ex.nightly_job(orders, vips, False), ex.nightly_job(orders, vips, True))

    def test_profiler_finds_names(self) -> None:
        orders = ex.load_orders(500)
        rows = ex.profile_top_functions(lambda: ex.nightly_job(orders, ["cust1"], False), top=10)
        self.assertTrue(rows)
        self.assertTrue(all(isinstance(name, str) and seconds >= 0 for name, seconds in rows))

    def test_set_is_faster(self) -> None:
        orders = ex.load_orders(5000)
        vips = [f"cust{i}" for i in range(0, 500)]
        speedup = ex.compare_speed(lambda: ex.vip_customers_slow(orders, vips),
                                   lambda: ex.vip_customers_fast(orders, vips), number=1)
        self.assertGreater(speedup, 2)


class TestPercentiles(unittest.TestCase):
    def test_percentile(self) -> None:
        values = list(range(1, 101))
        self.assertEqual(ex.percentile(values, 50), 50)
        self.assertEqual(ex.percentile(values, 95), 95)
        self.assertEqual(ex.percentile(values, 100), 100)
        self.assertEqual(ex.percentile([7], 99), 7)
        with self.assertRaises(ValueError):
            ex.percentile([], 50)
        with self.assertRaises(ValueError):
            ex.percentile([1], 0)

    def test_summary(self) -> None:
        summary = ex.latency_summary(ex.simulated_latencies(10_000))
        self.assertLess(summary["p50"], 60)
        self.assertGreater(summary["p99"], 300)
        self.assertLessEqual(summary["p95"], summary["p99"])


class TestAmdahl(unittest.TestCase):
    def test_amdahl(self) -> None:
        self.assertAlmostEqual(ex.amdahl_speedup(0.1, 100), 1 / (0.9 + 0.001))
        self.assertAlmostEqual(ex.amdahl_speedup(0.9, 2), 1 / 0.55)
        self.assertAlmostEqual(ex.amdahl_speedup(0, 10), 1)
        with self.assertRaises(ValueError):
            ex.amdahl_speedup(1.5, 2)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertAlmostEqual(sol.max_overall_speedup(0.8), 5)
        self.assertEqual(sol.max_overall_speedup(1), float("inf"))
        prices = [100, 250, 19.99]
        for region in ("north", "south", "east"):
            self.assertEqual(sol.tax_fast(prices, region), sol.tax_slow(prices, region))
        self.assertFalse(sol.meets_slo([10, 20, 30, 400], 100, 50))
        self.assertTrue(sol.meets_slo([10, 20, 30, 400], 75, 50))
        self.assertEqual(sol.best_plan(0.6, 2, 0.2, 50), "A")


if __name__ == "__main__":
    unittest.main()
