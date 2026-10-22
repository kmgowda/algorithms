import random
import unittest

import ch33_examples as ex
import ch33_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_count(self) -> None:
        r = random.Random(33)
        for _ in range(300):
            s = "".join(r.choice("ab") for _ in range(r.randint(0, 15)))
            self.assertEqual(ex.count_palindromes(s), sol.brute_count(s))

    def test_front(self) -> None:
        self.assertEqual((sol.shortest_front_palindrome("abcd"), sol.shortest_front_palindrome("aacecaaa")), ("dcbabcd", "aaacecaaa"))
        self.assertEqual(sol.shortest_front_palindrome(""), "")
        r = random.Random(2)
        for _ in range(300):
            s = "".join(r.choice("ab") for _ in range(r.randint(1, 10)))
            p = sol.shortest_front_palindrome(s)
            self.assertTrue(p == p[::-1] and p.endswith(s))
            best = min(k for k in range(len(s) + 1) if (s[len(s) - k:][::-1] + s) == (s[len(s) - k:][::-1] + s)[::-1])
            self.assertEqual(len(p), len(s) + best)

    def test_odd_only(self) -> None:
        self.assertEqual((sol.odd_only("noon"), ex.expand_around_centres("noon")[0]), ("n", "noon"))


if __name__ == "__main__":
    unittest.main()
