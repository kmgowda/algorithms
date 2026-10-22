import itertools
import math
import unittest

import ch07_examples as ex


class TestChapter7(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.orders(5), ex.arrangements(10, 3), ex.choose(10, 3), ex.choose(52, 5)), (120, 720, 120, 2598960))
        self.assertEqual((ex.choose_mod(1000, 500), len(str(ex.choose(1000, 500)))), (159835829, 300))
        self.assertEqual((ex.with_repetition(3, 4), sum(ex.choose(10, k) for k in range(11))), (15, 1024))

    def test_every_case(self) -> None:
        self.assertEqual((ex.orders(0), ex.choose(5, 0), ex.choose(5, 5), ex.choose(5, 6), ex.choose_mod(5, 6), ex.choose_mod(0, 0)), (1, 1, 1, 0, 0, 1))
        self.assertEqual((ex.arrangements(5, 0), ex.with_repetition(0, 0), ex.with_repetition(0, 3), ex.with_repetition(3, 0)), (1, 1, 0, 1))
        for n in range(8):
            for k in range(n + 2):
                self.assertEqual(ex.choose(n, k), len(list(itertools.combinations(range(n), k))))
                self.assertEqual(ex.choose_mod(n, k), ex.choose(n, k) % ex.P)
            for k in range(5):
                self.assertEqual(ex.with_repetition(n, k), len(list(itertools.combinations_with_replacement(range(n), k))))


class TestDepth(unittest.TestCase):
    def test_pascal_and_lucas(self) -> None:
        self.assertEqual((ex.pascal_mod(6, 4)[6], ex.pascal_mod(0, 1)), ([1, 2, 3, 0, 3, 2, 1], [[0]]))
        for m in (1, 2, 6, 10, 12):
            for i, row in enumerate(ex.pascal_mod(15, m)):
                self.assertEqual(row, [math.comb(i, j) % m for j in range(i + 1)])
        log = []
        self.assertEqual((ex.lucas(12, 5, 5, log), log), (2, [(2, 0, 1), (2, 1, 2)]))
        for p in (2, 3, 5, 7, 13):
            for n in range(40):
                for k in range(n + 2):
                    self.assertEqual(ex.lucas(n, k, p), math.comb(n, k) % p if k <= n else 0)

    def test_chapter_numbers(self) -> None:
        self.assertEqual((ex.lucas(7, 3, 2), ex.pascal_mod(4, 4)[4], ex.derangements(4), ex.catalan(4)), (1, [1, 0, 2, 0, 1], 9, 14))
        self.assertEqual(sum(1 for n in range(1, 101) if n % 2 == 0 or n % 3 == 0 or n % 5 == 0), 74)
        self.assertEqual((ex.choose(9, 2), ex.choose(9, 3), ex.catalan(29)), (36, 84, 1002242216651368))
        log = []
        ex.lucas(10 ** 18, 10 ** 9, 13, log)
        self.assertEqual(len(log), 17)

    def test_inclusion_exclusion_catalan_pigeonhole(self) -> None:
        self.assertEqual([ex.derangements(n) for n in range(7)], [1, 0, 1, 2, 9, 44, 265])
        self.assertEqual([ex.derangements(n) for n in range(8)], [ex.derangements_by_listing(n) for n in range(8)])
        self.assertEqual(ex.derangements(10), 1334961)
        self.assertEqual([ex.catalan(n) for n in range(8)], [1, 1, 2, 5, 14, 42, 132, 429])
        self.assertEqual([ex.catalan(n) for n in range(7)], [ex.balanced_by_listing(n) for n in range(7)])
        self.assertEqual((ex.block_divisible([3, 1, 4, 1, 5, 9, 2], 7), ex.block_divisible([], 3)), ((0, 5), None))
        r = __import__("random").Random(7)
        for _ in range(300):
            n = r.randint(1, 30)
            vals = [r.randint(-100, 100) for _ in range(n)]
            i, j = ex.block_divisible(vals, n)
            self.assertEqual(sum(vals[i:j]) % n, 0)


if __name__ == "__main__":
    unittest.main()
