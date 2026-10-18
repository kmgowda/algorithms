import itertools
import math
import random
import unittest

import ch12_examples as ex
import ch12_solutions as sol


def apply_script(a, ops):
    out, i = [], 0
    for op in ops:
        if op.startswith("keep"):
            out.append(a[i])
            i += 1
        elif op.startswith("replace"):
            out.append(op[-1])
            i += 1
        elif op.startswith("delete"):
            i += 1
        else:
            out.append(op[-1])
    return "".join(out)


class TestSpaceReconstruction(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
            b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
            d = ex.edit_distance_full(a, b)
            self.assertEqual(ex.edit_distance_two_rows(a, b), d)
            ops = ex.edit_script(a, b)
            self.assertEqual(apply_script(a, ops), b)
            self.assertEqual(sum(1 for o in ops if not o.startswith("keep")), d)
            coins = sorted(set(rng.sample(range(1, 9), rng.randint(1, 3))))
            amt = rng.randint(0, 20)
            got = ex.coin_change_with_coins(coins, amt)
            combos = [c for r in range(amt + 1) for c in itertools.combinations_with_replacement(coins, r) if sum(c) == amt]
            if combos:
                self.assertEqual(sum(got), amt)
                self.assertEqual(len(got), min(map(len, combos)))
            else:
                self.assertIsNone(got)
            items = [(f"i{k}", rng.randint(1, 5), rng.randint(1, 30)) for k in range(rng.randint(0, 6))]
            cap = rng.randint(0, 12)
            value, chosen = ex.knapsack_one_row_with_items(items, cap)
            brute = max((sum(v for _, _, v in c) for r in range(len(items) + 1) for c in itertools.combinations(items, r)
                         if sum(w for _, w, _ in c) <= cap), default=0)
            picked = [it for it in items if it[0] in chosen]
            self.assertEqual(value, brute)
            self.assertEqual(sum(v for _, _, v in picked), brute)
            self.assertLessEqual(sum(w for _, w, _ in picked), cap)
        for r in range(1, 8):
            for c in range(1, 8):
                self.assertEqual(ex.grid_paths_one_row(r, c), math.comb(r + c - 2, r - 1))

    def test_memory_and_solutions(self) -> None:
        a, b = "x" * 600, "y" * 600
        full = ex.peak_memory(ex.edit_distance_full, a, b)
        rows = ex.peak_memory(ex.edit_distance_two_rows, a, b)
        self.assertEqual(full[0], rows[0])
        self.assertLess(rows[1] * 50, full[1])
        self.assertEqual(sol.lcs_two_rows("ACCGGTCG", "GTCGTTCG"), 5)
        self.assertEqual(sol.fib_constant_space(90), 2880067194370816120)
        self.assertEqual(sol.min_path_with_route([[1, 3, 1], [1, 5, 1], [4, 2, 1]]), (7, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]))


if __name__ == "__main__":
    unittest.main()
