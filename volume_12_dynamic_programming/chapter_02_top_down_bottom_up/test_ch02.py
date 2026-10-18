import random
import unittest
from collections import deque

import ch02_examples as ex
import ch02_solutions as sol


def bfs_steps(n):
    dist, q = {n: 0}, deque([n])
    while q:
        k = q.popleft()
        if k == 1:
            return dist[k]
        nxt = [k - 1] + ([k // 2] if k % 2 == 0 else []) + ([k // 3] if k % 3 == 0 else [])
        for m in nxt:
            if m >= 1 and m not in dist:
                dist[m] = dist[k] + 1
                q.append(m)


class TestTopDownBottomUp(unittest.TestCase):
    def test_agree(self) -> None:
        for n in range(1, 400):
            b = bfs_steps(n)
            self.assertEqual(ex.min_steps_top_down(n), b)
            self.assertEqual(ex.min_steps_bottom_up(n), b)
        a, b = 0, 1
        for n in range(60):
            self.assertEqual(ex.fib_bottom_up(n), a)
            a, b = b, a + b
        for n in range(20):
            self.assertEqual(sol.stairs_top_down(n), sol.stairs_bottom_up(n))

    def test_examples(self) -> None:
        self.assertIn("RecursionError", ex.deep_top_down_fails(100000))
        self.assertEqual(ex.deep_top_down_fails(50), "ok")
        ans, visited = ex.sparse_top_down_count(10 ** 6)
        self.assertLess(visited, 1000)
        self.assertGreater(ans, 0)
        table = ex.shipping_cost_table(10, {1: 60, 2: 100, 5: 220})
        self.assertEqual(table[10], 440)
        self.assertEqual(table[3], 160)
        self.assertEqual(sol.min_cost_climbing([10, 15, 20]), 15)
        self.assertEqual(sol.min_cost_climbing([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]), 6)
        self.assertEqual(sol.fill_order(4), [1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main()
