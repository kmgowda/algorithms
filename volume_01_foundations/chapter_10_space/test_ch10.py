import random
import unittest

import ch10_examples as ex


class TestChapter10(unittest.TestCase):
    def test_every_case(self) -> None:
        for a in ([], [7], [1, 2], [1, 2, 3], list(ex.SHELF)):
            b = list(a)
            ex.reverse_in_place(b)
            self.assertEqual(b, a[::-1])
            self.assertEqual(ex.reverse_by_copying(a), a[::-1])
        rows = [([], (False, 0), (None, 0)), ([5], (False, 0), (None, 1)), ([5, 5], (True, 1), (5, 2)),
                ([1, 2, 3, 4], (False, 6), (None, 4)), ([4, 1, 2, 4], (True, 3), (4, 4)),
                (list(range(9)), (False, 36), (None, 9)), (ex.RETURNS, (True, 17), (63, 5))]
        for items, pairs, seen in rows:
            self.assertEqual((ex.has_duplicate_pairs(items), ex.first_duplicate_with_memory(items)), (pairs, seen))

    def test_reverse(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            xs = [rng.randint(0, 99) for _ in range(rng.randint(0, 12))]
            ys = xs[:]
            ex.reverse_in_place(ys)
            self.assertEqual(ys, xs[::-1])
            self.assertEqual(ex.reverse_by_copying(xs), xs[::-1])
            self.assertEqual(ex.has_duplicate_pairs(xs)[0], len(set(xs)) < len(xs))
            self.assertEqual(ex.first_duplicate_with_memory(xs)[0] is not None, len(set(xs)) < len(xs))

    def test_examples(self) -> None:
        self.assertEqual(ex.has_duplicate_pairs(list(range(9))), (False, 36))
        self.assertEqual(ex.first_duplicate_with_memory(ex.RETURNS), (63, 5))
        self.assertEqual(ex.first_duplicate_with_memory([31, 12, 70, 12]), (12, 4))


if __name__ == "__main__":
    unittest.main()
