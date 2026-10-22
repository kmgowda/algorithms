import unittest

import ch02_solutions as sol


class TestChapter29Solutions(unittest.TestCase):
    def test_simulator_smallest(self) -> None:
        self.assertEqual(sol.cache_misses([]), 0)
        self.assertEqual(sol.cache_misses([0, 8, 63]), 1)                       # one line
        self.assertEqual(sol.cache_misses([0, 64, 0], capacity_lines=1), 3)     # evicted, fetched again

    def test_scan_bound(self) -> None:
        self.assertEqual(sol.cache_misses(sol.scan(0, 1000)), 125)
        self.assertEqual(sol.cache_misses(sol.scan(56, 2)), 2)                  # the bound is tight
        for start in range(0, 64, 8):
            for n in range(0, 40):
                misses = sol.cache_misses(sol.scan(start, n), capacity_lines=1)
                self.assertLessEqual(misses, -(-n // 8) + (1 if n else 0))

    def test_transpose_results(self) -> None:
        for n in (0, 1, 2, 5, 8):
            a = list(range(n * n))
            want = [a[r * n + c] for c in range(n) for r in range(n)]
            self.assertEqual(sol.transpose_naive(a, n), want)
            for t in (1, 3, 8, 20):
                self.assertEqual(sol.transpose_blocked(a, n, t), want)
        self.assertEqual(sol.transpose_addresses(0), [])

    def test_transpose_misses(self) -> None:
        naive = sol.cache_misses(sol.transpose_addresses(64), capacity_lines=16)
        tiled = sol.cache_misses(sol.transpose_addresses(64, 8), capacity_lines=16)
        self.assertEqual((naive, tiled), (4608, 1024))

    def test_three_orders(self) -> None:
        self.assertEqual(sol.three_orders(), (512, 512, 4060))


if __name__ == "__main__":
    unittest.main()
