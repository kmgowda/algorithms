import random
import unittest

import ch16_examples as ex
import ch16_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_rooms_equal_overlap(self) -> None:
        r = random.Random(16)
        for _ in range(150):
            reqs = []
            for i in range(r.randint(0, 8)):
                s = r.randint(0, 12)
                reqs.append((f"r{i}", s, s + r.randint(1, 5)))
            self.assertEqual(ex.rooms_needed(reqs)[0], ex.max_overlap(reqs))

    def test_stab_points(self) -> None:
        self.assertEqual(sol.stab_points(ex.REQUESTS), [10, 12, 14, 16])
        self.assertEqual(sol.stab_points([]), [])
        r = random.Random(3)
        for _ in range(150):
            reqs = []
            for i in range(r.randint(0, 6)):
                s = r.randint(0, 10)
                reqs.append((f"r{i}", s, s + r.randint(1, 4)))
            pts = sol.stab_points(reqs)
            self.assertTrue(all(any(s <= t < e for t in pts) for _, s, e in reqs))
            self.assertEqual(len(pts), sol.fewest_points_brute(reqs))

    def test_shortest_first_trap(self) -> None:
        self.assertEqual(len(ex.by_rule(sol.SHORT_TRAP, lambda r: r[2] - r[1])), 1)
        self.assertEqual(len(ex.earliest_finish(sol.SHORT_TRAP)), 2)
        self.assertEqual(ex.most_by_brute_force(sol.SHORT_TRAP), 2)


if __name__ == "__main__":
    unittest.main()
