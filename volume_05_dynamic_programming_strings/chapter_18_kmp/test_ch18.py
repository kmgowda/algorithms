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


    def test_traces_and_automaton(self) -> None:
        import random
        self.assertEqual(ex.failure_trace("abacab")[2], (3, "c", 1, [0], 0))
        self.assertEqual([st[4] for st in ex.failure_trace("aabaaa")], [1, 0, 1, 2, 2])
        self.assertEqual(ex.failure_trace("aabaaa")[4], (5, "a", 2, [1], 2))
        tr = ex.kmp_trace("abacaabacab", "abacab")
        self.assertEqual((tr[5], tr[10][-1], ex.kmp_search("abacaabacab", "abacab")), ((5, "a", 5, [1, 0], 1, False), True, ([5], 13)))
        self.assertEqual(ex.automaton("abacab", "abc")[5], {"a": 1, "b": 6, "c": 0})
        self.assertEqual(ex.automaton("abacab", "abc")[3], {"a": 1, "b": 2, "c": 4})
        self.assertEqual(ex.failure("ATATATATAG"), [0, 0, 1, 2, 3, 4, 5, 6, 7, 0])
        self.assertEqual((ex.failure_trace(""), ex.failure_trace("a"), ex.automaton_search("abc", "")), ([], [], [0, 1, 2, 3]))
        r = random.Random(18)
        for _ in range(300):
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 30)))
            p = "".join(r.choice("ab") for _ in range(r.randint(1, 5)))
            found, comps = ex.kmp_search(t, p)
            self.assertEqual(ex.automaton_search(t, p), found)
            self.assertLessEqual(comps, 2 * len(t))


if __name__ == "__main__":
    unittest.main()
