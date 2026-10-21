import random
import unittest

import ch25_examples as ex


class TestChapter25(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual([ex.balanced(s) for s in ("", "no brackets", "([]{})", "{[()]}", "([)]", "((())", "]", "(()")],
                         [True, True, True, True, False, False, False, False])
        self.assertEqual([ex.evaluate_postfix(s.split()) for s in ("3 4 + 2 *", "7", "5 2 -", "2 5 -")], [14, 7, 3, -3])
        for bad, err in (("6 0 /", ZeroDivisionError), ("3 +", IndexError), ("+", IndexError), ("3 4", ValueError)):
            with self.assertRaises(err):
                ex.evaluate_postfix(bad.split())
        self.assertEqual([ex.next_taller(h) for h in ([], [5], [1, 2, 3], [3, 2, 1], [4, 4, 5])],
                         [[], [None], [1, 2, None], [None, None, None], [2, 2, None]])
        e = ex.Editor()
        self.assertEqual((e.undo(), e.redo()), (None, None))
        e.edit("a"); e.edit("b"); e.undo(); e.edit("c")
        self.assertEqual((e.undo_stack, e.redo_stack, e.redo()), (["a", "c"], [], None))

    def test_examples(self) -> None:
        e = ex.Editor()
        for a in ("add title", "add photo", "bold text"):
            e.edit(a)
        e.undo(); e.undo(); e.redo()
        self.assertEqual((e.undo_stack, e.redo_stack), (["add title", "add photo"], ["bold text"]))
        e.edit("add caption")
        self.assertEqual(e.redo_stack, [])
        self.assertEqual([ex.balanced(s) for s in ("([]{})", "{[()]}", "([)]", "((())", "]", "")],
                         [True, True, False, False, False, True])
        self.assertEqual(ex.evaluate_postfix("3 4 + 2 *".split()), 14)
        self.assertEqual(ex.evaluate_postfix("5 1 2 + 4 * + 3 -".split()), 14)
        self.assertEqual(ex.evaluate_postfix("8 2 -".split()), 6)

    def test_next_taller_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            h = [rng.randint(1, 30) for _ in range(rng.randint(0, 12))]
            brute = [next((k for k in range(i + 1, len(h)) if h[k] > h[i]), None) for i in range(len(h))]
            self.assertEqual(ex.next_taller(h), brute)


if __name__ == "__main__":
    unittest.main()
