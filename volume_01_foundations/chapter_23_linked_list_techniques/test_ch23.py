import random
import unittest

import ch23_examples as ex


class TestChapter23(unittest.TestCase):
    def test_all(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            xs = [rng.randint(0, 50) for _ in range(rng.randint(0, 12))]
            self.assertEqual(ex.values_of(ex.reverse(ex.build(xs))), xs[::-1])
            if xs:
                self.assertEqual(ex.middle(ex.build(xs)).value, xs[len(xs) // 2])
                self.assertTrue(ex.has_cycle(ex.with_loop(xs, rng.randrange(len(xs))))[0])
            self.assertFalse(ex.has_cycle(ex.build(xs))[0])
            a, b = sorted(xs), sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 8)))
            self.assertEqual(ex.values_of(ex.merge(ex.build(a), ex.build(b))), sorted(a + b))
        self.assertEqual(ex.middle(ex.build(range(1, 7))).value, 4)
        self.assertEqual(ex.has_cycle(ex.with_loop(list(range(7)), 3)), (True, 4))
        self.assertEqual(ex.values_of(ex.merge(ex.build([3, 8, 9]), ex.build([1, 4, 10, 12]))),
                         [1, 3, 4, 8, 9, 10, 12])


if __name__ == "__main__":
    unittest.main()
