import random
import unittest

import ch24_examples as ex


class TestChapter24(unittest.TestCase):
    def test_examples(self) -> None:
        sa = ex.suffix_array("banana")
        self.assertEqual((ex.lcp_kasai("banana", sa), ex.longest_repeat("banana"), ex.distinct_substrings("banana")), ([0, 1, 3, 0, 0, 2], "ana", 15))
        self.assertEqual(ex.longest_repeat("the club reads; the club meets"), "the club ")
        self.assertEqual(ex.longest_common("reading club", "the club meets"), " club")
        self.assertEqual(ex.longest_common("mississippi", "missouri"), "miss")

    def test_every_case(self) -> None:
        self.assertEqual((ex.longest_repeat("abcdefg"), ex.longest_repeat("aaaa"), ex.distinct_substrings("aaaa"), ex.longest_repeat("")), ("", "aaa", 4, ""))
        self.assertEqual((ex.distinct_substrings(""), ex.distinct_substrings("a"), ex.longest_common("abc", "xyz"), ex.longest_common("", "abc")), (0, 1, "", ""))
        sa = ex.suffix_array("abab")
        self.assertEqual((ex.lcp_kasai("abab", sa), ex.longest_repeat("abab"), ex.distinct_substrings("abab")), ([0, 2, 0, 1], "ab", 7))
        r = random.Random(24)
        for _ in range(200):
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 14)))
            subs = {t[i:j] for i in range(len(t)) for j in range(i + 1, len(t) + 1)}
            self.assertEqual(ex.distinct_substrings(t), len(subs))
            rep = max((s for s in subs if sum(t.startswith(s, i) for i in range(len(t))) >= 2), key=len, default="")
            self.assertEqual(len(ex.longest_repeat(t)), len(rep))


if __name__ == "__main__":
    unittest.main()
