import random
import unittest

import ch02_examples as ex


PILE9 = [58, 25, 91, 12, 70, 47, 84, 31, 63]
CASES = [PILE9, sorted(PILE9), sorted(PILE9, reverse=True), [47] * 9, [58, 25, 58, 12, 25, 47, 58, 12, 47], [47], []]


class TestChapter08(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual([tuple(ex.selection_sort(list(a)).values()) for a in CASES], [(36, 7), (36, 0), (36, 4), (36, 0), (36, 6), (0, 0), (0, 0)])

    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 50) for _ in range(rng.randint(0, 25))]
            b = list(a)
            c = ex.selection_sort(b)
            self.assertEqual(b, sorted(a))
            self.assertEqual(c["comparisons"], len(a) * (len(a) - 1) // 2 if a else 0)
            self.assertLessEqual(c["swaps"], max(len(a) - 1, 0))

    def test_examples(self) -> None:
        a = list(ex.PILE)
        p = []
        self.assertEqual(ex.selection_sort(a, p), {"comparisons": 36, "swaps": 7})
        self.assertEqual(p[0], (0, 3, [12, 25, 91, 58, 70, 47, 84, 31, 63]))
        self.assertEqual(ex.selection_sort(sorted(ex.PILE))["swaps"], 0)
        self.assertEqual(ex.selection_sort(sorted(ex.PILE, reverse=True))["swaps"], 4)
        self.assertEqual(ex.selection_sort([5, 4, 3, 2, 1])["swaps"], 2)
        b = [2, 3, 4, 5, 1]
        self.assertEqual(ex.selection_sort(b)["swaps"], 4)          # Problem 8.2: a rotation forces n - 1 swaps
        self.assertEqual(ex.insertion_moves(ex.PILE), 17)
        sel, ins = ex.crate_comparison(trials=50)
        self.assertLess(sel, 20)
        self.assertGreater(ins, sel)


if __name__ == "__main__":
    unittest.main()
