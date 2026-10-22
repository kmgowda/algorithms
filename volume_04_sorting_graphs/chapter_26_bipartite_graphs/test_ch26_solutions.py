import itertools
import random
import unittest

import ch26_examples as ex
import ch26_solutions as sol


def brute_colourings(adj: dict) -> list[dict]:
    vs = list(adj)
    out = []
    for bits in itertools.product((0, 1), repeat=len(vs)):
        c = dict(zip(vs, bits))
        if all(c[v] != c[w] for v in adj for w in adj[v]):
            out.append(c)
    return out


class TestChapter23Solutions(unittest.TestCase):
    def test_balanced_club(self) -> None:
        club = ex.adjacency(ex.MEMBERS + sol.NEW_MEMBERS, ex.QUARRELS + sol.NEW_QUARRELS)
        blue, amber = sol.balanced_teams(club)
        self.assertEqual((len(blue), len(amber)), (7, 6))
        self.assertEqual(blue, ["Ana", "Cai", "Eva", "Gus", "Hal", "Kim", "Max"])
        side = {v: 0 for v in blue} | {v: 1 for v in amber}
        for a, b in ex.QUARRELS + sol.NEW_QUARRELS:
            self.assertNotEqual(side[a], side[b])
        colour, _ = ex.two_colour(club)
        self.assertEqual(sum(1 for v in colour if colour[v] == 0), 8)       # plain BFS colouring: 8 against 5

    def test_smallest(self) -> None:
        self.assertEqual(sol.balanced_teams({}), ([], []))
        self.assertEqual(sol.balanced_teams(ex.adjacency("A", [])), (["A"], []))
        self.assertEqual(sol.balanced_teams(ex.adjacency("AB", [])), (["A"], ["B"]))
        self.assertIsNone(sol.balanced_teams(ex.adjacency("A", [("A", "A")])))
        self.assertIsNone(sol.balanced_teams(ex.adjacency("ABC", [("A", "B"), ("B", "C"), ("C", "A")])))

    def test_balanced_random_against_brute_force(self) -> None:
        rng = random.Random(23)
        for _ in range(300):
            n = rng.randint(0, 9)
            names = [str(i) for i in range(n)]
            roads = [tuple(rng.sample(names, 2)) for _ in range(rng.randint(0, 8)) if n > 1]
            adj = ex.adjacency(names, roads)
            got, all_c = sol.balanced_teams(adj), brute_colourings(adj)
            self.assertEqual(got is None, not all_c)
            self.assertEqual(sol.count_two_colourings(adj), len(all_c))
            if got is not None:
                best = min(abs(n - 2 * sum(1 for v in c if c[v] == 0)) for c in all_c)
                self.assertEqual(abs(len(got[0]) - len(got[1])), best)
                self.assertEqual(sorted(got[0] + got[1]), sorted(names))
                side = {v: 0 for v in got[0]} | {v: 1 for v in got[1]}
                self.assertTrue(all(side[a] != side[b] for a, b in roads))

    def test_count(self) -> None:
        self.assertEqual(sol.count_two_colourings({}), 1)
        self.assertEqual(sol.count_two_colourings(ex.adjacency(ex.MEMBERS, ex.QUARRELS)), 2)
        club = ex.adjacency(ex.MEMBERS + sol.NEW_MEMBERS, ex.QUARRELS + sol.NEW_QUARRELS)
        self.assertEqual(sol.count_two_colourings(club), 8)
        self.assertEqual(sol.count_two_colourings(ex.adjacency(ex.PLACES, ex.ROADS)), 0)

    def test_greedy_scan_counterexample(self) -> None:
        path = ex.adjacency("ABCD", [("A", "B"), ("B", "C"), ("C", "D")])
        self.assertIsNone(sol.greedy_scan_colour(path, ["A", "D", "B", "C"]))
        self.assertIsNotNone(ex.two_colour(path)[0])
        self.assertIsNotNone(sol.greedy_scan_colour(path, ["A", "B", "C", "D"]))


if __name__ == "__main__":
    unittest.main()
