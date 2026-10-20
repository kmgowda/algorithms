import random
import unittest

import ch10_examples as ex


class TestChapter10(unittest.TestCase):
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
