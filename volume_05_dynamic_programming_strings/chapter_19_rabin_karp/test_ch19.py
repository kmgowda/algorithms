import random
import unittest

import ch19_examples as ex


class TestChapter19(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.rabin_karp(ex.NEWSLETTER, "club"), ex.rabin_karp(ex.NEWSLETTER, "club", mod=7)), (([12, 38], 2, 0), ([12, 38], 14, 12)))
        r = random.Random(19)
        t = "".join(r.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(10000))
        self.assertEqual([ex.rabin_karp(t, "library", m)[2] for m in (7, 101, 1_000_000_007)], [1443, 113, 0])
        self.assertEqual(ex.rabin_karp("a" * 1000, "a" * 9 + "b"), ([], 0, 0))
        self.assertEqual(ex.many_patterns(ex.NEWSLETTER, ["club", "maps", "read"]), {"club": [12, 38], "maps": [49], "read": [4, 43]})

    def test_every_case(self) -> None:
        self.assertEqual([ex.rabin_karp(t, p) for t, p in (("", "a"), ("abc", ""), ("ab", "abc"), ("aaaa", "aa"), ("abc", "abc"))],
                         [([], 0, 0), ([0, 1, 2, 3], 0, 0), ([], 0, 0), ([0, 1, 2], 3, 0), ([0], 1, 0)])
        r = random.Random(1)
        for _ in range(300):
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 30)))
            p = "".join(r.choice("ab") for _ in range(r.randint(1, 5)))
            for mod in (3, 1_000_000_007):
                self.assertEqual(ex.rabin_karp(t, p, mod)[0], [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)])


if __name__ == "__main__":
    unittest.main()
