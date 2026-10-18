import itertools
import random
import unittest
from collections import deque

import ch10_examples as ex
import ch10_solutions as sol


class TestBitmask(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(60):
            n = rng.randint(1, 7)
            d = [[0 if i == j else rng.randint(1, 30) for j in range(n)] for i in range(n)]
            total, route = ex.held_karp(d)
            brute = min(sum(d[a][b] for a, b in zip((0, *p, 0), (*p, 0))) for p in itertools.permutations(range(1, n))) if n > 1 else 0
            self.assertEqual(total, brute)
            self.assertEqual(route[0], 0)
            self.assertEqual(route[-1], 0)
            self.assertEqual(sorted(route[:-1]), list(range(n)))
            self.assertEqual(sum(d[a][b] for a, b in zip(route, route[1:])), total)
            cost = [[rng.randint(1, 20) for _ in range(n)] for _ in range(n)]
            self.assertEqual(ex.assignment_bitmask(cost), min(sum(cost[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n))))
            vals = [rng.randint(1, 6) for _ in range(rng.randint(1, 7))]
            k = rng.randint(1, 3)
            brute_k = sum(vals) % k == 0 and any(all(sum(v for v, g in zip(vals, lab) if g == gi) == sum(vals) // k for gi in range(k))
                                                 for lab in itertools.product(range(k), repeat=len(vals)))
            self.assertEqual(sol.can_partition_k_bitmask(vals, k), brute_k)

    def test_visit_all(self) -> None:
        rng = random.Random(2)
        for _ in range(40):
            n = rng.randint(1, 6)
            adj = [[] for _ in range(n)]
            for i in range(1, n):
                j = rng.randrange(i)
                adj[i].append(j)
                adj[j].append(i)
            dist = [[0] * n for _ in range(n)]
            for s in range(n):
                seen, q = {s: 0}, deque([s])
                while q:
                    v = q.popleft()
                    for w in adj[v]:
                        if w not in seen:
                            seen[w] = seen[v] + 1
                            q.append(w)
                for t in range(n):
                    dist[s][t] = seen[t]
            brute = min(sum(dist[a][b] for a, b in zip(p, p[1:])) for p in itertools.permutations(range(n)))
            self.assertEqual(ex.visit_all_nodes(adj), brute)

    def test_examples(self) -> None:
        self.assertEqual(ex.set_to_mask([0, 2, 3]), 13)
        self.assertEqual(ex.mask_to_set(13), [0, 2, 3])
        self.assertEqual(ex.held_karp([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]])[0], 80)
        team = ex.minimum_team(["python", "sql", "design", "ml"],
                               {"Asha": ["python", "ml"], "Ben": ["sql"], "Cy": ["design", "sql"], "Dev": ["python"]})
        self.assertEqual(team, ["Asha", "Cy"])
        self.assertEqual(sol.count_subsets_with_sum([1, 2, 3, 4, 5], 5), 3)
        self.assertTrue(sol.can_partition_k_bitmask([4, 3, 2, 3, 5, 2, 1], 4))
        self.assertEqual(sol.count_beautiful_arrangements(4), 8)


if __name__ == "__main__":
    unittest.main()
