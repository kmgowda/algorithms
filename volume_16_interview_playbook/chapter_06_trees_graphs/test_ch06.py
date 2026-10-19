import itertools
import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


def random_bst(rng, n):
    root = None
    for v in rng.sample(range(100), n):
        if root is None:
            root = ex.TreeNode(v)
            continue
        cur = root
        while True:
            side = "left" if v < cur.val else "right"
            if getattr(cur, side) is None:
                setattr(cur, side, ex.TreeNode(v))
                break
            cur = getattr(cur, side)
    return root


def inorder(n):
    return inorder(n.left) + [n.val] + inorder(n.right) if n else []


def paths(n):
    """Every root-to-node path, to check depth, LCA and diameter by brute force."""
    out = {}

    def go(node, path):
        if node:
            out[node.val] = path + [node]
            go(node.left, path + [node])
            go(node.right, path + [node])

    go(n, [])
    return out


class TestTreesGraphs(unittest.TestCase):
    def test_trees(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            root = random_bst(rng, rng.randint(0, 12))
            p = paths(root)
            self.assertEqual(ex.max_depth(root), max((len(v) for v in p.values()), default=0))
            self.assertTrue(ex.is_valid_bst(root))
            self.assertEqual(sum(ex.level_order(root), []).__len__(), len(p))
            if len(p) >= 2:
                a, b = rng.sample(sorted(p), 2)
                common = [x for x, y in zip(p[a], p[b]) if x is y]
                self.assertEqual(ex.lowest_common_ancestor(root, a, b), common[-1])
                best = max(len(p[x]) + len(p[y]) - 2 * len([u for u, v in zip(p[x], p[y]) if u is v])
                           for x, y in itertools.combinations(p, 2))
                self.assertEqual(sol.diameter(root), best)
                if root.left:
                    root.left.val = root.val + 1                 # left child bigger than the root
                else:
                    root.right.val = root.val - 1                # right child smaller than the root
                self.assertFalse(ex.is_valid_bst(root))
            mirrored = inorder(ex.invert(random_bst(random.Random(7), 6)))
            self.assertEqual(mirrored, sorted(mirrored, reverse=True))

    def test_graphs(self) -> None:
        rng = random.Random(2)
        for _ in range(100):
            rows, cols = rng.randint(1, 5), rng.randint(1, 5)
            grid = ["".join(rng.choice("01") for _ in range(cols)) for _ in range(rows)]
            parent = {}

            def find(x):
                while parent[x] != x:
                    x = parent[x]
                return x

            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] == "1":
                        parent[(r, c)] = (r, c)
                        for nr, nc in ((r - 1, c), (r, c - 1)):
                            if (nr, nc) in parent:
                                parent[find((nr, nc))] = find((r, c))
            self.assertEqual(ex.count_islands(grid), len({find(x) for x in parent}))
            n = rng.randint(1, 5)
            pre = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 6))]
            ok = any(all(order.index(a) > order.index(b) for a, b in pre) for order in itertools.permutations(range(n)))
            self.assertEqual(ex.can_finish(n, pre), ok)
        self.assertEqual(sol.rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]]), 4)
        self.assertEqual(sol.rotting_oranges([[2, 1, 1], [0, 1, 1], [1, 0, 1]]), -1)
        self.assertEqual(sol.right_side_view(ex.from_level_list([1, 2, 3, None, 5, None, 4])), [1, 3, 4])
        self.assertEqual(ex.org_chart_depth({"CEO": ["CTO", "CFO"], "CTO": ["Lead"], "Lead": ["Dev"]}, "CEO"), 4)


if __name__ == "__main__":
    unittest.main()
