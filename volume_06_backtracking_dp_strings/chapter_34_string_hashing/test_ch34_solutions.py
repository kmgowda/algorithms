import random
import unittest

import ch34_examples as ex
import ch34_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_get(self) -> None:
        r = random.Random(34)
        s = "".join(r.choice("abc ") for _ in range(60))
        ph = ex.PrefixHash(s)
        for a in range(0, 61, 3):
            for b in range(a, 61, 5):
                self.assertEqual(ph.get(a, b), sol.direct_hash(s[a:b]))

    def test_lcp(self) -> None:
        s = "the club reads, the club meets"
        ph = ex.PrefixHash(s)
        self.assertEqual(sol.lcp_by_hash(ph, len(s), 0, 16), 9)
        r = random.Random(2)
        for _ in range(200):
            t = "".join(r.choice("ab") for _ in range(r.randint(1, 25)))
            i, j = r.randrange(len(t)), r.randrange(len(t))
            want = 0
            while i + want < len(t) and j + want < len(t) and t[i + want] == t[j + want]:
                want += 1
            self.assertEqual(sol.lcp_by_hash(ex.PrefixHash(t), len(t), i, j), want)

    def test_length_bug(self) -> None:
        self.assertTrue(sol.same_no_length("\0a", 0, 2, 1, 2))
        self.assertFalse(ex.same("\0a", 0, 2, 1, 2))


if __name__ == "__main__":
    unittest.main()
