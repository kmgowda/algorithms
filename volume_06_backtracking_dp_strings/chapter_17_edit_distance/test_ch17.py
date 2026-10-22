import random
import unittest

import ch17_examples as ex


class TestChapter9(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(ex.edit_distance("LIBRAY", "LIBRARY")[:2], (1, ["insert R"]))
        d, e, t = ex.edit_distance("PEOMS", "POEMS")
        self.assertEqual((d, e, t[2]), (2, ["replace E with O", "replace O with E"], [2, 1, 1, 1, 2, 3]))
        self.assertEqual(ex.edit_distance("KITTEN", "SITTING")[0], 3)
        self.assertEqual(ex.suggest("PALYS", ex.TITLES)[:3], [(2, "PLAYS"), (3, "ATLAS"), (3, "MAPS")])
        self.assertEqual(ex.suggest("NOBEL", ex.TITLES)[0], (1, "NOVEL"))

    def test_every_case(self) -> None:
        self.assertEqual(ex.edit_distance("", "ABC")[:2], (3, ["insert A", "insert B", "insert C"]))
        self.assertEqual(ex.edit_distance("ABC", "")[0], 3)
        self.assertEqual((ex.edit_distance("ABC", "ABC")[:2], ex.edit_distance("ABC", "XYZ")[0], ex.edit_distance("AB", "BA")[0]), ((0, []), 3, 2))
        self.assertEqual((ex.edit_distance("MAPS", "MOPS")[0], ex.edit_distance("CAT", "CART")[1], ex.edit_distance("NOVEL", "NOBEL")[1]),
                         (1, ["insert R"], ["replace V with B"]))
        r = random.Random(9)
        for _ in range(200):
            a = "".join(r.choice("AB") for _ in range(r.randint(0, 6)))
            b = "".join(r.choice("AB") for _ in range(r.randint(0, 6)))
            d, edits, _ = ex.edit_distance(a, b)
            self.assertEqual(len(edits), d)
            self.assertEqual(d, ex.edit_distance(b, a)[0])
            self.assertLessEqual(abs(len(a) - len(b)), d)


    def test_alignment(self) -> None:
        import functools
        import random
        self.assertEqual(ex.align("GATTACA", "GCATGCU")[:3], (0, "G-ATTACA", "GCA-TGCU"))
        self.assertEqual(ex.align("GATTACA", "GCATGCU", 0, -1, -1)[0], -4)
        self.assertEqual(ex.align("ACGTGCA", "ACGGCA", 2, -1, -2)[:3], (10, "ACGTGCA", "ACG-GCA"))
        self.assertEqual(ex.suggest("PALYS", ex.TITLES)[:4], [(2, "PLAYS"), (3, "ATLAS"), (3, "MAPS"), (3, "POEMS")])
        self.assertEqual(ex.suggest("NOBEL", ex.TITLES)[:3], [(1, "NOVEL"), (4, "COMIC"), (4, "POEMS")])
        self.assertEqual((ex.align("", "ABC")[:3], ex.align("A", "")[:3], ex.align("", "")[:3]),
                         ((-3, "---", "ABC"), (-1, "A", "-"), (0, "", "")))
        r = random.Random(9)
        for _ in range(200):
            a = "".join(r.choice("ACGT") for _ in range(r.randint(0, 7)))
            b = "".join(r.choice("ACGT") for _ in range(r.randint(0, 7)))
            mt, mm, gp = r.choice([(1, -1, -1), (2, -1, -2), (0, -1, -1), (3, -2, -1)])

            @functools.lru_cache(maxsize=None)
            def best(i: int, j: int) -> int:
                if i == 0 or j == 0:
                    return (i + j) * gp
                return max(best(i - 1, j - 1) + (mt if a[i - 1] == b[j - 1] else mm), best(i - 1, j) + gp, best(i, j - 1) + gp)

            score, top, bottom, _ = ex.align(a, b, mt, mm, gp)
            self.assertEqual(score, best(len(a), len(b)))
            self.assertEqual(ex.alignment_score(top, bottom, mt, mm, gp), score)
            self.assertEqual((top.replace("-", ""), bottom.replace("-", "")), (a, b))
            self.assertEqual(ex.align(a, b, 0, -1, -1)[0], -ex.edit_distance(a, b)[0])


if __name__ == "__main__":
    unittest.main()
