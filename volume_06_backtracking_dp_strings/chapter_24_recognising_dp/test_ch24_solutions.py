import random
import unittest

import ch24_examples as ex
import ch24_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_calls(self) -> None:
        full = {k: k for k in range(1, 15)}
        for n in range(0, 14):
            calls = [0]
            ex.best_plain(n, full, calls)
            self.assertEqual(calls[0], 2 ** n)

    def test_cut_cost(self) -> None:
        self.assertEqual([sol.best_with_cut_cost(8, ex.PRICE, c) for c in (0, 1, 3)], [22, 21, 20])
        r = random.Random(24)
        for _ in range(150):
            price = {k: r.randint(1, 20) for k in range(1, 9) if r.random() < 0.7}
            n, c = r.randint(1, 10), r.randint(0, 4)
            self.assertEqual(sol.best_with_cut_cost(n, price, c), sol.brute_cut_cost(n, price, c))

    def test_impossible_length(self) -> None:
        self.assertEqual(ex.best_memo(3, {2: 5}, {}), float("-inf"))
        self.assertEqual(ex.best_plain(3, {2: 5}, [0]), float("-inf"))
        self.assertEqual(ex.best_table(3, {2: 5})[0], None)


if __name__ == "__main__":
    unittest.main()
