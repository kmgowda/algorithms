import random
import unittest

import ch18_examples as ex


class TestChapter18(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.failure("abacab"), ex.failure("aaaab"), ex.failure("abcd")), ([0, 0, 1, 0, 1, 2], [0, 1, 2, 3, 0], [0, 0, 0, 0]))
        self.assertEqual(ex.kmp_search("abacabacab", "abacab"), ([0, 4], 10))
        t = "a" * 1000
        self.assertEqual((ex.kmp_search(t, "a" * 9 + "b")[1], ex.kmp_search(t, "b" + "a" * 9)[1], len(ex.kmp_search(t, "aaa")[0])), (1991, 1000, 998))

    def test_every_case(self) -> None:
        self.assertEqual([ex.kmp_search(t, p) for t, p in (("", "a"), ("abc", ""), ("ab", "abc"), ("aaaa", "aa"))],
                         [([], 0), ([0, 1, 2, 3], 0), ([], 2), ([0, 1, 2], 4)])
        self.assertEqual((ex.failure(""), ex.failure("a")), ([], [0]))
        self.assertEqual((ex.failure("abab"), ex.failure("aabaa"), ex.failure("abcab"), ex.kmp_search("ababa", "aba")[0], ex.failure("abcabcabc")[-1]),
                         ([0, 0, 1, 2], [0, 1, 0, 1, 2], [0, 0, 0, 1, 2], [0, 2], 6))
        r = random.Random(18)
        for _ in range(300):
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 30)))
            p = "".join(r.choice("ab") for _ in range(r.randint(1, 5)))
            found, comps = ex.kmp_search(t, p)
            self.assertEqual(found, [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)])
            self.assertLessEqual(comps, 2 * len(t))


if __name__ == "__main__":
    unittest.main()
