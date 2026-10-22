import random
import unittest

import ch12_examples as ex


class TestChapter12(unittest.TestCase):
    def test_party(self) -> None:
        total, guests, pair = ex.party(ex.REPORTS, ex.FUN, "Director")
        self.assertEqual((total, guests), (26, ["Ben", "Cai", "Dev", "Director", "Eva", "Fay"]))
        self.assertEqual((pair["Maya"], pair["Omar"], pair["Director"]), ((12, 10), (9, 13), (26, 25)))
        self.assertEqual(ex.brute(ex.REPORTS, ex.FUN), 26)
        self.assertEqual(ex.subtree_sizes(ex.REPORTS, "Director")["Maya"], 5)

    def test_every_case(self) -> None:
        cases = [({"A": []}, {"A": 5}), ({"A": ["B"], "B": []}, {"A": 5, "B": 9}),
                 ({"A": ["B", "C"], "B": [], "C": []}, {"A": 10, "B": 4, "C": 5}), ({"A": ["B"], "B": []}, {"A": 5, "B": 5})]
        self.assertEqual([ex.party(r, f, "A")[:2] for r, f in cases], [(5, ["A"]), (9, ["B"]), (10, ["A"]), (5, ["A"])])
        f = dict(ex.FUN)
        f["Director"] = 0
        self.assertEqual(ex.party(ex.REPORTS, f, "Director")[0], 25)
        rng = random.Random(12)
        for _ in range(100):
            n = rng.randint(1, 9)
            reports = {i: [] for i in range(n)}
            for i in range(1, n):
                reports[rng.randrange(i)].append(i)
            fun = {i: rng.randint(1, 9) for i in range(n)}
            total, guests, _ = ex.party(reports, fun, 0)
            self.assertEqual(total, ex.brute(reports, fun))
            self.assertEqual(sum(fun[g] for g in guests), total)


    def test_rerooting(self) -> None:
        import random
        from collections import deque

        def bfs_far(reports):
            adj = {p: list(rs) for p, rs in reports.items()}
            for p, rs in reports.items():
                for r in rs:
                    adj[r].append(p)
            out = {}
            for s0 in adj:
                dist, q = {s0: 0}, deque([s0])
                while q:
                    u = q.popleft()
                    for v in adj[u]:
                        if v not in dist:
                            dist[v] = dist[u] + 1
                            q.append(v)
                out[s0] = max(dist.values())
            return out

        keen = dict(ex.FUN, Gus=9)
        self.assertEqual(ex.party(ex.REPORTS, keen, "Director")[:2], (30, ["Ben", "Dev", "Director", "Eva", "Fay", "Gus"]))
        far = ex.farthest_colleague(ex.REPORTS, "Director")
        self.assertEqual((far["Gus"], far["Director"], far["Maya"]), (6, 3, 4))
        self.assertEqual(far, bfs_far(ex.REPORTS))
        self.assertEqual(ex.farthest_colleague({"A": []}, "A"), {"A": 0})
        r = random.Random(12)
        for _ in range(100):
            n = r.randint(1, 12)
            reports = {i: [] for i in range(n)}
            for i in range(1, n):
                reports[r.randrange(i)].append(i)
            self.assertEqual(ex.farthest_colleague(reports, 0), bfs_far(reports))


if __name__ == "__main__":
    unittest.main()
