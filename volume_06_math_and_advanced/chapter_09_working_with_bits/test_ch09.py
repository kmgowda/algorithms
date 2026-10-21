import random
import unittest

import ch09_examples as ex


class TestChapter9(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.to_binary(5), ex.to_binary(84), ex.to_binary(255)), ("00000101", "01010100", "11111111"))
        a, b = ex.make_set(["large print", "audio", "kids"]), ex.make_set(["audio", "e-book", "kids"])
        self.assertEqual((a, b, ex.members(a & b), ex.members(a ^ b), ex.members(a & ~b)), (19, 26, ["audio", "kids"], ["large print", "e-book"], ["large print"]))
        self.assertEqual((ex.popcount(84), ex.popcount(2 ** 40 - 1), len(ex.subsets(a))), ((3, 3), (40, 40), 8))

    def test_every_case(self) -> None:
        self.assertEqual((ex.to_binary(0), ex.members(0), ex.subsets(0), ex.make_set([]), 84 >> 2, 84 << 1), ("00000000", [], [0], 0, 21, 168))
        with self.assertRaises(ValueError):
            ex.to_binary(-1)
        r = random.Random(9)
        for _ in range(300):
            n = r.randint(0, 2 ** 20)
            self.assertEqual(ex.popcount(n)[0], bin(n).count("1"))
            m = r.randint(0, 63)
            self.assertEqual(len(ex.subsets(m)), 2 ** bin(m).count("1"))


if __name__ == "__main__":
    unittest.main()
