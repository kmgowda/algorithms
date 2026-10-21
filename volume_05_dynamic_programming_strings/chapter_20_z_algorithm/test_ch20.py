import random
import unittest

import ch20_examples as ex


class TestChapter20(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.z_array("abacaba"), ex.z_array("aabxaab")), (([7, 0, 1, 0, 3, 0, 1], 8), ([7, 1, 0, 0, 3, 1, 0], 9)))
        self.assertEqual((ex.z_search("abacabacab", "abacab"), ex.z_search("the club meets the club", "club")), ([0, 4], [4, 19]))
        self.assertEqual((ex.z_array("a" * 1000)[1], ex.z_array("ab" * 500)[1]), (999, 1498))

    def test_every_case(self) -> None:
        self.assertEqual((ex.z_array(""), ex.z_array("a")), (([], 0), ([1], 0)))
        self.assertEqual([ex.z_search(t, p) for t, p in (("", "a"), ("abc", ""), ("aaaa", "aa"), ("ab", "abc"), ("a\0b", "\0"))],
                         [[], [0, 1, 2, 3], [0, 1, 2], [], [1]])
        self.assertEqual((ex.z_array("aaaa")[0], ex.z_array("abab")[0], ex.z_search("xabab", "ab"), ex.z_array("abcabcabcab")[0][3]), ([4, 3, 2, 1], [4, 0, 2, 0], [1, 3], 8))
        r = random.Random(20)
        for _ in range(300):
            s = "".join(r.choice("ab") for _ in range(r.randint(1, 25)))
            z, comps = ex.z_array(s)
            for i in range(1, len(s)):
                k = 0
                while i + k < len(s) and s[k] == s[i + k]:
                    k += 1
                self.assertEqual(z[i], k)
            self.assertLessEqual(comps, 2 * len(s))
            p = "".join(r.choice("ab") for _ in range(r.randint(1, 4)))
            self.assertEqual(ex.z_search(s, p), [i for i in range(len(s) - len(p) + 1) if s.startswith(p, i)])


if __name__ == "__main__":
    unittest.main()
