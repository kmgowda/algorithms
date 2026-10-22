import itertools
import unittest

import ch06_examples as ex


class TestChapter30(unittest.TestCase):
    def test_books(self) -> None:
        log = []
        self.assertEqual(ex.branch_and_bound(ex.BOOKS, 20, True, log), (16, ["Poems", "Atlas", "Novel"], 13))
        self.assertEqual(log[-1], (1, 0, 13.67, 16))
        self.assertEqual(ex.branch_and_bound(ex.BOOKS, 20, False)[2], 47)
        shop = ex.random_shop(20, 20)
        cap = sum(p for _, p, _ in shop) // 3
        self.assertEqual(ex.branch_and_bound(shop, cap)[::2], (69, 21))
        shop = ex.random_shop(30, 30)
        self.assertEqual(ex.branch_and_bound(shop, sum(p for _, p, _ in shop) // 3)[::2], (138, 128))

    def test_every_case(self) -> None:
        self.assertEqual((ex.branch_and_bound([], 20), ex.branch_and_bound(ex.BOOKS, 0)), ((0, [], 1), (0, [], 1)))
        self.assertEqual(ex.branch_and_bound(ex.BOOKS, 100)[0], 25)
        self.assertEqual(ex.branch_and_bound([("Big", 25, 9)], 20), (0, [], 2))
        items = sorted(ex.BOOKS, key=lambda b: b[2] / b[1], reverse=True)
        self.assertAlmostEqual(ex.fractional_bound(items, 1, 20), 13.6667, places=3)
        self.assertEqual(ex.fractional_bound(items, 4, 6), 2.0)
        shop = ex.random_shop(10, 10)
        cap = sum(p for _, p, _ in shop) // 3
        brute = max(sum(v for *_, v in c) for k in range(11) for c in itertools.combinations(shop, k)
                    if sum(p for _, p, _ in c) <= cap)
        self.assertEqual(ex.branch_and_bound(shop, cap)[0], brute)


    def test_best_first(self) -> None:
        self.assertEqual(ex.best_first(ex.BOOKS, 20), (16, ["Poems", "Atlas", "Novel"], 6))
        got = []
        for n in (10, 20, 30, 40):
            shop = ex.random_shop(n, n)
            cap = sum(p for _, p, _ in shop) // 3
            depth, best = ex.branch_and_bound(shop, cap), ex.best_first(shop, cap)
            self.assertEqual(depth[0], best[0])
            got.append((depth[2], best[2]))
        self.assertEqual(got, [(15, 10), (21, 11), (128, 100), (129, 91)])
        self.assertEqual((ex.best_first([], 20), ex.best_first(ex.BOOKS, 0)), ((0, [], 0), (0, [], 0)))

    def test_tours(self) -> None:
        got = {k: ex.tour_branch_and_bound(ex.BRANCHES, ex.town_minutes, k) for k in ("none", "cheapest", "tree")}
        self.assertEqual({k: (v[0], v[2]) for k, v in got.items()}, {"none": (21, 62), "cheapest": (21, 26), "tree": (21, 22)})
        self.assertEqual(got["tree"][1], ["Library", "North", "South", "West", "East", "Library"])
        for n in (5, 6, 7, 8):
            places, dist = ex.random_map(n, n)
            brute = min(sum(dist(a, b) for a, b in zip((0,) + p + (0,), p + (0,)))
                        for p in itertools.permutations(places[1:]))
            for k in ("none", "cheapest", "tree"):
                self.assertEqual(ex.tour_branch_and_bound(places, dist, k)[0], brute)
        places, dist = ex.random_map(10, 10)
        self.assertEqual([ex.tour_branch_and_bound(places, dist, k)[2] for k in ("none", "cheapest", "tree")],
                         [345790, 8807, 4298])
        self.assertEqual(ex.tour_branch_and_bound(["Home"], lambda a, b: 0, "tree"), (0, ["Home", "Home"], 1))
        self.assertEqual(ex.tree_weight([], ex.town_minutes), 0)


if __name__ == "__main__":
    unittest.main()
