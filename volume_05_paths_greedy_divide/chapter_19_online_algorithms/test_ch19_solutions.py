import random
import unittest

import ch19_examples as ex
import ch19_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_ratio_bound(self) -> None:
        for rent, buy in ((1, 7), (10, 100), (5, 5), (2, 8)):          # buy a multiple of rent: exactly 2 - rent/buy
            self.assertAlmostEqual(ex.worst_ratio(rent, buy), sol.ratio_bound(rent, buy))
        for rent, buy in ((3, 10), (7, 3), (4, 9)):
            self.assertLess(ex.worst_ratio(rent, buy), 2)

    def test_phases(self) -> None:
        self.assertEqual(sol.phases(ex.REQUESTS, ex.SHELF), 4)
        self.assertEqual(sol.phases([], 3), 0)
        r = random.Random(19)
        for _ in range(200):
            seq = [r.choice("ABCDEF") for _ in range(r.randint(0, 30))]
            k = r.randint(1, 4)
            p = sol.phases(seq, k)
            self.assertLessEqual(ex.lru(seq, k), k * p)
            self.assertGreaterEqual(ex.belady(seq, k), max(p - 1, 0))

    def test_neither_dominates(self) -> None:
        a, b = sol.lru_worse_than_fifo(), sol.fifo_worse_than_lru()
        self.assertEqual((a, b), (list("ABACB"), list("ABACA")))
        self.assertGreater(ex.lru(a, 2), ex.fifo(a, 2))
        self.assertGreater(ex.fifo(b, 2), ex.lru(b, 2))


if __name__ == "__main__":
    unittest.main()
