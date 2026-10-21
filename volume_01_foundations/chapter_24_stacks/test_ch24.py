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
        with self.assertRaises(IndexError):
            ex.Stack().peek()
        with self.assertRaises(AttributeError):
            ex.LinkedStack().peek()
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

    def test_examples(self) -> None:
        self.assertEqual(ex.sort_with_stacks([47, 12, 63, 25, 84]), [12, 25, 47, 63, 84])
        rng = random.Random(2)
        for _ in range(200):
            xs = [rng.randint(0, 50) for _ in range(rng.randint(0, 10))]
            self.assertEqual(ex.sort_with_stacks(xs), sorted(xs))
        self.assertEqual(ex.reverse_word("STACK"), "KCATS")


if __name__ == "__main__":
    unittest.main()
