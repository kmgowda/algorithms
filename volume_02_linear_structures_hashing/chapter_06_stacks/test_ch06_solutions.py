import itertools
import random
import unittest

import ch06_solutions as sol


def has_312(order: list[int]) -> bool:
    return any(c > b > a for a_i, a in enumerate(order) for b in order[a_i + 1:] for c in order[:a_i]
               if order.index(c) < a_i and order.index(b) > a_i)


class TestThinkingProblems(unittest.TestCase):
    def test_leave_orders_smallest(self) -> None:
        self.assertTrue(sol.can_leave_in_order([]))
        self.assertTrue(sol.can_leave_in_order([1]))
        self.assertFalse(sol.can_leave_in_order([3, 1, 2]))

    def test_leave_orders_match_the_triple_rule(self) -> None:
        for n in range(1, 7):
            count = 0
            for p in itertools.permutations(range(1, n + 1)):
                ok = sol.can_leave_in_order(list(p))
                self.assertEqual(ok, not has_312(list(p)))
                count += ok
            self.assertEqual(count, [1, 2, 5, 14, 42, 132][n - 1])

    def test_min_stack_example(self) -> None:
        m = sol.MinStack()
        self.assertTrue(m.is_empty())
        with self.assertRaises(IndexError):
            m.smallest()
        with self.assertRaises(IndexError):
            m.pop()
        for b in (47, 12, 63):
            m.push(b)
        self.assertEqual(m.pop(), 63)
        m.push(25)
        self.assertEqual(m.smallest(), 12)
        m.pop()
        m.pop()
        self.assertEqual(m.smallest(), 47)

    def test_min_stack_against_scan(self) -> None:
        rng = random.Random(6)
        for _ in range(200):
            m, ref = sol.MinStack(), []
            for _ in range(rng.randint(0, 30)):
                if ref and rng.random() < 0.4:
                    self.assertEqual(m.pop(), ref.pop())
                else:
                    x = rng.randint(0, 9)
                    m.push(x)
                    ref.append(x)
                if ref:
                    self.assertEqual(m.smallest(), min(ref))
            self.assertEqual(m.is_empty(), not ref)

    def test_one_number_is_wrong(self) -> None:
        w = sol.OneNumberMin()
        for b in (47, 12, 63):
            w.push(b)
        w.pop()
        self.assertEqual(w.pop(), 12)
        self.assertEqual(w.smallest(), 12)       # but the pile holds only 47


if __name__ == "__main__":
    unittest.main()
