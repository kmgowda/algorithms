import math
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestMemoization(unittest.TestCase):
    def test_fibonacci(self) -> None:
        a, b = 0, 1
        for n in range(25):
            self.assertEqual(ex.fib_naive(n), a)
            self.assertEqual(ex.fib_memo(n), a)
            self.assertEqual(ex.fib_cached(n), a)
            a, b = b, a + b
        calls, distinct = ex.distinct_subproblems(20)
        self.assertEqual(calls, 2 * ex.fib_memo(21) - 1)
        self.assertEqual(distinct, 21)

    def test_grid(self) -> None:
        for r in range(1, 8):
            for c in range(1, 8):
                self.assertEqual(ex.grid_routes_naive(r, c), math.comb(r + c - 2, r - 1))
        self.assertEqual(ex.grid_routes_memo(30, 30), math.comb(58, 29))

    def test_cache_and_solutions(self) -> None:
        quote, calls = ex.make_cached_quote(lambda route: len(route) * 12.5)
        for r in ["BLR-DEL", "BLR-DEL", "BOM-GOI", "BLR-DEL"]:
            quote(r)
        self.assertEqual(calls[0], 2)
        self.assertEqual(sol.tribonacci(25), 1389537)
        self.assertEqual(sol.tile_ways(10), 89)
        self.assertEqual(sol.binomial(30, 15), math.comb(30, 15))
        self.assertEqual(sol.collatz_steps(27), 111)


if __name__ == "__main__":
    unittest.main()
