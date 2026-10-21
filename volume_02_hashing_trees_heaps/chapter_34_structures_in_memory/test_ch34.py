import unittest

import ch34_examples as ex


class TestChapter63(unittest.TestCase):
    def test_chains_and_grid(self) -> None:
        values = list(range(1, 501))
        for shuffled in (False, True):
            head = ex.build_chain(values, shuffle_memory=shuffled)
            self.assertEqual(ex.sum_chain(head), sum(values))
            walked, node = [], head
            while node:
                walked.append(node.value)
                node = node.next
            self.assertEqual(walked, values)
        self.assertIsNone(ex.build_chain([]))
        grid = [[r * 10 + c for c in range(7)] for r in range(5)]
        self.assertEqual(ex.grid_sums(grid), (sum(map(sum, grid)),) * 2)

    def test_memory_order(self) -> None:
        b = ex.bytes_per_item(10_000)
        self.assertLess(b["array.array"], b["list"])
        self.assertLess(b["list"], b["linked list"])
        self.assertAlmostEqual(b["array.array"], 8, delta=0.5)

    def test_loan_report_runs(self) -> None:
        out = ex.loan_report(n=5_000, days=30)
        self.assertEqual(set(out), {"linked records ms", "parallel arrays ms"})


if __name__ == "__main__":
    unittest.main()
