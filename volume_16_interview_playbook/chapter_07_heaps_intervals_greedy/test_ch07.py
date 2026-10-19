import itertools
import random
import unittest
from collections import Counter, deque

import ch07_examples as ex
import ch07_solutions as sol


def random_intervals(rng, n):
    out = []
    for _ in range(n):
        s = rng.randint(0, 20)
        out.append([s, s + rng.randint(1, 6)])
    return out


class TestHeapsIntervalsGreedy(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            nums = [rng.randint(0, 9) for _ in range(rng.randint(1, 12))]
            k = rng.randint(1, len(nums))
            self.assertEqual(ex.kth_largest(nums, k), sorted(nums, reverse=True)[k - 1])
            counts = Counter(nums)
            kk = rng.randint(1, len(counts))
            got = ex.top_k_frequent(nums, kk)
            self.assertEqual(len(got), kk)
            threshold = sorted(counts.values(), reverse=True)[kk - 1]
            self.assertTrue(all(counts[v] >= threshold for v in got))
            ivs = random_intervals(rng, rng.randint(0, 7))
            covered = {x for s, e in ivs for x in range(2 * s, 2 * e + 1)}
            merged = ex.merge_intervals(ivs)
            self.assertEqual({x for s, e in merged for x in range(2 * s, 2 * e + 1)}, covered)
            self.assertTrue(all(a[1] < b[0] for a, b in zip(merged, merged[1:])))
            new = random_intervals(rng, 1)[0]
            self.assertEqual(ex.insert_interval(merged, new), ex.merge_intervals(merged + [new]))
            best_keep = max((r for r in range(len(ivs) + 1) for c in itertools.combinations(sorted(ivs), r)
                             if all(a[1] <= b[0] for a, b in zip(c, c[1:]))), default=0)
            self.assertEqual(ex.min_removals(ivs), len(ivs) - best_keep)
            peak = max((sum(1 for s, e in ivs if s <= t < e) for t in range(0, 30)), default=0)
            self.assertEqual(ex.meeting_rooms(ivs), peak)
            jumps = [rng.randint(0, 3) for _ in range(rng.randint(1, 8))]
            dist = {0: 0}
            q = deque([0])
            while q:
                i = q.popleft()
                for j in range(i + 1, min(len(jumps), i + jumps[i] + 1)):
                    if j not in dist:
                        dist[j] = dist[i] + 1
                        q.append(j)
            self.assertEqual(ex.can_jump(jumps), len(jumps) - 1 in dist)
            if len(jumps) - 1 in dist:
                self.assertEqual(sol.min_jumps(jumps), dist[len(jumps) - 1])
            n = rng.randint(1, 6)
            gas = [rng.randint(0, 5) for _ in range(n)]
            cost = [rng.randint(0, 5) for _ in range(n)]
            starts = [s for s in range(n) if all(sum(gas[(s + i) % n] - cost[(s + i) % n] for i in range(m + 1)) >= 0 for m in range(n))]
            self.assertEqual(sol.gas_station(gas, cost), starts[0] if starts else -1)

    def test_examples(self) -> None:
        self.assertEqual(ex.top_k_frequent([1, 1, 1, 2, 2, 3], 2), [1, 2])
        self.assertEqual(ex.busiest_hour([[9, 10], [9, 12], [11, 13], [12, 14]]), 2)
        self.assertEqual(sol.k_closest([(1, 3), (-2, 2), (5, 8)], 1), [(-2, 2)])


if __name__ == "__main__":
    unittest.main()
