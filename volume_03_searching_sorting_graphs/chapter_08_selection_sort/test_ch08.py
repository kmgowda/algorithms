import random
import unittest

import ch08_examples as ex


class TestChapter08(unittest.TestCase):
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
        self.assertEqual(ex.insertion_moves(ex.PILE), 17)
        sel, ins = ex.crate_comparison(trials=50)
        self.assertLess(sel, 20)
        self.assertGreater(ins, sel)


if __name__ == "__main__":
    unittest.main()
