import itertools
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def random_graph(rng, n, m, directed):
    g = {v: [] for v in range(n)}
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b and b not in g[a]:
            g[a].append(b)
            if not directed and a not in g[b]:
                g[b].append(a)
    return g


class TestDFS(unittest.TestCase):
    def test_orders_and_paths(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            g = random_graph(rng, rng.randint(1, 12), rng.randint(0, 25), rng.random() < 0.5)
            s = rng.randrange(len(g))
            rec = ex.dfs_recursive(g, s)
            self.assertEqual(rec, ex.dfs_iterative(g, s))
            self.assertEqual(len(rec), len(set(rec)))
            for t in g:
                p = ex.find_path(g, s, t)
                self.assertEqual(p is not None, t in rec)
                if p:
                    self.assertEqual((p[0], p[-1]), (s, t))
                    self.assertTrue(all(b in g[a] for a, b in zip(p, p[1:])))

    def test_times_nest(self) -> None:
        rng = random.Random(2)
        for _ in range(100):
            g = random_graph(rng, 10, 15, True)
            d, f = ex.discovery_finish_times(g)
            self.assertEqual(sorted(list(d.values()) + list(f.values())), list(range(20)))
            for u, v in itertools.combinations(g, 2):
                a, b = (d[u], f[u]), (d[v], f[v])
                nested = (a[0] < b[0] < b[1] < a[1]) or (b[0] < a[0] < a[1] < b[1])
                disjoint = a[1] < b[0] or b[1] < a[0]
                self.assertTrue(nested or disjoint)      # the parenthesis theorem

    def test_examples(self) -> None:
        maze = {"entrance": ["hall"], "hall": ["entrance", "library", "kitchen"], "library": ["hall", "secret"],
                "kitchen": ["hall"], "secret": ["library", "treasure"], "treasure": ["secret"]}
        self.assertEqual(ex.maze_rooms(maze, "entrance", "treasure"), ["entrance", "hall", "library", "secret", "treasure"])
        self.assertTrue(ex.can_unlock_all([[1], [2], [3], []]))
        self.assertFalse(ex.can_unlock_all([[1, 3], [3, 0, 1], [2], [0]]))
        self.assertIsNone(ex.find_path({"a": [], "b": []}, "a", "b"))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.all_paths({0: [1, 2], 1: [3], 2: [3], 3: []}, 0, 3), [[0, 1, 3], [0, 2, 3]])
        self.assertEqual(sol.count_components({1: [2], 2: [1], 3: [], 4: [5], 5: [4]}), 3)
        g = {"a": ["b"], "b": ["a"]}
        c = sol.clone_graph(g)
        self.assertEqual(c, g)
        self.assertIsNot(c["a"], g["a"])
        self.assertEqual(sol.depth_of_dfs_tree({i: [i + 1] for i in range(10)} | {10: []}, 0), 10)


if __name__ == "__main__":
    unittest.main()
