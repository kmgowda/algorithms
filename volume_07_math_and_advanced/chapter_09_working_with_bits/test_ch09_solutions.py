import unittest

import ch09_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_power_of_two_test(self) -> None:
        powers = {1 << k for k in range(17)}
        for n in range(1 << 16):
            self.assertEqual((n & (n - 1)) == 0, n == 0 or n in powers)
            self.assertEqual(sol.is_power_of_two(n), n in powers)

    def test_ones_up_to(self) -> None:
        self.assertEqual(sol.ones_up_to(-1), [])
        self.assertEqual(sol.ones_up_to(0), [0])
        self.assertEqual(sol.ones_up_to(1000), [bin(i).count("1") for i in range(1001)])
        self.assertEqual(sum(sol.ones_up_to(255)), 1024)

    def test_the_bug(self) -> None:
        import ch09_examples as ex
        self.assertEqual(sol.buggy_subsets(0b10010), [18, 16, 2])
        self.assertEqual(sol.buggy_subsets(0), [])
        for mask in range(64):
            self.assertEqual(len(sol.buggy_subsets(mask)), 2 ** bin(mask).count("1") - 1)
            self.assertEqual(sorted(sol.subsets_fixed(mask)), sorted(ex.subsets(mask)))


if __name__ == "__main__":
    unittest.main()
