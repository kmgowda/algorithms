import itertools
import random
import unittest
from collections import deque

import ch02_examples as ex
import ch02_solutions as sol


def brute_snacks(appetites, snacks):
    best = 0
    for perm in itertools.permutations(range(len(snacks)), min(len(snacks), len(appetites))):
        best = max(best, sum(1 for c, s in enumerate(perm) if snacks[s] >= appetites[c]))
    for r in range(len(appetites) + 1):
        for kids in itertools.combinations(range(len(appetites)), r):
            for perm in itertools.permutations(range(len(snacks)), min(r, len(snacks))):
                best = max(best, sum(1 for c, s in zip(kids, perm) if snacks[s] >= appetites[c]))
    return best


def bfs_jumps(jumps):
    n = len(jumps)
    dist, q = {0: 0}, deque([0])
    while q:
        i = q.popleft()
        for k in range(1, jumps[i] + 1):
            j = i + k
            if j < n and j not in dist:
                dist[j] = dist[i] + 1
                q.append(j)
    return dist.get(n - 1)


def brute_boats(weights, limit):
    n = len(weights)
    best = n

    def go(left, boats):
        nonlocal best
        if not left:
            best = min(best, boats)
            return
        a, rest = left[0], left[1:]
        go(rest, boats + 1)
        for i, b in enumerate(rest):
            if a + b <= limit:
                go(rest[:i] + rest[i + 1:], boats + 1)
    go(list(weights), 0)
    return best


class TestGreedy(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            a = [rng.randint(1, 6) for _ in range(rng.randint(0, 4))]
            s = [rng.randint(1, 6) for _ in range(rng.randint(0, 4))]
            self.assertEqual(ex.assign_snacks(a, s), brute_snacks(a, s))
            jumps = [rng.randint(0, 3) for _ in range(rng.randint(1, 8))]
            d = bfs_jumps(jumps)
            self.assertEqual(ex.can_reach_end(jumps), d is not None)
            if d is not None:
                self.assertEqual(sol.min_jumps(jumps), d)
            limit = rng.randint(3, 8)
            w = [rng.randint(1, limit) for _ in range(rng.randint(0, 6))]
            self.assertEqual(ex.boats_needed(w, limit), brute_boats(w, limit))

    def test_gas_station(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            n = rng.randint(1, 6)
            fuel = [rng.randint(0, 5) for _ in range(n)]
            cost = [rng.randint(0, 5) for _ in range(n)]
            valid = [s for s in range(n) if all(sum(fuel[(s + k) % n] - cost[(s + k) % n] for k in range(m + 1)) >= 0 for m in range(n))]
            got = ex.min_refuel_start(fuel, cost)
            if valid:
                self.assertIn(got, valid)
            else:
                self.assertEqual(got, -1)

    def test_examples(self) -> None:
        self.assertEqual(ex.make_change_canonical(788), {500: 1, 200: 1, 50: 1, 20: 1, 10: 1, 5: 1, 2: 1, 1: 1})
        self.assertEqual(sol.max_profit_many_trades([7, 1, 5, 3, 6, 4]), 7)
        self.assertEqual(sol.smallest_after_removing([1, 4, 3, 2, 2, 1, 9], 3), "1219")
        self.assertTrue(sol.lemonade_change([5, 5, 5, 10, 20]))
        self.assertFalse(sol.lemonade_change([5, 5, 10, 10, 20]))


if __name__ == "__main__":
    unittest.main()
