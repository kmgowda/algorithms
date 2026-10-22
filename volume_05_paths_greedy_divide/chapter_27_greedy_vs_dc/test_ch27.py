import random
import unittest

import ch27_examples as ex


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


class TestBothWays(unittest.TestCase):
    def test_stretch(self) -> None:
        log = []
        self.assertEqual(ex.stretch_greedy([5, -9, 6, -2, 3, -1, 4, -8], log), 10)
        self.assertEqual(log, [5, -4, 6, 4, 7, 6, 10, 2])
        self.assertEqual((ex.stretch_greedy([7]), ex.stretch_greedy([-3, -1, -2])), (7, -1))
        log = []
        self.assertEqual((ex.stretch_greedy([2, -5, 4, -1, 3], log), log), (6, [2, -3, 4, 3, 6]))
        self.assertEqual(ex.depth(100), 7)
        r = random.Random(4)
        for _ in range(300):
            v = [r.randint(-9, 9) for _ in range(r.randint(1, 15))]
            self.assertEqual(ex.stretch_greedy(v), max(sum(v[i:j + 1]) for i in range(len(v)) for j in range(i, len(v))))
        self.assertEqual((ex.stretch_dc_work(1024), ex.stretch_summary_work(1024)), ((11264, 2047), (2047, 11)))
        self.assertEqual((ex.stretch_dc_work(1), ex.stretch_summary_work(1)), ((1, 1), (1, 1)))

    def test_codes(self) -> None:
        c = {"A": 15, "B": 7, "C": 6, "D": 6, "E": 5}
        self.assertEqual((ex.total_bits(c, ex.code_lengths_huffman(c)), ex.total_bits(c, ex.code_lengths_split(c))), (87, 89))
        from collections import Counter
        t = Counter("LIBRARY BOOK SALE")
        self.assertEqual((ex.total_bits(t, ex.code_lengths_huffman(t)), ex.total_bits(t, ex.code_lengths_split(t))), (58, 58))
        self.assertEqual(ex.code_lengths_split({"A": 4}), {"A": 1})
        self.assertEqual(ex.code_lengths_huffman({"A": 4}), {"A": 1})
        self.assertEqual(ex.split_worse_count(), 57)
        r = random.Random(9)
        for _ in range(200):
            cc = {chr(65 + i): r.randint(1, 30) for i in range(r.randint(2, 8))}
            self.assertGreaterEqual(ex.total_bits(cc, ex.code_lengths_split(cc)), ex.total_bits(cc, ex.code_lengths_huffman(cc)))


if __name__ == "__main__":
    unittest.main()
