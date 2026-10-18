import itertools
import random
import statistics
import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestExamples(unittest.TestCase):
    def test_is_sorted(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            v = [rng.randint(0, 5) for _ in range(rng.randint(0, 8))]
            self.assertEqual(ex.is_sorted(v), v == sorted(v))

    def test_leaderboard(self) -> None:
        self.assertEqual(ex.leaderboard([("Zoe", 90), ("Ali", 95), ("Ben", 90)]),
                         [("Ali", 95), ("Ben", 90), ("Zoe", 90)])

    def test_gap_median_merge(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            v = [rng.randint(0, 100) for _ in range(rng.randint(2, 10))]
            self.assertEqual(ex.smallest_gap(v), min(abs(a - b) for a, b in itertools.combinations(v, 2)))
            self.assertEqual(ex.median(v), statistics.median(v))
            meetings = []
            for _ in range(rng.randint(0, 6)):
                s = rng.randint(0, 20)
                meetings.append((s, s + rng.randint(0, 5)))
            merged = ex.merge_meetings(meetings)
            covered = {t for s, e in meetings for t in range(s * 2, e * 2 + 1)}
            self.assertEqual({t for s, e in merged for t in range(s * 2, e * 2 + 1)}, covered)
            self.assertTrue(all(merged[i][1] < merged[i + 1][0] for i in range(len(merged) - 1)))
        with self.assertRaises(ValueError):
            ex.median([])

    def test_largest_number(self) -> None:
        self.assertEqual(ex.largest_number([3, 30, 34, 5, 9]), "9534330")
        self.assertEqual(ex.largest_number([0, 0]), "0")
        rng = random.Random(3)
        for _ in range(100):
            nums = [rng.randint(0, 99) for _ in range(rng.randint(1, 5))]
            best = max(int("".join(map(str, p))) for p in itertools.permutations(nums))
            self.assertEqual(ex.largest_number(nums), str(best))

    def test_versions(self) -> None:
        self.assertEqual(ex.sort_versions(["1.10.0", "1.9.3", "1.2.10", "1.2.9"]), ["1.2.9", "1.2.10", "1.9.3", "1.10.0"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.relative_order([2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]),
                         [2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19])
        self.assertTrue(sol.can_attend_all([(9, 10), (10, 11)]))
        self.assertFalse(sol.can_attend_all([(9, 11), (10, 12)]))
        self.assertEqual(sol.sort_by_last_name(["Maya Rao", "Leo Adams", "ali rao"]), ["Leo Adams", "ali rao", "Maya Rao"])
        self.assertEqual(sol.h_index([3, 0, 6, 1, 5]), 3)
        self.assertEqual(sol.h_index([]), 0)


if __name__ == "__main__":
    unittest.main()
