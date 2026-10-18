import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestMatching(unittest.TestCase):
    def test_random_matchings(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            people = [f"p{i}" for i in range(rng.randint(0, 5))]
            jobs = [f"j{i}" for i in range(rng.randint(1, 5))]
            likes = {p: rng.sample(jobs, rng.randint(0, len(jobs))) for p in people}
            m = ex.max_bipartite_matching(likes)
            self.assertEqual(len(m), sol.brute_force_matching(likes))
            self.assertEqual(len(m), sol.matching_via_flow(likes))
            self.assertEqual(len(set(m.values())), len(m))
            self.assertTrue(all(j in likes[p] for j, p in m.items()))

    def test_assignment(self) -> None:
        rng = random.Random(2)
        for _ in range(100):
            n = rng.randint(1, 6)
            cost = [[rng.randint(1, 20) for _ in range(n)] for _ in range(n)]
            total, perm = ex.min_cost_assignment(cost)
            self.assertEqual(sorted(perm), list(range(n)))
            self.assertEqual(total, ex.bitmask_assignment(cost))

    def test_examples(self) -> None:
        likes = {"Ana": ["cook", "driver"], "Ben": ["cook"], "Cy": ["driver", "guide"], "Dev": ["guide"]}
        self.assertEqual(len(ex.max_bipartite_matching(likes)), 3)
        self.assertFalse(sol.is_perfect(likes))
        cost = [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]
        self.assertEqual(ex.min_cost_assignment(cost)[0], 13)
        placed = ex.school_admissions({"Ria": ["North"], "Sam": ["North", "South"], "Tia": ["North"], "Uma": ["South"]},
                                      {"North": 2, "South": 1})
        self.assertEqual(sum(len(v) for v in placed.values()), 3)
        self.assertEqual(len(placed["North"]), 2)


if __name__ == "__main__":
    unittest.main()
