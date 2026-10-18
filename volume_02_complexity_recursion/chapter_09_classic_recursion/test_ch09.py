import math
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestPower(unittest.TestCase):
    def test_power(self) -> None:
        for base in (2, 3, 7):
            for exponent in range(0, 40):
                self.assertEqual(ex.power_slow(base, exponent)[0], base ** exponent)
                self.assertEqual(ex.power_fast(base, exponent)[0], base ** exponent)
        self.assertEqual(ex.power_slow(2, 30)[1], 30)
        self.assertLessEqual(ex.power_fast(2, 30)[1], 2 * 5)
        self.assertLessEqual(ex.power_fast(3, 1_000_000)[1], 2 * (1_000_000).bit_length())

    def test_power_mod(self) -> None:
        for base in range(0, 20):
            for exponent in range(0, 30):
                for modulus in (1, 2, 7, 561, 1_000_000_007):
                    self.assertEqual(ex.power_mod(base, exponent, modulus), pow(base, exponent, modulus))


class TestGcd(unittest.TestCase):
    def test_gcd(self) -> None:
        for a in range(0, 60):
            for b in range(0, 60):
                self.assertEqual(ex.gcd(a, b), math.gcd(a, b))
        self.assertEqual(ex.gcd_steps(1071, 462), [(1071, 462), (462, 147), (147, 21), (21, 0)])
        self.assertEqual(ex.aspect_ratio(1920, 1080), "16:9")
        self.assertEqual(ex.aspect_ratio(2560, 1600), "8:5")


class TestFibonacci(unittest.TestCase):
    def test_memo(self) -> None:
        a, b = 0, 1
        for n in range(100):
            self.assertEqual(ex.fibonacci_memo(n), a)
            self.assertEqual(ex.fibonacci_cached(n), a)
            a, b = b, a + b
        self.assertEqual(ex.memo_call_count(30), 2 * 30 - 1)


class TestHanoiAndFlatten(unittest.TestCase):
    def test_hanoi(self) -> None:
        for disks in range(0, 11):
            moves = ex.hanoi(disks)
            self.assertEqual(len(moves), 2 ** disks - 1)
            self.assertTrue(ex.hanoi_is_valid(disks, moves))
        self.assertFalse(ex.hanoi_is_valid(2, [(2, "A", "C")]))

    def test_flatten_and_products(self) -> None:
        self.assertEqual(ex.flatten([1, [2, [3, 4]], 5, [[[6]]]]), [1, 2, 3, 4, 5, 6])
        self.assertEqual(ex.flatten([]), [])
        self.assertEqual(ex.all_products(ex.SHOP), ["Phone X", "Phone Y", "Speaker", "Buds", "Over-ear"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.lcm(12, 18), 36)
        self.assertEqual(sol.lcm(0, 5), 0)
        self.assertEqual([sol.climb_stairs(n) for n in range(1, 8)], [1, 2, 3, 5, 8, 13, 21])
        self.assertEqual(sol.hanoi_moves_needed(64), 18_446_744_073_709_551_615)
        self.assertEqual(sol.nested_sum([1, [2, [3]], 4]), 10)
        self.assertEqual(sol.count_paths_in_grid(3, 7), math.comb(8, 2))
        self.assertEqual(sol.count_paths_in_grid(10, 10), math.comb(18, 9))
        for n in range(0, 300):
            self.assertEqual(sol.binary_digits(n), bin(n)[2:])


if __name__ == "__main__":
    unittest.main()
