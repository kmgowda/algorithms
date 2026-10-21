import unittest

import ch17_examples as ex


class TestChapter46(unittest.TestCase):
    def test_shapes(self) -> None:
        self.assertEqual(ex.insert_all(range(1000)), (999, 499_500))
        self.assertEqual(ex.insert_all([47, 25, 63, 12, 31, 58, 70])[0], 2)
        self.assertEqual(ex.insert_all([70, 63, 58, 47])[0], 3)
        self.assertLess(ex.average_random_height(1000, trials=5), 30)
        self.assertGreater(ex.deliveries(), 100)


if __name__ == "__main__":
    unittest.main()
