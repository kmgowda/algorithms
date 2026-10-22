import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_call_count(self) -> None:
        for n in range(0, 40):
            self.assertEqual(ex.plain_calls(n), 2 * ex.ways_memo(n + 1) - 1)

    def test_no_double_two(self) -> None:
        for n in range(0, 16):
            self.assertEqual(sol.no_double_two(n), sol.no_double_two_brute(n))
        self.assertEqual([sol.no_double_two(n) for n in range(8)], [1, 1, 2, 3, 4, 6, 9, 13])

    def test_zero_step(self) -> None:
        with self.assertRaises(ValueError):
            ex.ways_memo(5, (0, 1))
        self.assertEqual(ex.ways_memo(10), 89)


if __name__ == "__main__":
    unittest.main()
