import random
import unittest

import ch16_examples as ex


class TestChapter15(unittest.TestCase):
    def test_room(self) -> None:
        kept = ex.earliest_finish(ex.REQUESTS)
        self.assertEqual([r[0] for r in kept], ["Chess", "Knitting", "Writers", "Film"])
        self.assertEqual(ex.most_by_brute_force(ex.REQUESTS), 4)
        self.assertEqual(len(ex.by_rule(ex.REQUESTS, lambda r: r[1])), 3)
        rooms, of = ex.rooms_needed(ex.REQUESTS)
        self.assertEqual((rooms, ex.max_overlap(ex.REQUESTS), of["Coding"], of["Film"]), (3, 3, 2, 2))

    def test_practice(self) -> None:
        import itertools
        no_knit = [r for r in ex.REQUESTS if r[0] != "Knitting"]
        self.assertEqual([r[0] for r in ex.earliest_finish(no_knit)], ["Chess", "Maps", "Writers", "Film"])

        def ok(group):
            s = sorted(group, key=lambda r: r[1])
            return all(a[2] <= b[1] for a, b in zip(s, s[1:]))
        best = max(k + ex.most_by_brute_force([r for r in ex.REQUESTS if r not in a])
                   for k in range(9) for a in itertools.combinations(ex.REQUESTS, k) if ok(a))
        self.assertEqual(best, 7)

    def test_every_case(self) -> None:
        self.assertEqual((ex.earliest_finish([]), ex.rooms_needed([])), ([], (0, {})))
        self.assertEqual(len(ex.earliest_finish([("A", 9, 10), ("B", 10, 11)])), 2)
        s = [("Long", 9, 17), ("a", 10, 11), ("b", 12, 13)]
        self.assertEqual((len(ex.by_rule(s, lambda r: r[1])), len(ex.earliest_finish(s))), (1, 2))
        t = [("x", 9, 12), ("short", 11, 13), ("y", 12, 15)]
        self.assertEqual((len(ex.by_rule(t, lambda r: r[2] - r[1])), len(ex.earliest_finish(t))), (1, 2))
        self.assertEqual(ex.rooms_needed([("A", 9, 10), ("B", 9, 10), ("C", 9, 10)])[0], 3)
        rng = random.Random(2)
        for _ in range(100):
            reqs = [(str(i), s, s + rng.randint(1, 4)) for i, s in enumerate(rng.randint(8, 16) for _ in range(7))]
            self.assertEqual(len(ex.earliest_finish(reqs)), ex.most_by_brute_force(reqs))
            self.assertEqual(ex.rooms_needed(reqs)[0], ex.max_overlap(reqs))

    def test_stable_matching(self) -> None:
        log = []
        m = ex.gale_shapley(ex.VOLUNTEERS, ex.DESKS, log)
        self.assertEqual(m, {"Ana": "Stage", "Ben": "Tickets", "Cai": "Cafe", "Dev": "Signs"})
        self.assertEqual(len(log), 11)
        self.assertEqual(log[5], ("Dev", "Tickets", "swaps Cai for"))
        self.assertEqual(ex.blocking_pairs(m, ex.VOLUNTEERS, ex.DESKS), [])
        self.assertEqual(ex.all_stable(ex.VOLUNTEERS, ex.DESKS), [m])
        first_choice = {"Ana": "Cafe", "Ben": "Stage", "Cai": "Tickets", "Dev": "Signs"}
        self.assertEqual(ex.blocking_pairs(first_choice, ex.VOLUNTEERS, ex.DESKS), [("Dev", "Tickets")])

    def test_stable_every_case(self) -> None:
        self.assertEqual(ex.gale_shapley({}, {}), {})
        self.assertEqual(ex.gale_shapley({"A": ["X"]}, {"X": ["A"]}), {"A": "X"})
        p = {"A": ["X", "Y"], "B": ["Y", "X"]}
        r = {"X": ["B", "A"], "Y": ["A", "B"]}
        self.assertEqual(ex.gale_shapley(p, r), {"A": "X", "B": "Y"})               # proposers get first choices
        self.assertEqual(ex.gale_shapley(r, p), {"X": "B", "Y": "A"})               # now the other side does
        self.assertEqual(len(ex.all_stable(p, r)), 2)
        import random
        rng = random.Random(15)
        for _ in range(100):
            n = rng.randint(1, 5)
            ps, rs = [f"p{i}" for i in range(n)], [f"r{i}" for i in range(n)]
            pp = {x: rng.sample(rs, n) for x in ps}
            rp = {x: rng.sample(ps, n) for x in rs}
            log = []
            m = ex.gale_shapley(pp, rp, log)
            self.assertEqual(ex.blocking_pairs(m, pp, rp), [])
            self.assertLessEqual(len(log), n * n)
            stable = ex.all_stable(pp, rp)
            for p_ in ps:                                                          # proposer-optimal
                self.assertEqual(min(pp[p_].index(s[p_]) for s in stable), pp[p_].index(m[p_]))

if __name__ == "__main__":
    unittest.main()
