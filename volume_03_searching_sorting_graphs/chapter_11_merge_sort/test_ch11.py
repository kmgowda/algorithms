import random
import unittest

import ch11_examples as ex


PILE9 = [58, 25, 91, 12, 70, 47, 84, 31, 63]
CASES = [PILE9, sorted(PILE9), sorted(PILE9, reverse=True), [47] * 9, [58, 25, 58, 12, 25, 47, 58, 12, 47], [47], []]


class TestChapter11(unittest.TestCase):
    def test_every_case(self) -> None:
        got = []
        for a in CASES:
            c = {"comparisons": 0}
            result = ex.merge_sort(list(a), c)
            self.assertEqual(result, sorted(a))
            got.append(c["comparisons"])
        self.assertEqual(got, [21, 13, 16, 13, 20, 0, 0])

    def test_sorts_and_stable(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 30) for _ in range(rng.randint(0, 40))]
            self.assertEqual(ex.merge_sort(a), sorted(a))
        recs = [(k, i) for i, k in enumerate([3, 1, 3, 2, 1, 3])]

        class Key:
            def __init__(self, r): self.r = r
            def __le__(self, o): return self.r[0] <= o.r[0]
        out = [k.r for k in ex.merge_sort([Key(r) for r in recs])]
        self.assertEqual(out, sorted(recs, key=lambda r: r[0]))

    def test_examples(self) -> None:
        c = {"comparisons": 0}
        self.assertEqual(ex.merge_sort(ex.PILE, c), sorted(ex.PILE))
        self.assertEqual(c["comparisons"], 21)
        c = {"comparisons": 0}
        ex.merge([12, 25, 58, 91], [31, 47, 63, 70, 84], c)
        self.assertEqual(c["comparisons"], 8)
        c = {"comparisons": 0}
        self.assertEqual(ex.merge([3, 8, 15], [5, 9], c), [3, 5, 8, 9, 15])
        self.assertEqual(c["comparisons"], 4)

    def test_branch_lists(self) -> None:
        rng = random.Random(2)
        lists = [sorted(rng.sample(range(10 ** 6), 1000)) for _ in range(8)]
        c = {"comparisons": 0}
        self.assertEqual(ex.merge_branch_lists(lists, c), sorted(x for l in lists for x in l))
        self.assertLessEqual(c["comparisons"], 24_000)


if __name__ == "__main__":
    unittest.main()
