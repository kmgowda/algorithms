import random
import unittest

import ch13_examples as ex
import ch13_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_first_pass_may_be_unstable(self) -> None:       # Thinking Problem 1
        rng = random.Random(2)
        for _ in range(300):
            a = [rng.randint(0, 999) for _ in range(rng.randint(0, 30))]
            self.assertEqual(sol.radix_sort_first_pass_unstable(a, 3), sorted(a))
        self.assertEqual(sol.radix_sort_first_pass_unstable([], 2), [])
        self.assertEqual(sol.radix_sort_first_pass_unstable([7], 2), [7])
        # ... but radix sort as a whole is then not stable on records with equal keys
        tied = [("Ana", 31), ("Ben", 31)]
        first = ex.counting_sort_unstable(tied, 9, key=lambda r: r[1] % 10)
        self.assertEqual([r[0] for r in first], ["Ben", "Ana"])
        second = ex.counting_sort(first, 9, key=lambda r: r[1] // 10 % 10)
        self.assertEqual([r[0] for r in second], ["Ben", "Ana"])

    def test_only_last_stable_is_not_enough(self) -> None:
        self.assertEqual(sol.radix_sort_only_last_stable([102, 101], 3), [102, 101])
        self.assertEqual(ex.radix_sort([102, 101], 3), [101, 102])

    def test_sort_cubic_range(self) -> None:                  # Thinking Problem 2
        self.assertEqual(sol.sort_cubic_range([]), [])
        self.assertEqual(sol.sort_cubic_range([0]), [0])
        self.assertEqual(sol.sort_cubic_range([7, 0]), [0, 7])
        self.assertEqual(sol.sort_cubic_range([7, 0, 5, 3]), [0, 3, 5, 7])
        self.assertEqual(sol.sort_cubic_range([5, 5, 5]), [5, 5, 5])
        with self.assertRaises(ValueError):
            sol.sort_cubic_range([8, 0])                      # 8 is not below 2**3
        rng = random.Random(3)
        for _ in range(200):
            n = rng.randint(2, 50)
            a = [rng.randrange(n ** 3) for _ in range(n)]
            self.assertEqual(sol.sort_cubic_range(a), sorted(a))
        s = sol.cubic_range_steps(1_000_000)
        self.assertEqual((s["base n, 3 passes"], s["decimal passes"], s["base 10"]), (12_000_000, 18, 36_000_360))

    def test_negative_index_bug(self) -> None:                # Thinking Problem 3
        self.assertEqual(ex.counting_sort([3, -1, 2], 3), [2, 3, -1])
        with self.assertRaises(IndexError):
            ex.counting_sort([-5, 1], 1)
        self.assertEqual(ex.counting_sort_any([3, -1, 2]), [-1, 2, 3])


if __name__ == "__main__":
    unittest.main()
