import unittest

import ch19_examples as ex


class TestChapter19(unittest.TestCase):
    def test_every_case(self) -> None:
        for target, lin, bins in [(12, 1, 3), (58, 5, 1), (91, 9, 4), (50, 9, 4)]:
            c = ex.operation_costs(ex.SHELF, target)
            self.assertEqual((c["linear search"], c["binary search"], c["read position k"], c["append"],
                              c["insert at front"]), (lin, bins, 1, 1, 9))
        e = ex.operation_costs([], 5)
        self.assertEqual((e["linear search"], e["binary search"], e["insert at front"]), (0, 0, 0))

    def test_costs(self) -> None:
        self.assertEqual(ex.operation_costs(ex.SHELF, 63), {"read position k": 1, "linear search": 6,
                                                           "binary search": 3, "append": 1, "insert at front": 9})
        big = ex.operation_costs(list(range(1_000_000)), 999_999)
        self.assertLessEqual(big["binary search"], 20)
        self.assertEqual(big["linear search"], 1_000_000)


if __name__ == "__main__":
    unittest.main()
