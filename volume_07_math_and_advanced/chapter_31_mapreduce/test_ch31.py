import random
import unittest
from collections import Counter

import ch31_examples as ex


class TestChapter28(unittest.TestCase):
    def test_examples(self) -> None:
        wc = ex.word_count(ex.NEWSLETTERS)
        self.assertEqual((wc["the"], wc["monday"], len(wc)), (4, 2, 13))
        idx = ex.inverted_index(ex.NEWSLETTERS)
        self.assertEqual((idx["monday"], idx["maps"], idx["the"]), ([2, 4], [1, 3], [1, 2, 3, 4]))
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


class TestDepth(unittest.TestCase):
    def test_combiner_and_cost(self) -> None:
        wcm = lambda line: [(w, 1) for w in line.split()]
        add = lambda k, vs: sum(vs)
        plain, sent = ex.map_reduce_counted(ex.NEWSLETTERS * 250, wcm, add, machines=10)
        comb, sent_c = ex.map_reduce_counted(ex.NEWSLETTERS * 250, wcm, add, machines=10, combiner=add)
        self.assertEqual((plain == comb, sent, sent_c), (True, 5250, 80))
        with self.assertRaises(ValueError):
            ex.map_reduce_counted([], wcm, add, machines=0)

    def test_join_sort_matrix_topk(self) -> None:
        j = ex.join(ex.BRANCHES, ex.VISITS)
        self.assertEqual((sorted(j["North"]), j["South"]), ([("Ada Lane", 1), ("Ada Lane", 2), ("Ada Lane", 3)], []))
        import random
        r = random.Random(5)
        vals = [r.randrange(10 ** 6) for _ in range(10000)]
        srt, sizes = ex.sample_sort(vals, 4)
        self.assertEqual((srt == sorted(vals), sizes), (True, [2235, 3208, 2148, 2409]))
        self.assertEqual(ex.sample_sort([3, 1, 2], 1)[0], [1, 2, 3])
        self.assertEqual(ex.matrix_vector({(0, 0): 2, (0, 1): 1, (1, 1): 3, (2, 0): 1, (2, 2): 4}, {0: 1, 1: 2, 2: 3}), {0: 4, 1: 6, 2: 13})
        self.assertEqual(ex.top_k_two_jobs(ex.NEWSLETTERS, 3), ([("the", 4), ("club", 2), ("library", 2)], 9))


if __name__ == "__main__":
    unittest.main()
