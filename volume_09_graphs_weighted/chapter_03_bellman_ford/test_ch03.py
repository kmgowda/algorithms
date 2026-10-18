import math
import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


def brute(vertices, edges, s, t):
    out = {v: [] for v in vertices}
    for u, v, w in edges:
        out[u].append((v, w))
    best = math.inf

    def go(v, seen, cost):
        nonlocal best
        if v == t:
            best = min(best, cost)
        for w2, c in out[v]:
            if w2 not in seen:
                go(w2, seen | {w2}, cost + c)
    go(s, {s}, 0)
    return best


def has_negative_cycle_brute(vertices, edges):
    out = {v: [] for v in vertices}
    for u, v, w in edges:
        out[u].append((v, w))
    found = False

    def go(start, v, seen, cost):
        nonlocal found
        for w2, c in out[v]:
            if w2 == start and cost + c < 0:
                found = True
            elif w2 not in seen and w2 > start:
                go(start, w2, seen | {w2}, cost + c)
    for s in vertices:
        go(s, s, {s}, 0)
    return found


class TestBellmanFord(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            n = rng.randint(1, 6)
            vertices = list(range(n))
            edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-4, 9)) for _ in range(rng.randint(0, 10))]
            edges = [e for e in edges if e[0] != e[1]]
            neg_any = has_negative_cycle_brute(vertices, edges)
            cyc = ex.find_negative_cycle(vertices, edges)
            self.assertEqual(cyc is not None, neg_any)
            if cyc:
                w = {(u, v): min(c for a, b, c in edges if (a, b) == (u, v)) for u, v, _ in edges}
                total = sum(w[(a, b)] for a, b in zip(cyc, cyc[1:] + cyc[:1]))
                self.assertLess(total, 0)
            if not neg_any:
                dist, _, neg = ex.bellman_ford(vertices, edges, 0)
                self.assertFalse(neg)
                spfa = sol.spfa(vertices, edges, 0)
                for t in vertices:
                    self.assertEqual(dist[t], brute(vertices, edges, 0, t))
                    self.assertEqual(spfa[t], dist[t])

    def test_examples(self) -> None:
        dist, _, neg = ex.bellman_ford(["A", "B", "C", "D"], [("A", "B", 4), ("A", "C", 5), ("C", "B", -3), ("B", "D", 2)], "A")
        self.assertEqual((dist["B"], dist["D"], neg), (2, 4, False))
        rates = {"USD": {"EUR": 0.9, "INR": 83.0}, "EUR": {"INR": 93.0, "USD": 1.11}, "INR": {"USD": 0.0121, "EUR": 0.0108}}
        loop = ex.arbitrage(rates)
        money = 1.0
        for a, b in zip(loop, loop[1:]):
            money *= rates[a][b]
        self.assertGreater(money, 1.0)
        fair = {"USD": {"EUR": 0.9}, "EUR": {"USD": 1 / 0.9}}
        self.assertIsNone(ex.arbitrage(fair))
        self.assertEqual(ex.cheapest_with_stops(3, [(0, 1, 100), (1, 2, 100), (0, 2, 500)], 0, 2, 1), 200)
        self.assertEqual(ex.cheapest_with_stops(3, [(0, 1, 100), (1, 2, 100), (0, 2, 500)], 0, 2, 0), 500)

    def test_solutions(self) -> None:
        V = ["A", "B", "C", "D"]
        E = [("A", "B", 4), ("A", "C", 5), ("C", "B", -3), ("B", "D", 2)]
        self.assertLessEqual(sol.rounds_needed(V, E, "A"), 3)
        self.assertEqual(sol.affected_by_negative_cycle(["s", "a", "b", "t"],
                                                        [("s", "a", 1), ("a", "b", -2), ("b", "a", 1), ("b", "t", 1)], "s"),
                         {"a", "b", "t"})


if __name__ == "__main__":
    unittest.main()
