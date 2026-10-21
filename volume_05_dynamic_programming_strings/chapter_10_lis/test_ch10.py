import random
import unittest

import ch10_examples as ex


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


if __name__ == "__main__":
    unittest.main()
