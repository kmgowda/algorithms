import itertools
import random
import unittest
from collections import deque

import ch09_examples as ex
import ch09_solutions as sol


def random_tree(rng, n):
    nodes = [ex.Node(rng.randint(-5, 10)) for _ in range(n)]
    adj = {i: [] for i in range(n)}
    for i in range(1, n):
        p = rng.randrange(i)
        nodes[p].children.append(nodes[i])
        adj[p].append(i)
        adj[i].append(p)
    return nodes, adj


def all_nodes(root):
    out, stack = [], [root]
    while stack:
        v = stack.pop()
        out.append(v)
        stack += v.children
    return out


class TestTreesGraphs(unittest.TestCase):
    def test_random_trees(self) -> None:
        rng = random.Random(1)
        for _ in range(100):
            n = rng.randint(1, 9)
            nodes, adj = random_tree(rng, n)
            for nd in nodes:
                nd.value = abs(nd.value)
            parent = {c: p for p in range(n) for c in adj[p] if c > p}
            best = max(sum(nodes[i].value for i in range(n) if m >> i & 1) for m in range(1 << n)
                       if all(not (m >> c & 1 and m >> p & 1) for c, p in parent.items()))
            self.assertEqual(ex.tree_robber(nodes[0]), best)
            far = 0
            for s in range(n):
                dist, q = {s: 0}, deque([s])
                while q:
                    v = q.popleft()
                    for w in adj[v]:
                        if w not in dist:
                            dist[w] = dist[v] + 1
                            q.append(w)
                far = max(far, max(dist.values()))
            self.assertEqual(ex.tree_diameter(adj, 0), far)
            sizes = ex.subtree_sizes(adj, 0)
            self.assertEqual(sizes[0], n)

    def test_path_sum_and_cameras(self) -> None:
        rng = random.Random(2)
        for _ in range(80):
            nodes, adj = random_tree(rng, rng.randint(1, 8))
            n = len(nodes)
            best = None
            for s in range(n):
                prev, q = {s: None}, deque([s])
                while q:
                    v = q.popleft()
                    for w in adj[v]:
                        if w not in prev:
                            prev[w] = v
                            q.append(w)
                for t in range(n):
                    total, v = 0, t
                    while v is not None:
                        total += nodes[v].value
                        v = prev[v]
                    best = total if best is None else max(best, total)
            self.assertEqual(sol.max_path_sum(nodes[0]), best)
            fewest = min(bin(m).count("1") for m in range(1 << n)
                         if all(m >> v & 1 or any(m >> w & 1 for w in adj[v]) for v in range(n)))
            self.assertEqual(sol.min_cameras(nodes[0]), fewest)

    def test_examples(self) -> None:
        stages = [["Home"], ["A1", "A2"], ["B1", "B2", "B3"], ["Goa"]]
        cost = {("Home", "A1"): 4, ("Home", "A2"): 2, ("A1", "B1"): 3, ("A1", "B2"): 1, ("A2", "B2"): 6, ("A2", "B3"): 2,
                ("B1", "Goa"): 2, ("B2", "Goa"): 3, ("B3", "Goa"): 7}
        self.assertEqual(ex.multistage_shortest(stages, cost), (8, ["Home", "A1", "B2", "Goa"]))
        self.assertEqual(ex.tree_robber(ex.Node(3, ex.Node(4, ex.Node(1), ex.Node(3)), ex.Node(5, ex.Node(1)))), 9)
        org = {"CEO": ["CTO", "CFO"], "CTO": ["Dev1", "Dev2"], "CFO": ["Acc"]}
        self.assertEqual(ex.party_guests(org, {"CEO": 5, "CTO": 3, "CFO": 2, "Dev1": 4, "Dev2": 4, "Acc": 6}, "CEO"), 19)
        self.assertEqual(sol.count_paths_dag({"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}, "a", "d"), 2)
        chain = {i: [] for i in range(5000)}
        for i in range(4999):
            chain[i].append(i + 1)
            chain[i + 1].append(i)
        self.assertEqual(ex.tree_diameter(chain, 0), 4999)


if __name__ == "__main__":
    unittest.main()
