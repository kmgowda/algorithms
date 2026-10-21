import itertools
import random
import unittest

import ch05_examples as ex


class TestChapter5(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual((ex.running_totals([]), ex.running_totals([5, -2, 3])), ([], [5, 3, 6]))
        for vals, want in [([9, 3, 5], (9, 0)), ([3, 5, 9], (9, 2)), ([4, 9, 2, 9], (9, 1)), ([7], (7, 0)),
                           ([-5, -2, -9], (-2, 1))]:
            self.assertEqual(ex.max_with_position(vals), want)
        for target, pos, looks in [(12, 0, 1), (58, 4, 5), (91, 8, 9), (50, -1, 9)]:
            self.assertEqual((ex.linear_search(ex.SHELF, target), ex.looks_for(ex.SHELF, target)), (pos, looks))
        self.assertEqual((ex.linear_search([47, 12, 47], 47), ex.linear_search([], 5), ex.looks_for([], 5)), (0, -1, 0))
        self.assertEqual((ex.any_above(ex.SHELF, 10), ex.any_above(ex.SHELF, 95), ex.any_above([], 5)),
                         ((True, 1), (False, 9), (False, 0)))
        self.assertEqual((ex.all_above(ex.SHELF, 5), ex.all_above(ex.SHELF, 20), ex.all_above([], 5)),
                         ((True, 9), (False, 1), (True, 0)))

    def test_against_builtins(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            xs = [rng.randint(-20, 20) for _ in range(rng.randint(1, 15))]
            self.assertEqual(ex.running_totals(xs), list(itertools.accumulate(xs)))
            self.assertEqual(ex.max_with_position(xs), (max(xs), xs.index(max(xs))))
            t = rng.randint(-20, 20)
            self.assertEqual(ex.linear_search(xs, t), xs.index(t) if t in xs else -1)
            self.assertEqual(ex.any_above(xs, t)[0], any(x > t for x in xs))
            self.assertEqual(ex.all_above(xs, t)[0], all(x > t for x in xs))

    def test_examples(self) -> None:
        self.assertEqual(ex.running_totals(ex.SHELF)[-1], 481)
        self.assertEqual(ex.running_totals(ex.SHELF)[3], 115)
        self.assertEqual(ex.max_with_position([v for _, v in ex.VISITS]), (61, 5))
        self.assertEqual([ex.looks_for(ex.SHELF, t) for t in (63, 12, 91, 64, 50)], [6, 1, 9, 9, 9])
        self.assertEqual(ex.any_above(ex.SHELF, 80), (True, 8))
        self.assertEqual(ex.all_above(ex.SHELF, 20), (False, 1))


if __name__ == "__main__":
    unittest.main()
