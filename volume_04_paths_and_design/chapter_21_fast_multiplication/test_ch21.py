import random
import unittest

import ch21_examples as ex


class TestChapter21(unittest.TestCase):
    def test_counts(self) -> None:
        c = [[0], [0], [0]]
        self.assertEqual(ex.karatsuba(1234, 5678, c[2]), 7006652)
        ex.school(1234, 5678, c[0])
        ex.split_four(1234, 5678, c[1])
        self.assertEqual([k[0] for k in c], [16, 16, 11])
        r = random.Random(1)
        got = []
        for n in (2, 4, 8, 16, 32, 64, 128):
            x, y = r.randrange(10 ** (n - 1), 10 ** n), r.randrange(10 ** (n - 1), 10 ** n)
            c = [[0], [0], [0]]
            self.assertEqual({ex.school(x, y, c[0]), ex.split_four(x, y, c[1]), ex.karatsuba(x, y, c[2])}, {x * y})
            got.append(tuple(k[0] for k in c))
        self.assertEqual(got, [(4, 4, 3), (16, 16, 9), (64, 64, 43), (256, 175, 115), (1024, 886, 365),
                               (4096, 3634, 1073), (16384, 13822, 3103)])

    def test_every_case(self) -> None:
        c = [0]
        self.assertEqual((ex.karatsuba(0, 12345, c), c[0]), (0, 1))
        self.assertEqual((ex.karatsuba(7, 8, [0]), ex.karatsuba(99, 99, [0])), (56, 9801))
        with self.assertRaises(ValueError):
            ex.karatsuba(-12, 34, [0])


if __name__ == "__main__":
    unittest.main()
