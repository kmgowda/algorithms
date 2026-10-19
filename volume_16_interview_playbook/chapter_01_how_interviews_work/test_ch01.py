import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestInterviews(unittest.TestCase):
    def test_rubric(self) -> None:
        self.assertAlmostEqual(sum(ex.RUBRIC.values()), 1.0)
        self.assertEqual(ex.interview_score({a: 4 for a in ex.RUBRIC}), 4.0)
        self.assertEqual(ex.interview_score({}), 1.0)
        r = {"problem solving": 4, "coding": 3, "communication": 4, "testing": 2, "complexity analysis": 3}
        self.assertEqual(ex.interview_score(r), 3.35)
        self.assertEqual(ex.hiring_signal(3.35), "hire")
        self.assertEqual([ex.hiring_signal(s) for s in (3.6, 3.0, 2.2, 1.5)], ["strong hire", "hire", "no hire", "strong no hire"])
        self.assertEqual(sol.weakest_area(r), "testing")
        self.assertEqual(sol.score_if_improved(r, "testing"), 3.5)

    def test_time_and_complexity(self) -> None:
        for total in (30, 45, 60):
            self.assertEqual(sum(ex.time_plan(total).values()), total)
        self.assertIn("O(2^n)", ex.feasible_complexity(20))
        self.assertNotIn("O(n^2)", ex.feasible_complexity(10 ** 5))
        self.assertEqual(sol.best_feasible(3000), "O(n^2)")
        self.assertEqual(sol.best_feasible(10 ** 5), "O(n log n)")


if __name__ == "__main__":
    unittest.main()
