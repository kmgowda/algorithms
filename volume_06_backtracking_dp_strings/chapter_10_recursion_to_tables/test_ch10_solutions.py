import itertools
import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


def brute_k(effort, k):
    n, best = len(effort), None
    def go(i, total):
        nonlocal best
        if i == n + 1:
            best = total if best is None else min(best, total)
            return
        for s in range(1, k + 1):
            if i + s <= n + 1:
                go(i + s, total + (effort[i + s - 1] if i + s <= n else 0))
    go(0, 0)
    return best


class TestThinkingProblems(unittest.TestCase):
    def test_two_numbers(self) -> None:
        for n in range(0, 60):
            self.assertEqual(ex.ways_two_numbers(n), ex.ways_table(n)[n])

    def test_k_steps(self) -> None:
        self.assertEqual(sol.least_effort_k(ex.EFFORT, 2), ex.least_effort(ex.EFFORT)[0])
        self.assertEqual((sol.least_effort_k(ex.EFFORT, 3), sol.least_effort_k(ex.EFFORT, 1)), (7, 40))
        self.assertEqual(sol.least_effort_k([], 2), 0)
        r = random.Random(10)
        for _ in range(100):
            e = [r.randint(0, 9) for _ in range(r.randint(0, 9))]
            k = r.randint(1, 4)
            self.assertEqual(sol.least_effort_k(e, k), brute_k(e, k))
        with self.assertRaises(ValueError):
            sol.least_effort_k([1], 0)

    def test_wrong_order(self) -> None:
        self.assertEqual(sol.wrong_order_table(6), [1, 1, 1, 0, 0, 0, 0])


if __name__ == "__main__":
    unittest.main()
