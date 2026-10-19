import math
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


class TestRSA(unittest.TestCase):
    def test_primality(self) -> None:
        small = [n for n in range(2, 3000) if all(n % d for d in range(2, math.isqrt(n) + 1))]
        self.assertEqual([n for n in range(3000) if ex.is_probable_prime(n)], small)
        self.assertFalse(ex.is_probable_prime(561))            # a Carmichael number fools Fermat's test
        self.assertTrue(ex.is_probable_prime(2 ** 61 - 1))

    def test_round_trip(self) -> None:
        rng = random.Random(1)
        for seed in range(15):
            public, private = ex.make_keys(64, seed=seed)
            for _ in range(10):
                m = rng.randrange(public[1])
                self.assertEqual(ex.decrypt(ex.encrypt(m, public), private), m)
                self.assertTrue(ex.verify(m, ex.sign(m, private), public))
        self.assertEqual(ex.int_to_text(ex.text_to_int("Hi!")), "Hi!")

    def test_solutions(self) -> None:
        pub, priv = sol.toy_keys(61, 53, 17)
        self.assertEqual(pub, (17, 3233))
        self.assertEqual(priv, (2753, 3233))
        self.assertEqual(pow(pow(65, 17, 3233), 2753, 3233), 65)
        self.assertEqual(sol.crack_small_key(pub), priv)
        blocks = sol.encrypt_blocks("aab", pub)
        self.assertEqual(blocks[0], blocks[1])
        with self.assertRaises(ValueError):
            sol.toy_keys(61, 53, 4)
        p, _ = ex.factor_time(3233)
        self.assertEqual(p, 53)


if __name__ == "__main__":
    unittest.main()
