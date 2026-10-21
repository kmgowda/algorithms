import random
import unittest

import ch29_examples as ex


class TestChapter29(unittest.TestCase):
    def test_leaflet(self) -> None:
        d = ex.diff(ex.OLD, ex.NEW)
        self.assertEqual((ex.changes(d), ex.apply_diff(ex.OLD, d)), ((3, 2, 2), ex.NEW))
        self.assertEqual(d[1:3], [("- ", "Opening hours: 9 to 5"), ("+ ", "Opening hours: 9 to 6")])

    def test_every_case(self) -> None:
        self.assertEqual((ex.diff([], []), ex.diff([], ["a"]), ex.diff(["a"], [])), ([], [("+ ", "a")], [("- ", "a")]))
        self.assertEqual((ex.changes(ex.diff(["a", "b"], ["a", "b"])), ex.diff(["a", "b"], ["b", "a"])), ((2, 0, 0), [("- ", "a"), ("  ", "b"), ("+ ", "a")]))
        self.assertEqual(ex.diff(["x", "y", "z"], ["x", "z"]), [("  ", "x"), ("- ", "y"), ("  ", "z")])
        r = random.Random(29)
        for _ in range(300):
            a = [r.choice("xyz") for _ in range(r.randint(0, 8))]
            b = [r.choice("xyz") for _ in range(r.randint(0, 8))]
            d = ex.diff(a, b)
            self.assertEqual(ex.apply_diff(a, d), b)
            self.assertEqual([x for t, x in d if t != "+ "], a)
            L = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
            for i in range(len(a)):
                for j in range(len(b)):
                    L[i + 1][j + 1] = L[i][j] + 1 if a[i] == b[j] else max(L[i][j + 1], L[i + 1][j])
            self.assertEqual(ex.changes(d)[0], L[-1][-1])


if __name__ == "__main__":
    unittest.main()
