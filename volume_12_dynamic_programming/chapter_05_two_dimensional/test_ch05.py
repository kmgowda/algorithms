import itertools
import random
import unittest
from collections import deque

import ch05_examples as ex
import ch05_solutions as sol


def bfs_edit(a, b, alphabet):
    """Edit distance by BFS over strings (tiny inputs only)."""
    dist, q = {a: 0}, deque([a])
    while q:
        s = q.popleft()
        if s == b:
            return dist[s]
        nxt = set()
        for i in range(len(s) + 1):
            for ch in alphabet:
                nxt.add(s[:i] + ch + s[i:])
                if i < len(s):
                    nxt.add(s[:i] + ch + s[i + 1:])
            if i < len(s):
                nxt.add(s[:i] + s[i + 1:])
        for t in nxt:
            if t not in dist and len(t) <= max(len(a), len(b)) + 1:
                dist[t] = dist[s] + 1
                q.append(t)


def brute_lcs(a, b):
    for r in range(min(len(a), len(b)), -1, -1):
        subs = {"".join(c) for c in itertools.combinations(a, r)}
        if any(self_sub(s, b) for s in subs):
            return r
    return 0


def self_sub(s, b):
    it = iter(b)
    return all(ch in it for ch in s)


class TestTwoDimensional(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(60):
            a = "".join(rng.choice("ab") for _ in range(rng.randint(0, 4)))
            b = "".join(rng.choice("ab") for _ in range(rng.randint(0, 4)))
            self.assertEqual(ex.edit_distance(a, b), bfs_edit(a, b, "ab"))
            self.assertEqual(ex.lcs_length(a, b), brute_lcs(a, b))
            s = ex.lcs_string(a, b)
            self.assertEqual(len(s), ex.lcs_length(a, b))
            self.assertTrue(self_sub(s, a) and self_sub(s, b))
            sub = sol.longest_common_substring(a, b)
            self.assertTrue(sub in a and sub in b)
            best = max((j - i for i in range(len(a) + 1) for j in range(i, len(a) + 1) if a[i:j] in b), default=0)
            self.assertEqual(len(sub), best)
        for _ in range(60):
            r, c = rng.randint(1, 4), rng.randint(1, 4)
            grid = ["".join(rng.choice("..#") for _ in range(c)) for _ in range(r)]
            moves = [0] * (r - 1) + [1] * (c - 1)
            count = 0
            for order in set(itertools.permutations(moves)):
                y = x = 0
                ok = grid[0][0] != "#"
                for m in order:
                    y, x = (y + 1, x) if m == 0 else (y, x + 1)
                    ok = ok and grid[y][x] != "#"
                count += ok
            self.assertEqual(ex.grid_paths_with_blocks(grid), count)

    def test_examples(self) -> None:
        self.assertEqual(ex.edit_distance("kitten", "sitting"), 3)
        self.assertEqual(ex.edit_distance("horse", "ros"), 3)
        self.assertEqual(ex.lcs_length("ACCGGTCG", "GTCGTTCG"), 5)
        top = ex.suggest("recieve", ["receive", "relieve", "recipe", "deceive", "review"])
        self.assertEqual(top[0], "relieve")              # 1 replacement; a swap of neighbours counts as 2 edits
        self.assertIn("receive", top)
        diff = ex.line_diff(["buy milk", "call mum", "pay rent", "gym"], ["buy milk", "pay rent", "book train", "gym"])
        self.assertEqual(diff, ["  buy milk", "- call mum", "  pay rent", "+ book train", "  gym"])
        self.assertEqual(sol.largest_square(["10100", "10111", "11111", "10010"]), 2)
        self.assertEqual(sol.falling_path_min([[2, 1, 3], [6, 5, 4], [7, 8, 9]]), 13)
        self.assertTrue(sol.is_interleaving("aabcc", "dbbca", "aadbbcbcac"))
        self.assertFalse(sol.is_interleaving("aabcc", "dbbca", "aadbbbaccc"))


if __name__ == "__main__":
    unittest.main()
