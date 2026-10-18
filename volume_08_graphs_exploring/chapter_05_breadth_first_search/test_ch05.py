import itertools
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


def random_graph(rng, n, m):
    g = {v: [] for v in range(n)}
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b and b not in g[a]:
            g[a].append(b)
            g[b].append(a)
    return g


def brute_shortest(g, s, t):
    """Try paths of length 0, 1, 2, ... by brute force."""
    n = len(g)
    for length in range(n):
        for mid in itertools.permutations([v for v in g if v not in (s, t)], max(0, length - 1)):
            route = [s, *mid, t] if s != t else [s]
            if all(b in g[a] for a, b in zip(route, route[1:])) and len(route) == length + 1:
                return length
    return -1


class TestBFS(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(60):
            g = random_graph(rng, rng.randint(1, 6), rng.randint(0, 10))
            s = rng.randrange(len(g))
            dist = ex.bfs_distances(g, s)
            for t in g:
                expected = brute_shortest(g, s, t)
                self.assertEqual(dist.get(t, -1), expected)
                p = ex.shortest_path(g, s, t)
                self.assertEqual(-1 if p is None else len(p) - 1, expected)

    def test_multi_source(self) -> None:
        rng = random.Random(2)
        for _ in range(50):
            g = random_graph(rng, 15, 20)
            sources = rng.sample(range(15), 3)
            multi = ex.multi_source_distances(g, sources)
            for v in g:
                ds = [ex.bfs_distances(g, s).get(v) for s in sources]
                ds = [d for d in ds if d is not None]
                self.assertEqual(multi.get(v), min(ds) if ds else None)

    def test_examples(self) -> None:
        metro = {"Central": ["Park", "Market"], "Park": ["Central", "Zoo"], "Market": ["Central", "Port", "Zoo"],
                 "Zoo": ["Park", "Market", "Airport"], "Port": ["Market"], "Airport": ["Zoo"]}
        self.assertEqual(len(ex.shortest_path(metro, "Central", "Airport")), 4)
        self.assertEqual(ex.degrees_of_separation(metro, "Port", "Airport"), 3)
        self.assertEqual(ex.degrees_of_separation({"a": [], "b": []}, "a", "b"), -1)
        self.assertEqual(ex.word_ladder("cold", "warm", ["cord", "card", "ward", "warm", "word", "worm"]), 5)
        self.assertEqual(ex.word_ladder("cold", "warm", ["cord"]), 0)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.open_lock(["0201", "0101", "0102", "1212", "2002"], "0202"), 6)
        self.assertEqual(sol.open_lock(["0000"], "8888"), -1)
        self.assertEqual(sol.knight_moves(8, (0, 0), (7, 7)), 6)
        self.assertEqual(sol.knight_moves(8, (0, 0), (0, 0)), 0)
        g = {"a": ["b"], "b": ["a", "c"], "c": ["b", "d"], "d": ["c"]}
        self.assertEqual(sol.within_k(g, "a", 2), ["b", "c"])
        self.assertEqual(sol.level_widths(g, "b"), [1, 2, 1])


if __name__ == "__main__":
    unittest.main()
