import unittest

import ch10_examples as ex


class TestChapter10(unittest.TestCase):
    def test_examples(self) -> None:
        codes = [ex.gray(i) for i in range(8)]
        self.assertEqual(([format(c, "03b") for c in codes], ex.flips(codes)), (["000", "001", "011", "010", "110", "111", "101", "100"], [1] * 7))
        self.assertEqual((ex.flips(list(range(8))), ex.gray(255), ex.lowest_bit(84), ex.lowest_bit(96)), ([1, 2, 1, 3, 1, 2, 1], 128, 4, 32))
        self.assertEqual((sum(ex.flips(list(range(256)))), sum(ex.flips([ex.gray(i) for i in range(256)]))), (502, 255))

    def test_every_case(self) -> None:
        self.assertEqual((ex.gray(0), ex.from_gray(0), ex.is_power_of_two(0), ex.is_power_of_two(1), ex.lowest_bit(0), ex.flips([]), ex.flips([5])),
                         (0, 0, False, True, 0, [], []))
        self.assertEqual(bin(ex.gray(7) ^ ex.gray(0)).count("1"), 1)
        for n in range(5000):
            self.assertEqual(ex.from_gray(ex.gray(n)), n)
            self.assertEqual(ex.is_power_of_two(n), n > 0 and bin(n).count("1") == 1)


if __name__ == "__main__":
    unittest.main()
