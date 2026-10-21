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


if __name__ == "__main__":
    unittest.main()
