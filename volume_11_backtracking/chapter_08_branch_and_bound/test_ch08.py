import itertools
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestBranchAndBound(unittest.TestCase):
    def test_assignment(self) -> None:
        rng = random.Random(1)
        for _ in range(80):
            n = rng.randint(1, 6)
            cost = [[rng.randint(1, 30) for _ in range(n)] for _ in range(n)]
            best, perm, nodes = ex.assignment_bnb(cost)
            self.assertEqual(best, sol.assignment_brute_nodes(cost)[0])
            self.assertEqual(sorted(perm), list(range(n)))
            self.assertEqual(sum(cost[i][perm[i]] for i in range(n)), best)

    def test_tsp(self) -> None:
        rng = random.Random(2)
        for _ in range(40):
            n = rng.randint(1, 7)
            pts = [(rng.random() * 100, rng.random() * 100) for _ in range(n)]
            d = [[round(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5) for b in pts] for a in pts]
            length, tour, _ = ex.tsp_bnb(d)
            self.assertEqual(length, ex.tsp_brute(d)[0])
            if n > 1:
                self.assertEqual(sorted(tour[:-1]), list(range(n)))

    def test_knapsack(self) -> None:
        rng = random.Random(3)
        for _ in range(100):
            items = [(f"i{k}", rng.randint(1, 8), rng.randint(1, 40)) for k in range(rng.randint(0, 8))]
            cap = rng.randint(0, 20)
            brute = max((sum(v for _, _, v in c) for r in range(len(items) + 1) for c in itertools.combinations(items, r)
                         if sum(w for _, w, _ in c) <= cap), default=0)
            value, take, _ = ex.knapsack_best_first(items, cap)
            self.assertEqual(value, brute)
            chosen = [it for it in items if it[0] in take]
            self.assertLessEqual(sum(w for _, w, _ in chosen), cap)
            self.assertEqual(sum(v for _, _, v in chosen), value)
            self.assertEqual(sol.knapsack_dfs_bnb([(w, v) for _, w, v in items], cap), brute)

    def test_examples(self) -> None:
        self.assertEqual(ex.assignment_bnb([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]])[0], 13)
        self.assertEqual(sol.max_profit_assignment([[3, 1], [1, 3]]), (6, [0, 1]))
        crew = ex.crew_assignment(["Ira", "Jo", "Kai"], ["BLR-DEL", "BOM-GOI", "MAA-CCU"], [[3, 1, 4], [2, 5, 1], [1, 2, 3]])
        self.assertEqual(crew, {"Ira": "BOM-GOI", "Jo": "MAA-CCU", "Kai": "BLR-DEL"})


if __name__ == "__main__":
    unittest.main()
