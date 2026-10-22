import importlib.util
import itertools
import random
import unittest
from fractions import Fraction
from pathlib import Path

import ch24_examples as ex

_spec = importlib.util.spec_from_file_location(
    "ch23_corners_for_ch24", Path(__file__).resolve().parent.parent / "chapter_23_linear_programs" / "ch23_examples.py")
corners = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(corners)


class TestChapter24(unittest.TestCase):
    def test_library_trace(self) -> None:
        steps = []
        res = ex.simplex(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C, trace=steps)
        self.assertEqual((res["status"], res["x"], res["value"], res["slack"]), ("optimal", [30, 20], 130, [0, 0, 30]))
        self.assertEqual(steps, [(0, 2, 40), (1, 3, 20)])          # x enters for s1 (walk 40), y enters for s2 (walk 20)
        self.assertEqual(res["duals"], [1, 1, 0])
        self.assertEqual(ex.corners_walked(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C), [(0, 0), (40, 0), (30, 20)])
        T, basis = ex.tableau(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C)
        ex.pivot(T, basis, 0, 0)
        self.assertEqual(T[-1], [0, Fraction(1, 2), Fraction(-3, 2), 0, 0, -120])
        self.assertEqual(ex.leaving(T, basis, 1), 1)

    def test_every_case(self) -> None:
        self.assertEqual(ex.simplex([[1, -1]], [2], [1, 1])["status"], "unbounded")
        self.assertEqual(ex.simplex(ex.LIBRARY_A + [[0, -1]], ex.LIBRARY_B + [-45], ex.LIBRARY_C)["status"], "infeasible")
        start = ex.simplex(ex.LIBRARY_A + [[0, -1]], ex.LIBRARY_B + [-10], ex.LIBRARY_C)
        self.assertEqual((start["status"], start["x"], start["value"]), ("optimal", [30, 20], 130))
        self.assertEqual(ex.simplex(ex.LIBRARY_A, ex.LIBRARY_B, [-1, -1])["pivots"], 0)     # best at the origin
        tie = ex.simplex(ex.LIBRARY_A, ex.LIBRARY_B, [2, 2])
        self.assertEqual(tie["value"], 100)
        self.assertIn(0, [v for k, v in enumerate(tie["tableau"][-1][:-1]) if k not in tie["basis"]])
        self.assertEqual(ex.simplex([], [], [-1, -2])["value"], 0)                          # no rules
        self.assertEqual(ex.simplex([[3]], [12], [5])["x"], [4])                            # one variable
        self.assertEqual(ex.simplex([[1, 1], [1, 0], [0, 1]], [2, 1, 1], [1, 1])["value"], 2)  # degenerate corner
        self.assertEqual(ex.simplex([[1]], [0], [1])["value"], 0)

    def test_cycling_and_bland(self) -> None:
        T, basis = ex.tableau(ex.CYCLING_A, ex.CYCLING_B, ex.CYCLING_C)
        steps = []
        self.assertEqual(ex.run(T, basis, "largest", steps), "cycling")
        self.assertEqual(len(steps), 6)
        self.assertTrue(all(walk == 0 for _, _, walk in steps))
        res = ex.simplex(ex.CYCLING_A, ex.CYCLING_B, ex.CYCLING_C)
        self.assertEqual((res["status"], res["value"], res["x"]), ("optimal", 1, [1, 0, 1, 0]))

    def test_klee_minty(self) -> None:
        for n in range(1, 7):
            res = ex.simplex(*ex.klee_minty(n), rule="largest")
            self.assertEqual((res["pivots"], res["value"]), (2 ** n - 1, 5 ** n))

    def test_random_against_corners(self) -> None:
        r = random.Random(24)
        for _ in range(150):
            m, n = r.randint(1, 4), r.randint(1, 3)
            A = [[r.randint(-2, 6) for _ in range(n)] for _ in range(m)]
            b = [r.randint(-3, 20) for _ in range(m)]
            c = [r.randint(-2, 5) for _ in range(n)]
            res = ex.simplex(A, b, c)
            pts = corners.corners(A, b)
            if res["status"] == "infeasible":
                self.assertEqual(pts, [])
            elif res["status"] == "optimal":
                self.assertEqual(res["value"], max(sum(ci * xi for ci, xi in zip(c, x)) for x in pts))
                self.assertTrue(corners.feasible(A, b, res["x"]))
            else:
                self.assertEqual(res["status"], "unbounded")
                capped = [ex.simplex(A + [[1] * n], b + [cap], c)["value"] for cap in (100, 200)]
                self.assertLess(capped[0], capped[1])          # a bigger cap always buys more: no best plan


if __name__ == "__main__":
    unittest.main()
