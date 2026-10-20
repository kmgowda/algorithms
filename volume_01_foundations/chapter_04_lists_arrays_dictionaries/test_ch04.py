import bisect
import random
import unittest

import ch04_examples as ex


class TestChapter4(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
