import unittest

import ch23_examples as ex


class TestChapter23(unittest.TestCase):
    def test_examples(self) -> None:
        a, b = [0], [0]
        self.assertEqual((ex.has_repeat_pairs(ex.RETURNS, a), a[0], ex.has_repeat_sorted(ex.RETURNS, b), b[0]), (True, 14, True, 1))
        c1, c2 = [0], [0]
        self.assertEqual((ex.horner([2, -6, 2, -1], 3, c1), c1[0], ex.naive_poly([2, -6, 2, -1], 3, c2), c2[0]), (5, 4, 5, 6))
        self.assertEqual(ex.k_smallest(ex.RETURNS, 3), [12, 12, 25])

    def test_every_case(self) -> None:
        self.assertFalse(ex.has_repeat_pairs([], [0]) or ex.has_repeat_sorted([], [0]) or ex.has_repeat_sorted([5], [0]))
        d, a, b = list(range(1000)), [0], [0]
        ex.has_repeat_pairs(d, a)
        ex.has_repeat_sorted(d, b)
        self.assertEqual((a[0], b[0]), (499500, 999))
        self.assertEqual([ex.mode(v) for v in ([], [4, 4, 7, 7], [9], [3, 1, 3, 2, 1, 3])], [None, 4, 9, 3])
        c1, c2 = [0], [0]
        ex.horner([1] * 11, 2, c1)
        ex.naive_poly([1] * 11, 2, c2)
        self.assertEqual((c1[0], c2[0], ex.horner([], 5, [0]), ex.horner([7], 5, [0])), (11, 55, 0, 7))
        self.assertEqual((ex.k_smallest([], 3), ex.k_smallest([5, 1], 5)), ([], [1, 5]))


if __name__ == "__main__":
    unittest.main()
