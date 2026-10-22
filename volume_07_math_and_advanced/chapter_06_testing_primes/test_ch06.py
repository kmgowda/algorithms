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


class TestDepth(unittest.TestCase):
    def test_verdicts_and_chains(self) -> None:
        self.assertEqual((ex.verdict(2 ** 61 - 1), ex.verdict(10 ** 30 + 57), ex.verdict(561), ex.verdict(1)),
                         ("prime", "probably prime", "composite", "composite"))
        self.assertEqual(ex.EXACT_BELOW, 318665857834031151167461)
        self.assertEqual(ex.squaring_chain(561, 2), [263, 166, 67, 1, 1])
        self.assertEqual(ex.squaring_chain(341, 2), [32, 1, 1])
        self.assertEqual(ex.squaring_chain(97, 2), [8, 64, 22, 96, 1, 1])
        self.assertEqual(67 * 67 % 561, 1)

    def test_liars_and_korselt(self) -> None:
        self.assertEqual((ex.liar_counts(561), ex.liar_counts(341), ex.liar_counts(9)), ((320, 10, 560), (100, 50, 340), (2, 2, 8)))
        self.assertEqual(ex.worst_strong_liar_share(3000), (0.25, 9))
        carmichael = [n for n in range(3, 10000, 2) if not ex.trial(n) and all(ex.fermat(n, a) for a in range(2, n) if math.gcd(a, n) == 1)]
        self.assertEqual([n for n in range(3, 10000) if ex.korselt(n)], carmichael)

    def test_chapter_numbers(self) -> None:
        self.assertEqual((pow(2, 90, 91), ex.is_strong_liar(25, 7), ex.korselt(1105), round(ex.filter_share(2000), 3)), (64, True, True, 0.853))
        self.assertEqual(ex.pollard_rho(91), 7)

    def test_pollard(self) -> None:
        log = []
        self.assertEqual(ex.pollard_rho(8051, 1, log), 97)
        self.assertEqual(log, [(1, 5, 26, 1), (2, 26, 7474, 1), (3, 677, 871, 97)])
        self.assertEqual((ex.pollard_rho(1), ex.pollard_rho(10), ex.factor_completely(1), ex.factor_completely(97)), (None, 2, [], [97]))
        self.assertEqual(ex.factor_completely(2 ** 64 + 1), [274177, 67280421310721])
        import random
        r = random.Random(6)
        for _ in range(200):
            n = r.randint(2, 10 ** 12)
            f = ex.factor_completely(n)
            self.assertEqual(math.prod(f), n)
            self.assertTrue(all(ex.miller_rabin(q) for q in f))


if __name__ == "__main__":
    unittest.main()
