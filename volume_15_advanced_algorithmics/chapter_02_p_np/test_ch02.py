import itertools
import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestPNP(unittest.TestCase):
    def test_check_and_solve(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            vals = [rng.randint(1, 20) for _ in range(rng.randint(0, 9))]
            t = rng.randint(0, 60)
            found = ex.solve_subset_sum(vals, t)
            exists = any(sum(c) == t for r in range(len(vals) + 1) for c in itertools.combinations(vals, r))
            self.assertEqual(found is not None, exists)
            if found is not None:
                self.assertTrue(ex.check_subset_sum(vals, t, found))
            n = rng.randint(1, 5)
            clauses = [tuple(rng.choice([1, -1]) * rng.randint(1, n) for _ in range(3)) for _ in range(rng.randint(1, 8))]
            a = ex.solve_sat(clauses, n)
            brute = any(ex.check_sat(clauses, {i + 1: b for i, b in enumerate(bits)}) for bits in itertools.product([False, True], repeat=n))
            self.assertEqual(a is not None, brute)
            two = [tuple(rng.choice([1, -1]) * rng.randint(1, n) for _ in range(2)) for _ in range(rng.randint(1, 8))]
            res = sol.two_sat(two, n)
            brute2 = any(ex.check_sat(two, {i + 1: b for i, b in enumerate(bits)}) for bits in itertools.product([False, True], repeat=n))
            self.assertEqual(res is not None, brute2, two)
            if res is not None:
                self.assertTrue(ex.check_sat(two, {v: res.get(v, False) for v in range(1, n + 1)}))

    def test_examples(self) -> None:
        solved = [[5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8], [1, 9, 8, 3, 4, 2, 5, 6, 7],
                  [8, 5, 9, 7, 6, 1, 4, 2, 3], [4, 2, 6, 8, 5, 3, 7, 9, 1], [7, 1, 3, 9, 2, 4, 8, 5, 6],
                  [9, 6, 1, 5, 3, 7, 2, 8, 4], [2, 8, 7, 4, 1, 9, 6, 3, 5], [3, 4, 5, 2, 8, 6, 1, 7, 9]]
        self.assertTrue(ex.check_sudoku(solved))
        solved[0][0], solved[0][1] = solved[0][1], solved[0][0]
        self.assertFalse(ex.check_sudoku(solved))
        self.assertFalse(ex.check_subset_sum([1, 2], 2, [1, 1]))
        times = ex.verify_vs_solve([8, 14])
        self.assertLess(times[1][1], times[1][2])
        self.assertTrue(ex.exam_schedule_ok([("Maths", "Physics"), ("Physics", "Art")], {"Maths": 0, "Physics": 1, "Art": 0}, 2))
        self.assertFalse(ex.exam_schedule_ok([("Maths", "Physics")], {"Maths": 0, "Physics": 0}, 2))
        self.assertTrue(sol.check_hamiltonian_cycle({0: {1, 3}, 1: {0, 2}, 2: {1, 3}, 3: {2, 0}}, [0, 1, 2, 3]))
        self.assertFalse(sol.check_hamiltonian_cycle({0: {1, 3}, 1: {0, 2}, 2: {1, 3}, 3: {2, 0}}, [0, 2, 1, 3]))
        self.assertEqual(sol.classify("3-SAT"), "NP-complete")


if __name__ == "__main__":
    unittest.main()
