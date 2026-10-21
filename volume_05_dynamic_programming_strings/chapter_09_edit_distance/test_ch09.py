import random
import unittest

import ch09_examples as ex


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


if __name__ == "__main__":
    unittest.main()
