import bisect
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


class TestBST(unittest.TestCase):
    def test_against_model(self) -> None:
        rng = random.Random(1)
        tree, model = ex.BST(), {}
        for _ in range(3000):
            k = rng.randint(0, 200)
            op = rng.random()
            if op < 0.5:
                tree.insert(k, -k)
                model[k] = -k
            elif op < 0.8:
                if k in model:
                    tree.delete(k)
                    del model[k]
                else:
                    with self.assertRaises(KeyError):
                        tree.delete(k)
            else:
                self.assertEqual(k in tree, k in model)
            self.assertEqual(tree.size, len(model))
        keys = sorted(model)
        self.assertEqual(list(tree.keys()), keys)
        self.assertTrue(ex.is_valid_bst(tree.root))
        for q in range(-5, 210):
            i = bisect.bisect_right(keys, q)
            self.assertEqual(tree.floor(q), keys[i - 1] if i else None)
            j = bisect.bisect_left(keys, q)
            self.assertEqual(tree.ceiling(q), keys[j] if j < len(keys) else None)
        self.assertEqual(tree.range(40, 120), [x for x in keys if 40 <= x <= 120])
        self.assertEqual((tree.minimum(), tree.maximum()), (keys[0], keys[-1]))

    def test_errors_and_validity(self) -> None:
        t = ex.BST()
        with self.assertRaises(KeyError):
            t.search(1)
        with self.assertRaises(ValueError):
            t.minimum()
        bad = ex.Node(10)
        bad.left = ex.Node(5)
        bad.left.right = ex.Node(12)         # 12 is in 10's LEFT subtree: invalid
        self.assertFalse(ex.is_valid_bst(bad))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        t = sol.from_sorted(list(range(1, 16)))
        self.assertEqual(t.height(), 3)
        self.assertEqual(sol.kth_smallest(t, 4), 4)
        with self.assertRaises(IndexError):
            sol.kth_smallest(t, 99)
        self.assertEqual(sol.lca_bst(t.root, 3, 6), 4)
        self.assertEqual(sol.lca_bst(t.root, 1, 15), 8)
        self.assertEqual(sol.closest_key(t, 7.6), 8)
        self.assertEqual(sol.closest_key(t, 100), 15)


if __name__ == "__main__":
    unittest.main()
