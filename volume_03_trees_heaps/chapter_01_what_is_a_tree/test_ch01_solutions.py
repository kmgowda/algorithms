import itertools
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestChapter01Solutions(unittest.TestCase):
    def test_is_tree_small(self) -> None:
        self.assertFalse(sol.is_tree({}))                         # no nodes: no root
        self.assertTrue(sol.is_tree({}, ["A"]))                   # one node, no edges
        self.assertFalse(sol.is_tree({}, ["A", "B"]))             # two roots
        self.assertTrue(sol.is_tree({"B": "A"}))
        self.assertFalse(sol.is_tree({"A": "A"}))                 # a node that is its own parent
        self.assertFalse(sol.is_tree({"A": "B", "B": "A"}))       # a loop and no root

    def test_thinking_problem_3(self) -> None:
        p = {"B": "A", "C": "D", "D": "C"}                        # 4 nodes, 3 edges, one root, yet a loop
        self.assertEqual(len(p), 3)
        self.assertFalse(sol.is_tree(p))

    def test_library(self) -> None:
        up = ex.parents(ex.SECTIONS)
        self.assertTrue(sol.is_tree(up))
        bad = dict(up, Science="Maths")                          # Practice Problem 2: a loop
        self.assertFalse(sol.is_tree(bad))
        self.assertEqual(sol.leaves_and_inner(ex.SECTIONS, "Library"), (7, 5))

    def test_all_maps_on_four_nodes(self) -> None:
        """Brute force: a map is a tree exactly when walking up from every node reaches the single root."""
        names = "ABCD"
        for choice in itertools.product([None, *names], repeat=4):
            parent = {v: p for v, p in zip(names, choice) if p is not None}

            def reaches_root(v):
                seen = set()
                while v in parent:
                    if v in seen:
                        return False
                    seen.add(v)
                    v = parent[v]
                return True
            roots = [v for v in names if v not in parent]
            want = len(roots) == 1 and all(reaches_root(v) for v in names)
            self.assertEqual(sol.is_tree(parent, names), want, parent)

    def test_more_leaves_than_inner(self) -> None:
        wide = {"r": ["a", "b"], "a": ["c", "d", "e"], "b": ["f", "g"]}
        leaves, inner = sol.leaves_and_inner(wide, "r")
        self.assertGreater(leaves, inner)
        three = {i: [3 * i + 1, 3 * i + 2, 3 * i + 3] for i in range(40)}   # Challenge 1: 3 children, depth 4
        self.assertEqual(sol.leaves_and_inner(three, 0), (81, 40))


if __name__ == "__main__":
    unittest.main()
