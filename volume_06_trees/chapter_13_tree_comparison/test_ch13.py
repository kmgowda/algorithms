import math
import random
import unittest

import ch13_examples as ex
import ch13_solutions as sol


class TestComparison(unittest.TestCase):
    def test_avl_correct_and_short(self) -> None:
        rng = random.Random(1)
        root, model = None, set()
        for _ in range(3000):
            k = rng.randint(0, 5000)
            root = ex.avl_insert(root, k)
            model.add(k)
        for q in range(0, 5000, 13):
            self.assertEqual(ex.contains(root, q), q in model)
        self.assertLessEqual(ex.height(root), 1.45 * math.log2(len(model) + 2))

    def test_height_table(self) -> None:
        t = ex.height_table(2000)
        self.assertEqual(t["plain BST"]["sorted"], 1999)
        self.assertLessEqual(t["AVL"]["sorted"], 16)
        self.assertLess(t["plain BST"]["random"], 60)
        self.assertEqual(t["B-tree t=100 bound"]["sorted"], 1)

    def test_lookup_race(self) -> None:
        r = ex.lookup_race(5000, lookups=500)
        self.assertLess(r["hash set"], r["AVL tree"])

    def test_choose(self) -> None:
        self.assertEqual(ex.choose_structure(need_order=False), "hash table")
        self.assertEqual(ex.choose_structure(need_order=True, on_disk=True), "B+ tree")
        self.assertEqual(ex.choose_structure(need_order=True, prefix_queries=True), "trie")
        self.assertEqual(ex.choose_structure(need_order=True, changes_often=False), "sorted array + binary search")
        self.assertEqual(ex.choose_structure(need_order=True, read_heavy=True), "AVL tree")


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        reads = {s: sol.disk_reads(10**9, s) for s in ("AVL", "red-black", "B-tree t=500")}
        self.assertLessEqual(reads["B-tree t=500"], 4)
        self.assertGreater(reads["red-black"], reads["AVL"])
        with self.assertRaises(ValueError):
            sol.disk_reads(10, "list")
        self.assertEqual(sol.pick_for("search-box suggestions"), "trie")


if __name__ == "__main__":
    unittest.main()
