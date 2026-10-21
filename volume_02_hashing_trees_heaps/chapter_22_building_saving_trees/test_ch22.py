import random
import unittest

import ch22_examples as ex


def random_tree(rng, values, depth=6):
    if depth == 0 or not values or rng.random() < 0.2:
        return None
    return ex.Node(values.pop(), random_tree(rng, values, depth - 1), random_tree(rng, values, depth - 1))


class TestChapter51(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
