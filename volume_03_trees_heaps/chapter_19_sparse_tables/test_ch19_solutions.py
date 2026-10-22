import random
import unittest

import ch19_examples as ex
import ch19_solutions as sol


class TestChapter19Solutions(unittest.TestCase):
    def test_first_at_most_examples(self) -> None:
        st = ex.SparseTable(ex.NOISE)                       # 5 3 7 4 6 2 8 9
        self.assertEqual(sol.first_at_most(st, 1, 3), 1)
        self.assertEqual(sol.first_at_most(st, 2, 3), 5)
        self.assertEqual(sol.first_at_most(st, 6, 4), None)
        self.assertEqual(sol.first_at_most(st, 0, 1), None)
        self.assertEqual(sol.first_at_most(st, 8, 99), None)  # starting past the end

    def test_smallest_inputs(self) -> None:
        self.assertIsNone(sol.first_at_most(ex.SparseTable([]), 0, 5))
        one = ex.SparseTable([7])
        self.assertEqual((sol.first_at_most(one, 0, 7), sol.first_at_most(one, 0, 6)), (0, None))

    def test_against_scan(self) -> None:
        rng = random.Random(3)
        for n in range(1, 40):
            vals = [rng.randint(0, 20) for _ in range(n)]
            st = ex.SparseTable(vals)
            for a in range(n + 1):
                for t in (-1, 5, 10, 20):
                    want = next((i for i in range(a, n) if vals[i] <= t), None)
                    self.assertEqual(sol.first_at_most(st, a, t), want)

    def test_naive_repair_is_wrong(self) -> None:
        st = ex.SparseTable(ex.NOISE)
        sol.naive_repair(st, 5, 10)
        self.assertEqual(st.query(4, 5)[0], 2)              # stale: the true minimum of 6 and 10 is 6
        self.assertEqual(st.query(0, 7)[0], 2)              # stale: the true minimum is 3

    def test_cells_to_repair(self) -> None:
        self.assertEqual(sol.cells_to_repair(1, 0), 1)
        self.assertEqual(sol.cells_to_repair(8, 5), 7)
        for n in (1, 2, 5, 8, 33):
            st = ex.SparseTable(list(range(n)))
            for i in range(n):
                brute = sum(1 for k, row in enumerate(st.table) for s in range(len(row)) if s <= i < s + (1 << k))
                self.assertEqual(sol.cells_to_repair(n, i), brute)
        self.assertEqual(sol.cells_to_repair(1024, 512), 1024)


if __name__ == "__main__":
    unittest.main()
