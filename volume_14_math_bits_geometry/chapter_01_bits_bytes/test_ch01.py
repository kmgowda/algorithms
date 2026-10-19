import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestBits(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            n = rng.randint(0, 255)
            self.assertEqual(ex.to_binary(n), format(n, "08b"))
            self.assertEqual(ex.from_binary(ex.to_binary(n)), n)
            s = rng.randint(-128, 127)
            self.assertEqual(ex.twos_complement(s), format(s & 0xFF, "08b"))
            big = rng.randint(-2 ** 40, 2 ** 40)
            w = ex.wrap_signed(big)
            self.assertTrue(-2 ** 31 <= w < 2 ** 31)
            self.assertEqual((w - big) % 2 ** 32, 0)
            b = rng.randint(2, 16)
            self.assertEqual(int(sol.to_base(n, b), b), n)
            x, y = rng.randint(0, 1000), rng.randint(0, 1000)
            self.assertEqual(sol.add_binary(bin(x)[2:], bin(y)[2:]), bin(x + y)[2:])

    def test_examples(self) -> None:
        self.assertEqual(ex.twos_complement(-1), "11111111")
        self.assertEqual(ex.wrap_signed(2_147_483_648), -2_147_483_648)
        self.assertFalse(0.1 + 0.2 == 0.3)
        self.assertTrue(ex.close_enough(0.1 + 0.2, 0.3))
        self.assertEqual(ex.float_bits(1.0), "0 01111111111 " + "0" * 52)
        self.assertEqual(ex.money_in_cents(["0.10"] * 10), 100)
        self.assertEqual(ex.money_in_cents(["12.5", "3"]), 1550)
        self.assertEqual(sol.reverse_integer(-120), -21)
        self.assertEqual(sol.reverse_integer(1534236469), 0)


if __name__ == "__main__":
    unittest.main()
