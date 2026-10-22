import random
import unittest

import ch19_examples as ex
import ch19_solutions as sol


class TestChapter19Solutions(unittest.TestCase):
    def test_iddfs_town(self) -> None:
        adj = ex.adjacency()
        b = ex.bfs(adj, "Library")
        for goal in ex.PLACES:
            route = sol.iddfs(adj, "Library", goal)
            self.assertEqual(len(route) - 1, b["depth"][goal])
        self.assertEqual(sol.iddfs(adj, "Library", "Harbour"), ["Library", "School", "Station", "Harbour"])

    def test_iddfs_small(self) -> None:
        self.assertEqual(sol.iddfs({"A": []}, "A", "A"), ["A"])
        self.assertIsNone(sol.iddfs({"A": [], "B": []}, "A", "B"))
        island = ex.adjacency(ex.PLACES + ["Island"], ex.ROADS)
        self.assertIsNone(sol.iddfs(island, "Library", "Island"))
        self.assertEqual(sol.iddfs({"A": ["A", "B"], "B": ["A"]}, "A", "B"), ["A", "B"])
        random.seed(2)
        for _ in range(300):
            n = random.randint(1, 7)
            roads = [(i, j) for i in range(n) for j in range(i + 1, n) if random.random() < 0.4]
            adj = ex.adjacency(list(range(n)), roads)
            a, g = random.randrange(n), random.randrange(n)
            d = ex.bfs(adj, a)["depth"].get(g)
            r = sol.iddfs(adj, a, g)
            self.assertEqual(None if r is None else len(r) - 1, d)

    def test_counts(self) -> None:
        self.assertEqual(sol.count_tree_visits(3, 6), (1093, 1636))
        self.assertEqual(sol.count_tree_visits(2, 0), (1, 1))

    def test_shared_visited_bug(self) -> None:
        adj = ex.adjacency()
        self.assertEqual(sol.iddfs_shared_visited(adj, "Library", "Harbour"),
                         ["Library", "School", "Market", "Station", "Harbour"])     # 4 roads, not 3
        self.assertEqual(sol.iddfs_shared_visited({"A": []}, "A", "A"), ["A"])


if __name__ == "__main__":
    unittest.main()
