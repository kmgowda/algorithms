import itertools
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


def brute(places, roads):
    """Labels from every minimum spanning tree, found by trying every set of V - 1 roads."""
    idx = range(len(roads))
    spanning = [c for c in itertools.combinations(idx, len(places) - 1)
                if len(ex.kruskal(places, [roads[i] for i in c])) == len(places) - 1]
    best = min(sum(roads[i][2] for i in c) for c in spanning)
    mins = [set(c) for c in spanning if sum(roads[i][2] for i in c) == best]
    return ["every" if all(i in t for t in mins) else "some" if any(i in t for t in mins) else "none" for i in idx]


class TestChapter8Solutions(unittest.TestCase):
    def test_town(self) -> None:
        labels = sol.classify_roads(ex.PLACES, ex.ROADS)
        self.assertEqual(labels.count("every"), 7)
        self.assertEqual(sorted(r for r, l in zip(ex.ROADS, labels) if l == "every"),
                         sorted(ex.kruskal(ex.PLACES, ex.ROADS)))
        cheaper = [(a, b, 4 if (a, b) == ("Park", "Hospital") else w) for a, b, w in ex.ROADS]
        labels = sol.classify_roads(ex.PLACES, cheaper)
        self.assertEqual((labels.count("every"), labels.count("some")), (4, 4))
        self.assertEqual(len(ex.minimum_trees(ex.PLACES, cheaper)), 4)

    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.classify_roads([], []), [])
        self.assertEqual(sol.classify_roads(["A"], []), [])
        self.assertEqual(sol.classify_roads(["A", "B"], [("A", "B", 7)]), ["every"])
        self.assertEqual(sol.classify_roads(["A", "B"], [("A", "B", 7), ("A", "B", 7)]), ["some", "some"])
        self.assertEqual(sol.classify_roads(["A", "B"], [("A", "B", 7), ("A", "B", 2)]), ["none", "every"])
        tri = [("A", "B", 2), ("B", "C", 2), ("A", "C", 2)]
        self.assertEqual(sol.classify_roads(list("ABC"), tri), ["some"] * 3)
        self.assertEqual(sol.classify_roads(list("ABC"), [("A", "B", -1), ("B", "C", 2), ("A", "C", 2)]),
                         ["every", "some", "some"])

    def test_against_brute_force(self) -> None:
        rng = random.Random(8)
        for _ in range(200):
            n = rng.randint(2, 5)
            places = list(range(n))
            roads = [(i - 1, i, rng.randint(1, 3)) for i in range(1, n)]           # joined up
            for _ in range(rng.randint(0, 4)):
                a, b = rng.sample(places, 2)
                roads.append((a, b, rng.randint(1, 3)))
            rng.shuffle(roads)
            self.assertEqual(sol.classify_roads(places, roads), brute(places, roads))

    def test_split_and_join(self) -> None:
        good = sol.split_and_join(ex.PLACES, ex.ROADS, ["Library", "School", "Park", "Market"])
        self.assertEqual(ex.total(good), 25)
        bad = sol.split_and_join(ex.PLACES, ex.ROADS, ["Library", "School", "Park", "Station"])
        self.assertEqual((ex.total(bad), len(bad)), (32, 7))
        self.assertIn(("School", "Station", 9), bad)
        self.assertEqual(sol.split_and_join(["A"], [], ["A"]), [])


if __name__ == "__main__":
    unittest.main()
