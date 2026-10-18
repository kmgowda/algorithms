import random
import unittest

import ch12_examples as ex
import ch12_solutions as sol


def random_tree(rng, values):
    if not values:
        return None
    i = rng.randrange(len(values))
    return ex.Node(values[i], random_tree(rng, values[:i]), random_tree(rng, values[i + 1:]))


def pre(t):
    return [] if t is None else [t.value] + pre(t.left) + pre(t.right)


def ino(t):
    return [] if t is None else ino(t.left) + [t.value] + ino(t.right)


def post(t):
    return [] if t is None else post(t.left) + post(t.right) + [t.value]


class TestSerialization(unittest.TestCase):
    def test_round_trips_and_construction(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            values = rng.sample(range(-50, 50), rng.randint(0, 15))
            t = random_tree(rng, values)
            self.assertTrue(ex.same_tree(t, ex.deserialize(ex.serialize(t))))
            self.assertTrue(ex.same_tree(t, ex.build_from_pre_in(pre(t), ino(t))))
            self.assertTrue(ex.same_tree(t, sol.build_from_post_in(post(t), ino(t))))
            bst_values = sorted(values)
            b = random_tree(rng, bst_values)            # random_tree on sorted values builds a BST
            self.assertTrue(ex.same_tree(b, sol.bst_from_preorder(pre(b))))

    def test_views(self) -> None:
        fam = ex.Node("G", ex.Node("M", ex.Node("A"), ex.Node("B")), ex.Node("U", None, ex.Node("C")))
        self.assertEqual(ex.vertical_columns(fam), [["A"], ["M"], ["G", "B"], ["U"], ["C"]])
        self.assertEqual(ex.top_view(fam), ["A", "M", "G", "U", "C"])
        self.assertEqual(ex.bottom_view(fam), ["A", "M", "B", "U", "C"])
        self.assertEqual(ex.vertical_columns(None), [])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        t = ex.Node(1, ex.Node(2, None, ex.Node(4)), ex.Node(3))
        self.assertEqual(sol.serialize_levels(t), [1, 2, 3, None, 4])
        self.assertEqual(sol.left_view(t), [1, 2, 4])
        self.assertEqual(ex.serialize(sol.bst_from_preorder([8, 5, 1, 7, 10, 12])), "8,5,1,#,#,7,#,#,10,#,12,#,#")


if __name__ == "__main__":
    unittest.main()
