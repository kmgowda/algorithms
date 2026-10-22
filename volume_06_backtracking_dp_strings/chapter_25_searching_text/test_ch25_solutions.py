import random
import unittest

import ch25_examples as ex
import ch25_solutions as sol


def brute_wild(text, pattern):
    m = len(pattern)
    return [s for s in range(len(text) - m + 1)
            if all(p == "?" or p == t for p, t in zip(pattern, text[s:s + m]))]


class TestChapter25Solutions(unittest.TestCase):
    def test_wildcard_search(self) -> None:
        self.assertEqual(sol.wildcard_search("", ""), ([0], 0))
        self.assertEqual(sol.wildcard_search("", "a"), ([], 0))
        self.assertEqual(sol.wildcard_search("ab", ""), ([0, 1, 2], 0))
        self.assertEqual(sol.wildcard_search("ab", "??")[0], [0])
        self.assertEqual(sol.wildcard_search("abcab", "a?")[0], [0, 3])
        found, comparisons = sol.wildcard_search(ex.random_text(), "???????y")
        self.assertEqual((len(found), comparisons), (383, 9993))
        r = random.Random(25)
        for _ in range(300):
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 12)))
            p = "".join(r.choice("ab?") for _ in range(r.randint(0, 4)))
            self.assertEqual(sol.wildcard_search(t, p)[0], brute_wild(t, p))
            if "?" not in p:
                self.assertEqual(sol.wildcard_search(t, p), ex.naive_search(t, p))

    def test_skip_ahead_bug(self) -> None:
        self.assertEqual(sol.skip_ahead_bug("aab", "ab"), [])
        self.assertEqual(ex.naive_search("aab", "ab")[0], [1])
        self.assertEqual(sol.skip_ahead_bug("aaab", "aab", 0), [])

    def test_first_letter_bound(self) -> None:
        r = random.Random(1)
        for _ in range(300):
            t = "".join(r.choice("abc") for _ in range(r.randint(0, 30)))
            p = "a" + "".join(r.choice("bc") for _ in range(r.randint(0, 4)))
            self.assertTrue(sol.first_letter_bound_holds(t, p))
        self.assertTrue(sol.first_letter_bound_holds(ex.NEWSLETTER, "club"))


if __name__ == "__main__":
    unittest.main()
