import itertools
import math
import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


def random_wgraph(rng, n, m):
    g = {v: {} for v in range(n)}
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            g[a][b] = rng.randint(0, 9)
    return g


def relax_until_stable(g, s):
    dist = {v: math.inf for v in g}
    dist[s] = 0
    changed = True
    while changed:
        changed = False
        for u in g:
            for v, w in g[u].items():
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    changed = True
    return dist


class TestDijkstra(unittest.TestCase):
    def test_against_reference(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            g = random_wgraph(rng, rng.randint(1, 15), rng.randint(0, 40))
            s = rng.randrange(len(g))
            dist, parent = ex.dijkstra(g, s)
            ref = relax_until_stable(g, s)
            for v in g:
                self.assertEqual(dist.get(v, math.inf), ref[v])
                if v in dist:
                    r = ex.route(parent, v)
                    self.assertEqual(sum(g[a][b] for a, b in zip(r, r[1:])), dist[v])
                    self.assertEqual(ex.dijkstra_to_target(g, s, v)[0], dist[v])
                else:
                    self.assertEqual(ex.dijkstra_to_target(g, s, v), (math.inf, []))

    def test_examples(self) -> None:
        self.assertEqual(ex.network_delay([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2), 2)
        self.assertEqual(ex.network_delay([(1, 2, 1)], 2, 2), -1)
        self.assertEqual(ex.counterexample_negative(), (2.0, 1.0))
        with self.assertRaises(ValueError):
            ex.dijkstra({"a": {"b": -1}, "b": {}}, "a")


class TestSolutions(unittest.TestCase):
    def test_effort_brute_force(self) -> None:
        rng = random.Random(2)
        for _ in range(40):
            h = [[rng.randint(1, 9) for _ in range(3)] for _ in range(3)]
            best = math.inf
            cells = [(r, c) for r in range(3) for c in range(3)]

            def dfs(cell, seen, effort):
                nonlocal best
                if cell == (2, 2):
                    best = min(best, effort)
                    return
                r, c = cell
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if (nr, nc) in cells and (nr, nc) not in seen:
                        dfs((nr, nc), seen | {(nr, nc)}, max(effort, abs(h[nr][nc] - h[r][c])))
            dfs((0, 0), {(0, 0)}, 0)
            self.assertEqual(sol.min_effort_path(h), best)

    def test_others(self) -> None:
        self.assertEqual(sol.cheapest_flight_cost(3, [(0, 1, 100), (1, 2, 100), (0, 2, 500)], 0, 2), 200)
        self.assertAlmostEqual(sol.most_reliable_path({"a": {"b": 0.9, "c": 0.5}, "b": {"c": 0.9}, "c": {}}, "a", "c"), 0.81)
        self.assertEqual(sol.settled_order({"a": {"b": 3, "c": 1}, "c": {"b": 1}, "b": {}}, "a"), ["a", "c", "b"])


if __name__ == "__main__":
    unittest.main()
