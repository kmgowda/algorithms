import math
import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestML(unittest.TestCase):
    def test_gradient_descent(self) -> None:
        rng = random.Random(1)
        for _ in range(20):
            xs = [rng.uniform(0, 5) for _ in range(rng.randint(3, 15))]
            ys = [rng.uniform(-2, 2) * x + rng.uniform(-3, 3) + rng.gauss(0, 0.5) for x in xs]
            if max(xs) - min(xs) < 0.5:
                continue
            w, b, hist = ex.gradient_descent_line(xs, ys, 0.02, 5000)
            ew, eb = ex.least_squares(xs, ys)
            self.assertAlmostEqual(w, ew, delta=0.05)
            self.assertAlmostEqual(b, eb, delta=0.05)
            self.assertTrue(all(h2 <= h1 + 1e-9 for h1, h2 in zip(hist, hist[1:])))
        self.assertAlmostEqual(sol.minimise_1d(lambda x: (x - 3) ** 2, lambda x: 2 * (x - 3), 0.0, 0.1, 200), 3, places=5)

    def test_kmeans(self) -> None:
        rng = random.Random(2)
        pts = ex.make_blobs([(0, 0), (20, 0), (10, 15)], 30, 1.0, rng)
        best = ex.best_of_restarts(pts, 3, 10, rng)
        centres, labels, cost = ex.kmeans(pts, 3, rng)
        self.assertGreaterEqual(cost, best - 1e-6)
        for p, lab in zip(pts, labels):
            self.assertEqual(min(range(3), key=lambda c: math.dist(p, centres[c])), lab)
        self.assertEqual(sorted((round(x / 10), round(y / 10)) for x, y in ex.segment_customers(pts, 3, rng)),
                         [(0, 0), (1, 2), (2, 0)])
        costs = sol.elbow(pts, 5, rng)
        self.assertTrue(all(b <= a + 1e-6 for a, b in zip(costs, costs[1:])))
        self.assertGreater(costs[1] / costs[2], 3)
        scaled = sol.scale_features([(100, 1), (300, 3), (200, 2)])
        self.assertAlmostEqual(sum(p[0] for p in scaled), 0)
        self.assertAlmostEqual(scaled[0][0], scaled[0][1])


if __name__ == "__main__":
    unittest.main()
