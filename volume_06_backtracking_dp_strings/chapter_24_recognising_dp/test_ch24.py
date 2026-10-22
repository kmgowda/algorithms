import unittest

import ch24_examples as ex


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


    def test_state_machine(self) -> None:
        import random
        best, plan, rows = ex.trade_cooldown(ex.PRICES)
        self.assertEqual((best, plan), (13, [(1, "buy"), (2, "sell"), (5, "buy"), (8, "sell")]))
        self.assertEqual(rows[2], (-3, -1, 5))
        self.assertEqual(ex.trade_k(ex.PRICES, 4), (19, [0, 8, 13, 17, 19]))
        self.assertEqual((ex.trade_brute(ex.PRICES), ex.trade_brute(ex.PRICES, cooldown=True)), (19, 13))
        self.assertEqual((ex.trade_cooldown([])[0], ex.trade_cooldown([5])[0], ex.trade_k([], 2)[0], ex.trade_k([5, 9], 0)[0]),
                         (0, 0, 0, 0))
        self.assertEqual((ex.trade_cooldown([9, 5, 1])[0], ex.trade_k([9, 5, 1], 3)[0]), (0, 0))
        r = random.Random(16)
        for _ in range(300):
            p = [r.randint(1, 12) for _ in range(r.randint(0, 9))]
            k = r.randint(0, 4)
            self.assertEqual(ex.trade_cooldown(p)[0], ex.trade_brute(p, cooldown=True))
            self.assertEqual(ex.trade_k(p, k)[0], ex.trade_brute(p, k=k))
            money, plan, _ = ex.trade_cooldown(p)
            gain = sum(-p[d - 1] if a == "buy" else p[d - 1] for d, a in plan)
            self.assertEqual(gain, money)


if __name__ == "__main__":
    unittest.main()
