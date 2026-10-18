import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestPriorityQueues(unittest.TestCase):
    def test_three_implementations_agree(self) -> None:
        rng = random.Random(1)
        queues = [ex.SortedListPQ(), ex.UnsortedListPQ(), ex.HeapPQ()]
        for step in range(2000):
            if rng.random() < 0.6 or not len(queues[0]):
                p = rng.randint(0, 9)
                for q in queues:
                    q.push(step, p)
            else:
                outs = [q.pop() for q in queues]
                self.assertEqual(len(set(outs)), 1)
        with self.assertRaises(IndexError):
            ex.HeapPQ().pop()

    def test_triage_and_jobs(self) -> None:
        self.assertEqual(ex.triage([("sprain", 4), ("chest pain", 1), ("cut", 3), ("breathing", 1), ("fever", 3)]),
                         ["chest pain", "breathing", "cut", "fever", "sprain"])
        self.assertEqual(ex.run_jobs([(0, "backup", 3, 5), (1, "click", 1, 1), (2, "email", 2, 2), (2, "keypress", 1, 1)]),
                         [("backup", 5), ("click", 6), ("keypress", 7), ("email", 9)])
        self.assertEqual(ex.run_jobs([(5, "late", 1, 2)]), [("late", 7)])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.max_priority_order([("Ana", 50), ("Ben", 200), ("Cy", 120)]), ["Ben", "Cy", "Ana"])
        self.assertEqual(sol.boarding_order([("Ana", "economy"), ("Ben", "first"), ("Cy", "business"), ("Dev", "first")]),
                         ["Ben", "Dev", "Cy", "Ana"])
        self.assertEqual(sol.merge_deadlines([(1, "a1"), (5, "a2")], [(2, "b1"), (3, "b2")]), ["a1", "b1", "b2", "a2"])


if __name__ == "__main__":
    unittest.main()
