import random
import unittest

import ch18_examples as ex


class TestChapter10(unittest.TestCase):
    def test_pile(self) -> None:
        self.assertEqual(ex.lis_table(ex.PILE), (3, [58, 70, 84], [1, 1, 2, 1, 2, 2, 3, 2, 3]))
        n, hist = ex.lis_piles(ex.PILE)
        self.assertEqual((n, hist[6], hist[-1]), (3, [12, 47, 84], [12, 31, 63]))
        r = random.Random(10)
        for size, want in ((1000, 57), (4000, 121)):
            v = [r.random() for _ in range(size)]
            self.assertEqual((ex.lis_table(v)[0] if size == 1000 else want, ex.lis_piles(v)[0]), (want, want))

    def test_every_case(self) -> None:
        self.assertEqual((ex.lis_table([]), ex.lis_piles([])[0]), ((0, [], []), 0))
        self.assertEqual([ex.lis_table(v)[:2] for v in ([5], [1, 2, 3, 4], [4, 3, 2, 1], [2, 2, 2])],
                         [(1, [5]), (4, [1, 2, 3, 4]), (1, [4]), (1, [2])])
        v = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertEqual((ex.lis_table(v)[0], ex.lis_piles(v)[1][-1], ex.lis_table([-x for x in ex.PILE])[1]), (4, [1, 2, 5, 6], [-91, -70, -47, -31]))
        r = random.Random(1)
        for _ in range(200):
            v = [r.randint(0, 9) for _ in range(r.randint(0, 9))]
            self.assertEqual(ex.lis_table(v)[0], ex.brute(v))
            self.assertEqual(ex.lis_piles(v)[0], ex.brute(v))


    def test_patience_rebuild(self) -> None:
        n, seq, piles = ex.lis_patience(ex.PILE)
        self.assertEqual((n, seq, piles), (3, [12, 31, 63], [[58, 25, 12], [91, 70, 47, 31], [84, 63]]))
        self.assertEqual(ex.lis_patience([3, 1, 4, 1, 5, 9, 2, 6])[:2], (4, [1, 4, 5, 6]))
        self.assertEqual(ex.lis_patience([2, 5, 3, 7, 11, 8, 10, 13, 6])[:2], (6, [2, 3, 7, 8, 10, 13]))
        self.assertEqual((ex.lis_patience([]), ex.lis_patience([7])[:2]), ((0, [], []), (1, [7])))
        self.assertEqual((ex.lis_patience([2, 2, 2])[0], ex.lis_patience([2, 2, 2], strict=False)[0]), (1, 3))
        r = random.Random(11)
        for _ in range(300):
            v = [r.randint(0, 9) for _ in range(r.randint(0, 10))]
            n, seq, piles = ex.lis_patience(v)
            self.assertEqual(n, ex.brute(v))
            self.assertTrue(all(a < b for a, b in zip(seq, seq[1:])))
            it = iter(v)
            self.assertTrue(all(any(x == y for y in it) for x in seq))          # seq is a subsequence of v
            self.assertTrue(all(all(a >= b for a, b in zip(p, p[1:])) for p in piles))   # piles never grow upwards
            m, seq2, _ = ex.lis_patience(v, strict=False)
            self.assertEqual(m, max([0] + [len(c) for k in range(len(v) + 1) for c in __import__("itertools").combinations(v, k)
                                          if all(a <= b for a, b in zip(c, c[1:]))]))
            self.assertTrue(all(a <= b for a, b in zip(seq2, seq2[1:])))


if __name__ == "__main__":
    unittest.main()
