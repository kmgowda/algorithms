import math
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestRedBlack(unittest.TestCase):
    def test_random_inserts_keep_rules(self) -> None:
        rng = random.Random(1)
        t, model = ex.RedBlackTree(), {}
        for _ in range(3000):
            k = rng.randint(0, 1000)
            t.insert(k, -k)
            model[k] = -k
            ex.check(t.root)
        self.assertEqual(list(t.keys()), sorted(model))
        self.assertEqual(t.size, len(model))
        for k in list(model)[:100]:
            self.assertEqual(t.get(k), model[k])
        with self.assertRaises(KeyError):
            t.get(-1)
        self.assertLessEqual(t.height(), sol.height_bound(len(model)))

    def test_sorted_input(self) -> None:
        for n in (10, 1000, 10_000):
            t = ex.RedBlackTree()
            for k in range(n):
                t.insert(k)
            ex.check(t.root)
            self.assertLessEqual(t.height(), 2 * math.log2(n + 1))

    def test_word_index(self) -> None:
        idx = ex.word_index("the lion and the zebra and the eagle")
        self.assertEqual([(w, idx.get(w)) for w in idx.keys()],
                         [("and", 2), ("eagle", 1), ("lion", 1), ("the", 3), ("zebra", 1)])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        t = ex.RedBlackTree()
        for k in range(1, 16):
            t.insert(k)
        self.assertEqual(sol.count_red(t.root) + sol.as_23_tree_nodes(t.root), 15)
        self.assertEqual(sol.floor_key(t, 7.5), 7)
        self.assertIsNone(sol.floor_key(t, 0))
        self.assertAlmostEqual(sol.height_bound(15), 8.0)


if __name__ == "__main__":
    unittest.main()
