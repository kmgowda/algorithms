import itertools
import random
import unittest

from ch25_solutions import round_set_cover


def best(universe, sets, cost):
    out = None
    for k in range(len(sets) + 1):
        for g in itertools.combinations(sorted(sets), k):
            if universe <= set().union(*[sets[s] for s in g]):
                total = sum(cost[s] for s in g)
                out = total if out is None else min(out, total)
    return out


class TestRoundSetCover(unittest.TestCase):
    def test_smallest(self) -> None:
        self.assertEqual(round_set_cover(set(), {"A": {1}}, {"A": 4}), [])
        self.assertEqual(round_set_cover({1}, {"A": {1}}, {"A": 4}), ["A"])
        with self.assertRaises(ValueError):
            round_set_cover({1, 2}, {"A": {1}}, {"A": 1})

    def test_vertex_cover_is_f_two(self) -> None:
        sets = {"a": {1, 3}, "b": {1, 2}, "c": {2, 3}}          # a triangle: roads 1, 2, 3; each road in 2 lists
        self.assertEqual(round_set_cover({1, 2, 3}, sets, {"a": 1, "b": 1, "c": 1}), ["a", "b", "c"])

    def test_random_within_f(self) -> None:
        r = random.Random(25)
        for _ in range(60):
            universe = set(range(1, 7))
            sets = {s: {e for e in universe if r.random() < 0.4} for s in "ABCDE"}
            sets["E"] |= universe - set().union(*sets.values())
            cost = {s: r.randint(1, 6) for s in sets}
            chosen = round_set_cover(universe, sets, cost)
            f = max(sum(e in sets[s] for s in sets) for e in universe)
            self.assertTrue(universe <= set().union(*[sets[s] for s in chosen]))
            self.assertLessEqual(sum(cost[s] for s in chosen), f * best(universe, sets, cost))


if __name__ == "__main__":
    unittest.main()
