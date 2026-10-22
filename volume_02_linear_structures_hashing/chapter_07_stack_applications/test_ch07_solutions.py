import itertools
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


def brute_rectangle(h: list[int]) -> int:
    return max((min(h[i:j + 1]) * (j - i + 1) for i in range(len(h)) for j in range(i, len(h))), default=0)


class TestThinkingProblems(unittest.TestCase):
    def test_one_kind_counter_matches_stack(self) -> None:
        for n in range(9):
            for chars in itertools.product("()", repeat=n):
                s = "".join(chars)
                self.assertEqual(sol.balanced_one_kind(s), ex.balanced(s))
        self.assertTrue(sol.balanced_one_kind(""))
        self.assertFalse(sol.balanced_one_kind(")("))

    def test_rectangle_smallest_inputs(self) -> None:
        self.assertEqual(sol.largest_rectangle([]), 0)
        self.assertEqual(sol.largest_rectangle([7]), 7)
        self.assertEqual(sol.largest_rectangle([0, 0]), 0)
        self.assertEqual(sol.largest_rectangle([3, 3, 3]), 9)

    def test_rectangle_examples(self) -> None:
        self.assertEqual(sol.largest_rectangle([6, 2, 5, 4, 5, 1, 6]), 12)
        self.assertEqual(sol.largest_rectangle([22, 18, 25, 15, 17, 28, 20]), 105)

    def test_rectangle_against_brute_force(self) -> None:
        rng = random.Random(7)
        for _ in range(500):
            h = [rng.randint(0, 6) for _ in range(rng.randint(0, 10))]
            self.assertEqual(sol.largest_rectangle(h), brute_rectangle(h))

    def test_two_slots_fails(self) -> None:
        tokens = "3 4 2 * + 1 -".split()
        self.assertEqual(ex.evaluate_postfix(tokens), 10)
        self.assertEqual(sol.evaluate_postfix_two_slots(tokens), 7)
        self.assertEqual(sol.evaluate_postfix_two_slots("3 4 + 2 *".split()), 14)   # depth 2 is fine


if __name__ == "__main__":
    unittest.main()
