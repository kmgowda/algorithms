import random
import unittest

import ch18_examples as ex


class TestChapter18(unittest.TestCase):
    def test_sorts_and_stable(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 15) for _ in range(rng.randint(0, 40))]
            b = list(a)
            ex.timsort(b)
            self.assertEqual(b, sorted(a))
        recs = [(rng.randint(0, 4), i) for i in range(60)]

        class K:
            def __init__(self, r): self.r = r
            def __lt__(self, o): return self.r[0] < o.r[0]
            def __le__(self, o): return self.r[0] <= o.r[0]
            def __ge__(self, o): return self.r[0] >= o.r[0]
        b = [K(r) for r in recs]
        ex.timsort(b)
        self.assertEqual([k.r for k in b], sorted(recs, key=lambda r: r[0]))

    def test_every_case(self) -> None:
        p = list(ex.PILE)
        rows = [(p, 5, 27, 21), (sorted(p), 1, 8, 13), (sorted(p, reverse=True), 1, 8, 16), ([47] * 9, 1, 8, 13),
                ([12, 31, 58, 70, 91, 25, 47, 63, 84], 2, 16, 18), ([47], 1, 0, 0), ([], 0, 0, 0)]
        for a, runs, tim, mer in rows:
            self.assertEqual(len(ex.find_runs(list(a))), runs)
            b, c = list(a), {"comparisons": 0}
            ex.timsort(b, c)
            self.assertEqual((b, c["comparisons"], ex.merge_sort_comparisons(a)), (sorted(a), tim, mer))

    def test_examples(self) -> None:
        a, log = list(ex.PILE), []
        ex.timsort(a, log=log)
        self.assertEqual(log[0], ("runs", [[25, 58], [12, 91], [47, 70], [31, 84], [63]]))
        a = [3, 7, 9, 6, 4, 2, 5, 8]
        self.assertEqual([a[s:e] for s, e in ex.find_runs(a)], [[3, 7, 9], [2, 4, 6], [5, 8]])


if __name__ == "__main__":
    unittest.main()
