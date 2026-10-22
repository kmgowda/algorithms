import bisect
import random
import unittest

import ch04_examples as ex


class TestChapter4(unittest.TestCase):
    def test_every_case(self) -> None:
        for new, shifts in [(5, 9), (40, 6), (58, 4), (95, 0)]:
            s = list(ex.SHELF)
            self.assertEqual(ex.insert_sorted(s, new), shifts)
            self.assertEqual(s, sorted(ex.SHELF + [new]))
        s = []
        self.assertEqual((ex.insert_sorted(s, 40), s), (0, [40]))
        for index, shifts in [(0, 8), (4, 4), (8, 0)]:
            self.assertEqual(ex.remove_at(list(ex.SHELF), index), shifts)
        s = [7]
        self.assertEqual((ex.remove_at(s, 0), s), (0, []))
        with self.assertRaises(IndexError):
            ex.remove_at([], 0)
        for bad in (9, -1):
            s = list(ex.SHELF)
            with self.assertRaises(IndexError):
                ex.remove_at(s, bad)
            self.assertEqual(s, ex.SHELF)
        self.assertIsNone(ex.TITLES.get(47))
        with self.assertRaises(KeyError):
            ex.TITLES[47]
        self.assertEqual([ex.copies_while_appending(n) for n in (0, 1, 2, 3, 9, 16, 17)], [0, 0, 1, 2, 4, 4, 5])

    def test_insert_and_remove(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            xs = sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 12)))
            new = rng.randint(0, 50)
            expected = xs[:]
            bisect.insort_right(expected, new)
            shifts = ex.insert_sorted(xs, new)
            self.assertEqual(xs, expected)
            self.assertEqual(shifts, sum(1 for v in xs if v > new))
            if xs:
                k = rng.randrange(len(xs))
                ys, zs = xs[:], xs[:]
                del zs[k]
                self.assertEqual(ex.remove_at(ys, k), len(xs) - 1 - k)
                self.assertEqual(ys, zs)

    def test_examples(self) -> None:
        s = ex.SHELF[:]
        self.assertEqual(ex.insert_sorted(s, 40), 6)
        self.assertEqual(ex.insert_sorted(ex.SHELF[:], 95), 0)
        self.assertEqual(ex.insert_sorted(ex.SHELF[:], 5), 9)
        s = [12, 25, 31, 47, 58, 63, 70]
        self.assertEqual(ex.insert_sorted(s, 60), 2)
        self.assertEqual(ex.address_of(1000, 7), 1007)
        self.assertEqual(ex.copies_while_appending(9), 4)


    def test_sizes_and_items_copied(self) -> None:
        self.assertEqual(ex.address_of(2000, 6, 8), 2048)
        self.assertEqual(ex.address_of(2000, 0, 8), 2000)
        self.assertEqual(ex.address_of(1000, 7), 1007)
        self.assertEqual([ex.items_copied_while_appending(n) for n in (0, 1, 2, 9, 16, 17)], [0, 0, 1, 15, 15, 31])

if __name__ == "__main__":
    unittest.main()
