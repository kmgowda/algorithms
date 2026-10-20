import unittest

import ch19_examples as ex


class TestChapter19(unittest.TestCase):
    def test_costs(self) -> None:
        self.assertEqual(ex.operation_costs(ex.SHELF, 63), {"read position k": 1, "linear search": 6,
                                                           "binary search": 3, "append": 1, "insert at front": 9})
        big = ex.operation_costs(list(range(1_000_000)), 999_999)
        self.assertLessEqual(big["binary search"], 20)
        self.assertEqual(big["linear search"], 1_000_000)


if __name__ == "__main__":
    unittest.main()
