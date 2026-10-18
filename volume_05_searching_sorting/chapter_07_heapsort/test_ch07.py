import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


class TestHeapsort(unittest.TestCase):
    def test_build_and_sort(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
            h = list(v)
            ex.build_max_heap(h)
            self.assertTrue(ex.is_max_heap(h))
            self.assertEqual(sorted(h), sorted(v))
            ex.heapsort(h)
            self.assertEqual(h, sorted(v))

    def test_top_k_and_triage(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            v = [rng.randint(0, 100) for _ in range(rng.randint(1, 20))]
            k = rng.randint(1, len(v))
            self.assertEqual(ex.top_k_largest(v, k), sorted(v, reverse=True)[:k])
        self.assertEqual(ex.emergency_order([(2, "ankle"), (5, "chest"), (3, "cut"), (5, "allergy")]),
                         ["chest", "allergy", "cut", "ankle"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        rng = random.Random(3)
        for _ in range(200):
            v = [rng.randint(0, 50) for _ in range(rng.randint(1, 15))]
            k = rng.randint(1, len(v))
            self.assertEqual(sol.kth_largest(v, k), sorted(v, reverse=True)[k - 1])
        self.assertEqual(sol.last_stone([2, 7, 4, 1, 8, 1]), 1)
        self.assertEqual(sol.last_stone([3, 3]), 0)
        self.assertEqual(sol.heap_children([10, 5, 8, 4, 1], 1), [4, 1])
        steps = sol.heapsort_steps([4, 10, 3, 5])
        self.assertEqual(steps[0], [10, 5, 3, 4])
        self.assertEqual(steps[-1], [3, 4, 5, 10])


if __name__ == "__main__":
    unittest.main()
