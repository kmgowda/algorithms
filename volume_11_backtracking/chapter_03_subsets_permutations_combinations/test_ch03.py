import itertools
import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


def norm(lists):
    return sorted(tuple(x) for x in lists)


class TestGenerators(unittest.TestCase):
    def test_against_itertools(self) -> None:
        rng = random.Random(1)
        for n in range(0, 6):
            items = [chr(97 + i) for i in range(n)]
            all_subsets = [list(c) for r in range(n + 1) for c in itertools.combinations(items, r)]
            self.assertEqual(norm(ex.subsets(items)), norm(all_subsets))
            self.assertEqual(norm(sol.subsets_by_bitmask(items)), norm(all_subsets))
            self.assertEqual(norm(ex.permutations(items)), norm(itertools.permutations(items)))
            for k in range(n + 1):
                self.assertEqual(ex.combinations(n, k), [list(c) for c in itertools.combinations(range(1, n + 1), k)])
        for _ in range(50):
            v = [rng.randint(1, 3) for _ in range(rng.randint(0, 6))]
            expected = {tuple(sorted(c)) for r in range(len(v) + 1) for c in itertools.combinations(v, r)}
            got = ex.subsets_with_duplicates(v)
            self.assertEqual(len(got), len(expected))
            self.assertEqual({tuple(x) for x in got}, expected)
            perms = ex.unique_permutations(v)
            self.assertEqual(perms, [list(p) for p in sorted(set(itertools.permutations(v)))])

    def test_sums(self) -> None:
        rng = random.Random(2)
        for _ in range(50):
            cands = rng.sample(range(2, 10), rng.randint(1, 4))
            t = rng.randint(1, 15)
            got = ex.combination_sum(cands, t)
            self.assertTrue(all(sum(g) == t for g in got))
            brute = {tuple(sorted(c)) for r in range(1, t + 1) for c in itertools.combinations_with_replacement(sorted(cands), r) if sum(c) == t}
            self.assertEqual({tuple(g) for g in got}, brute)
            multi = [rng.randint(1, 6) for _ in range(rng.randint(1, 7))]
            brute_once = {tuple(sorted(c)) for r in range(1, len(multi) + 1) for c in itertools.combinations(multi, r) if sum(c) == t}
            once = sol.combination_sum_once(multi, t)
            self.assertEqual(len(once), len(brute_once))
            self.assertEqual({tuple(x) for x in once}, brute_once)

    def test_examples(self) -> None:
        self.assertEqual(ex.combination_sum([2, 3, 5], 8), [[2, 2, 2, 2], [2, 3, 3], [3, 5]])
        self.assertEqual(len(ex.team_lineups(["Asha", "Ben", "Cy", "Dev", "Eli"], 3, {"Asha", "Dev"})), 12)
        self.assertEqual(sol.k_digits_sum(3, 9), [[1, 2, 6], [1, 3, 5], [2, 3, 4]])
        for p in itertools.permutations([1, 2, 2, 3]):
            ordered = sorted(set(itertools.permutations([1, 2, 2, 3])))
            idx = ordered.index(p)
            expected = list(ordered[(idx + 1) % len(ordered)])
            self.assertEqual(sol.next_permutation(list(p)), expected)


if __name__ == "__main__":
    unittest.main()
