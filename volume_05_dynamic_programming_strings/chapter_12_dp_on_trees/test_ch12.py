import random
import unittest

import ch12_examples as ex


class TestChapter12(unittest.TestCase):
    def test_party(self) -> None:
        total, guests, pair = ex.party(ex.REPORTS, ex.FUN, "Director")
        self.assertEqual((total, guests), (26, ["Ben", "Cai", "Dev", "Director", "Eva", "Fay"]))
        self.assertEqual((pair["Maya"], pair["Omar"], pair["Director"]), ((12, 10), (9, 13), (26, 25)))
        self.assertEqual(ex.brute(ex.REPORTS, ex.FUN), 26)
        self.assertEqual(ex.subtree_sizes(ex.REPORTS, "Director")["Maya"], 5)

    def test_every_case(self) -> None:
        cases = [({"A": []}, {"A": 5}), ({"A": ["B"], "B": []}, {"A": 5, "B": 9}),
                 ({"A": ["B", "C"], "B": [], "C": []}, {"A": 10, "B": 4, "C": 5}), ({"A": ["B"], "B": []}, {"A": 5, "B": 5})]
        self.assertEqual([ex.party(r, f, "A")[:2] for r, f in cases], [(5, ["A"]), (9, ["B"]), (10, ["A"]), (5, ["A"])])
        f = dict(ex.FUN)
        f["Director"] = 0
        self.assertEqual(ex.party(ex.REPORTS, f, "Director")[0], 25)
        rng = random.Random(12)
        for _ in range(100):
            n = rng.randint(1, 9)
            reports = {i: [] for i in range(n)}
            for i in range(1, n):
                reports[rng.randrange(i)].append(i)
            fun = {i: rng.randint(1, 9) for i in range(n)}
            total, guests, _ = ex.party(reports, fun, 0)
            self.assertEqual(total, ex.brute(reports, fun))
            self.assertEqual(sum(fun[g] for g in guests), total)


if __name__ == "__main__":
    unittest.main()
