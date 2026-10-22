import itertools
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


def brute_trips(places, roads, start):
    adj = ex.neighbours(places, roads)
    out = []
    rest = [p for p in places if p != start]
    for p in itertools.permutations(rest):
        path = [start, *p]
        if len(places) >= 3 and all(b in adj[a] for a, b in zip(path, path[1:])) and start in adj[path[-1]] \
                and path[1] < path[-1]:
            out.append(path + [start])
    return sorted(out)


class TestChapter07Solutions(unittest.TestCase):
    def test_round_trips(self) -> None:
        trips, nodes = sol.round_trips(ex.PLACES, ex.ROADS, "Library")
        self.assertEqual((len(trips), nodes), (1, 59))
        self.assertEqual(sol.round_trips(["A"], [], "A"), ([], 0))
        self.assertEqual(sol.round_trips(["A", "B"], [("A", "B")], "A"), ([], 0))
        self.assertEqual(sol.round_trips(list("ABC"), [("A", "B"), ("B", "C"), ("A", "C")], "A")[0], [["A", "B", "C", "A"]])
        r = random.Random(7)
        for _ in range(80):
            n = r.randint(3, 7)
            places = [f"p{i}" for i in range(n)]
            roads = [e for e in itertools.combinations(places, 2) if r.random() < 0.5]
            self.assertEqual(sorted(sol.round_trips(places, roads, "p0")[0]), brute_trips(places, roads, "p0"))

    def test_greedy_and_bug(self) -> None:
        r = random.Random(8)
        for _ in range(50):
            places, roads = ex.random_graph(r.randint(1, 15), 0.4, r.randint(0, 999))
            col = sol.greedy_colour(places, roads)
            adj = ex.neighbours(places, roads)
            self.assertTrue(all(col[a] != col[b] for a, b in roads))
            self.assertLessEqual(max(col.values()), max((len(adj[p]) for p in places), default=0))
        path = (["A", "B", "C"], [("A", "B"), ("B", "C")])
        self.assertEqual(sol.one_way_out_bug(*path, "A"), [])
        self.assertEqual(ex.hamiltonian(*path, "A")[0], [["A", "B", "C"]])


if __name__ == "__main__":
    unittest.main()
