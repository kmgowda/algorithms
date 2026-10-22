import random
import unittest

import ch23_examples as ex


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

    def test_calls_and_ops(self) -> None:
        def leaves(t):
            return 1 if not t[2] else sum(leaves(k) for k in t[2])
        self.assertEqual(leaves(ex.karatsuba_calls(1234, 5678)), 11)
        self.assertEqual(ex.karatsuba_calls(7, 8), (7, 8, []))
        c = [0]
        self.assertEqual((ex.karatsuba(99, 99, c), c[0]), (9801, 5))
        self.assertEqual(ex.ops_table(), [(16, 512, 1411, 512), (32, 2048, 5108, 1860), (64, 8192, 15030, 6097),
                                          (128, 32768, 45695, 19228), (256, 131072, 139537, 59957),
                                          (512, 524288, 419325, 184183), (1024, 2097152, 1261027, 558709)])

    def test_strassen(self) -> None:
        c = [0]
        self.assertEqual(ex.strassen([[1, 3], [7, 5]], [[6, 8], [4, 2]], c), [[18, 14], [62, 66]])
        self.assertEqual(c[0], 7)
        self.assertEqual(ex.strassen([[4]], [[5]], [0]), [[20]])
        self.assertEqual(ex.strassen([[2, 0], [1, 3]], [[1, 4], [2, 1]], [0]), [[2, 8], [7, 7]])
        self.assertEqual((ex.school(99, 99, c), ex.split_four(99, 99, [0])), (9801, 9801))
        r = random.Random(2)
        for n, s_count, school_count in ((2, 7, 8), (4, 49, 64), (8, 343, 512), (16, 2401, 4096)):
            A = [[r.randint(-9, 9) for _ in range(n)] for _ in range(n)]
            B = [[r.randint(-9, 9) for _ in range(n)] for _ in range(n)]
            c1, c2 = [0], [0]
            self.assertEqual(ex.strassen(A, B, c1), ex.matrix_school(A, B, c2))
            self.assertEqual((c1[0], c2[0]), (s_count, school_count))

    def test_every_case(self) -> None:
        c = [0]
        self.assertEqual((ex.karatsuba(0, 12345, c), c[0]), (0, 1))
        self.assertEqual((ex.karatsuba(7, 8, [0]), ex.karatsuba(99, 99, [0])), (56, 9801))
        with self.assertRaises(ValueError):
            ex.karatsuba(-12, 34, [0])


if __name__ == "__main__":
    unittest.main()
