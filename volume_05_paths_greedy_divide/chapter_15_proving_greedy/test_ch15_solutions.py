import random
import unittest

import ch15_examples as ex
import ch15_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_shortest_first(self) -> None:
        r = random.Random(15)
        for _ in range(100):
            jobs = [(i, r.randint(1, 9)) for i in range(r.randint(0, 6))]
            self.assertEqual(sol.total_finish(sol.shortest_first(jobs)), sol.best_total_finish(jobs))

    def test_rewards(self) -> None:
        jobs = [("a", 2, 100), ("b", 1, 19), ("c", 2, 27), ("d", 1, 25), ("e", 3, 15)]
        self.assertEqual(sol.schedule_rewards(jobs), (142, {2: "a", 1: "c", 3: "e"}))
        self.assertEqual(sol.schedule_rewards([]), (0, {}))
        r = random.Random(2)
        for _ in range(150):
            jobs = [(i, r.randint(1, 4), r.randint(1, 30)) for i in range(r.randint(0, 7))]
            self.assertEqual(sol.schedule_rewards(jobs)[0], sol.best_rewards(jobs))

    def test_slack_trap(self) -> None:
        self.assertEqual(ex.lateness(sol.least_slack_first(sol.SLACK_TRAP))[0], 2)
        self.assertEqual(ex.best_lateness(sol.SLACK_TRAP), 1)
        self.assertEqual(ex.lateness(ex.earliest_deadline_first(sol.SLACK_TRAP))[0], 1)


if __name__ == "__main__":
    unittest.main()
