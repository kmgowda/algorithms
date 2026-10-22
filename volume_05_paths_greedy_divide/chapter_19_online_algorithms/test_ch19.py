import random
import unittest

import ch19_examples as ex


class TestChapter19(unittest.TestCase):
    def test_ski_rental(self) -> None:
        self.assertEqual([ex.ski_rental(d, 10, 100) for d in (3, 9, 10, 30)], [30, 90, 190, 190])
        self.assertEqual([ex.ski_best(d, 10, 100) for d in (3, 9, 10, 30)], [30, 90, 100, 100])
        self.assertAlmostEqual(ex.worst_ratio(10, 100), 1.9)
        for rent, buy in ((1, 7), (3, 10), (10, 100), (5, 5)):
            self.assertLess(ex.worst_ratio(rent, buy), 2)

    def test_paging(self) -> None:
        self.assertEqual((ex.lru(ex.REQUESTS, ex.SHELF), ex.fifo(ex.REQUESTS, ex.SHELF), ex.belady(ex.REQUESTS, ex.SHELF)), (10, 9, 7))

    def test_every_case(self) -> None:
        self.assertEqual((ex.ski_rental(0, 10, 100), ex.ski_best(0, 10, 100)), (0, 0))
        with self.assertRaises(ValueError):
            ex.ski_rental(5, 0, 100)
        self.assertEqual((ex.lru([], 3), ex.lru(["A"] * 5, 3), ex.lru(list("ABC"), 0)), (0, 1, 3))
        adv = ex.adversary_sequence(ex.lru, 3, 12)
        self.assertEqual((ex.lru(adv, 3), ex.belady(adv, 3)), (12, 6))
        r = random.Random(19)
        for _ in range(200):
            seq = [r.choice("ABCDE") for _ in range(r.randint(0, 30))]
            k = r.randint(1, 4)
            self.assertLessEqual(ex.belady(seq, k), min(ex.lru(seq, k), ex.fifo(seq, k)))


if __name__ == "__main__":
    unittest.main()
