"""Volume 1, Chapter 25 - Stack Applications.

Run:  python3 ch25_examples.py
"""

from __future__ import annotations


class Editor:
    """Undo and redo with two stacks (Figure 25.1)."""

    def __init__(self):
        self.undo_stack: list[str] = []
        self.redo_stack: list[str] = []

    def edit(self, action: str) -> None:
        self.undo_stack.append(action)
        self.redo_stack.clear()                 # a new edit invalidates the redo history

    def undo(self) -> str | None:
        if not self.undo_stack:
            return None
        action = self.undo_stack.pop()
        self.redo_stack.append(action)
        return action

    def redo(self) -> str | None:
        if not self.redo_stack:
            return None
        action = self.redo_stack.pop()
        self.undo_stack.append(action)
        return action


def balanced(text: str) -> bool:
    """True if every bracket in text is closed by the matching kind, innermost first (Figure 25.2)."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def evaluate_postfix(tokens: list[str]) -> float:
    """Evaluate a postfix expression such as ['3', '4', '+', '2', '*'] (Figure 25.3)."""
    ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b, "/": lambda a, b: a / b}
    stack: list[float] = []
    for t in tokens:
        if t in ops:
            right, left = stack.pop(), stack.pop()
            stack.append(ops[t](left, right))
        else:
            stack.append(float(t))
    if len(stack) != 1:
        raise ValueError("malformed expression")
    return stack[0]


def next_taller(heights: list[int]) -> list[int | None]:
    """For each book, the index of the first taller book to its right, with a monotonic stack: O(n) (Figure 25.4)."""
    answer: list[int | None] = [None] * len(heights)
    waiting: list[int] = []                     # indexes, heights decreasing bottom to top
    for i, h in enumerate(heights):
        while waiting and heights[waiting[-1]] < h:
            answer[waiting.pop()] = i
        waiting.append(i)
    return answer


if __name__ == "__main__":
    e = Editor()
    for a in ("add title", "add photo", "bold text"):
        e.edit(a)
    e.undo(); e.undo(); e.redo()
    print(e.undo_stack, e.redo_stack)
    print([balanced(s) for s in ("([]{})", "{[()]}", "([)]", "((())", "]")])
    print(evaluate_postfix("3 4 + 2 *".split()), evaluate_postfix("5 1 2 + 4 * + 3 -".split()))
    h = [22, 18, 25, 15, 17, 28, 20]
    print([h[j] if j is not None else None for j in next_taller(h)])
