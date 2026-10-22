import unittest

import ch25_examples as ex


class TestChapter25(unittest.TestCase):
    def test_seating(self) -> None:
        s = ex.all_seatings(ex.READERS)
        log = []
        found = ex.explore(ex.READERS, None, log)
        self.assertEqual((len(s), len([r for r in s if ex.allowed(r)]), len(found), len(log)), (24, 12, 12, 65))
        self.assertEqual([ex.tree_size(n) for n in (1, 2, 3, 4, 5, 8, 10)], [2, 5, 16, 65, 326, 109601, 9864101])

    def test_every_case(self) -> None:
        self.assertEqual((ex.explore([]), ex.explore(["Ana"]), ex.explore(["Ana", "Ben"])), ([[]], [["Ana"]], []))
        self.assertEqual(ex.explore(["Ana", "Ben", "Cai"]), [["Ana", "Cai", "Ben"], ["Ben", "Cai", "Ana"]])


    def test_skiena_form(self) -> None:
        found, nodes = ex.seatings_by_search(ex.READERS)
        self.assertEqual((found, nodes), (ex.explore(ex.READERS), 65))
        found, nodes = ex.seatings_by_search(ex.READERS, check_early=True)
        self.assertEqual((len(found), nodes), (12, 43))
        self.assertEqual(ex.seatings_by_search(["Ana", "Ben", "Cai"], True), ([["Ana", "Cai", "Ben"], ["Ben", "Cai", "Ana"]], 10))
        self.assertEqual((ex.seatings_by_search([]), ex.seatings_by_search(["Ana"], True)), (([[]], 1), ([["Ana"]], 2)))

    def test_merge_sort_contrast(self) -> None:
        log = []
        self.assertEqual((ex.merge_sort_calls([3, 1, 4, 2], log), len(log)), ([1, 2, 3, 4], 7))
        log = []
        ex.merge_sort_calls([58, 25, 91, 12, 70, 47, 84, 31], log)
        self.assertEqual(len(log), 15)
        self.assertEqual((ex.merge_sort_calls([]), ex.merge_sort_calls([5])), ([], [5]))


if __name__ == "__main__":
    unittest.main()
