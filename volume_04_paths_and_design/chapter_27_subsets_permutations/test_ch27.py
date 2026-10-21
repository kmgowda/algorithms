import itertools
import unittest

import ch27_examples as ex


class TestChapter27(unittest.TestCase):
    def test_books(self) -> None:
        self.assertEqual((len(ex.subsets(ex.BOOKS)), len(ex.permutations(ex.BOOKS)), len(ex.combinations(ex.BOOKS, 2))), (16, 24, 6))
        self.assertEqual(ex.combinations(ex.BOOKS, 2)[0], ["Atlas", "Novel"])
        self.assertEqual(ex.distinct_permutations(list("AAB")), [["A", "A", "B"], ["A", "B", "A"], ["B", "A", "A"]])
        self.assertEqual(len(ex.distinct_permutations(list("BOOKS"))), 60)

    def test_every_case(self) -> None:
        self.assertEqual((ex.subsets([]), ex.permutations([]), ex.combinations([], 0)), ([[]], [[]], [[]]))
        self.assertEqual((ex.combinations(ex.BOOKS, 0), ex.combinations(ex.BOOKS, 5)), ([[]], []))
        self.assertEqual([len(ex.combinations(list(range(6)), k)) for k in range(7)], [1, 6, 15, 20, 15, 6, 1])
        for n in range(6):
            items = list(range(n))
            self.assertEqual(sorted(map(tuple, ex.permutations(items))), sorted(itertools.permutations(items)))


if __name__ == "__main__":
    unittest.main()
