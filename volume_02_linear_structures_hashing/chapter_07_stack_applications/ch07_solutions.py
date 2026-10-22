"""Volume 2, Chapter 7 - Thinking Problems.

Problem 1: one kind of bracket needs only a counter.
Problem 2: the largest rectangle under a row of books, in O(n) with a monotonic stack.
Problem 3: the wrong postfix evaluator that keeps only the two newest values, kept here so the tests can show it.
"""

from __future__ import annotations


def balanced_one_kind(text: str) -> bool:
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def largest_rectangle(heights: list[int]) -> int:
    best = 0
    waiting: list[int] = []                     # indexes, heights increasing bottom to top
    for i, h in enumerate(heights + [0]):       # a final height 0 answers every waiting book
        while waiting and heights[waiting[-1]] >= h:
            top = heights[waiting.pop()]
            left = waiting[-1] + 1 if waiting else 0
            best = max(best, top * (i - left))
        waiting.append(i)
    return best


def evaluate_postfix_two_slots(tokens: list[str]) -> float:
    """WRONG: keeps only the two newest values, so older ones fall off the bottom."""
    ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b, "/": lambda a, b: a / b}
    slots: list[float] = []
    for t in tokens:
        if t in ops:
            right, left = slots.pop(), (slots.pop() if slots else 0.0)
            slots.append(ops[t](left, right))
        else:
            slots = (slots + [float(t)])[-2:]
    return slots[-1]


if __name__ == "__main__":
    print(balanced_one_kind("(()())"), largest_rectangle([6, 2, 5, 4, 5, 1, 6]))
    print(evaluate_postfix_two_slots("3 4 2 * + 1 -".split()))
