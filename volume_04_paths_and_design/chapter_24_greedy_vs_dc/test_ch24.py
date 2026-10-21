import random
import unittest

import ch24_examples as ex


class TestChapter24(unittest.TestCase):
    def test_examples(self) -> None:
        a, b = [0], [0]
        self.assertEqual((ex.max_greedy(ex.VISITORS, a), a[0], ex.max_dc(ex.VISITORS, b), b[0], ex.depth(8)), (26, 7, 26, 7, 3))
        got = []
        for n in (8, 100, 1000):
            v = random.Random(n).sample(range(10 * n), n)
            c, d = [0], [0]
            self.assertEqual(ex.sort_greedy(v, c), ex.sort_dc(v, d))
            got.append((c[0], d[0], ex.depth(n)))
        self.assertEqual(got, [(28, 15, 3), (4950, 537, 7), (499500, 8707, 10)])

    def test_every_case(self) -> None:
        self.assertEqual((ex.max_greedy([5], [0]), ex.max_dc([5], [0]), ex.depth(1)), (5, 5, 0))
        self.assertEqual((ex.sort_dc([], [0]), ex.sort_greedy([], [0]), ex.sort_dc([2, 2, 1], [0])), ([], [], [1, 2, 2]))


if __name__ == "__main__":
    unittest.main()
