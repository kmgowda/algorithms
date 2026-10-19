import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestComparison(unittest.TestCase):
    def test_quality(self) -> None:
        rng = random.Random(1)
        for _ in range(25):
            n = rng.randint(3, 8)
            pts = [(rng.random() * 50, rng.random() * 50) for _ in range(n)]
            opt = ex.tour_length(pts, ex.exact_tsp(pts))
            for tour in (ex.mst_tour(pts), ex.nearest_neighbour(pts), ex.two_opt(pts, ex.nearest_neighbour(pts)),
                         ex.randomized_restarts(pts, 5, rng), sol.best_start_nearest_neighbour(pts)):
                self.assertEqual(sorted(tour), list(range(n)))
                self.assertGreaterEqual(ex.tour_length(pts, tour), opt - 1e-9)
            self.assertLessEqual(ex.tour_length(pts, ex.mst_tour(pts)), 2 * opt + 1e-9)
            nn = ex.nearest_neighbour(pts)
            self.assertLessEqual(ex.tour_length(pts, ex.two_opt(pts, nn)), ex.tour_length(pts, nn) + 1e-9)
            self.assertLessEqual(ex.tour_length(pts, sol.best_start_nearest_neighbour(pts)), ex.tour_length(pts, nn) + 1e-9)

    def test_compare_and_guide(self) -> None:
        r = ex.compare(8, 2)
        self.assertLessEqual(r["exact"][0], min(v[0] for v in r.values()) + 1e-9)
        big = ex.compare(40, 3)
        self.assertNotIn("exact", big)
        self.assertLessEqual(big["random restarts + 2-opt"][0], big["nearest neighbour"][0])
        self.assertAlmostEqual(sol.gap_percent(110, 100), 10)
        self.assertEqual(sol.pick_approaches()["route for 8 delivery stops"], "exact (brute force, backtracking, DP, branch-and-bound)")
        self.assertEqual(ex.choose_approach(set()), "start exact on small cases, then measure approximations and heuristics against it")


if __name__ == "__main__":
    unittest.main()
