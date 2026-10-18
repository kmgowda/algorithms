import random
import unittest
from collections import deque

import ch09_examples as ex
import ch09_solutions as sol


class TestQueues(unittest.TestCase):
    def test_against_model(self) -> None:
        rng = random.Random(9)
        for cls in (ex.LinkedQueue, ex.TwoStackQueue):
            q, model = cls(), deque()
            for _ in range(3000):
                if rng.random() < 0.55:
                    v = rng.randint(0, 99)
                    q.enqueue(v)
                    model.append(v)
                elif model:
                    self.assertEqual(q.dequeue(), model.popleft())
                self.assertEqual(len(q), len(model))
            empty = cls()
            with self.assertRaises(IndexError):
                empty.dequeue()
        lq = ex.LinkedQueue()
        lq.enqueue("x")
        self.assertEqual(lq.peek(), "x")
        self.assertFalse(lq.is_empty())
        with self.assertRaises(IndexError):
            ex.LinkedQueue().peek()

    def test_cost(self) -> None:
        self.assertEqual(ex.slow_list_queue_cost(4), 6)

    def test_applications(self) -> None:
        self.assertEqual(ex.serve_ticket_line(["Ana", "Ben", "Cy"]), ["Ana", "Ben", "Cy"])
        self.assertEqual(ex.print_jobs([("report", 12), ("photo", 3), ("poster", 6)], 6),
                         [("report", 2.0), ("photo", 2.5), ("poster", 3.5)])
        self.assertEqual(ex.call_center([(0, "A", 5), (1, "B", 3), (2, "C", 4), (3, "D", 2)], 2),
                         {"A": 0, "B": 0, "C": 2, "D": 2})
        self.assertEqual(ex.rate_limiter([0, 0.2, 0.4, 0.6, 1.1, 1.3], 3, 1.0),
                         [True, True, True, False, True, True])
        network = {"Maya": ["Leo", "Zoe"], "Leo": ["Sam"], "Zoe": ["Sam", "Ali"], "Sam": ["Kim"]}
        self.assertEqual(ex.bfs_levels(network, "Maya"),
                         {"Maya": 0, "Leo": 1, "Zoe": 1, "Sam": 2, "Ali": 2, "Kim": 3})


class TestSolutions(unittest.TestCase):
    def test_queue_stack(self) -> None:
        rng = random.Random(2)
        s, model = sol.QueueStack(), []
        for _ in range(500):
            if rng.random() < 0.6 or not model:
                v = rng.randint(0, 9)
                s.push(v)
                model.append(v)
            else:
                self.assertEqual(s.top(), model[-1])
                self.assertEqual(s.pop(), model.pop())
            self.assertEqual(s.empty(), not model)

    def test_others(self) -> None:
        self.assertEqual(sol.hot_potato(["Ana", "Ben", "Cy", "Dev", "Eve"], 3), "Ana")   # Dev, Cy, Eve, Ben leave in that order
        self.assertEqual(sol.hot_potato(["Solo"], 5), "Solo")
        self.assertEqual(sol.recent_counter([1, 100, 3001, 3002]), [1, 2, 3, 3])
        self.assertEqual(sol.first_unique_stream("aabcbd"), ["a", "#", "b", "b", "c", "c"])
        self.assertEqual(sol.average_wait([0, 1, 2, 10], 3), (0 + 2 + 4 + 0) / 4)
        self.assertEqual(sol.average_wait([], 3), 0.0)


if __name__ == "__main__":
    unittest.main()
