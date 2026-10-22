import random
import unittest
from collections import deque

import ch20_examples as ex
import ch20_solutions as sol


def neighbours(reports):
    g = {p: set(rs) for p, rs in reports.items()}
    for p, rs in reports.items():
        for r in rs:
            g[r].add(p)
    return g


def bfs_sum(reports):
    g, out = neighbours(reports), {}
    for s in g:
        dist, q = {s: 0}, deque([s])
        while q:
            u = q.popleft()
            for v in g[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        out[s] = sum(dist.values())
    return out


def random_tree(r, n):
    reports = {i: [] for i in range(n)}
    for i in range(1, n):
        reports[r.randrange(i)].append(i)
    return reports


class TestChapter20Solutions(unittest.TestCase):
    def test_total_distances(self) -> None:
        t = sol.total_distances(ex.REPORTS, "Director")
        self.assertEqual((t["Director"], t["Maya"], t["Gus"]), (21, 22, 38))
        self.assertEqual(t, bfs_sum(ex.REPORTS))
        self.assertEqual(sol.total_distances({"A": []}, "A"), {"A": 0})
        self.assertEqual(sol.total_distances({"A": ["B"], "B": []}, "A"), {"A": 1, "B": 1})
        r = random.Random(20)
        for _ in range(100):
            reports = random_tree(r, r.randint(1, 12))
            self.assertEqual(sol.total_distances(reports, 0), bfs_sum(reports))

    def test_leaf_first_is_best_for_equal_fun(self) -> None:
        r = random.Random(21)
        for _ in range(100):
            reports = random_tree(r, r.randint(1, 10))
            ones = {p: 1 for p in reports}
            chosen = sol.leaf_first(reports, 0)
            self.assertEqual(len(chosen), ex.party(reports, ones, 0)[0])
            boss = {c: p for p, rs in reports.items() for c in rs}
            self.assertTrue(all(boss.get(x) not in chosen for x in chosen))
        self.assertEqual(sol.leaf_first({"A": []}, "A"), {"A"})

    def test_wrong_reroot(self) -> None:
        self.assertEqual(sol.farthest_wrong(ex.REPORTS, "Director"), ex.farthest_colleague(ex.REPORTS, "Director"))
        chain = {"A": ["B"], "B": ["C"], "C": []}
        self.assertEqual((sol.farthest_wrong(chain, "A"), ex.farthest_colleague(chain, "A")),
                         ({"A": 2, "B": 3, "C": 4}, {"A": 2, "B": 1, "C": 2}))


if __name__ == "__main__":
    unittest.main()
