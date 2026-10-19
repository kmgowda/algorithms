import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestPatterns(unittest.TestCase):
    def test_suggestions(self) -> None:
        cases = {
            "Given a sorted array, find the first position of a target.": "binary search",
            "Return all subsets of a set of numbers.": "backtracking",
            "Count the number of ways to climb n stairs.": "dynamic programming",
            "Given course prerequisites, find an order to take all courses.": "topological sort",
            "Find the k largest elements in a stream.": "heap",
            "Find the next greater element for each value.": "stack",
        }
        for text, tech in cases.items():
            self.assertEqual(ex.suggest_techniques(text, 1)[0][0], tech)
        self.assertEqual(ex.suggest_techniques("Hello there", 3), [])
        self.assertEqual(sol.classify_set(), {"LC 3": "sliding window", "LC 20": "stack", "LC 200": "BFS",
                                              "LC 322": "dynamic programming", "LC 347": "heap", "LC 56": "sort + sweep / greedy"})

    def test_hints(self) -> None:
        self.assertIn("backtracking", ex.constraint_hint(10))
        self.assertIn("O(n log n)", ex.constraint_hint(10 ** 5))
        self.assertIn("O(n)", ex.constraint_hint(10 ** 8))
        self.assertIn("backtracking", sol.combined_hint("Return all subsets of the numbers.", 15))


if __name__ == "__main__":
    unittest.main()
