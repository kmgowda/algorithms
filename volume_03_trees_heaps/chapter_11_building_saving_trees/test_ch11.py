import random
import unittest

import ch11_examples as ex


def random_tree(rng, values, depth=6):
    if depth == 0 or not values or rng.random() < 0.2:
        return None
    return ex.Node(values.pop(), random_tree(rng, values, depth - 1), random_tree(rng, values, depth - 1))


class TestChapter51(unittest.TestCase):
    def test_every_case(self) -> None:
        N = ex.Node
        for tree, text in [(None, "#"), (N(5), "5 # #"), (N(3, N(2, N(1))), "3 2 1 # # # #"), (N(2, N(1), N(3)), "2 1 # # 3 # #")]:
            self.assertEqual(ex.save(tree), text)
            self.assertEqual(ex.preorder(ex.load(text)), ex.preorder(tree))
        self.assertIsNone(ex.from_pre_in([], []))
        self.assertEqual(ex.preorder(ex.from_pre_in([5], [5])), [5])
        left, right = ex.from_pre_in([1, 2, 3], [3, 2, 1]), ex.from_pre_in([1, 2, 3], [1, 2, 3])
        self.assertEqual((left.left.value, left.right, right.right.value, right.left), (2, None, 2, None))
        with self.assertRaises(StopIteration):
            ex.from_pre_in([1, 1], [1, 1])
        for keys, h, root in [([], -1, None), ([5], 0, 5), ([1, 2], 1, 1), (list(range(1, 8)), 2, 4), (list(range(1, 101)), 6, 50)]:
            r = ex.balanced_from_sorted(keys)
            self.assertEqual((ex.height(r), r.value if r else None, ex.inorder(r)), (h, root, keys))

    def test_complete(self) -> None:
        self.assertEqual([ex.complete(t) for t in ("58 25 12 # # 47", "58 25 12 # # 47 # # 84 # 91 # #", "#", "",
                                                   "# #", "1 2 # #", "5 # 8 6 # # #")],
                         [False, True, True, False, False, False, True])
        rng = random.Random(5)
        for _ in range(200):
            keys = rng.sample(range(100), rng.randint(0, 20))
            line = ex.save(ex.balanced_from_sorted(sorted(keys)))
            self.assertTrue(ex.complete(line))
            self.assertFalse(ex.complete(line + " #"))
            self.assertFalse(ex.complete(" ".join(line.split()[:-1])))

    def test_round_trips(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            vals = rng.sample(range(1000), 60)
            t = random_tree(rng, vals)
            s = ex.save(t)
            self.assertEqual(ex.save(ex.load(s)), s)
            if t:
                self.assertEqual(ex.save(ex.from_pre_in(ex.preorder(t), ex.inorder(t))), s)
                self.assertEqual(s.split().count("#"), len(ex.preorder(t)) + 1)

    def test_examples(self) -> None:
        self.assertEqual(ex.save(ex.Node(7, ex.Node(3))), "7 3 # # #")
        self.assertEqual(ex.save(ex.balanced_from_sorted([1, 2, 3, 4, 5, 6])), "3 1 # 2 # # 5 4 # # 6 # #")
        b = ex.balanced_from_sorted(list(range(1000)))
        self.assertEqual((ex.height(b), ex.inorder(b)), (9, list(range(1000))))


    def test_optimal_bst(self) -> None:
        import random
        ks, fs = list(ex.REQUESTS), list(ex.REQUESTS.values())
        total, root = ex.optimal_bst(ks, fs)
        self.assertEqual(total, 39)
        opt = ex.build_optimal(ks, root)
        self.assertEqual(ex.looks(opt, ex.REQUESTS), 39)
        self.assertEqual(ex.looks(ex.balanced_from_sorted(ks), ex.REQUESTS), 47)
        self.assertEqual(ex.inorder(opt), ks)
        self.assertEqual(ex.optimal_bst([], []), (0, [[None]]))

        def brute(f, i, j, d):
            if i >= j:
                return 0
            return min(f[r] * d + brute(f, i, r, d + 1) + brute(f, r + 1, j, d + 1) for r in range(i, j))
        r = random.Random(11)
        for _ in range(200):
            n = r.randint(0, 7)
            f = [r.randint(0, 9) for _ in range(n)]
            self.assertEqual(ex.optimal_bst(list(range(n)), f)[0], brute(f, 0, n, 1))


if __name__ == "__main__":
    unittest.main()
