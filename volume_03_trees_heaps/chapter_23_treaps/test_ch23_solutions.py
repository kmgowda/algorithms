import random
import unittest

import ch23_examples as ex
import ch23_solutions as sol


class TestChapter23Solutions(unittest.TestCase):
    def test_insert_then_delete(self) -> None:
        self.assertEqual(sol.insert_then_delete([1], {1: 5}, 2, 9), (1, 0, True))      # the counterexample
        self.assertEqual(sol.insert_then_delete([], {}, 2, 9), (0, 0, True))           # smallest input
        rng = random.Random(1)
        for _ in range(300):
            keys = rng.sample(range(60), rng.randrange(0, 20))
            prios = {k: rng.random() for k in keys}
            new = rng.choice([k for k in range(60) if k not in prios])
            up, down, same = sol.insert_then_delete(keys, prios, new, rng.random())
            self.assertTrue(same)
            self.assertLessEqual(down, up)

    def test_implicit_treap(self) -> None:
        q = sol.ImplicitTreap()
        self.assertEqual((len(q), q.to_list()), (0, []))
        with self.assertRaises(IndexError):
            q.delete_at(0)
        with self.assertRaises(IndexError):
            q.insert_at(1, "x")
        q.insert_at(0, "Ana")                                # one item
        self.assertEqual((q.get(0), q.delete_at(0), len(q)), ("Ana", "Ana", 0))
        q = sol.ImplicitTreap(["Ana", "Ben", "Chen"])
        q.insert_at(1, "class 4B")
        q.insert_at(4, "Dev")                                # at the very end
        self.assertEqual(q.to_list(), ["Ana", "class 4B", "Ben", "Chen", "Dev"])
        self.assertEqual(q.delete_at(0), "Ana")
        self.assertEqual(q.get(3), "Dev")
        rng, ref, q = random.Random(2), [], sol.ImplicitTreap(seed=5)
        for i in range(3000):
            if ref and rng.random() < 0.4:
                j = rng.randrange(len(ref))
                self.assertEqual(q.delete_at(j), ref.pop(j))
            else:
                j = rng.randrange(len(ref) + 1)
                q.insert_at(j, i)
                ref.insert(j, i)
        self.assertEqual(q.to_list(), ref)
        big = sol.ImplicitTreap(range(4096))
        self.assertLess(big.height(), 40)                   # sequential appends still give a shallow tree

    def test_arrival_priority_bug(self) -> None:
        t = sol.arrival_priority_treap(ex.SHELF)
        self.assertEqual((t.height(), t.rotations), (8, 8))  # a path, one rotation per card
        self.assertTrue(t.valid())
        t = sol.arrival_priority_treap(ex.RETURNS)
        self.assertEqual(t.shape(), ex.plain_bst_shape(list(reversed(ex.RETURNS))))
        self.assertEqual(sol.arrival_priority_treap([]).height(), -1)


if __name__ == "__main__":
    unittest.main()
