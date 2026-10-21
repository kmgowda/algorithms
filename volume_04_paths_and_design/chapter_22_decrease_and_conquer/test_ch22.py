import math
import unittest

import ch22_examples as ex


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
        for a in range(0, 60):
            for b in range(0, 60):
                self.assertEqual(ex.peasant(a, b), a * b)
                self.assertEqual(ex.euclid(a, b), math.gcd(a, b))


if __name__ == "__main__":
    unittest.main()
