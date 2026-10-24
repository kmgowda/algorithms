import fnmatch
import random
import unittest

import ch36_examples as ex


class TestChapter28(unittest.TestCase):
    def test_titles(self) -> None:
        self.assertEqual(ex.search("tre?s*", ex.TITLES), ["treasure island", "trees of britain", "tress"])
        self.assertEqual((ex.search("*island", ex.TITLES), ex.search("t?e *", ex.TITLES)), (["treasure island", "island"], ["the treasure map"]))
        self.assertEqual([ex.wildcard("t*s", w)[0] for w in ("tress", "trees", "tree")], [True, True, False])
        c = [0]
        self.assertEqual((ex.plain_recursion("*a*a*a*b", "a" * 20, c), c[0], ex.wildcard("*a*a*a*b", "a" * 20)[0]), (False, 15092, False))

    def test_every_case(self) -> None:
        got = [ex.wildcard(p, t)[0] for p, t in (("", ""), ("", "a"), ("*", ""), ("?", ""), ("**", "abc"), ("a", "a"))]
        self.assertEqual(got, [True, False, True, False, True, True])
        self.assertEqual((ex.wildcard("b?k", "book")[0], ex.wildcard("*k", "book")[0], ex.wildcard("tree*", "tree")[0]), (False, True, True))
        self.assertEqual(ex.wildcard("t*s", "tress")[1][2], [False, True, True, True, True, True])
        r = random.Random(28)
        for _ in range(500):
            p = "".join(r.choice("ab?*") for _ in range(r.randint(0, 5)))
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 6)))
            self.assertEqual(ex.wildcard(p, t)[0], fnmatch.fnmatchcase(t, p))
            self.assertEqual(ex.plain_recursion(p, t, [0]), ex.wildcard(p, t)[0])


    def test_regex_nfa(self) -> None:
        import random
        import re
        self.assertEqual(ex.build_nfa("ab*")[:2], (1, 6))
        self.assertEqual((ex.nfa_match("ab*", "abb")[0], ex.nfa_match("ab*", "ba")[0], ex.nfa_match("", "")[0], ex.nfa_match("", "a")[0]),
                         (True, False, True, False))
        self.assertEqual([ex.backtrack_match("(a*)*b", "a" * n)[1] for n in (10, 15)], [7169, 229377])
        self.assertEqual([ex.nfa_match("(a*)*b", "a" * n)[1] for n in (10, 15, 20)], [66, 96, 126])
        r = random.Random(28)
        pieces = ["a", "b", ".", "a*", "(a|b)", "(ab)*", "b*", "(a|bb)*"]
        for _ in range(400):
            rx = "".join(r.choice(pieces) for _ in range(r.randint(0, 4)))
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 6)))
            want = re.fullmatch(rx, t) is not None
            self.assertEqual(ex.nfa_match(rx, t)[0], want, (rx, t))
            self.assertEqual(ex.backtrack_match(rx, t)[0], want, (rx, t))


    def test_bitap(self) -> None:
        import random
        self.assertEqual(ex.bitap("the club met at the clib", "club"), [7])
        self.assertEqual(ex.bitap("the club met at the clib", "club", 1), [7, 23])
        self.assertEqual(ex.bitap("abc", ""), [])
        r = random.Random(36)
        for _ in range(300):
            text = "".join(r.choice("ab") for _ in range(r.randint(0, 20)))
            pat = "".join(r.choice("ab") for _ in range(r.randint(1, 5)))
            k = r.randint(0, 2)
            brute = [e for e in range(len(pat) - 1, len(text))
                     if sum(a != b for a, b in zip(text[e - len(pat) + 1:e + 1], pat)) <= k]
            self.assertEqual(ex.bitap(text, pat, k), brute)


if __name__ == "__main__":
    unittest.main()
