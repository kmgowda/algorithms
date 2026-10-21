import fnmatch
import random
import unittest

import ch28_examples as ex


class TestChapter28(unittest.TestCase):
    def test_titles(self) -> None:
        self.assertEqual(ex.search("tre?s*", ex.TITLES), ["treasure island", "trees of britain", "tress"])
        self.assertEqual((ex.search("*island", ex.TITLES), ex.search("t?e *", ex.TITLES)), (["treasure island", "island"], ["the treasure map"]))
        self.assertEqual([ex.wildcard("t*s", w)[0] for w in ("tress", "trees", "tree")], [True, True, False])
        c = [0]
        self.assertEqual((ex.plain_recursion("*a*a*a*b", "a" * 20, c), c[0], ex.wildcard("*a*a*a*b", "a" * 20)[0]), (False, 15092, False))

    def test_every_case(self) -> None:
        got = [ex.wildcard(p, t)[0] for p, t in (("", ""), ("", "a"), ("*", ""), ("?", ""), ("**", "abc"), ("a", "a"))]
        self.assertEqual(got, [True, False, True, False, True, True])
        self.assertEqual((ex.wildcard("b?k", "book")[0], ex.wildcard("*k", "book")[0], ex.wildcard("tree*", "tree")[0]), (False, True, True))
        self.assertEqual(ex.wildcard("t*s", "tress")[1][2], [False, True, True, True, True, True])
        r = random.Random(28)
        for _ in range(500):
            p = "".join(r.choice("ab?*") for _ in range(r.randint(0, 5)))
            t = "".join(r.choice("ab") for _ in range(r.randint(0, 6)))
            self.assertEqual(ex.wildcard(p, t)[0], fnmatch.fnmatchcase(t, p))
            self.assertEqual(ex.plain_recursion(p, t, [0]), ex.wildcard(p, t)[0])


if __name__ == "__main__":
    unittest.main()
