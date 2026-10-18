import random
import sys
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestTreap(unittest.TestCase):
    def test_random_ops(self) -> None:
        rng = random.Random(1)
        t, model = ex.Treap(seed=2), set()
        for _ in range(3000):
            k = rng.randint(0, 300)
            if rng.random() < 0.6:
                t.insert(k)
                model.add(k)
            else:
                t.delete(k)
                model.discard(k)
            if rng.random() < 0.05:
                ex.check_treap(t.root)
        ex.check_treap(t.root)
        self.assertEqual(list(ex.inorder(t.root)), sorted(model))
        self.assertEqual(t.contains(5), 5 in model)

    def test_sorted_input_is_short(self) -> None:
        self.assertTrue(all(h < 40 for h in sol.treap_heights(2000, [1, 2, 3])))


class TestSplay(unittest.TestCase):
    def test_model(self) -> None:
        rng = random.Random(3)
        t, model = ex.SplayTree(), set()
        for _ in range(3000):
            k = rng.randint(0, 300)
            if rng.random() < 0.5:
                t.insert(k)
                model.add(k)
            else:
                self.assertEqual(t.contains(k), k in model)
                if k in model:
                    self.assertEqual(t.root.key, k)
        self.assertEqual(list(ex.inorder(t.root)), sorted(model))

    def test_hot_key_at_root(self) -> None:
        self.assertEqual(sol.splay_depth_of_hot_key(200, 42, 3), 0)
        self.assertEqual(ex.recent_contacts(["Maya", "Leo", "Zoe", "Leo", "Ana"]), "Ana")


class TestAA(unittest.TestCase):
    def test_random_and_sorted(self) -> None:
        rng = random.Random(4)
        t, model = None, set()
        for _ in range(3000):
            k = rng.randint(0, 2000)
            t = ex.aa_insert(t, k)
            model.add(k)
        ex.check_aa(t)
        self.assertEqual(list(ex.inorder(t)), sorted(model))
        s = None
        for k in range(2000):
            s = ex.aa_insert(s, k)
        ex.check_aa(s)
        self.assertLessEqual(ex.height(s), 22)


class TestSolutions(unittest.TestCase):
    def test_range_split(self) -> None:
        t = ex.Treap(4)
        for k in range(20):
            t.insert(k)
        self.assertEqual(sol.range_split(t, 5, 9), [5, 6, 7, 8, 9])
        self.assertEqual(list(ex.inorder(t.root)), list(range(20)))
        ex.check_treap(t.root)


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    unittest.main()
