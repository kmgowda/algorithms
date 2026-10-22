import random
import unittest

import ch19_examples as ex


class TestChapter19(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.rabin_karp(ex.NEWSLETTER, "club"), ex.rabin_karp(ex.NEWSLETTER, "club", mod=7)), (([12, 38], 2, 0), ([12, 38], 14, 12)))
        t = ex.random_text()
        self.assertEqual([ex.rabin_karp(t, "library", m)[2] for m in (7, 101, 1_000_000_007)], [1436, 100, 0])
        self.assertEqual(ex.rabin_karp(t, "library", 1009)[2], 7)
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


    def test_attack_and_random_base(self) -> None:
        a, b = ex.find_collision(5, 1_000_003)
        self.assertEqual((a, b), ("sneuw", "ppyna"))
        self.assertEqual(ex.fingerprint(a, 1_000_003), ex.fingerprint(b, 1_000_003))
        self.assertEqual(ex.rabin_karp(a * 3 + b, b, 1_000_003), ([15], 4, 3))
        self.assertNotEqual(ex.fingerprint(a, 1_000_003, 1234), ex.fingerprint(b, 1_000_003, 1234))
        self.assertEqual(ex.rabin_karp(a * 3 + b, b, 1_000_003, base=1234), ([15], 1, 0))
        self.assertEqual(ex.colliding_bases(a, b, 1009), 1)
        r = random.Random(19)
        for _ in range(40):
            m = r.randint(1, 5)
            x = "".join(r.choice("abc") for _ in range(m))
            y = "".join(r.choice("abc") for _ in range(m))
            if x != y:
                self.assertLessEqual(ex.colliding_bases(x, y, 101), m - 1)
        self.assertEqual(ex.many_patterns("ab", ["abc"]), {"abc": []})


if __name__ == "__main__":
    unittest.main()
