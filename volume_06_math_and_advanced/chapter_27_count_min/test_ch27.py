import random
import unittest
from collections import Counter

import ch27_examples as ex


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


if __name__ == "__main__":
    unittest.main()
