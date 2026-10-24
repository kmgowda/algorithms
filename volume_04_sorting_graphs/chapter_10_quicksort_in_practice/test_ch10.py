import random
import sys
import unittest

import ch10_examples as ex


PILE9 = [58, 25, 91, 12, 70, 47, 84, 31, 63]
CASES = [PILE9, sorted(PILE9), sorted(PILE9, reverse=True), [47] * 9, [58, 25, 58, 12, 25, 47, 58, 12, 47], [47], []]


class TestChapter13(unittest.TestCase):
    def test_every_case(self) -> None:
        got = []
        for a in CASES:
            c = {"comparisons": 0}
            b = list(a)
            ex.quicksort_practical(b, cutoff=1, counter=c)
            self.assertEqual(b, sorted(a))
            got.append(c["comparisons"])
        self.assertEqual(got, [20, 21, 21, 9, 18, 0, 0])

    def test_sorts(self) -> None:
        sys.setrecursionlimit(5000)
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, rng.choice([3, 50])) for _ in range(rng.randint(0, 60))]
            for fn in (ex.quicksort_random, ex.quicksort_practical):
                b = list(a)
                fn(b)
                self.assertEqual(b, sorted(a))

    def test_partition3(self) -> None:
        b = [3, 1, 3, 2, 3, 1, 2, 3]
        self.assertEqual(ex.partition3(b, 0, 7), (4, 7))
        self.assertEqual(b[4:], [3, 3, 3, 3])
        self.assertEqual(ex.median_of_three(list(ex.PILE), 0, 8), 8)

    def test_equal_keys_fast(self) -> None:
        c = {"comparisons": 0}
        ex.quicksort_practical([7] * 1000, counter=c)
        self.assertLessEqual(c["comparisons"], 1000)

    def test_hoare(self) -> None:
        a, log = list(ex.PILE), []
        self.assertEqual(ex.hoare_partition(a, 0, 8, None, log), 5)
        self.assertEqual(a, [58, 25, 63, 12, 31, 47, 84, 70, 91])
        self.assertEqual(len(log), 2)
        b = [4, 1, 3, 2, 5]
        self.assertEqual(ex.hoare_partition(b, 0, 4), 2)
        self.assertEqual(b, [2, 1, 3, 4, 5])
        rng = random.Random(4)
        for _ in range(300):
            x = [rng.randint(0, 9) for _ in range(rng.randint(0, 30))]
            y = list(x)
            ex.quicksort_hoare(y)
            self.assertEqual(y, sorted(x))
        for x in ([], [7], [7] * 9, [2, 1]):
            y = list(x)
            ex.quicksort_hoare(y)
            self.assertEqual(y, sorted(x))
        c = {"comparisons": 0, "swaps": 0}
        ex.quicksort_hoare([7] * 4000, counter=c)
        self.assertEqual(c["comparisons"], 55454)
        self.assertEqual(ex.lomuto_counts(list(ex.PILE)), {"comparisons": 17, "swaps": 16})


    def test_fisher_yates(self) -> None:
        import random
        for n in range(1, 6):
            counts = ex.shuffle_outcomes(n)
            self.assertEqual(len(counts), len(set(counts)))
            self.assertEqual(set(counts.values()), {1})
        naive = ex.shuffle_outcomes(3, naive=True)
        self.assertEqual(sum(naive.values()), 27)
        self.assertEqual(sorted(naive.values()), [4, 4, 4, 5, 5, 5])
        a = ex.fisher_yates(list(ex.PILE), random.Random(10))
        self.assertEqual(sorted(a), sorted(ex.PILE))
        self.assertEqual(ex.fisher_yates([]), [])


if __name__ == "__main__":
    unittest.main()
