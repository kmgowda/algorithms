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


if __name__ == "__main__":
    unittest.main()
