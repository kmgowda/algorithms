import unittest

import ch16_examples as ex


class TestChapter16(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual([ex.master(*abd) for abd in [(1, 2, 0), (1, 2, 1), (2, 2, 1), (4, 2, 1), (8, 2, 2), (3, 3, 1),
                                                     (2, 4, 1)]],
                         ["O(n^0 log n)", "O(n^1)", "O(n^1 log n)", "O(n^log_2(4))", "O(n^log_2(8))", "O(n^1 log n)",
                          "O(n^1)"])
        sizes = (1, 2, 512, 513, 1023, 1024)
        self.assertEqual([ex.unroll("T(n/2)+1", n) for n in sizes], [1, 2, 10, 10, 10, 11])
        self.assertEqual([ex.unroll("T(n/2)+n", n) for n in sizes], [1, 3, 1023, 1024, 2036, 2047])
        self.assertEqual([ex.unroll("2T(n/2)+n", n) for n in sizes], [1, 4, 5120, 5121, 9217, 11264])

    def test_unroll(self) -> None:
        for k in range(0, 12):
            n = 2 ** k
            self.assertEqual(ex.unroll("T(n/2)+1", n), k + 1)
            self.assertEqual(ex.unroll("2T(n/2)+n", n), n * (k + 1))
            self.assertLess(ex.unroll("T(n/2)+n", n), 2 * n + 1)
        for n in range(1, 15):
            self.assertEqual(ex.unroll("2T(n-1)+1", n), 2 ** n - 1)
            self.assertEqual(ex.unroll("T(n-1)+1", n), n)
        self.assertEqual(ex.unroll("2T(n/2)+n", 1024), 11264)
        self.assertEqual(ex.unroll("T(n/2)+n", 1024), 2047)

    def test_master(self) -> None:
        self.assertEqual(ex.master(1, 2, 1), "O(n^1)")
        self.assertEqual(ex.master(2, 2, 1), "O(n^1 log n)")
        self.assertEqual(ex.master(4, 2, 1), "O(n^log_2(4))")

    def test_new_shapes(self) -> None:
        for n in range(1, 40):
            self.assertEqual(ex.unroll("T(n-1)+n", n), n * (n + 1) // 2)
        self.assertEqual((ex.unroll("T(n-1)+n", 9), ex.unroll("T(n-1)+n", 100)), (45, 5050))
        self.assertEqual(ex.unroll("2T(n/2)+n", 8), 32)
        self.assertEqual(ex.unroll("T(n-1)+n", 0), 1)
        fib = [0, 1]
        for _ in range(30):
            fib.append(fib[-1] + fib[-2])
        for n in range(0, 22):
            self.assertEqual(ex.fib_calls(n), 2 * fib[n + 1] - 1)
        self.assertEqual([ex.fib_calls(n) for n in (0, 1, 5, 20)], [1, 1, 15, 21891])
        self.assertEqual(ex.deepest_frames("2T(n-1)+1", 10), 10)
        self.assertEqual(ex.deepest_frames("T(n/2)+1", 1024), 11)
        self.assertEqual(ex.deepest_frames("T(n-1)+1", 1), 1)


if __name__ == "__main__":
    unittest.main()
