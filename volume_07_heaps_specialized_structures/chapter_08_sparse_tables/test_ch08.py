import random
import unittest
from math import gcd
from functools import reduce

import ch08_examples as ex
import ch08_solutions as sol


class TestSparseTable(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(100):
            v = [rng.randint(1, 60) for _ in range(rng.randint(1, 40))]
            st = ex.SparseTable(v)
            qs = []
            for _ in range(30):
                a = rng.randrange(len(v))
                b = rng.randrange(a, len(v))
                qs.append((a, b))
                self.assertEqual(st.query(a, b), min(v[a:b + 1]))
            self.assertEqual(sol.range_max(v, qs), [max(v[a:b + 1]) for a, b in qs])
            self.assertEqual(sol.range_gcd(v, qs), [reduce(gcd, v[a:b + 1]) for a, b in qs])
            for a, b in qs:
                self.assertEqual(sol.range_sum_disjoint(v, a, b), sum(v[a:b + 1]))

    def test_lca(self) -> None:
        tree = {"CEO": None, "CTO": "CEO", "CFO": "CEO", "Dev": "CTO", "QA": "CTO", "Ana": "Dev", "Acct": "CFO"}
        self.assertEqual(ex.lca_by_rmq(tree, [("Ana", "QA"), ("Ana", "Acct"), ("Dev", "Ana"), ("QA", "QA")]),
                         ["CTO", "CEO", "Dev", "QA"])

    def test_examples(self) -> None:
        self.assertEqual(ex.lowest_temperature([12, 9, 14, 7, 11, 15, 6, 10], [(0, 3), (4, 7), (2, 2)]), [7, 6, 14])
        self.assertEqual(sol.table_cells(8), 8 + 7 + 5 + 1)


if __name__ == "__main__":
    unittest.main()
