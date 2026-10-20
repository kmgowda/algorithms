import random
import unittest

import ch44_examples as ex


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.25:
        return None
    return ex.Node(rng.randint(0, 50), random_tree(rng, depth - 1), random_tree(rng, depth - 1))


def values(n):
    return [] if n is None else [n.value] + values(n.left) + values(n.right)


class TestChapter44(unittest.TestCase):
    def test_library(self) -> None:
        lib = ex.library()
        self.assertEqual((ex.size(lib), ex.total(lib), ex.height(lib), ex.best_walk(lib)), (9, 108, 3, 37))
        lib.right.right.left.value = 40
        self.assertEqual(ex.best_walk(lib), 52)

    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            t = random_tree(rng, 6)
            v = values(t)
            self.assertEqual(ex.size(t), len(v))
            self.assertEqual(ex.total(t), sum(v))
            if v:
                self.assertEqual(ex.largest(t), max(v))
            self.assertTrue(ex.same_tree(t, ex.mirror(ex.mirror(t))))
        self.assertTrue(ex.symmetric(ex.Node(1, ex.Node(2, ex.Node(3), ex.Node(4)), ex.Node(2, ex.Node(4), ex.Node(3)))))
        self.assertFalse(ex.symmetric(ex.Node(1, ex.Node(2), ex.Node(3))))


if __name__ == "__main__":
    unittest.main()
