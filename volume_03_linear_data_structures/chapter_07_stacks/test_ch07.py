import itertools
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


class TestStacks(unittest.TestCase):
    def test_both_implementations_match(self) -> None:
        rng = random.Random(2)
        for cls in (ex.ArrayStack, ex.LinkedStack):
            stack, model = cls(), []
            for _ in range(2000):
                if rng.random() < 0.6:
                    v = rng.randint(0, 99)
                    stack.push(v)
                    model.append(v)
                elif model:
                    self.assertEqual(stack.peek(), model[-1])
                    self.assertEqual(stack.pop(), model.pop())
                self.assertEqual(len(stack), len(model))
                self.assertEqual(stack.is_empty(), not model)
            empty = cls()
            with self.assertRaises(IndexError):
                empty.pop()
            with self.assertRaises(IndexError):
                empty.peek()

    def test_reverse(self) -> None:
        self.assertEqual(ex.reverse_with_stack([1, 2, 3]), [3, 2, 1])
        self.assertEqual(ex.reverse_with_stack([]), [])

    def test_balanced(self) -> None:
        cases = {"(a[b]{c})": True, "(]": False, "((": False, ")": False, "": True, "print(prices[0])": True}
        for text, expected in cases.items():
            self.assertEqual(ex.is_balanced(text), expected, text)

    def test_editor(self) -> None:
        e = ex.TextEditor()
        for chunk in ("a", "b", "c"):
            e.type(chunk)
        e.undo()
        e.undo()
        self.assertEqual(e.text, "a")
        e.redo()
        self.assertEqual(e.text, "ab")
        e.type("X")
        e.redo()
        self.assertEqual(e.text, "abX")
        for _ in range(10):
            e.undo()
        self.assertEqual(e.text, "")

    def test_browser(self) -> None:
        b = ex.BrowserHistory("home")
        for page in ("animals", "lions", "cubs"):
            b.visit(page)
        self.assertEqual([b.back(), b.back(), b.forward()], ["lions", "animals", "lions"])
        b.visit("tigers")
        self.assertEqual(b.forward(), "tigers")
        self.assertEqual([b.back(), b.back(), b.back(), b.back()], ["lions", "animals", "home", "home"])


class TestSolutions(unittest.TestCase):
    def test_min_stack(self) -> None:
        rng = random.Random(6)
        m, model = sol.MinStack(), []
        for _ in range(1000):
            if rng.random() < 0.6 or not model:
                v = rng.randint(-50, 50)
                m.push(v)
                model.append(v)
            else:
                self.assertEqual(m.pop(), model.pop())
            if model:
                self.assertEqual(m.get_min(), min(model))
                self.assertEqual(m.top(), model[-1])

    def test_string_stacks(self) -> None:
        self.assertEqual(sol.remove_adjacent_duplicates("abbaca"), "ca")
        self.assertEqual(sol.simplify_path("/zoo/./animals/../lions/"), "/zoo/lions")
        self.assertEqual(sol.simplify_path("/../"), "/")
        self.assertTrue(sol.backspace_compare("ab#c", "ad#c"))
        self.assertFalse(sol.backspace_compare("a#c", "b"))

    def test_validate_pops(self) -> None:
        self.assertTrue(sol.validate_pops([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]))
        self.assertFalse(sol.validate_pops([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]))
        pushed = [1, 2, 3, 4]
        valid = set()

        def explore(i: int, stack: list[int], out: list[int]) -> None:
            if len(out) == len(pushed):
                valid.add(tuple(out))
                return
            if i < len(pushed):
                explore(i + 1, stack + [pushed[i]], out)
            if stack:
                explore(i, stack[:-1], out + [stack[-1]])

        explore(0, [], [])
        for order in itertools.permutations(pushed):
            self.assertEqual(sol.validate_pops(pushed, list(order)), order in valid)


if __name__ == "__main__":
    unittest.main()
