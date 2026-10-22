import random
import unittest
from collections import Counter

import ch29_examples as ex


class TestChapter26(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.majority("ABAACAADA"), ex.majority("ABCABC"), ex.majority([])), ("A", None, None))
        r = random.Random(26)
        loans = [r.choice(["Dune"] * 30 + ["Emma"] * 20 + ["Hamlet"] * 12) if r.random() < 0.5 else f"book{r.randrange(5000)}" for _ in range(20000)]
        mg = ex.misra_gries(loans, 10)
        self.assertEqual((mg["Dune"], mg["Emma"], mg["Hamlet"], len(mg)), (3385, 1854, 495, 9))
        visitors = [f"card{r.randrange(30000)}" for _ in range(100000)]
        self.assertEqual((len(set(visitors)), round(ex.distinct_estimate(visitors, 64))), (28894, 32834))

    def test_every_case(self) -> None:
        self.assertEqual((ex.majority("A"), ex.majority("AB"), ex.misra_gries([], 3), ex.distinct_estimate([]), ex.distinct_estimate("aab")), ("A", None, {}, 0.0, 2.0))
        self.assertEqual((ex.majority("ABBCB"), ex.misra_gries("abca", 3)), ("B", {"a": 1}))
        r = random.Random(1)
        for _ in range(100):
            s = [r.choice("abcde") for _ in range(r.randint(0, 60))]
            k = r.randint(2, 5)
            mg, true = ex.misra_gries(s, k), Counter(s)
            for x, c in true.items():
                self.assertGreaterEqual(mg.get(x, 0), c - len(s) // k)
                self.assertLessEqual(mg.get(x, 0), c)
            want = next((x for x, c in true.items() if 2 * c > len(s)), None)
            self.assertEqual(ex.majority(s), want)


class TestDepth(unittest.TestCase):
    def test_majority_trace(self) -> None:
        self.assertEqual([c for _, _, c in ex.majority_trace("ABAACAADA")], [1, 0, 1, 2, 1, 2, 3, 2, 3])
        self.assertEqual(ex.majority_trace(""), [])

    def test_space_saving(self) -> None:
        r = random.Random(34)
        for _ in range(100):
            n, k = r.randint(0, 300), r.randint(1, 8)
            stream = [r.choice("aaaaabbbcde") + str(r.randrange(3)) for _ in range(n)]
            true = Counter(stream)
            ss = ex.space_saving(stream, k)
            self.assertLessEqual(len(ss), k)
            for x, c in ss.items():
                self.assertGreaterEqual(c, true[x])
                self.assertLessEqual(c - true[x], n / k + 1e-9)
            for x, c in true.items():
                if c > n / k:
                    self.assertIn(x, ss)

    def test_distinct_sketches(self) -> None:
        r = random.Random(35)
        visitors = [f"card{r.randrange(3000)}" for _ in range(10000)]
        exact = len(set(visitors))
        self.assertLess(abs(ex.hyperloglog(visitors, 10) - exact) / exact, 0.1)
        self.assertLess(abs(ex.flajolet_martin(visitors, 64) - exact) / exact, 0.25)
        self.assertEqual(round(ex.hyperloglog([], 4)), 0)
        self.assertAlmostEqual(ex.hyperloglog(["one"], 6), 1, delta=0.1)
        self.assertEqual((ex.trailing_zeros(8), ex.trailing_zeros(1), ex.trailing_zeros(0)), (3, 0, 64))


if __name__ == "__main__":
    unittest.main()
