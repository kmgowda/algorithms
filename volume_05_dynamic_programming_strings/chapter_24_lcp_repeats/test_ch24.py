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


    def test_kasai_trace_and_queries(self) -> None:
        import random
        sa = ex.suffix_array("banana")
        self.assertEqual(ex.kasai_trace("banana", sa), [(0, 1, 0, 0), (1, 3, 0, 3), (2, 4, 2, 2), (3, 5, 1, 1), (4, 0, 0, 0)])
        q = ex.LCPQuery("banana")
        self.assertEqual((q.query(1, 3), q.query(0, 2), q.query(2, 4), q.query(5, 3), q.query(1, 1)), (3, 0, 2, 1, 5))
        self.assertEqual(ex.LCPQuery("a").query(0, 0), 1)

        def brute(t, i, j):
            k = 0
            while i + k < len(t) and j + k < len(t) and t[i + k] == t[j + k]:
                k += 1
            return k

        r = random.Random(24)
        for _ in range(100):
            t = "".join(r.choice("ab") for _ in range(r.randint(1, 20)))
            q = ex.LCPQuery(t)
            for _ in range(10):
                i, j = r.randrange(len(t)), r.randrange(len(t))
                self.assertEqual(q.query(i, j), brute(t, i, j))
            for i, j, start, h in ex.kasai_trace(t, ex.suffix_array(t)):
                self.assertLessEqual(start, h)


if __name__ == "__main__":
    unittest.main()
