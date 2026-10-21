import random
import unittest

import ch16_examples as ex


class TestChapter16(unittest.TestCase):
    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 20) for _ in range(rng.randint(0, 40))]
            self.assertEqual(ex.counting_sort(a, 20), sorted(a))
            b = [rng.randint(0, 99_999) for _ in range(rng.randint(0, 40))]
            self.assertEqual(ex.radix_sort(b, 5), sorted(b))
            c = [rng.randint(-50, 50) for _ in range(rng.randint(0, 30))]
            self.assertEqual(ex.counting_sort_any(c), sorted(c))

    def test_examples(self) -> None:
        s = {}
        self.assertEqual(ex.counting_sort(ex.GRADES, 5, steps=s), sorted(ex.GRADES))
        self.assertEqual((s["counts"], s["ends"]), ([0, 3, 2, 2, 3, 2], [0, 3, 5, 7, 10, 12]))
        p = []
        ex.radix_sort(ex.PILE, 2, passes=p)
        self.assertEqual(p[0], [70, 91, 31, 12, 63, 84, 25, 47, 58])

    def test_every_case(self) -> None:
        self.assertEqual(ex.counting_sort([4, 4, 4, 4], 5), [4, 4, 4, 4])
        self.assertEqual((ex.counting_sort([], 5), ex.counting_sort([7], 9)), ([], [7]))
        recs = [("Ben", 3), ("Ana", 1), ("Cai", 3), ("Dev", 2), ("Eva", 1)]
        self.assertEqual([r[0] for r in ex.counting_sort(recs, 3, key=lambda r: r[1])], ["Ana", "Eva", "Dev", "Ben", "Cai"])
        self.assertEqual(ex.counting_sort_any([3, -2, 0, -2, 5]), [-2, -2, 0, 3, 5])
        s = {}
        self.assertEqual(ex.counting_sort([2, 900000, 15], 900000, steps=s), [2, 15, 900000])
        self.assertEqual(len(s["counts"]), 900001)
        p = []
        self.assertEqual(ex.radix_sort([5, 312, 48, 7, 1000, 99], 4, passes=p), [5, 7, 48, 99, 312, 1000])
        self.assertEqual(p[2], [1000, 5, 7, 48, 99, 312])


if __name__ == "__main__":
    unittest.main()
