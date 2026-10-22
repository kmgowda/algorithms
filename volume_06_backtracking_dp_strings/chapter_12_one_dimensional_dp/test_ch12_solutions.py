import random
import unittest

import ch12_examples as ex
import ch12_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_recurrence(self) -> None:
        r = random.Random(12)
        for _ in range(200):
            t = [r.randint(0, 9) for _ in range(r.randint(0, 12))]
            self.assertEqual(ex.best_evenings(t)[0], sol.brute_evenings(t))

    def test_circle(self) -> None:
        self.assertEqual(sol.best_circle(ex.TALKS), 23)
        self.assertEqual((sol.best_circle([]), sol.best_circle([4]), sol.best_circle([5, 1, 5])), (0, 4, 5))
        r = random.Random(2)
        for _ in range(200):
            t = [r.randint(0, 9) for _ in range(r.randint(0, 11))]
            self.assertEqual(sol.best_circle(t), sol.brute_circle(t))

    def test_greedy_trap(self) -> None:
        self.assertEqual(sol.greedy_trap(), [1, 2, 2])
        self.assertEqual((sol.greedy_biggest([1, 2, 2]), ex.best_evenings([1, 2, 2])[0]), (2, 3))


if __name__ == "__main__":
    unittest.main()
