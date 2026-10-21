import random
import unittest
from collections import Counter

import ch26_examples as ex


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


if __name__ == "__main__":
    unittest.main()
