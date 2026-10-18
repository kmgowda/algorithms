import itertools
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestTemplate(unittest.TestCase):
    def test_generators(self) -> None:
        people = ["a", "b", "c", "d"]
        self.assertEqual(ex.arrangements(people), [list(p) for p in itertools.permutations(people)])
        rivals = {frozenset({"a", "b"}), frozenset({"c", "d"})}
        brute = [list(p) for p in itertools.permutations(people)
                 if all(frozenset(p[i:i + 2]) not in rivals for i in range(3))]
        self.assertEqual(ex.no_adjacent_rivals(people, rivals), brute)
        for n in range(1, 9):
            brute_bits = ["".join(p) for p in itertools.product("01", repeat=n) if "11" not in "".join(p)]
            self.assertEqual(ex.binary_strings_without_11(n), brute_bits)
            self.assertEqual(sol.count_with_visit_counter(n)[0], len(brute_bits))

    def test_maze_and_tests(self) -> None:
        paths = ex.maze_paths(["...", ".#.", "..."])
        self.assertEqual(len(paths), 2)
        self.assertTrue(all(p[0] == (0, 0) and p[-1] == (2, 2) for p in paths))
        self.assertEqual(len(ex.maze_paths(["...", "...", "..."])), 12)
        tests = ex.test_case_combinations({"os": ["linux", "mac"], "browser": ["chrome", "safari"], "lang": ["en", "hi"]},
                                          [{"os": "linux", "browser": "safari"}])
        self.assertEqual(len(tests), 6)

    def test_solutions(self) -> None:
        self.assertEqual(sol.words_from_tiles("aab", 2), ["aa", "ab", "ba"])
        self.assertEqual(sol.increasing_sequences(4, 2), [list(c) for c in itertools.combinations(range(1, 5), 2)])


if __name__ == "__main__":
    unittest.main()
