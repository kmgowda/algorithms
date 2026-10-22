import unittest

import ch12_examples as ex
import ch12_solutions as sol


def brute(books: int) -> int:
    k = 0
    while ex.gauss_sum(k + 1) <= books:
        k += 1
    return k


class TestChapter12Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual([sol.staircase_steps(n) for n in (0, 1, 2, 3, 5, 6)], [0, 1, 1, 2, 2, 3])

    def test_example(self) -> None:
        self.assertEqual(sol.staircase_steps(100), 13)
        self.assertEqual(sol.staircase_steps(5050), 100)
        self.assertEqual(sol.staircase_steps(5049), 99)

    def test_against_brute_force(self) -> None:
        for n in range(0, 3000):
            self.assertEqual(sol.staircase_steps(n), brute(n))
        for n in (10 ** 9, 10 ** 12 + 7):
            k = sol.staircase_steps(n)
            self.assertTrue(ex.gauss_sum(k) <= n < ex.gauss_sum(k + 1))


if __name__ == "__main__":
    unittest.main()
