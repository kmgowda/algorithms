import math
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.common_modulus(0, 0, 17, 7, 3233), 0)
        self.assertEqual(sol.common_modulus(1, 1, 17, 7, 3233), 1)
        with self.assertRaises(ValueError):
            sol.common_modulus(5, 5, 3, 9, 3233)

    def test_every_toy_message(self) -> None:
        n = 3233
        for m in range(n):
            self.assertEqual(sol.common_modulus(pow(m, 17, n), pow(m, 7, n), 17, 7, n), m)

    def test_lcm_exponent_also_decrypts(self) -> None:
        d = pow(17, -1, math.lcm(60, 52))
        self.assertEqual(d, 413)
        self.assertTrue(all(pow(pow(m, 17, 3233), d, 3233) == m for m in range(3233)))

    def test_euler_step_fails_but_rsa_does_not(self) -> None:
        self.assertFalse(sol.euler_shortcut_check(61, 3233, 3120))
        self.assertEqual(ex.decrypt(ex.encrypt(61, (3233, 17)), (3233, 2753)), 61)
        self.assertEqual(pow(pow(7, 5, 49), 17, 49), 0)          # a repeated prime really breaks RSA


if __name__ == "__main__":
    unittest.main()
