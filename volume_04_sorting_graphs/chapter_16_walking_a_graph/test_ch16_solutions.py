import unittest

import ch16_examples as ex
import ch16_solutions as sol


class TestChapter16Solutions(unittest.TestCase):
    def test_is_tree(self) -> None:
        self.assertFalse(sol.is_tree({}))
        self.assertTrue(sol.is_tree({"A": []}))
        self.assertTrue(sol.is_tree(ex.adjacency(["A", "B"], [("A", "B", 1)])))
        self.assertFalse(sol.is_tree(ex.adjacency(["A", "B"], [])))                       # two islands
        self.assertFalse(sol.is_tree(ex.adjacency(["A"], [("A", "A", 1)])))               # a self-loop
        self.assertFalse(sol.is_tree(ex.adjacency(["A", "B"], [("A", "B", 1), ("A", "B", 2)])))  # parallel roads
        self.assertFalse(sol.is_tree(ex.adjacency()))                                      # the town has cycles
        # n - 1 roads but not connected: a triangle plus an island
        tri = ex.adjacency(["A", "B", "C", "D"], [("A", "B", 1), ("B", "C", 1), ("A", "C", 1)])
        self.assertFalse(sol.is_tree(tri))
        # the stack-walk tree of the town (Figure 16.4) is a tree
        t = ex.walk_tree(ex.adjacency(), "Library")
        self.assertTrue(sol.is_tree(ex.adjacency(ex.PLACES, [(v, p, 0) for v, p in t.items() if p])))

    def test_is_tree_stops_early(self) -> None:
        class Counting(dict):
            reads = 0

            def __getitem__(self, k):
                Counting.reads += 1
                return dict.__getitem__(self, k)
        n = 50
        complete = Counting({i: [j for j in range(n) if j != i] for i in range(n)})
        self.assertFalse(sol.is_tree(complete))
        self.assertEqual(Counting.reads, 3)              # 49 + 49 + 49 > 2 * 49: stops after three lists

    def test_marking_late(self) -> None:
        tri = ex.adjacency(["A", "B", "C"], [("A", "B", 1), ("B", "C", 1), ("A", "C", 1)])
        self.assertEqual(sol.explore_marking_late(tri, "A"), ["A", "C", "B", "B"])
        order = sol.explore_marking_late(ex.adjacency(), "Library")
        self.assertEqual(len(order), 13)
        self.assertEqual((order.count("School"), order.count("Market"), order.count("Harbour")), (3, 3, 2))
        self.assertEqual(sol.explore_marking_late({"A": []}, "A"), ["A"])


if __name__ == "__main__":
    unittest.main()
