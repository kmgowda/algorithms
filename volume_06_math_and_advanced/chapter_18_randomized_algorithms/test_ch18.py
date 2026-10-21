import random
import unittest

import ch18_examples as ex


class TestChapter18(unittest.TestCase):
    def test_examples(self) -> None:
        rng = random.Random(18)
        pile = [58, 25, 91, 12, 70, 47, 84, 31, 63]
        self.assertEqual((ex.quickselect(pile, 4, rng), ex.quickselect(pile, 4, rng, "first")), ((58, 27), (58, 9)))
        s = list(range(2000))
        self.assertEqual((ex.quickselect(s, 1000, rng, "first")[1], ex.quickselect(s, 1000, rng)[1]), (1501500, 7639))
        A, B, bad = [[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 51]]
        C = ex.matmul(A, B)
        self.assertEqual((C, ex.freivalds(A, B, C, 10, rng), ex.freivalds(A, B, bad, 10, rng)), ([[19, 22], [43, 50]], True, False))
        self.assertEqual(sum(ex.freivalds(A, B, bad, 1, random.Random(s)) for s in range(1000)), 495)

    def test_every_case(self) -> None:
        r = random.Random(1)
        self.assertEqual((ex.quickselect([5], 0, r), ex.quickselect([2, 2, 2], 1, r)[0], ex.quickselect([3, 1, 2], 2, r)[0]), ((5, 1), 2, 3))
        with self.assertRaises(ValueError):
            ex.quickselect([], 0, r)
        for _ in range(300):
            v = [r.randint(0, 20) for _ in range(r.randint(1, 15))]
            k = r.randrange(len(v))
            self.assertEqual(ex.quickselect(v, k, r)[0], sorted(v)[k])


if __name__ == "__main__":
    unittest.main()
