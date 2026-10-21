import random
import unittest

import ch20_examples as ex


class TestChapter20(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 30) for _ in range(rng.randint(1, 40))]
            k = rng.randint(1, len(a))
            want = sorted(a)[k - 1]
            self.assertEqual(ex.quickselect(a, k), want)
            self.assertEqual(ex.quickselect(a, k, rng=random.Random(k)), want)
            self.assertEqual(ex.median_of_medians(a, k), want)

    def test_every_case(self) -> None:
        p = ex.PILE
        rows = [(p, 1, 12, 13), (p, 9, 91, 10), (p, 3, 31, 12), (p, 5, 58, 13), (sorted(p), 5, 58, 30),
                (sorted(p, reverse=True), 5, 58, 36), ([47, 12, 47, 91, 12, 47, 58], 4, 47, 11), ([47] * 9, 5, 47, 30),
                ([47], 1, 47, 0)]
        for a, k, ans, comps in rows:
            c = {"comparisons": 0}
            self.assertEqual(ex.quickselect(a, k, c), ans)
            self.assertEqual(c["comparisons"], comps)
            self.assertEqual(ex.median_of_medians(a, k), ans)
        with self.assertRaises(ValueError):
            ex.quickselect(p, 10)

    def test_examples(self) -> None:
        log = []
        ex.quickselect(ex.PILE, 5, log=log)
        self.assertEqual([(x[0], x[1]) for x in log], [(63, 5), (31, 2), (58, 4)])
        self.assertEqual(ex.smallest_k_heap(ex.PILE, 3), [12, 25, 31])


if __name__ == "__main__":
    unittest.main()
