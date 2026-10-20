import unittest

import ch08_examples as ex


class TestChapter8(unittest.TestCase):
    def test_witnesses(self) -> None:
        self.assertEqual(ex.first_n0(lambda n: 3 * n + 10, lambda n: n, 4), 10)
        self.assertTrue(ex.holds_from(lambda n: 5 * n + 2, lambda n: n, 6, 2))
        self.assertTrue(ex.holds_from(lambda n: 5 * n + 20, lambda n: n, 6, 20))
        self.assertTrue(ex.holds_from(lambda n: n * n / 4, lambda n: n * (n - 1) / 2, 1, 2))
        self.assertFalse(ex.holds_from(lambda n: n * n, lambda n: n, 1000, 1, 5000))

    def test_share(self) -> None:
        self.assertGreater(ex.dominant_share(10), 0.8)
        self.assertGreater(ex.dominant_share(1000), 0.998)
        self.assertLess(ex.dominant_share(1), 0.15)


if __name__ == "__main__":
    unittest.main()
