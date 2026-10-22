import random
import unittest

import ch24_examples as ex
import ch24_solutions as sol


def reach(out: dict, s) -> set:
    seen, stack = {s}, [s]
    while stack:
        v = stack.pop()
        for w in out.get(v, []):
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def brute_pieces(adj: dict, u) -> int:
    """Pieces of u's own piece after removing u."""
    own = reach(adj, u) - {u}
    seen, n = set(), 0
    for s in own:
        if s in seen:
            continue
        n += 1
        stack = [s]
        seen.add(s)
        while stack:
            v = stack.pop()
            for w in adj[v]:
                if w != u and w not in seen:
                    seen.add(w)
                    stack.append(w)
    return n


def random_graph(rng, parallel=False):
    n = rng.randint(1, 8)
    names = [str(i) for i in range(n)]
    roads = [tuple(rng.sample(names, 2)) for _ in range(rng.randint(0, 11)) if n > 1]
    if not parallel:
        roads = sorted({tuple(sorted(r)) for r in roads})
    return ex.adjacency(names, roads), roads


class TestChapter24Solutions(unittest.TestCase):
    def test_one_way_town(self) -> None:
        town = ex.adjacency(ex.PLACES, ex.ROADS)
        plan = sol.one_way_plan(town)
        self.assertEqual(len(plan), 12)
        out = {}
        for a, b in plan:
            out.setdefault(a, []).append(b)
        for p in ex.PLACES:
            self.assertEqual(reach(out, p), set(ex.PLACES))
        self.assertIsNone(sol.one_way_plan(ex.adjacency(ex.PLACES + ex.OUTER, ex.ROADS + ex.OUTER_ROADS)))

    def test_one_way_random(self) -> None:
        rng = random.Random(24)
        for _ in range(300):
            adj, roads = random_graph(rng, parallel=True)
            plan = sol.one_way_plan(adj)
            if ex.weak_links(adj)["bridges"]:
                self.assertIsNone(plan)
                continue
            self.assertEqual(sorted(map(sorted, plan)), sorted(map(sorted, roads)))   # each road once
            out = {}
            for a, b in plan:
                out.setdefault(a, []).append(b)
            for p in adj:
                self.assertEqual(reach(out, p), reach(adj, p))

    def test_one_way_smallest(self) -> None:
        self.assertEqual(sol.one_way_plan({}), [])
        self.assertEqual(sol.one_way_plan(ex.adjacency("A", [])), [])
        self.assertIsNone(sol.one_way_plan(ex.adjacency("AB", [("A", "B")])))
        self.assertEqual(len(sol.one_way_plan(ex.adjacency("AB", [("A", "B"), ("A", "B")]))), 2)

    def test_pieces_after_removal(self) -> None:
        big = ex.adjacency(ex.PLACES + ex.OUTER, ex.ROADS + ex.OUTER_ROADS)
        got = sol.pieces_after_removal(big)
        self.assertEqual({p for p, c in got.items() if c >= 2}, {"Harbour", "Hospital"})
        self.assertEqual((got["Harbour"], got["Library"], got["Lighthouse"]), (2, 1, 1))
        star = sol.pieces_after_removal(ex.adjacency("ABCD", [("A", "B"), ("B", "C"), ("B", "D")]))
        self.assertEqual(star, {"A": 1, "B": 3, "C": 1, "D": 1})
        self.assertEqual(sol.pieces_after_removal({}), {})
        self.assertEqual(sol.pieces_after_removal(ex.adjacency("A", [])), {"A": 0})
        self.assertEqual(sol.pieces_after_removal(ex.adjacency("AB", [("A", "B")])), {"A": 1, "B": 1})
        self.assertEqual(sol.pieces_after_removal(sol.BOWTIE)["C"], 2)

    def test_pieces_random_against_brute_force(self) -> None:
        rng = random.Random(240)
        for _ in range(300):
            adj, _ = random_graph(rng, parallel=True)
            got = sol.pieces_after_removal(adj)
            self.assertEqual(got, {u: brute_pieces(adj, u) for u in adj})
            self.assertEqual({u for u, c in got.items() if c >= 2}, set(ex.weak_links(adj)["cuts"]))

    def test_low_bug(self) -> None:
        self.assertEqual(ex.weak_links(sol.BOWTIE)["cuts"], ["C"])
        self.assertEqual(sol.weak_links_low_bug(sol.BOWTIE)["cuts"], [])
        self.assertEqual(sol.weak_links_low_bug(sol.BOWTIE)["low"]["E"], 1)
        rng = random.Random(241)
        for _ in range(400):                              # the bug never changes the bridges
            adj, _ = random_graph(rng, parallel=True)
            self.assertEqual(sol.weak_links_low_bug(adj)["bridges"], ex.weak_links(adj)["bridges"])


if __name__ == "__main__":
    unittest.main()
