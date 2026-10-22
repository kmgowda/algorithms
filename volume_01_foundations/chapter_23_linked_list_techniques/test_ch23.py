import random
import unittest

import ch23_examples as ex


class TestChapter23(unittest.TestCase):
    def test_every_case(self) -> None:
        B, V = ex.build, ex.values_of
        self.assertEqual([V(ex.reverse(B(a))) for a in ([], [7], [1, 2])], [[], [7], [2, 1]])
        self.assertIsNone(ex.middle(None))
        self.assertEqual([ex.middle(B(a)).value for a in ([7], [1, 2], [1, 2, 3], [1, 2, 3, 4, 5, 6])], [7, 2, 2, 4])
        self.assertEqual((ex.has_cycle(None), ex.has_cycle(B([7]))), ((False, 0), (False, 0)))
        self.assertEqual(ex.has_cycle(ex.with_loop([7], 0)), (True, 1))
        self.assertEqual(ex.has_cycle(ex.with_loop([1, 2], 0)), (True, 2))
        self.assertEqual(ex.has_cycle(ex.with_loop(list(range(8)), 0)), (True, 8))
        self.assertEqual(ex.has_cycle(ex.with_loop(list(range(8)), 7)), (True, 7))
        self.assertEqual(ex.has_cycle(B(range(8))), (False, 4))
        self.assertEqual((V(ex.merge(None, B([1, 2]))), V(ex.merge(None, None))), ([1, 2], []))
        a, b = B([4, 4]), B([4])
        first = a
        merged = ex.merge(a, b)
        self.assertIs(merged, first)
        self.assertEqual(V(merged), [4, 4, 4])

    def test_loop_start_and_recursive_reverse(self) -> None:
        B, V = ex.build, ex.values_of
        self.assertIsNone(ex.loop_start(None))
        self.assertIsNone(ex.loop_start(B([7])))
        self.assertIsNone(ex.loop_start(B(range(8))))
        node, length, meet, to_start = ex.loop_start(ex.with_loop([7], 0))
        self.assertEqual((node.value, length, to_start), (7, 1, 0))
        node, length, meet, to_start = ex.loop_start(ex.with_loop([12, 25, 47, 58, 63, 70, 84, 91], 3))
        self.assertEqual((node.value, length, meet, to_start), (58, 5, 5, 3))
        node, length, meet, to_start = ex.loop_start(ex.with_loop([12, 25, 31, 47, 58], 1))
        self.assertEqual((node.value, length, meet, to_start), (25, 4, 4, 1))
        node, length, _, to_start = ex.loop_start(ex.with_loop(list(range(8)), 7))
        self.assertEqual((node.value, length, to_start), (7, 1, 7))
        self.assertEqual([V(ex.reverse_recursive(B(a))) for a in ([], [7], [1, 2], [12, 25, 47, 63])],
                         [[], [7], [2, 1], [63, 47, 25, 12]])
        rng = random.Random(4)
        for _ in range(300):
            n = rng.randint(1, 15)
            back = rng.randrange(n)
            node, length, _, to_start = ex.loop_start(ex.with_loop(list(range(n)), back))
            self.assertEqual((node.value, length, to_start), (back, n - back, back))
            xs = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
            self.assertEqual(V(ex.reverse_recursive(B(xs))), xs[::-1])

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
