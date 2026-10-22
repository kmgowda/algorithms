import random
import unittest
from collections import Counter

import ch30_examples as ex


class TestChapter27(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual([ex.experiment(w, d) for w, d in ((100, 1), (100, 4), (1000, 4))],
                         [(123, 1107, 199.13), (123, 262, 145.11), (11, 32, 5.73)])

    def test_every_case(self) -> None:
        cm = ex.CountMin(50, 3)
        self.assertEqual(cm.estimate("never added"), 0)
        cm.add("x", 0)
        self.assertEqual(cm.estimate("x"), 0)
        for bad in ((0, 3), (5, 0)):
            with self.assertRaises(ValueError):
                ex.CountMin(*bad)
        with self.assertRaises(ValueError):
            cm.add("x", -1)
        r = random.Random(1)
        for _ in range(50):
            cm = ex.CountMin(r.randint(1, 30), r.randint(1, 4))
            s = [r.randrange(40) for _ in range(r.randint(0, 200))]
            for x in s:
                cm.add(x)
            for x, c in Counter(s).items():
                self.assertGreaterEqual(cm.estimate(x), c)
        one = ex.CountMin(1, 1)
        for x in "abc":
            one.add(x)
        self.assertEqual(one.estimate("a"), 3)


class TestDepth(unittest.TestCase):
    def test_sizing_and_guarantee(self) -> None:
        self.assertEqual((ex.sized_for(0.001, 0.01), ex.sized_for(0.01, 0.05)), ((2719, 5), (272, 3)))
        self.assertEqual((ex.guarantee_check(0.001, 0.01), ex.guarantee_check(0.005, 0.05)), ((2719, 5, 0, 0.0), (544, 3, 0, 0.0)))

    def test_variants(self) -> None:
        out = ex.compare_variants(100, 4)
        self.assertEqual(out, {"count-min": (145.11, 262, 123), "conservative": (73.29, 82, 0), "count sketch": (20.02, 94.0, -17.5)})
        import random
        from collections import Counter
        r = random.Random(36)
        stream = [r.choice("abcdefghij") for _ in range(2000)]
        cons = ex.CountMinConservative(5, 3)
        plain = ex.CountMin(5, 3)
        for x in stream:
            cons.add(x)
            plain.add(x)
        for x, c in Counter(stream).items():
            self.assertTrue(c <= cons.estimate(x) <= plain.estimate(x))
        cs = ex.CountSketch(50, 5)
        cs.add("a", 5)
        cs.add("a", -2)
        self.assertEqual(cs.estimate("a"), 3)

    def test_tiny_and_merge(self) -> None:
        rows, cols = ex.tiny_grid()
        self.assertEqual(rows, [[0, 4, 0, 0, 0, 2, 0, 1], [3, 0, 1, 0, 0, 0, 1, 2], [1, 3, 0, 1, 2, 0, 0, 0]])
        self.assertEqual(cols["dragons"], [1, 0, 1])
        a, b = ex.CountMin(100, 4), ex.CountMin(100, 4)
        for w in ("x", "y", "x"):
            a.add(w)
        for w in ("x", "z"):
            b.add(w)
        self.assertEqual(ex.merge(a, b).estimate("x"), 3)
        with self.assertRaises(ValueError):
            ex.merge(ex.CountMin(10, 2), ex.CountMin(11, 2))


if __name__ == "__main__":
    unittest.main()
