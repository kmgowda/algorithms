import random
import unittest

import ch24_examples as ex


class TestChapter24(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(ex.fft_multiply([1, 2, 3], [4, 5]), [4, 13, 22, 15])
        self.assertEqual(ex.big_multiply(1234, 5678), 7006652)
        self.assertEqual(ex.work_table()[0], (16, 256, 240))
        self.assertEqual(ex.work_table()[3], (1024, 1048576, 33792))

    def test_against_schoolbook(self) -> None:
        r = random.Random(24)
        for _ in range(200):
            a = [r.randint(-9, 9) for _ in range(r.randint(1, 40))]
            b = [r.randint(-9, 9) for _ in range(r.randint(1, 40))]
            self.assertEqual(ex.fft_multiply(a, b), ex.schoolbook_poly(a, b))
        for _ in range(100):
            x, y = r.randrange(10 ** r.randint(1, 60)), r.randrange(10 ** r.randint(1, 60))
            self.assertEqual(ex.big_multiply(x, y), x * y)

    def test_inverse(self) -> None:
        a = [3, 1, 4, 1, 5, 9, 2, 6]
        back = ex.fft(ex.fft(a), invert=True)
        self.assertEqual([round((v / 8).real) for v in back], a)
        for k, w in enumerate(ex.fft(a)):
            self.assertAlmostEqual(w, ex.evaluate(a, ex.roots_of_unity(8)[k]))

    def test_every_case(self) -> None:
        self.assertEqual((ex.fft_multiply([], [1]), ex.fft_multiply([5], [7])), ([], [35]))
        self.assertEqual((ex.big_multiply(0, 987), ex.big_multiply(1, 1), ex.big_multiply(99, 99)), (0, 1, 9801))
        with self.assertRaises(ValueError):
            ex.fft([1, 2, 3])
        with self.assertRaises(ValueError):
            ex.big_multiply(-1, 5)
        self.assertEqual(ex.fft([7]), [7])


if __name__ == "__main__":
    unittest.main()
