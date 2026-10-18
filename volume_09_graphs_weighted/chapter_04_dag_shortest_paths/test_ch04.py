import itertools
import math
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def random_dag(rng, n, m):
    g = {v: {} for v in range(n)}
    for _ in range(m):
        a, b = sorted(rng.sample(range(n), 2)) if n > 1 else (0, 0)
        if a != b:
            g[a][b] = rng.randint(-5, 9)
    return g


def all_paths(g, s, t):
    out, path = [], [s]

    def go(v):
        if v == t:
            out.append(list(path))
        for w in g[v]:
            path.append(w)
            go(w)
            path.pop()
    go(s)
    return out


class TestDAG(unittest.TestCase):
    def test_against_enumeration(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            g = random_dag(rng, rng.randint(1, 7), rng.randint(0, 12))
            short, long_ = ex.dag_shortest(g, 0), ex.dag_longest(g, 0)
            for t in g:
                costs = [sum(g[a][b] for a, b in zip(p, p[1:])) for p in all_paths(g, 0, t)]
                self.assertEqual(short[t], min(costs, default=math.inf))
                self.assertEqual(long_[t], max(costs, default=-math.inf))
                self.assertEqual(sol.count_paths(g, 0, t), len(costs))

    def test_cycle_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ex.topological_order({"a": {"b": 1}, "b": {"a": 1}})

    def test_projects(self) -> None:
        house = {"foundation": (5, []), "walls": (7, ["foundation"]), "plumbing": (3, ["foundation"]),
                 "roof": (4, ["walls"]), "electrics": (2, ["walls", "plumbing"]), "paint": (3, ["roof", "electrics"])}
        self.assertEqual(ex.critical_path(house), (19, ["foundation", "walls", "roof", "paint"]))
        s = sol.slack(house)
        self.assertEqual({t for t, v in s.items() if v == 0}, {"foundation", "walls", "roof", "paint"})
        self.assertEqual(s["electrics"], 2)
        self.assertEqual(s["plumbing"], 6)
        self.assertEqual(sol.max_points_route([[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]]), 23)


if __name__ == "__main__":
    unittest.main()
