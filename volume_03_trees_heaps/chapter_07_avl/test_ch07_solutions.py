import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


class TestChapter7Solutions(unittest.TestCase):
    def test_height_bounds(self) -> None:
        """Section 7.9's formal proof: both bounds hold on the sparsest trees, the worst case."""
        import math
        phi = (1 + 5 ** 0.5) / 2
        for hh in range(0, 30):
            n = ex.fewest_nodes(hh)
            self.assertEqual(n + 1, sol.fib(hh + 3))
            self.assertLessEqual(hh, math.log(n + 1, phi) - 1 + 1e-9)
            self.assertLess(hh, 1.4405 * math.log2(n + 2) - 1.3277)

    def test_shallowest_leaf(self) -> None:
        self.assertEqual(sol.shallowest_leaf(None), -1)
        self.assertEqual(sol.shallowest_leaf(ex.build([5])), 0)
        for hh in range(0, 11):                               # the sparsest trees meet the bound exactly
            self.assertEqual(sol.shallowest_leaf(ex.sparsest(hh)), -(-hh // 2))
        rng = random.Random(4)
        for _ in range(500):
            t = ex.build(rng.sample(range(300), rng.randint(1, 120)))
            self.assertGreaterEqual(sol.shallowest_leaf(t), -(-t.height // 2))

    def test_select(self) -> None:
        self.assertIsNone(sol.select(None, 1))                # empty tree
        one = sol.insert(None, 7)
        self.assertEqual([sol.select(one, k) for k in (0, 1, 2)], [None, 7, None])
        rng = random.Random(9)
        for _ in range(100):
            keys = rng.sample(range(1000), rng.randint(0, 80))
            root = None
            for k in keys:
                root = sol.insert(root, k)
            for k in rng.sample(keys, len(keys) // 2):
                root = sol.delete(root, k)
                keys.remove(k)
            self.assertTrue(sol.sizes_correct(root))
            self.assertEqual([sol.select(root, k) for k in range(1, len(keys) + 1)], sorted(keys))
            self.assertIsNone(sol.select(root, len(keys) + 1))

    def test_early_stop_bug(self) -> None:
        t, _ = sol.delete_early_stop(ex.build([20, 10, 30, 40]), 10)
        self.assertEqual((ex.shape(t), ex.balance(t), ex.is_avl(t)), ((20, None, (30, None, (40, None, None))), -2,
                                                                      False))
        self.assertTrue(ex.is_avl(ex.delete(ex.build([20, 10, 30, 40]), 10)))   # the real delete rotates


if __name__ == "__main__":
    unittest.main()
