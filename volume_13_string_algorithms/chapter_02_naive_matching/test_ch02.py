import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestNaive(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            t = "".join(rng.choice("ab") for _ in range(rng.randint(0, 25)))
            p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
            expected = [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]
            self.assertEqual(ex.naive_search(t, p)[0], expected)
            self.assertEqual(ex.first_occurrence(t, p), t.find(p))
            wild = "".join(rng.choice("ab?") for _ in range(rng.randint(1, 3)))
            self.assertEqual(sol.match_with_wildcards(t, wild),
                             [i for i in range(len(t) - len(wild) + 1) if all(c == "?" or c == t[i + j] for j, c in enumerate(wild))])
            k = rng.randint(0, 2)
            self.assertEqual(sol.count_matches_with_mismatches(t, p, k),
                             [i for i in range(len(t) - len(p) + 1) if sum(a != b for a, b in zip(t[i:i + len(p)], p)) <= k])

    def test_costs(self) -> None:
        t, p = ex.worst_case(10000, 50)
        self.assertEqual(ex.naive_search(t, p)[1], sol.worst_case_formula(10000, 50))
        t, p = ex.random_case(10000, 50, "abcdefghijklmnopqrstuvwxyz")
        self.assertLess(ex.naive_search(t, p)[1], 2 * 10000)
        self.assertEqual(ex.first_occurrence("sadbutsad", "sad"), 0)
        self.assertEqual(ex.first_occurrence("abc", ""), 0)
        self.assertEqual(ex.count_words("The cat sat. The cat ran!", "cat"), 2)
        self.assertEqual(ex.find_motif("ttgacatttgacaTATAAT", "tgaca"), [1, 8])


if __name__ == "__main__":
    unittest.main()
