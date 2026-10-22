import random
import unittest

import ch05_examples as ex


class TestChapter5(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.crt([2, 3, 2], [3, 5, 7]), ex.crt([1, 2, 3, 4], [2, 3, 5, 7])), ((23, 105), (53, 210)))
        self.assertEqual((ex.crt([3, 4], [6, 8]), ex.crt([1, 2], [4, 6]), ex.crt([2, 4], [6, 8])), ((None, 24), (None, 12), (20, 24)))

    def test_every_case(self) -> None:
        self.assertEqual([ex.crt(r, m) for r, m in (([], []), ([5], [7]), ([12], [7]), ([0, 0, 0], [3, 5, 7]), ([1, 1], [2, 4]))],
                         [(0, 1), (5, 7), (5, 7), (0, 105), (1, 4)])
        with self.assertRaises(ValueError):
            ex.crt([1], [0])
        self.assertEqual((ex.crt([1, 2], [2, 3]), ex.crt([900000 % 97, 900000 % 98, 900000 % 99], [97, 98, 99])[0]), ((5, 6), 900000))
        r = random.Random(5)
        for _ in range(300):
            mods = [r.randint(1, 12) for _ in range(r.randint(1, 3))]
            rems = [r.randint(0, 20) for _ in mods]
            self.assertEqual(ex.crt(rems, mods)[0], ex.crt_by_search(rems, mods))


class TestDepth(unittest.TestCase):
    def test_formula_and_trace(self) -> None:
        self.assertEqual(ex.crt_formula([2, 3, 2], [3, 5, 7]), (23, 105, [(35, 2, 140), (21, 1, 63), (15, 1, 30)]))
        self.assertEqual(ex.crt_trace([2, 3, 2], [3, 5, 7]), [(2, 2, 3), (2, 8, 15), (1, 23, 105)])
        self.assertEqual(ex.crt_trace([2, 4], [6, 8]), [(2, 2, 6), (3, 20, 24)])
        self.assertEqual(ex.crt_trace([3, 4], [6, 8])[-1], (None, None, 24))
        self.assertEqual((ex.crt_formula([], []), ex.crt_formula([0], [1])), ((0, 1, []), (0, 1, [(1, 0, 0)])))
        r = __import__("random").Random(5)
        for _ in range(300):
            ms = r.sample([2, 3, 5, 7, 11, 13, 17, 19, 23], r.randint(1, 4))
            rs = [r.randint(0, m - 1) for m in ms]
            self.assertEqual(ex.crt_formula(rs, ms)[0], ex.crt(rs, ms)[0])

    def test_chapter_numbers(self) -> None:
        self.assertEqual((ex.crt([1, 4, 6], [3, 5, 7]), ex.crt([5, 3], [6, 10]), ex.crt([1, 2], [4, 6])), ((34, 105), (23, 30), (None, 12)))
        self.assertEqual((ex.crt_formula([0, 0, 1], [3, 4, 5])[0], ex.to_residues(1000)), (36, [30, 20, 10]))
        self.assertEqual(ex.from_residues(ex.residue_mul(ex.to_residues(1000), ex.to_residues(1000))), 58_906)

    def test_residue_numbers(self) -> None:
        a, b = ex.to_residues(500_000), ex.to_residues(400_000)
        self.assertEqual((a, b, ex.from_residues(ex.residue_add(a, b))), ([62, 4, 50], [69, 62, 40], 900_000))
        self.assertEqual(ex.from_residues(ex.residue_mul(ex.to_residues(700), ex.to_residues(1300))), 910_000)
        self.assertEqual(ex.from_residues(ex.residue_mul(ex.to_residues(1000), ex.to_residues(1000))), 10 ** 6 % 941_094)


if __name__ == "__main__":
    unittest.main()
