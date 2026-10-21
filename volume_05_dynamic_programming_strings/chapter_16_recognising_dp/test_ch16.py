import unittest

import ch16_examples as ex


class TestChapter16(unittest.TestCase):
    def test_banner(self) -> None:
        c = [0]
        self.assertEqual((ex.best_plain(8, ex.PRICE, c), c[0], ex.best_memo(8, ex.PRICE, {})), (22, 256, 22))
        self.assertEqual(ex.best_table(8, ex.PRICE), (22, [2, 6], [0, 1, 5, 8, 10, 13, 17, 18, 22]))
        self.assertEqual([ex.greedy_best_rate(n, ex.PRICE) == ex.best_table(n, ex.PRICE)[0] for n in range(1, 9)],
                         [True, True, True, False, True, True, True, True])

    def test_every_case(self) -> None:
        self.assertEqual((ex.best_table(0, ex.PRICE)[:2], ex.best_table(1, ex.PRICE)[:2], ex.best_table(4, ex.PRICE)[:2]),
                         ((0, []), (1, [1]), (10, [2, 2])))
        self.assertEqual(ex.greedy_best_rate(4, ex.PRICE), 9)
        self.assertEqual((ex.best_table(3, {2: 3})[:2], ex.best_table(4, {2: 3})[:2]), ((None, []), (6, [2, 2])))
        for n in (10, 15):
            p = {k: ex.PRICE.get(k, 0) or 2 * k for k in range(1, n + 1)}
            c = [0]
            ex.best_plain(n, p, c)
            self.assertEqual(c[0], 2 ** n)


if __name__ == "__main__":
    unittest.main()
