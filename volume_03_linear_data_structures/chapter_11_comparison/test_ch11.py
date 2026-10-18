import random
import unittest
from collections import deque

import ch11_examples as ex
import ch11_solutions as sol


class TestStructures(unittest.TestCase):
    def test_singly_linked(self) -> None:
        rng = random.Random(1)
        s, model = ex.SinglyLinked(), deque()
        for _ in range(2000):
            op = rng.random()
            if op < 0.35:
                v = rng.randint(0, 9)
                s.append(v)
                model.append(v)
            elif op < 0.7:
                v = rng.randint(0, 9)
                s.push_front(v)
                model.appendleft(v)
            elif model:
                self.assertEqual(s.pop_front(), model.popleft())
            if model:
                i = rng.randrange(len(model))
                self.assertEqual(s.get(i), model[i])
            self.assertEqual(s.size, len(model))


class TestCostModel(unittest.TestCase):
    def test_table(self) -> None:
        t = ex.cost_table(1000)
        self.assertEqual(t["dynamic array"]["get middle"], 1)
        self.assertEqual(t["singly linked list"]["remove back"], 1000)
        self.assertEqual(t["doubly linked list"]["remove back"], 1)

    def test_best_structure(self) -> None:
        self.assertIn(ex.best_structure(["add front", "remove back"], 10_000),
                      ("doubly linked list", "deque (ring or blocks)"))
        self.assertEqual(ex.best_structure(["get middle", "add back"], 10_000), "dynamic array")

    def test_choose(self) -> None:
        self.assertEqual(ex.choose_for("undo button"), "stack (list end)")
        self.assertTrue(ex.choose_for("unknown").startswith("start with a list"))


class TestMeasurements(unittest.TestCase):
    def test_front_operations_deque_beats_list_at_scale(self) -> None:
        times = ex.time_front_operations(20_000, repeats=1)
        self.assertLess(times["deque"], times["list"])

    def test_middle_reads_list_beats_linked(self) -> None:
        times = ex.time_index_middle(50_000, lookups=50)
        self.assertLess(times["list"], times["linked"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        taxi = {"add back": 1000, "remove front": 1000}
        self.assertEqual(sol.total_steps("dynamic array", taxi, 500), 1000 * 1 + 1000 * 500)
        self.assertEqual(sol.ranking(taxi, 500)[-1], "dynamic array")
        # adding at the front only: the array (n steps) never beats the linked list (1 step)
        self.assertIsNone(sol.crossover_size({"add front": 1}, "singly linked list", "dynamic array", limit=500))
        # 10 middle reads + 1 front insert: array 10 + n vs linked 10*(n//2) + 1 -> array wins from n = 4
        self.assertEqual(sol.crossover_size({"get middle": 10, "add front": 1}, "singly linked list", "dynamic array"), 4)


if __name__ == "__main__":
    unittest.main()
