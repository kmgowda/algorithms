import random
import unittest

import ch18_examples as ex


class TestChapter47(unittest.TestCase):
    def test_every_case(self) -> None:
        balanced = (2, (1, None, None), (3, None, None))
        for keys, case in [([3, 2, 1], [("LL", 3)]), ([1, 2, 3], [("RR", 1)]), ([3, 1, 2], [("LR", 3)]),
                           ([1, 3, 2], [("RL", 1)]), ([2, 1, 3], [])]:
            log = []
            self.assertEqual((ex.shape(ex.build(keys, log)), log), (balanced, case))
        self.assertEqual((ex.h(ex.build([])), ex.h(ex.build([5]))), (-1, 0))
        self.assertEqual(ex.inorder(ex.build([5, 5])), [5])
        big = ex.build(range(1, 101))
        self.assertEqual((ex.h(big), ex.is_avl(big), ex.inorder(big)), (6, True, list(range(1, 101))))

    def test_avl(self) -> None:
        log = []
        t = ex.build([12, 25, 31, 47, 58, 63, 70], log)
        self.assertEqual(t.height, 2)
        self.assertEqual(log, [("RR", 12), ("RR", 31), ("RR", 25), ("RR", 58)])
        log = []
        self.assertEqual(ex.shape(ex.build([50, 40, 30, 20, 10], log)),
                         (40, (20, (10, None, None), (30, None, None)), (50, None, None)))
        self.assertEqual(ex.shape(ex.build([10, 30, 20])), (20, (10, None, None), (30, None, None)))
        self.assertEqual(ex.build(range(1000)).height, 9)
        rng = random.Random(1)
        for _ in range(100):
            keys = [rng.randint(0, 200) for _ in range(rng.randint(1, 60))]
            t = ex.build(keys)
            self.assertTrue(ex.is_avl(t))
            self.assertEqual(ex.inorder(t), sorted(set(keys)))


if __name__ == "__main__":
    unittest.main()
