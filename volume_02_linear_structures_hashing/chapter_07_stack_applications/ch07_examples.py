"""Volume 2, Chapter 7 - Stack Applications.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations


class Editor:
    """Undo and redo with two stacks (Figure 7.1)."""

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
    """True if every bracket in text is closed by the matching kind, innermost first (Figure 7.2)."""
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
    """Evaluate a postfix expression such as ['3', '4', '+', '2', '*'] (Figure 7.3)."""
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


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def to_postfix(tokens: list[str]) -> list[str]:
    """Section 7.6, Figure 7.4: turn an ordinary (infix) expression into postfix with a stack of waiting operators.
    Operators of equal precedence are left-associative: 8 - 3 - 2 becomes 8 3 - 2 -."""
    out: list[str] = []
    waiting: list[str] = []                     # operators and "(" not yet written out
    for t in tokens:
        if t in PRECEDENCE:
            while waiting and waiting[-1] != "(" and PRECEDENCE[waiting[-1]] >= PRECEDENCE[t]:
                out.append(waiting.pop())       # an earlier operator that binds at least as tightly goes first
            waiting.append(t)
        elif t == "(":
            waiting.append(t)
        elif t == ")":
            while waiting and waiting[-1] != "(":
                out.append(waiting.pop())
            if not waiting:
                raise ValueError("unmatched )")
            waiting.pop()                       # discard the "("
        else:
            out.append(t)                       # a number goes straight to the output
    while waiting:
        if waiting[-1] == "(":
            raise ValueError("unmatched (")
        out.append(waiting.pop())
    return out


def next_taller(heights: list[int]) -> list[int | None]:
    """For each book, the index of the first taller book to its right, with a monotonic stack: O(n) (Figure 7.5)."""
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
    print(" ".join(to_postfix("3 + 4 * 2 - 1".split())), " ".join(to_postfix("( 3 + 4 ) * ( 5 - 2 )".split())))
    h = [22, 18, 25, 15, 17, 28, 20]
    print([h[j] if j is not None else None for j in next_taller(h)])
