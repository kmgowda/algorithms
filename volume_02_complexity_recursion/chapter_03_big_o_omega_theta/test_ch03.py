import math
import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestBounds(unittest.TestCase):
    def test_exact_steps(self) -> None:
        self.assertEqual(ex.exact_steps_report_card(100), 505)
        self.assertEqual(ex.exact_steps_pairs(10), 45)

    def test_upper_lower_tight(self) -> None:
        linear = lambda n: n
        self.assertTrue(ex.is_upper_bound(ex.exact_steps_report_card, linear, 6, 5))
        self.assertFalse(ex.is_upper_bound(ex.exact_steps_report_card, linear, 6, 1))
        self.assertTrue(ex.is_lower_bound(ex.exact_steps_report_card, linear, 5, 1))
        self.assertTrue(ex.is_tight_bound(ex.exact_steps_pairs, lambda n: n * n, 0.25, 0.5, 2))

    def test_witness_search(self) -> None:
        c, n0 = ex.find_upper_witness(lambda n: 3 * n * n + 10 * n, lambda n: n * n)
        self.assertTrue(ex.is_upper_bound(lambda n: 3 * n * n + 10 * n, lambda n: n * n, c, n0))
        self.assertIsNone(ex.find_upper_witness(lambda n: n * n, lambda n: n, check_up_to=500))

    def test_ratio_trend(self) -> None:
        shrinking = ex.ratio_trend(lambda n: n, lambda n: n * n)
        self.assertTrue(all(a > b for a, b in zip(shrinking, shrinking[1:])))
        settling = ex.ratio_trend(ex.exact_steps_pairs, lambda n: n * n)
        self.assertAlmostEqual(settling[-1], 0.5, places=3)
        growing = ex.ratio_trend(lambda n: n * math.log2(n), lambda n: n)
        self.assertTrue(all(a < b for a, b in zip(growing, growing[1:])))

    def test_dominant_and_delivery(self) -> None:
        self.assertEqual(ex.dominant_term({3: 7, 1: 2, 0: 9}), 3)
        self.assertEqual(ex.dominant_term({0: 5}), 0)
        with self.assertRaises(ValueError):
            ex.dominant_term({2: 0})
        self.assertEqual(ex.delivery_window(5), (20, 40))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.exercise2_witness(), (5, 7))
        self.assertEqual(sol.exercise3_theta(), (0.5, 1.0, 6))
        self.assertFalse(sol.is_n_squared_big_o_of_n())
        self.assertTrue(sol.log_vs_sqrt_lower_bound())
        claims = sol.classify_claims()
        self.assertTrue(claims["n = O(n^2)"])
        self.assertFalse(claims["n log n = Theta(n)"])


if __name__ == "__main__":
    unittest.main()
