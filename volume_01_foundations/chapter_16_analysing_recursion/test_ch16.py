import unittest

import ch16_examples as ex


class TestChapter16(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
