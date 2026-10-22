import random
import unittest

import ch08_examples as ex


PILE9 = [58, 25, 91, 12, 70, 47, 84, 31, 63]
CASES = [PILE9, sorted(PILE9), sorted(PILE9, reverse=True), [47] * 9, [58, 25, 58, 12, 25, 47, 58, 12, 47], [47], []]


class TestChapter14(unittest.TestCase):
    def test_build_traces(self) -> None:                      # Section 8.4 and Problem 14.3
        for start, heap, comps in (([58, 25, 91, 12, 70, 47, 84, 31, 63], [91, 70, 84, 63, 25, 47, 58, 31, 12], 10),
                                   ([12, 25, 31, 47, 58, 63, 70], [70, 58, 63, 47, 25, 12, 31], 8),
                                   ([], [], 0), ([5], [5], 0)):
            a, c = list(start), {"comparisons": 0}
            for i in range(len(a) // 2 - 1, -1, -1):
                ex.sift_down(a, i, len(a), c)
            self.assertEqual((a, c["comparisons"]), (heap, comps))

    def test_every_case(self) -> None:
        got = []
        for a in CASES:
            c = {"comparisons": 0}
            b = list(a)
            ex.heapsort(b, c)
            self.assertEqual(b, sorted(a))
            got.append(c["comparisons"])
        self.assertEqual(got, [29, 35, 30, 21, 29, 0, 0])

    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 40) for _ in range(rng.randint(0, 40))]
            b = list(a)
            ex.heapsort(b)
            self.assertEqual(b, sorted(a))

    def test_examples(self) -> None:
        a, c, log = list(ex.PILE), {"comparisons": 0}, []
        ex.heapsort(a, c, log)
        self.assertEqual(c["comparisons"], 29)
        self.assertEqual(log[0], ("heap", [91, 70, 84, 63, 25, 47, 58, 31, 12]))
        self.assertEqual(log[1], (91, [84, 70, 58, 63, 25, 47, 12, 31, 91]))
        rng = random.Random(1)
        x = [rng.randint(0, 10 ** 6) for _ in range(5000)]
        self.assertEqual(ex.top_k_by_heapsort(x, 10), sorted(x, reverse=True)[:10])


if __name__ == "__main__":
    unittest.main()
