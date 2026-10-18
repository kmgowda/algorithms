import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


def reach(g, s):
    seen, stack = {s}, [s]
    while stack:
        v = stack.pop()
        for w in g[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def brute_sccs(g):
    r = {v: reach(g, v) for v in g}
    groups = {frozenset(w for w in g if w in r[v] and v in r[w]) for v in g}
    return sorted(sorted(c) for c in groups)


def normalize(comps):
    return sorted(sorted(c) for c in comps)


class TestComponents(unittest.TestCase):
    def test_scc_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            n = rng.randint(1, 10)
            g = {v: [] for v in range(n)}
            for _ in range(rng.randint(0, 20)):
                a, b = rng.randrange(n), rng.randrange(n)
                if b not in g[a]:
                    g[a].append(b)
            expected = brute_sccs(g)
            self.assertEqual(normalize(ex.kosaraju_scc(g)), expected)
            self.assertEqual(normalize(ex.tarjan_scc(g)), expected)
            comp_of, dag = ex.condensation(g)
            seen, stack = set(), []      # condensation must be acyclic: check via Kahn
            indeg = {c: 0 for c in dag}
            for c in dag:
                for d in dag[c]:
                    indeg[d] += 1
            ready = [c for c in dag if indeg[c] == 0]
            while ready:
                c = ready.pop()
                seen.add(c)
                for d in dag[c]:
                    indeg[d] -= 1
                    if indeg[d] == 0:
                        ready.append(d)
            self.assertEqual(len(seen), len(dag))

    def test_connected(self) -> None:
        friends = {"Ana": ["Ben"], "Ben": ["Ana"], "Cy": ["Dev"], "Dev": ["Cy"], "Eve": []}
        self.assertEqual(normalize(ex.connected_components(friends)), [["Ana", "Ben"], ["Cy", "Dev"], ["Eve"]])

    def test_long_chain(self) -> None:
        g = {i: [i + 1] for i in range(5000)} | {5000: [0]}
        self.assertEqual(len(ex.tarjan_scc(g)), 1)
        self.assertEqual(len(ex.kosaraju_scc(g)), 1)

    def test_industry(self) -> None:
        self.assertEqual(ex.one_way_neighbourhoods([("Old Town", "Market"), ("Market", "Harbour"), ("Harbour", "Old Town"),
                                                    ("Harbour", "Airport"), ("Airport", "Hotel"), ("Hotel", "Airport")]),
                         [["Airport", "Hotel"], ["Harbour", "Market", "Old Town"]])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertTrue(sol.is_strongly_connected({1: [2], 2: [3], 3: [1]}))
        self.assertFalse(sol.is_strongly_connected({1: [2], 2: []}))
        self.assertEqual(sol.min_roads_to_connect(6, [(0, 1), (2, 3)]), 3)
        self.assertEqual(sol.min_new_one_way_links({1: [2], 2: [3], 3: []}), 1)
        self.assertEqual(sol.min_new_one_way_links({1: [2], 2: [1]}), 0)
        self.assertEqual(sol.min_new_one_way_links({1: [], 2: [], 3: []}), 3)
        self.assertEqual(sorted(sol.largest_group({1: [2], 2: [1, 3], 3: [2], 4: []})), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
