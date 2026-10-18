import itertools
import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


def brute_partition(values, k):
    goal, rem = divmod(sum(values), k)
    if rem:
        return False
    for labels in itertools.product(range(k), repeat=len(values)):
        sums = [0] * k
        for v, g in zip(values, labels):
            sums[g] += v
        if all(s == goal for s in sums):
            return True
    return False


class TestPruning(unittest.TestCase):
    def test_subset_sum_modes_agree(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            vals = [rng.randint(1, 20) for _ in range(rng.randint(0, 10))]
            t = rng.randint(1, 60)
            truth = any(sum(c) == t for r in range(len(vals) + 1) for c in itertools.combinations(vals, r))
            counts = []
            for mode in ("none", "overshoot", "bounds", "sorted"):
                found, nodes = ex.subset_sum_count(vals, t, mode)
                self.assertEqual(found, truth)
                counts.append(nodes)
            self.assertLessEqual(counts[2], counts[1])
            self.assertLessEqual(counts[1], counts[0])
            best = max((sum(c) for r in range(len(vals) + 1) for c in itertools.combinations(vals, r) if sum(c) <= t), default=0)
            self.assertEqual(sol.max_subset_under(vals, t)[0], best)

    def test_partition(self) -> None:
        rng = random.Random(2)
        for _ in range(80):
            vals = [rng.randint(1, 6) for _ in range(rng.randint(1, 7))]
            k = rng.randint(1, 3)
            self.assertEqual(ex.can_partition_k(vals, k)[0], brute_partition(vals, k))
            self.assertEqual(ex.can_partition_k(vals, k, False)[0], brute_partition(vals, k))
        a = ex.can_partition_k([8, 9, 9, 5, 6, 9, 5, 2, 6, 8, 9, 9], 5, True)
        b = ex.can_partition_k([8, 9, 9, 5, 6, 9, 5, 2, 6, 8, 9, 9], 5, False)
        self.assertFalse(a[0] or b[0])
        self.assertLess(a[1] * 50, b[1])

    def test_queens_and_solutions(self) -> None:
        early, late = ex.queens_nodes(6, True), ex.queens_nodes(6, False)
        self.assertEqual(early[0], late[0])
        self.assertLess(early[1] * 100, late[1])
        self.assertEqual([sol.queens_with_symmetry(n) for n in range(1, 9)], [1, 0, 0, 2, 10, 4, 40, 92])
        self.assertTrue(sol.matchsticks_square([1, 1, 2, 2, 2]))
        self.assertFalse(sol.matchsticks_square([3, 3, 3, 3, 4]))
        self.assertEqual(ex.delivery_load_balance([4, 4, 2, 2], 2)[0], True)


if __name__ == "__main__":
    unittest.main()
