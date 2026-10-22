import itertools
import unittest

import ch08_examples as ex
import ch08_solutions as sol


def brute_stairs(n, broken):
    count = 0
    for k in range(n + 1):
        for steps in itertools.product((1, 2), repeat=k):
            if sum(steps) == n:
                spots = list(itertools.accumulate(steps))
                count += 0 in broken or not any(s in broken for s in spots)
    return count if 0 not in broken else 0


class TestChapter08Solutions(unittest.TestCase):
    def test_broken_stairs(self) -> None:
        self.assertEqual(sol.broken_stairs(0, set()), 1)
        self.assertEqual(sol.broken_stairs(1, set()), 1)
        self.assertEqual(sol.broken_stairs(25, set()), 121393)
        self.assertEqual(sol.broken_stairs(5, {5}), 0)
        self.assertEqual(sol.broken_stairs(10, {3, 7}), 8)
        self.assertEqual(sol.broken_stairs(6, {2, 3}), 0)
        for n in range(0, 11):
            for broken in ({1}, {2, 5}, {4}, set()):
                self.assertEqual(sol.broken_stairs(n, broken), brute_stairs(n, broken))

    def test_memo_key_bug(self) -> None:
        self.assertEqual(sol.ways_coins(4, [2, 1]), 3)
        self.assertEqual(sol.ways_coins(4, [2, 1], key_on_amount_only=True), 4)
        self.assertEqual(sol.ways_coins(0, [2, 1]), 1)
        self.assertEqual(sol.ways_coins(3, []), 0)
        self.assertEqual(sol.ways_coins(100, [50, 20, 10, 5, 2, 1]), 4562)

    def test_calls_formula(self) -> None:
        for n in range(0, 21):
            c = [0]
            w = ex.ways_naive(n, c)
            self.assertEqual(c[0], 2 * w - 1)


if __name__ == "__main__":
    unittest.main()
