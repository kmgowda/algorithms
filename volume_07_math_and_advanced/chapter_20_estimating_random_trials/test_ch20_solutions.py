import unittest

import ch20_examples as ex
import ch20_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_worst_case_error(self) -> None:
        for n in (1, 10, 100, 10000):
            for k in range(101):
                self.assertLessEqual(ex.standard_error(k / 100, n), sol.worst_standard_error(n) + 1e-15)
        self.assertEqual(ex.standard_error(0.5, 10000), sol.worst_standard_error(10000))

    def test_trials_for_any_p(self) -> None:
        self.assertEqual((sol.trials_for_any_p(0.01), sol.trials_for_any_p(0.05), sol.trials_for_any_p(0.1)), (10000, 400, 100))
        for h in (0.01, 0.02, 0.05):
            n = sol.trials_for_any_p(h)
            self.assertLessEqual(2 * sol.worst_standard_error(n), h + 1e-12)
            self.assertEqual(ex.trials_needed(0.5, h), n)

    def test_same_seed(self) -> None:
        self.assertEqual(sol.spread_of_estimates(20, 1000, True), 0.0)
        self.assertGreater(sol.spread_of_estimates(20, 1000, False), 0.01)


if __name__ == "__main__":
    unittest.main()
