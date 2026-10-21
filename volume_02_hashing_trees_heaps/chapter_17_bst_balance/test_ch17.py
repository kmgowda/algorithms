import unittest

import ch17_examples as ex


class TestChapter46(unittest.TestCase):
    def test_every_case(self) -> None:
        rows = [([], (-1, 0)), ([5], (0, 0)), (range(1, 101), (99, 4950)), (range(100, 0, -1), (99, 4950)),
                ([4, 2, 6, 1, 3, 5, 7], (2, 10)), ([1, 7, 2, 6, 3, 5, 4], (6, 21))]
        for keys, want in rows:
            self.assertEqual(ex.insert_all(keys), want)

    def test_shapes(self) -> None:
        self.assertEqual(ex.insert_all(range(1000)), (999, 499_500))
        self.assertEqual(ex.insert_all([47, 25, 63, 12, 31, 58, 70])[0], 2)
        self.assertEqual(ex.insert_all([70, 63, 58, 47])[0], 3)
        self.assertLess(ex.average_random_height(1000, trials=5), 30)
        self.assertGreater(ex.deliveries(), 100)


if __name__ == "__main__":
    unittest.main()
