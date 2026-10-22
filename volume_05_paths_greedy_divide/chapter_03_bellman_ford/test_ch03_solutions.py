import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol

INF = float("inf")


def reference(vertices, edges, start):
    """Floyd-Warshall: v is -inf when some u on a negative cycle is reachable from start and reaches v."""
    d = {u: {v: (0 if u == v else INF) for v in vertices} for u in vertices}
    for a, b, w in edges:
        d[a][b] = min(d[a][b], w)
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    reach = lambda a, b: a == b or d[a][b] < INF  # noqa: E731
    bad = [u for u in vertices if d[u][u] < 0 and reach(start, u)]
    out = {}
    for v in vertices:
        if any(reach(u, v) for u in bad):
            out[v] = -INF
        else:
            out[v] = d[start][v]
    return out


class TestChapter3Solutions(unittest.TestCase):
    def test_courier(self) -> None:
        self.assertEqual(sol.costs_with_minus_infinity(ex.DEPOTS, ex.LEGS, "A"), ex.bellman_ford(ex.DEPOTS, ex.LEGS, "A")[0])
        legs = [(a, b, -3 if (a, b) == ("E", "A") else w) for a, b, w in ex.LEGS]
        self.assertEqual(set(sol.costs_with_minus_infinity(ex.DEPOTS, legs, "A").values()), {-INF})

    def test_smallest(self) -> None:
        self.assertEqual(sol.costs_with_minus_infinity(["A"], [], "A"), {"A": 0})
        self.assertEqual(sol.costs_with_minus_infinity(["A", "B"], [], "A"), {"A": 0, "B": INF})
        far = [("A", "B", 1), ("C", "D", -3), ("D", "C", 1)]          # a negative cycle the start cannot reach
        self.assertEqual(sol.costs_with_minus_infinity(list("ABCD"), far, "A"), {"A": 0, "B": 1, "C": INF, "D": INF})
        side = [("A", "B", 1), ("A", "C", 1), ("C", "D", -3), ("D", "C", 1)]
        self.assertEqual(sol.costs_with_minus_infinity(list("ABCD"), side, "A"), {"A": 0, "B": 1, "C": -INF, "D": -INF})

    def test_random(self) -> None:
        rng = random.Random(5)
        for _ in range(300):
            vs = list(range(rng.randint(1, 6)))
            es = [(rng.choice(vs), rng.choice(vs), rng.randint(-4, 6)) for _ in range(rng.randint(0, 10))]
            es = [(a, b, w) for a, b, w in es if a != b]
            self.assertEqual(sol.costs_with_minus_infinity(vs, es, 0), reference(vs, es, 0))

    def test_bfs_round_is_wrong(self) -> None:
        self.assertEqual(sol.one_round_in_bfs_order(ex.DEPOTS, ex.LEGS, "A")["E"], 2)   # truth: -2
        self.assertEqual(ex.bellman_ford(ex.DEPOTS, ex.LEGS, "A")[0]["E"], -2)


if __name__ == "__main__":
    unittest.main()
