import random
import unittest

import ch26_examples as ex
import ch26_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_comparisons(self) -> None:
        r = random.Random(26)
        for _ in range(300):
            text = "".join(r.choice("AB") for _ in range(r.randint(1, 40)))
            pat = "".join(r.choice("AB") for _ in range(r.randint(1, 6)))
            self.assertLessEqual(ex.kmp_search(text, pat)[1], 2 * len(text) - 1)

    def test_period(self) -> None:
        self.assertEqual((sol.shortest_period("abcabcabc"), sol.shortest_period("aaaa"), sol.shortest_period("abcab")), ("abc", "a", "abcab"))
        self.assertEqual(sol.shortest_period(""), "")
        r = random.Random(2)
        for _ in range(300):
            s = "".join(r.choice("ab") for _ in range(r.randint(1, 12)))
            want = next(s[:p] for p in range(1, len(s) + 1) if len(s) % p == 0 and s[:p] * (len(s) // p) == s)
            self.assertEqual(sol.shortest_period(s), want)

    def test_reset_bug(self) -> None:
        self.assertEqual((sol.kmp_reset_bug("AAAA", "AAA"), ex.kmp_search("AAAA", "AAA")[0]), ([0], [0, 1]))


if __name__ == "__main__":
    unittest.main()
