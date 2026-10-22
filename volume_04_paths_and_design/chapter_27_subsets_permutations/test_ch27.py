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


    def test_cost(self) -> None:
        self.assertEqual(ex.output_cost(4), {"subsets": 16, "subset items": 32, "orders": 24, "order items": 96})
        self.assertEqual(ex.output_cost(8)["order items"], 8 * 40320)
        self.assertEqual(ex.output_cost(0), {"subsets": 1, "subset items": 0, "orders": 1, "order items": 0})

    def test_cartesian(self) -> None:
        got = ex.cartesian([o for _, o in ex.GENRES])
        self.assertEqual((len(got), got[0], got[-1]), (6, ["Odes", "Atlas", "Stars"], ["Haiku", "Atlas", "Rocks"]))
        self.assertEqual((ex.cartesian([]), ex.cartesian([["a"], []])), ([[]], []))
        self.assertEqual(sorted(map(tuple, ex.cartesian([[1, 2], [3, 4]]))), list(itertools.product([1, 2], [3, 4])))

    def test_brackets(self) -> None:
        self.assertEqual(ex.brackets(3)[0], ["((()))", "(()())", "(())()", "()(())", "()()()"])
        self.assertEqual([ex.brackets(n)[1] for n in range(6)], [1, 3, 8, 22, 64, 196])
        self.assertEqual([ex.brackets(n, False)[1] for n in range(6)], [1, 7, 31, 127, 511, 2047])
        for n in range(7):
            self.assertEqual(len(ex.brackets(n)[0]), ex.catalan(n))
            self.assertEqual(ex.brackets(n)[0], ex.brackets(n, False)[0])

    def test_next_permutation(self) -> None:
        self.assertEqual(ex.next_permutation(list("ACB")), list("BAC"))
        self.assertEqual((ex.next_permutation(list("CBA")), ex.next_permutation([]), ex.next_permutation([7])),
                         (None, None, None))
        row, seen = list("AABC"), []
        while row:
            seen.append("".join(row))
            row = ex.next_permutation(row)
        self.assertEqual(len(seen), 12)
        self.assertEqual(seen, sorted(set(seen)))


if __name__ == "__main__":
    unittest.main()
