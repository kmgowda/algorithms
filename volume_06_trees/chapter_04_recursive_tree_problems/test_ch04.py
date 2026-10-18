import itertools
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def random_tree(rng, n, lo=-5, hi=9):
    if n == 0:
        return None
    left = rng.randint(0, n - 1)
    return ex.Node(rng.randint(lo, hi), random_tree(rng, left, lo, hi), random_tree(rng, n - 1 - left, lo, hi))


def nodes(t):
    return [] if t is None else [t] + nodes(t.left) + nodes(t.right)


def height(t):
    return -1 if t is None else 1 + max(height(t.left), height(t.right))


def parent_map(t, parent=None, out=None):
    out = {} if out is None else out
    if t:
        out[t] = parent
        parent_map(t.left, t, out)
        parent_map(t.right, t, out)
    return out


def path_between(a, b, parents):
    up = []
    x = a
    while x:
        up.append(x)
        x = parents[x]
    y, down = b, []
    while y not in up:
        down.append(y)
        y = parents[y]
    return up[:up.index(y) + 1] + down[::-1]


class TestRecursiveProblems(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            t = random_tree(rng, rng.randint(1, 12))
            ns = nodes(t)
            balanced = all(abs(height(n.left) - height(n.right)) <= 1 for n in ns)
            self.assertEqual(ex.is_balanced(t), balanced)
            parents = parent_map(t)
            paths = [path_between(a, b, parents) for a, b in itertools.product(ns, ns)]
            self.assertEqual(ex.diameter(t), max(len(p) - 1 for p in paths))
            self.assertEqual(ex.max_path_sum(t), max(sum(n.value for n in p) for p in paths))
            leaf_paths = ex.all_root_to_leaf_paths(t)
            target = rng.randint(-10, 20)
            self.assertEqual(ex.has_path_sum(t, target), any(sum(p) == target for p in leaf_paths))

    def test_lca(self) -> None:
        org = ex.Node("CEO", ex.Node("CTO", ex.Node("Dev", ex.Node("Ana"), ex.Node("Ben")), ex.Node("QA")),
                      ex.Node("CFO", None, ex.Node("Acct")))
        self.assertEqual(ex.lowest_common_ancestor(org, "Ana", "QA").value, "CTO")
        self.assertEqual(ex.lowest_common_ancestor(org, "Ana", "Ben").value, "Dev")
        self.assertEqual(ex.lowest_common_ancestor(org, "Ben", "Acct").value, "CEO")
        self.assertEqual(ex.lowest_common_ancestor(org, "CTO", "Ben").value, "CTO")


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.min_depth(ex.Node(1, None, ex.Node(2, None, ex.Node(3)))), 3)
        t = ex.Node(1, ex.Node(2, ex.Node(3), ex.Node(4)), ex.Node(2, ex.Node(4), ex.Node(3)))
        self.assertTrue(sol.is_symmetric(t))
        self.assertFalse(sol.is_symmetric(ex.Node(1, ex.Node(2), ex.Node(3))))
        self.assertEqual(sol.count_good_nodes(ex.Node(3, ex.Node(1, ex.Node(3)), ex.Node(4, ex.Node(1), ex.Node(5)))), 4)
        named = ex.Node("a", ex.Node("b", ex.Node("d"), ex.Node("e")), ex.Node("c"))
        self.assertEqual(sol.distance_between(named, "d", "e"), 2)
        self.assertEqual(sol.distance_between(named, "d", "c"), 3)


if __name__ == "__main__":
    unittest.main()
