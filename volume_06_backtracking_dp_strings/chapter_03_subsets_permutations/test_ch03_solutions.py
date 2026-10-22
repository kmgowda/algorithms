import itertools
import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestChapter03Solutions(unittest.TestCase):
    def test_next_combination(self) -> None:
        for n in range(0, 7):
            for k in range(0, n + 1):
                every = [list(c) for c in itertools.combinations(range(n), k)]
                got, c = [], list(range(k))
                while c is not None:
                    got.append(c)
                    c = sol.next_combination(c, n)
                self.assertEqual(got, every)
        self.assertEqual(sol.next_combination([0, 3, 4], 5), [1, 2, 3])
        self.assertIsNone(sol.next_combination([2, 3, 4], 5))

    def test_reversed_skip_rule(self) -> None:
        for w in ["", "A", "AAB", "BOOKS", "AAAB", "ABAB"]:
            orders, _ = sol.distinct_permutations_reversed(list(w))
            self.assertEqual(sorted(orders), sorted(ex.distinct_permutations(list(w))))
            self.assertEqual(len(orders), len({tuple(o) for o in orders}))
        self.assertEqual(sol.distinct_permutations_reversed(list("AAB"))[1], 12)
        self.assertEqual(sol.distinct_permutations_reversed(list("AAAB"))[1], 32)


if __name__ == "__main__":
    unittest.main()
