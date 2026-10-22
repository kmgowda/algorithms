import math
import unittest

import ch25_examples as ex


class TestChapter22(unittest.TestCase):
    def test_examples(self) -> None:
        c = [0]
        self.assertEqual((ex.power(3, 13, c), c[0]), (3 ** 13, 7))
        log = []
        self.assertEqual(ex.peasant(13, 21, log), 273)
        self.assertEqual(log, [(13, 21, True), (6, 42, False), (3, 84, True), (1, 168, True)])
        self.assertEqual(max(ex.guess_number(s, 1, 1000) for s in range(1, 1001)), 10)
        log = []
        self.assertEqual((ex.euclid(1071, 462, log), len(log)), (21, 3))

    def test_every_case(self) -> None:
        counts = []
        for n in (0, 1, 2, 13, 64, 1000, 10 ** 6):
            c = [0]
            self.assertEqual(ex.power(2, n, c), 2 ** n)
            counts.append(c[0])
        self.assertEqual(counts, [0, 2, 3, 7, 8, 16, 27])
        self.assertEqual((ex.peasant(0, 5), ex.peasant(1, 5), ex.peasant(5, 0)), (0, 5, 0))
        self.assertEqual([ex.euclid(*p) for p in ((7, 0), (0, 7), (12, 12), (17, 5))], [7, 7, 12, 1])
        log = []
        ex.euclid(89, 55, log)
        self.assertEqual(len(log), 9)
        self.assertEqual(ex.guess_number(1, 1, 1), 1)
        c = [0]
        self.assertEqual((ex.power(5, 10, c), c[0], ex.peasant(9, 15), ex.euclid(84, 36)), (9765625, 6, 135, 12))
        self.assertEqual((ex.power_steps(13), ex.power_steps(1), ex.power_steps(0)), ([1, 3, 6, 13], [1], []))
        self.assertEqual(len(ex.power_steps(10 ** 6)), 20)
        c = [0]
        self.assertEqual(ex.insertion_sort_rec([58, 25, 91, 12, 70, 47, 84, 31, 63], c), [12, 25, 31, 47, 58, 63, 70, 84, 91])
        self.assertEqual(c[0], 23)
        self.assertEqual((ex.insertion_sort_rec([], [0]), ex.insertion_sort_rec([4], [0])), ([], [4]))

    def test_josephus(self) -> None:
        self.assertEqual(ex.josephus_order(10), [2, 4, 6, 8, 10, 3, 7, 1, 9, 5])
        self.assertEqual((ex.josephus(1), ex.josephus(10), ex.josephus(41)), (1, 5, 19))
        self.assertEqual(ex.josephus_order(1), [1])
        for n in range(1, 200):
            self.assertEqual(ex.josephus(n), ex.josephus_order(n)[-1])
            self.assertEqual(ex.josephus_bits(n), ex.josephus(n))
        with self.assertRaises(ValueError):
            ex.josephus(0)

    def test_pairs(self) -> None:
        for a in range(0, 60):
            for b in range(0, 60):
                self.assertEqual(ex.peasant(a, b), a * b)
                self.assertEqual(ex.euclid(a, b), math.gcd(a, b))


if __name__ == "__main__":
    unittest.main()
