import unittest

import ch08_examples as ex


class TestChapter8(unittest.TestCase):
    def test_every_case(self) -> None:
        f, g = (lambda n: 3 * n + 10), (lambda n: n)
        self.assertEqual((ex.first_n0(f, g, 4), ex.first_n0(f, g, 13)), (10, 1))
        self.assertIsNone(ex.first_n0(f, g, 3, upto=3000))
        self.assertEqual(ex.first_n0(lambda n: n, lambda n: n * n, 1), 1)
        self.assertIsNone(ex.first_n0(lambda n: n * n, lambda n: n, 1000, upto=3000))
        self.assertEqual(ex.first_n0(lambda n: 5, lambda n: 1, 5), 1)
        self.assertEqual([round(ex.dominant_share(n), 3) for n in (0, 1000)], [0.0, 0.998])

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
