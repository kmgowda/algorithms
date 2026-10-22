import unittest

import ch05_examples as ex


class TestChapter5(unittest.TestCase):
    def test_counts(self) -> None:
        self.assertEqual(ex.count_sets(10, ex.COINS), (10, [1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 10]))
        self.assertEqual(ex.count_orders(10, ex.COINS), (128, [1, 1, 2, 3, 5, 9, 15, 26, 44, 75, 128]))
        self.assertEqual(ex.count_sets(100, [1, 2, 5, 10, 20, 50, 100])[0], 4563)
        self.assertEqual(ex.count_sets(200, [1, 2, 5, 10, 20, 50, 100, 200])[0], 73682)

    def test_every_case(self) -> None:
        self.assertEqual((ex.count_sets(0, [1, 2])[0], ex.count_sets(3, [2])[0], ex.count_orders(3, [2])[0], ex.count_sets(5, [])[0]), (1, 0, 0, 0))
        self.assertEqual((ex.count_sets(4, [1, 2])[0], ex.count_orders(4, [1, 2])[0]), (3, 5))
        self.assertEqual([ex.decodings(m) for m in ("12", "226", "2101", "10", "0", "", "1111111111", "301")], [2, 3, 1, 1, 0, 1, 89, 0])
        self.assertEqual((ex.count_sets(6, [1, 2])[0], ex.count_orders(6, [1, 2])[0], ex.decodings("1212"), ex.count_sets(7, ex.COINS)[0]), (4, 13, 5, 6))
        import itertools
        self.assertEqual(sum(1 for k in range(5) for s in itertools.combinations([1, 2, 5, 10], k) if sum(s) == 8), 1)
        for a in range(0, 30):
            self.assertEqual(ex.count_sets(a, ex.COINS)[0], ex.brute_sets(a, ex.COINS))


    def test_digit_dp(self) -> None:
        self.assertEqual((ex.count_digit_sum(253, 10)[0], ex.count_digit_sum(99, 10)[0]), (25, 9))
        self.assertEqual((ex.count_digit_sum(10 ** 6, 10)[0], ex.count_digit_sum(0, 0)[0], ex.count_digit_sum(-1, 0)[0]),
                         (2997, 1, 0))
        self.assertEqual((ex.free_digit_table(2, 10)[2][10], ex.free_digit_table(2, 10)[2][9]), (9, 10))
        for n in range(0, 400, 7):
            for t in range(0, 20):
                self.assertEqual(ex.count_digit_sum(n, t)[0], sum(1 for x in range(n + 1) if sum(map(int, str(x))) == t))


if __name__ == "__main__":
    unittest.main()
