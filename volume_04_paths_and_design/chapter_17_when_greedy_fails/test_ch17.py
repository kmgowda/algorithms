import unittest

import ch17_examples as ex


class TestChapter17(unittest.TestCase):
    def test_gallery(self) -> None:
        self.assertEqual(ex.nearest_neighbour(), (23, ["Library", "North", "West", "South", "East", "Library"]))
        self.assertEqual(ex.best_tour(), (21, ["Library", "East", "West", "South", "North", "Library"]))
        self.assertEqual(ex.greedy_cover(ex.GENRES, ex.SUPPLIERS), ["Big Books", "Mapworks"])
        self.assertEqual(len(ex.greedy_cover(ex.GENRES, ex.SUPPLIERS2)), 3)
        self.assertEqual(ex.smallest_cover(ex.GENRES, ex.SUPPLIERS2), ["North Shop", "South Shop"])

    def test_every_case(self) -> None:
        self.assertEqual(ex.greedy_cover(set(), ex.SUPPLIERS), [])
        self.assertEqual(ex.smallest_cover({"poetry"}, ex.SUPPLIERS), ["Big Books"])
        self.assertEqual(ex.greedy_cover({"opera"}, ex.SUPPLIERS), ["(cannot cover everything)"])
        self.assertEqual([ex.nearest_neighbour(s)[0] for s in ex.BRANCHES], [23, 24, 21, 23, 21])
        self.assertEqual({ex.best_tour(s)[0] for s in ex.BRANCHES}, {21})


if __name__ == "__main__":
    unittest.main()
