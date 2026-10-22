import itertools
import random
import unittest

import ch15_solutions as sol


class TestChapter15Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.gray_order([]), [[]])
        self.assertEqual(sol.gray_order(["A"]), [[], ["A"]])
        self.assertEqual(sol.changed_items([[]]), [])
        self.assertEqual(sol.distinct_permutations([]), [[]])
        self.assertEqual(sol.distinct_permutations(["A"]), [["A"]])
        self.assertEqual(sol.distinct_permutations(["A", "A"]), [["A", "A"]])

    def test_worked_example(self) -> None:
        order = sol.gray_order(list("ABC"))
        self.assertEqual(["".join(s) for s in order], ["", "C", "BC", "B", "AB", "ABC", "AC", "A"])
        self.assertEqual(sol.changed_items(order), list("CBCACBC"))   # the Hanoi pattern 1 2 1 3 1 2 1
        self.assertEqual(["".join(p) for p in sol.distinct_permutations(list("ABA"))], ["ABA", "AAB", "BAA"])

    def test_gray_order_against_brute_force(self) -> None:
        for n in range(0, 10):
            items = list("ABCDEFGHIJ"[:n])
            order = sol.gray_order(items)
            self.assertEqual(len(order), 2 ** n)
            self.assertEqual(sorted(tuple(sorted(s)) for s in order),
                             sorted(c for r in range(n + 1) for c in itertools.combinations(items, r)))
            self.assertEqual(len(sol.changed_items(order)), 2 ** n - 1)          # one item per step
        with self.assertRaises(ValueError):
            sol.changed_items([[], ["A", "B"]])

    def test_distinct_permutations_against_brute_force(self) -> None:
        rng = random.Random(15)
        for _ in range(200):
            items = [rng.choice("ABC") for _ in range(rng.randint(0, 6))]
            got = [tuple(p) for p in sol.distinct_permutations(items)]
            self.assertEqual(len(got), len(set(got)))                            # no repeats
            self.assertEqual(set(got), set(itertools.permutations(items)))      # and none missing


if __name__ == "__main__":
    unittest.main()
