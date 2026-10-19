import itertools
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


class TestApproximation(unittest.TestCase):
    def test_guarantees(self) -> None:
        rng = random.Random(1)
        for _ in range(80):
            edges = [(u, v) for u, v in itertools.combinations(range(7), 2) if rng.random() < 0.4]
            cover = ex.vertex_cover_2approx(edges)
            self.assertTrue(all(u in cover or v in cover for u, v in edges))
            self.assertLessEqual(len(cover), 2 * ex.vertex_cover_exact(edges))
            bad = sol.greedy_vertex_cover_bad(edges)
            self.assertTrue(all(u in bad or v in bad for u, v in edges))
            pts = [(rng.random() * 50, rng.random() * 50) for _ in range(rng.randint(2, 7))]
            length, tour = ex.tsp_mst_2approx(pts)
            self.assertEqual(sorted(tour[:-1]), list(range(len(pts))))
            self.assertLessEqual(length, 2 * ex.tsp_exact(pts) + 1e-9)
            jobs = [rng.randint(1, 10) for _ in range(rng.randint(1, 7))]
            m = rng.randint(1, 3)
            opt = min(max(sum(j for j, a in zip(jobs, assign) if a == k) for k in range(m))
                      for assign in itertools.product(range(m), repeat=len(jobs)))
            self.assertLessEqual(sol.load_balancing_lpt(jobs, m) * 3, 4 * opt)
            items = [round(rng.uniform(0.05, 0.9), 2) for _ in range(rng.randint(1, 10))]
            bins = sol.greedy_bin_packing(items, 1.0)
            self.assertTrue(all(sum(b) <= 1.0 + 1e-9 for b in bins))
            self.assertEqual(sorted(x for b in bins for x in b), sorted(items))
        ratios = ex.measured_ratios(20, rng)
        self.assertLessEqual(ratios["vertex cover"], 2.0)
        self.assertLessEqual(ratios["TSP"], 2.0)

    def test_examples(self) -> None:
        self.assertEqual(ex.vertex_cover_2approx([(0, 1), (0, 2), (0, 3), (0, 4)]), {0, 1})
        self.assertEqual(ex.greedy_set_cover(set(range(1, 6)), {"A": {1, 2, 3}, "B": {2, 4}, "C": {3, 4}, "D": {4, 5}}), ["A", "D"])
        with self.assertRaises(ValueError):
            ex.greedy_set_cover({1, 2}, {"A": {1}})
        self.assertEqual(ex.place_cell_towers(set(range(8)), {"hill": {0, 1, 2, 3}, "river": {3, 4, 5}, "farm": {5, 6, 7}, "school": {1, 6}}),
                         ["hill", "farm", "river"])
        self.assertEqual(sol.load_balancing_lpt([7, 5, 4, 4, 3, 3], 3), 10)   # also the optimum here


if __name__ == "__main__":
    unittest.main()
