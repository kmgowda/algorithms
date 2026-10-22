import random
import unittest

import ch04_examples as ex


def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


PILE9 = [58, 25, 91, 12, 70, 47, 84, 31, 63]
CASES = [PILE9, sorted(PILE9), sorted(PILE9, reverse=True), [47] * 9, [58, 25, 58, 12, 25, 47, 58, 12, 47], [47], []]


class TestChapter10(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual([tuple(ex.bubble_sort(list(a)).values()) for a in CASES], [(33, 17), (8, 0), (36, 36), (8, 0), (35, 17), (0, 0), (0, 0)])
        self.assertEqual([tuple(ex.shell_sort(list(a), [4, 1]).values()) for a in CASES], [(27, 17), (13, 0), (20, 12), (13, 0), (24, 13), (0, 0), (0, 0)])

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
