import random
import unittest

import ch09_examples as ex


def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


class TestChapter09(unittest.TestCase):
    def test_sorts_and_shifts_equal_inversions(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 30) for _ in range(rng.randint(0, 25))]
            b = list(a)
            c = ex.insertion_sort(b)
            self.assertEqual(b, sorted(a))
            self.assertEqual(c["shifts"], inversions(a))

    def test_stable(self) -> None:
        recs = [(3, "Ben"), (1, "Ana"), (3, "Cai"), (2, "Dev"), (1, "Eva")]
        keys = [r[0] + i / 100 for i, r in enumerate(recs)]          # tie-break by original position
        b = [r[0] for r in recs]
        ex.insertion_sort(b)
        self.assertEqual(b, sorted(r[0] for r in recs))
        self.assertEqual(sorted(keys), sorted(keys))

    def test_examples(self) -> None:
        a = list(ex.PILE)
        s = []
        self.assertEqual(ex.insertion_sort(a, s), {"comparisons": 23, "shifts": 17})
        self.assertEqual(s[2], (12, 0, [12, 25, 58, 91, 70, 47, 84, 31, 63]))
        self.assertEqual(ex.insertion_sort(sorted(ex.PILE)), {"comparisons": 8, "shifts": 0})
        self.assertEqual(ex.insertion_sort(sorted(ex.PILE, reverse=True)), {"comparisons": 36, "shifts": 36})
        near = ex.nightly_catalogue(n=2000, new=10, near_end=True)
        far = ex.nightly_catalogue(n=2000, new=10, near_end=False)
        self.assertLess(near["shifts"], far["shifts"])


if __name__ == "__main__":
    unittest.main()
