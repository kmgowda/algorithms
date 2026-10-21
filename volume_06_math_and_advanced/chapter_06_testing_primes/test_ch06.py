import math
import unittest

import ch06_examples as ex


class TestChapter6(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual([ex.fermat(n, a) for n, a in ((97, 2), (91, 2), (341, 2), (561, 2), (561, 5))], [True, False, True, True, True])
        self.assertEqual((ex.miller_rabin(341), ex.miller_rabin(561)), (False, False))
        carmichael = [n for n in range(3, 10000, 2) if not ex.trial(n) and all(ex.fermat(n, a) for a in range(2, n) if math.gcd(a, n) == 1)]
        self.assertEqual(carmichael, [561, 1105, 1729, 2465, 2821, 6601, 8911])
        self.assertEqual((ex.next_prime(10 ** 30) - 10 ** 30, ex.miller_rabin(2 ** 61 - 1), ex.miller_rabin(2 ** 61 + 1)), (57, True, False))

    def test_every_case(self) -> None:
        self.assertEqual([ex.miller_rabin(n) for n in (0, 1, 2, 3, 4, 37, 39)], [False, False, True, True, False, True, False])
        self.assertEqual(ex.next_prime(1000), 1009)
        for n in range(20000):
            self.assertEqual(ex.miller_rabin(n), ex.trial(n))


if __name__ == "__main__":
    unittest.main()
