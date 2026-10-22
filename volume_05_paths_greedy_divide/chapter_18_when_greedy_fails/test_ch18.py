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
        self.assertEqual(ex.two_opt(ex.nearest_neighbour()[1]), (21, ["Library", "North", "South", "West", "East", "Library"]))

    def test_caching(self) -> None:
        log = []
        q = ex.REQUESTS
        self.assertEqual(ex.farthest_in_future(q, 3, log), 7)
        self.assertEqual([o for _, kind, o in log if kind == "miss" and o], ["C", "D", "A", "B"])
        self.assertEqual((ex.least_recently_used(q, 3), ex.first_in_first_out(q, 3), ex.fewest_misses(q, 3)), (10, 9, 7))
        self.assertEqual((ex.first_in_first_out(q, 4), ex.farthest_in_future(q, 4)), (10, 6))   # more room, more misses

    def test_caching_every_case(self) -> None:
        self.assertEqual([ex.farthest_in_future([], 3), ex.least_recently_used([], 3), ex.fewest_misses([], 3)], [0, 0, 0])
        self.assertEqual(ex.farthest_in_future(ex.REQUESTS, 0), 12)
        self.assertEqual(ex.farthest_in_future(["A", "A", "A"], 1), 1)
        self.assertEqual(ex.farthest_in_future(ex.REQUESTS, 5), 5)
        import random
        rng = random.Random(17)
        for _ in range(200):
            q = [rng.choice("ABCDE") for _ in range(rng.randint(0, 10))]
            k = rng.randint(0, 4)
            self.assertEqual(ex.farthest_in_future(q, k), ex.fewest_misses(q, k))
            self.assertLessEqual(ex.farthest_in_future(q, k), min(ex.least_recently_used(q, k), ex.first_in_first_out(q, k)))

if __name__ == "__main__":
    unittest.main()
