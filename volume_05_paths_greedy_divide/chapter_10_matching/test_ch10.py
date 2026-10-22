import itertools
import random
import unittest

import ch10_examples as ex


class TestChapter10(unittest.TestCase):
    def test_festival(self) -> None:
        log = []
        m = ex.max_matching(ex.CAN_DO, log)
        self.assertEqual(m, {"Tickets": "Ben", "Cafe": "Ana", "Stage": "Dev", "Signs": "Cai", "First aid": "Eva"})
        self.assertEqual(log[1][2], {"Tickets": "Ben", "Cafe": "Ana"})
        g = ex.greedy_matching(ex.CAN_DO)
        self.assertEqual((len(g), "Ben" in g.values()), (4, False))

    def test_assignment(self) -> None:
        self.assertEqual(ex.best_assignment(ex.MINUTES), (7, (0, 3, 1, 2)))
        self.assertEqual(ex.greedy_assignment(ex.MINUTES)[0], 17)

    def test_every_case(self) -> None:
        self.assertEqual((ex.max_matching({}), ex.max_matching({"A": []})), ({}, {}))
        self.assertEqual(ex.max_matching({"A": ["x"], "B": ["x"]}), {"x": "A"})
        self.assertEqual(ex.best_assignment([[5]]), (5, (0,)))
        two = {"Ana": ["Cafe", "Tickets"], "Ben": ["Cafe"]}
        self.assertEqual((len(ex.greedy_matching(two)), len(ex.max_matching(two))), (1, 2))
        # the matching is as large as any possible: brute force over all choices
        people = list(ex.CAN_DO)
        best = max(k for k in range(6) for group in itertools.combinations(people, k)
                   if any(len(set(c)) == k for c in itertools.product(*[ex.CAN_DO[p] for p in group])))
        self.assertEqual(best, 5)

    def test_try_assign_trace(self) -> None:
        calls = []
        ex.max_matching(ex.CAN_DO, calls=calls)
        dev = [c[1:] for c in calls if c[0] == "Dev"]
        self.assertEqual(dev[0], (0, "Dev", "Stage", "ask Cai"))
        self.assertEqual(dev[-1], (1, "Cai", "Signs", "free"))
        self.assertEqual(len(dev), 7)

    def test_konig_and_hopcroft_karp(self) -> None:
        m, cover = ex.konig_cover(ex.CAN_DO_SIX)
        self.assertEqual((len(m), sorted(cover)), (5, sorted(["Cai", "Dev", "Eva", "Tickets", "Cafe"])))
        for p, ds in ex.CAN_DO_SIX.items():                          # every pairing touches the cover
            self.assertTrue(all(p in cover or d in cover for d in ds))
        log = []
        self.assertEqual(len(ex.hopcroft_karp(ex.CAN_DO, log)), 5)
        self.assertEqual([len(ph) for ph in log], [4, 1])
        self.assertEqual(log[1][0], ["Ben", "Tickets", "Ana", "Cafe", "Cai", "Signs", "Eva", "First aid"])
        self.assertEqual((ex.hopcroft_karp({}), ex.hopcroft_karp({"A": []}), ex.konig_cover({})), ({}, {}, ({}, [])))
        rng = random.Random(3)
        for _ in range(100):
            cd = {f"p{i}": rng.sample(range(6), rng.randint(0, 3)) for i in range(rng.randint(0, 6))}
            k = len(ex.max_matching(cd))
            self.assertEqual(len(ex.hopcroft_karp(cd)), k)
            m, cover = ex.konig_cover(cd)
            self.assertEqual(len(cover), k)
            self.assertTrue(all(p in cover or d in cover for p, ds in cd.items() for d in ds))

    def test_practice(self) -> None:
        six = {**ex.CAN_DO, "Ana": ["Tickets", "Cafe", "Lost property"], "Fay": ["Cafe"]}
        m = ex.max_matching(six)
        self.assertEqual((len(m), m["Lost property"], m["Cafe"]), (6, "Ana", "Fay"))
        order = {p: ex.CAN_DO[p] for p in ["Eva", "Dev", "Cai", "Ben", "Ana"]}
        self.assertEqual(len(ex.max_matching(order)), 5)

    def test_hungarian(self) -> None:
        log = []
        self.assertEqual(ex.hungarian(ex.MINUTES, log), (7, [0, 3, 1, 2]))
        self.assertEqual(len(log), 2)                                # reduction alone is enough here
        log = []
        self.assertEqual(ex.hungarian(ex.SHELVING, log), (5, [1, 0, 2]))
        self.assertEqual(log[-1][1], [[1, 0, 1], [0, 0, 4], [0, 1, 0]])
        self.assertEqual((ex.hungarian([]), ex.hungarian([[4]])), ((0, []), (4, [0])))
        self.assertEqual(ex.hungarian([[3, 5], [4, 9]]), (9, [1, 0]))                  # Practice Problem 3
        rng = random.Random(5)
        for _ in range(150):
            n = rng.randint(1, 5)
            c = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]
            self.assertEqual(ex.hungarian(c)[0], ex.best_assignment(c)[0])


if __name__ == "__main__":
    unittest.main()
