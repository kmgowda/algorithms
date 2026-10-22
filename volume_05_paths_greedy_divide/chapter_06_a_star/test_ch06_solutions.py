import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestChapter6Solutions(unittest.TestCase):
    def test_town(self) -> None:
        adj = ex.weighted_adjacency()
        minutes, path, expanded = sol.parcel_a_star(adj, "Library", "Market", "Harbour")
        self.assertEqual((minutes, "Market" in path, expanded), (16, True, 5))

    def test_smallest(self) -> None:
        self.assertEqual(sol.parcel_a_star({"A": {}}, "A", "A", "A"), (0, ["A"], 1))
        self.assertEqual(sol.parcel_a_star({"A": {}, "B": {}}, "A", "B", "A")[:2], (float("inf"), None))

    def test_random(self) -> None:
        rng = random.Random(7)
        for _ in range(200):
            n = rng.randint(1, 7)
            adj = {i: {} for i in range(n)}
            for _ in range(rng.randint(0, 12)):
                a, b = rng.randrange(n), rng.randrange(n)
                if a != b:
                    adj[a][b] = adj[b][a] = rng.randint(1, 9)
            s, x, t = rng.randrange(n), rng.randrange(n), rng.randrange(n)
            d1, d2 = ex.true_remaining(adj, x), ex.true_remaining(adj, t)
            expect = d1.get(s, float("inf")) + d2.get(x, float("inf"))
            self.assertEqual(sol.parcel_a_star(adj, s, x, t)[0], expect)

    def test_average_speed_overestimates(self) -> None:
        adj = ex.weighted_adjacency()
        h = sol.average_speed_guess("Harbour")
        self.assertGreater(h("Museum"), 3)                      # the Museum is only 3 minutes away
        self.assertEqual(ex.a_star(adj, "Library", "Harbour", h)[0], 16)


if __name__ == "__main__":
    unittest.main()
