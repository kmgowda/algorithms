import random
import unittest

import ch24_examples as ex


class TestChapter24(unittest.TestCase):
    def test_every_case(self) -> None:
        for S in (ex.Stack, ex.LinkedStack):
            with self.assertRaises(IndexError):
                S().pop()
            s = S()
            s.push(5)
            self.assertEqual((s.pop(), s.is_empty()), (5, True))
        for S in (ex.Stack, ex.LinkedStack):
            with self.assertRaises(IndexError):
                S().peek()
        b = ex.BoundedStack(3)
        for v in (47, 12, 63):
            b.push(v)
        with self.assertRaises(OverflowError):
            b.push(25)
        self.assertEqual(b.pop(), 63)
        b.push(25)
        self.assertEqual([b.pop(), b.pop(), b.pop(), b.is_empty()], [25, 12, 47, True])
        with self.assertRaises(IndexError):
            b.pop()
        z = ex.BoundedStack(0)
        with self.assertRaises(OverflowError):
            z.push(1)
        self.assertTrue(z.is_empty())
        self.assertEqual([ex.sort_with_stacks(a) for a in ([], [7], [1, 2, 3], [3, 2, 1], [5, 5, 2])],
                         [[], [7], [1, 2, 3], [1, 2, 3], [2, 5, 5]])
        self.assertEqual([ex.reverse_word(w) for w in ("", "A", "AB", "LEVEL", "STACK")], ["", "A", "BA", "LEVEL", "KCATS"])

    def test_both_stacks(self) -> None:
        rng = random.Random(1)
        for cls in (ex.Stack, ex.LinkedStack):
            s, ref = cls(), []
            for _ in range(2000):
                if ref and rng.random() < 0.45:
                    self.assertEqual(s.pop(), ref.pop())
                else:
                    v = rng.randint(0, 99)
                    s.push(v)
                    ref.append(v)
                self.assertEqual(s.is_empty(), not ref)
                if ref:
                    self.assertEqual(s.peek(), ref[-1])
            with self.assertRaises(IndexError):
                cls().pop()

    def test_bounded_against_list(self) -> None:
        rng = random.Random(3)
        for cap in range(0, 6):
            s, ref = ex.BoundedStack(cap), []
            for _ in range(300):
                if rng.random() < 0.5:
                    v = rng.randint(0, 9)
                    if len(ref) == cap:
                        with self.assertRaises(OverflowError):
                            s.push(v)
                    else:
                        s.push(v)
                        ref.append(v)
                elif ref:
                    self.assertEqual(s.pop(), ref.pop())
                self.assertEqual(s.is_empty(), not ref)

    def test_examples(self) -> None:
        self.assertEqual(ex.sort_with_stacks([47, 12, 63, 25, 84]), [12, 25, 47, 63, 84])
        rng = random.Random(2)
        for _ in range(200):
            xs = [rng.randint(0, 50) for _ in range(rng.randint(0, 10))]
            self.assertEqual(ex.sort_with_stacks(xs), sorted(xs))
        self.assertEqual(ex.reverse_word("STACK"), "KCATS")


if __name__ == "__main__":
    unittest.main()
