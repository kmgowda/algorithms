import random
import unittest

import ch10_examples as ex


def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


class TestChapter10(unittest.TestCase):
    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 40) for _ in range(rng.randint(0, 30))]
            b, c = list(a), list(a)
            r = ex.bubble_sort(b)
            ex.shell_sort(c)
            self.assertEqual(b, sorted(a))
            self.assertEqual(c, sorted(a))
            self.assertEqual(r["swaps"], inversions(a))

    def test_examples(self) -> None:
        a, p = list(ex.PILE), []
        self.assertEqual(ex.bubble_sort(a, p), {"comparisons": 33, "swaps": 17})
        self.assertEqual(p[0], [25, 58, 12, 70, 47, 84, 31, 63, 91])
        self.assertEqual(ex.bubble_sort(sorted(ex.PILE)), {"comparisons": 8, "swaps": 0})
        a, r = list(ex.PILE), []
        self.assertEqual(ex.shell_sort(a, [4, 1], r), {"comparisons": 27, "shifts": 17})
        self.assertEqual(r[0][1], [58, 25, 84, 12, 63, 47, 91, 31, 70])
        m = ex.mixup_timing(n=1000)
        self.assertLess(m["near"]["bubble"], m["near"]["shell"])
        self.assertGreater(m["far"]["bubble"], m["far"]["shell"])


if __name__ == "__main__":
    unittest.main()
