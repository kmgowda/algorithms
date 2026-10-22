import random
import unittest

import ch26_examples as ex

S = "the club reads; the club meets"


class TestChapter26(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.same(S, 0, 8, 16, 24), ex.same(S, 4, 8, 20, 24), ex.same(S, 0, 3, 4, 7)), (True, True, False))
        self.assertEqual((ex.distinct_of_length("banana", 2), ex.distinct_of_length("banana", 3), ex.longest_repeat("banana"), ex.longest_repeat(S)),
                         (3, 3, "ana", "the club "))
        self.assertEqual([ex.collisions(10_000, m) for m in (1000, 100_000, 10_000_000, ex.MOD)], [49999, 496, 3, 0])

    def test_every_case(self) -> None:
        self.assertEqual((ex.distinct_of_length("", 1), ex.distinct_of_length("abc", 0), ex.distinct_of_length("abc", 4)), (0, 1, 0))
        self.assertEqual([ex.longest_repeat(t) for t in ("", "a", "abc", "aaaa")], ["", "", "", "aaa"])
        self.assertTrue(ex.same("abc", 0, 0, 2, 2))
        r = random.Random(26)
        for _ in range(200):
            t = "".join(r.choice("ab") for _ in range(r.randint(1, 15)))
            k = r.randint(1, len(t))
            self.assertEqual(ex.distinct_of_length(t, k), len({t[i:i + k] for i in range(len(t) - k + 1)}))
            subs = {t[i:j] for i in range(len(t)) for j in range(i + 1, len(t) + 1)}
            rep = max((x for x in subs if sum(t.startswith(x, i) for i in range(len(t))) >= 2), key=len, default="")
            self.assertEqual(len(ex.longest_repeat(t)), len(rep))


    def test_attack_and_double_hash(self) -> None:
        import random
        self.assertEqual([ex.overflow_attack(n) for n in (8, 9, 10, 11)], [(False, False), (False, False), (True, False), (True, False)])
        self.assertTrue(all(ex.overflow_attack(10, b)[0] for b in (257, 1_000_003, 911382323, 2 ** 31 - 1)))
        self.assertEqual((ex.thue_morse(0), ex.thue_morse(3)), ("a", "abbabaab"))
        r = random.Random(26)
        for seed in range(20):
            t = "".join(r.choice("ab") for _ in range(40))
            d = ex.DoubleHash(t, seed=seed)
            for _ in range(30):
                a, b = sorted((r.randrange(41), r.randrange(41)))
                c = r.randrange(41 - (b - a))
                self.assertEqual(d.get(a, b) == d.get(c, c + b - a), t[a:b] == t[c:c + b - a])


if __name__ == "__main__":
    unittest.main()
