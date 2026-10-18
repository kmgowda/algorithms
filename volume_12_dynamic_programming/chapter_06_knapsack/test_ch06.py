import itertools
import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestKnapsack(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            items = [(f"i{k}", rng.randint(1, 6), rng.randint(1, 30)) for k in range(rng.randint(0, 7))]
            cap = rng.randint(0, 15)
            brute = max((sum(v for _, _, v in c) for r in range(len(items) + 1) for c in itertools.combinations(items, r)
                         if sum(w for _, w, _ in c) <= cap), default=0)
            self.assertEqual(ex.knapsack_01_table(items, cap), brute)
            self.assertEqual(ex.knapsack_01(items, cap), brute)
            value, chosen = ex.cargo_plan(items, cap)
            self.assertEqual(value, brute)
            picked = [it for it in items if it[0] in chosen]
            self.assertEqual(sum(v for _, _, v in picked), brute)
            self.assertLessEqual(sum(w for _, w, _ in picked), cap)
            unb = max((sum(items[i][2] for i in combo) for r in range(cap + 1)
                       for combo in itertools.combinations_with_replacement(range(len(items)), r)
                       if sum(items[i][1] for i in combo) <= cap), default=0) if items and cap <= 10 else None
            if unb is not None:
                self.assertEqual(ex.knapsack_unbounded(items, cap), unb)
            vals = [rng.randint(1, 9) for _ in range(rng.randint(0, 8))]
            t = rng.randint(0, 30)
            self.assertEqual(ex.subset_sum(vals, t), any(sum(c) == t for r in range(len(vals) + 1) for c in itertools.combinations(vals, r)))
            signs = sum(1 for s in itertools.product((1, -1), repeat=len(vals)) if sum(a * b for a, b in zip(s, vals)) == t - 5)
            self.assertEqual(sol.target_sum_ways(vals, t - 5), signs)

    def test_examples(self) -> None:
        bag = [("camera", 5, 60), ("laptop", 4, 40), ("books", 4, 40), ("snacks", 1, 10)]
        self.assertEqual(ex.knapsack_01(bag, 8), 80)
        self.assertEqual(ex.knapsack_unbounded(bag, 8), 90)   # camera + 3 snacks
        self.assertTrue(ex.subset_sum([3, 34, 4, 12, 5, 2], 11))
        self.assertTrue(ex.can_split_equally([1, 5, 11, 5]))
        self.assertFalse(ex.can_split_equally([1, 2, 3, 5]))
        parcels = [("medicine", 2, 300), ("documents", 1, 120), ("phone", 1, 200), ("laptop", 3, 350), ("shoes", 2, 90)]
        self.assertEqual(ex.cargo_plan(parcels, 5), (670, ["documents", "laptop", "phone"]))
        self.assertEqual(sol.last_stone_weight([2, 7, 4, 1, 8, 1]), 1)
        self.assertEqual(sol.bounded_knapsack([(2, 3, 2), (3, 4, 1)], 7), 10)
        self.assertEqual(sol.ones_and_zeroes(["10", "0001", "111001", "1", "0"], 5, 3), 4)


if __name__ == "__main__":
    unittest.main()
