import math
import random
import unittest

import ch13_examples as ex


class TestChapter13(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual((ex.factorial(1), ex.factorial(5)), (1, 120))
        for bad in (0, -3, 2000):
            with self.assertRaises(RecursionError):
                ex.factorial(bad)
        self.assertEqual([ex.recursive_sum(a) for a in ([], [7], [12, 25, 31])], [0, 7, 68])
        self.assertEqual([ex.largest(a) for a in ([47], [91, 12, 47], [12, 47, 91], [47, 91, 91])], [47, 91, 91, 91])
        with self.assertRaises(RecursionError):
            ex.largest([])
        self.assertEqual((ex.count_dolls([]), ex.count_dolls([[[[[]]]]])), (1, 5))

    def test_recursion(self) -> None:
        rng = random.Random(1)
        for n in range(1, 50):
            self.assertEqual(ex.factorial(n), math.factorial(n))
        for _ in range(100):
            xs = [rng.randint(-50, 50) for _ in range(rng.randint(1, 30))]
            self.assertEqual(ex.recursive_sum(xs), sum(xs))
            self.assertEqual(ex.largest(xs), max(xs))
        self.assertEqual(ex.recursive_sum([]), 0)
        self.assertEqual(ex.count_dolls([[[[[]]]]]), 5)
        with self.assertRaises(RecursionError):
            ex.countdown_without_base(3)

    def test_before_and_after(self) -> None:
        for n, down in ((0, []), (1, [1]), (3, [3, 2, 1])):
            before, after = [], []
            ex.print_before(n, before)
            ex.print_after(n, after)
            self.assertEqual((before, after), (down, down[::-1]))

    def test_tail_and_loop(self) -> None:
        for n in range(1, 30):
            self.assertEqual(ex.factorial_tail(n), math.factorial(n))
            self.assertEqual(ex.factorial_loop(n), math.factorial(n))
        self.assertEqual(ex.factorial_loop(3000), math.factorial(3000))   # a loop has no depth limit
        with self.assertRaises(RecursionError):
            ex.factorial_tail(3000)                                       # Python keeps every frame


if __name__ == "__main__":
    unittest.main()
