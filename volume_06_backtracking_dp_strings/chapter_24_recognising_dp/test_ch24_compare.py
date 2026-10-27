"""Tests for ch24_compare: every strategy's answer is checked against brute force, and the work counts printed in
Sections 24.9-24.10 are pinned."""
import itertools
import unittest

import ch24_compare as c


def coins_brute(amount, coins):
    for k in range(amount + 1):
        for combo in itertools.combinations_with_replacement(coins, k):
            if sum(combo) == amount:
                return k
    return None


class TestCompare(unittest.TestCase):
    def test_coins_every_strategy(self):
        for amount in range(0, 31):
            r = c.coins_compare(amount)
            best = coins_brute(amount, c.COINS)
            self.assertEqual(r["best"], best)
            self.assertEqual(r["backtracking"][0], best)
            self.assertEqual(r["plain"][0], best)
            self.assertGreaterEqual(r["greedy"][0], best)

    def test_coins_printed_counts(self):
        r = c.coins_compare(6)
        self.assertEqual(r["greedy"][1], [4, 1, 1])
        self.assertEqual(r["backtracking"], (2, 8))
        self.assertEqual(r["plain"], (2, 24))
        self.assertEqual(c.plain_counts(6, c.COINS), [9, 6, 4, 2, 1, 1, 1])
        r = c.coins_compare(30)
        self.assertEqual((r["greedy"][0], r["best"], r["backtracking"][1], r["plain"][1]), (9, 8, 124, 2550408))

    def test_backtrack_log(self):
        log = []
        c.coins_backtrack(6, c.COINS, log)
        self.assertEqual([x[4] for x in log], ["branch", "branch", "branch", "new best", "branch", "new best",
                                               "cut", "cut"])

    def test_knapsack(self):
        r = c.knapsack_compare()
        self.assertEqual(r["best"], 16)
        self.assertEqual(r["dp"][0], 16)
        self.assertEqual(r["greedy"][0], 15)
        self.assertEqual(r["backtracking"], (16, 47))
        self.assertEqual(r["branch_and_bound"], (16, 13))

    def test_bookings(self):
        r = c.bookings_compare()
        self.assertEqual(r["dp"][0], 22)
        self.assertEqual(r["brute"], (22, 128))
        self.assertEqual(r["plain"], (22, 75))
        self.assertEqual(r["earliest_finish"][0], 19)
        self.assertEqual(r["biggest_first"][0], 20)
        self.assertEqual(r["earliest_count"], r["most_bookings"])

    def test_every_case(self):
        self.assertEqual(c.coins_compare(0)["best"], 0)
        self.assertEqual(c.coins_greedy(5, [4]), [])
        self.assertEqual(c.coins_backtrack(5, [4]), (float("inf"), 2))
        self.assertEqual(c.bookings_compare([])["dp"][0], 0)
        self.assertEqual(c.banner_compare(4)["greedy"], 9)
        self.assertEqual(c.banner_compare(4)["dp"], 10)


if __name__ == "__main__":
    unittest.main()
