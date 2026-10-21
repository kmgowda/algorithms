import random
import unittest
from collections import Counter

import ch28_examples as ex


class TestChapter28(unittest.TestCase):
    def test_examples(self) -> None:
        wc = ex.word_count(ex.NEWSLETTERS)
        self.assertEqual((wc["the"], wc["monday"], len(wc)), (4, 2, 13))
        idx = ex.inverted_index(ex.NEWSLETTERS)
        self.assertEqual((idx["monday"], idx["maps"], idx["the"]), ([1, 3], [0, 2], [0, 1, 2, 3]))
        self.assertEqual((ex.average_wrong(ex.LOANS), ex.average_right(ex.LOANS)), (8.0, 4.0))

    def test_every_case(self) -> None:
        self.assertEqual((ex.word_count([]), ex.word_count([""]), ex.word_count(["a a a"], 2)), ({}, {}, {"a": 3}))
        with self.assertRaises(ValueError):
            ex.word_count(["a"], 0)
        r = random.Random(28)
        for _ in range(100):
            lines = [" ".join(r.choice("abcde") for _ in range(r.randint(0, 6))) for _ in range(r.randint(0, 8))]
            want = dict(sorted(Counter(w for l in lines for w in l.split()).items()))
            self.assertEqual(ex.word_count(lines, r.randint(1, 5)), want)


if __name__ == "__main__":
    unittest.main()
