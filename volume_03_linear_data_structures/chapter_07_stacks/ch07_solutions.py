"""Volume 3, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

from typing import Any

from ch07_examples import ArrayStack


class MinStack:
    """Exercise 1 (LeetCode 155): push, pop, top, and get_min, all O(1).

    A second stack remembers the minimum at every height.
    """

    def __init__(self) -> None:
        self._items = ArrayStack()
        self._mins = ArrayStack()

    def push(self, value: Any) -> None:
        self._items.push(value)
        self._mins.push(value if self._mins.is_empty() or value < self._mins.peek() else self._mins.peek())

    def pop(self) -> Any:
        self._mins.pop()
        return self._items.pop()

    def top(self) -> Any:
        return self._items.peek()

    def get_min(self) -> Any:
        return self._mins.peek()


def remove_adjacent_duplicates(text: str) -> str:
    """Exercise 2 (LeetCode 1047): 'abbaca' -> 'ca'. Each letter cancels an identical letter on top."""
    stack: list[str] = []
    for ch in text:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)


def simplify_path(path: str) -> str:
    """Exercise 3 (LeetCode 71): '/zoo/./animals/../lions/' -> '/zoo/lions'."""
    stack: list[str] = []
    for part in path.split("/"):
        if part == "..":
            if stack:
                stack.pop()
        elif part and part != ".":
            stack.append(part)
    return "/" + "/".join(stack)


def backspace_compare(a: str, b: str) -> bool:
    """Exercise 4 (LeetCode 844): '#' deletes the previous character. Are the typed results equal?"""
    def typed(text: str) -> str:
        stack: list[str] = []
        for ch in text:
            if ch == "#":
                if stack:
                    stack.pop()
            else:
                stack.append(ch)
        return "".join(stack)
    return typed(a) == typed(b)


def validate_pops(pushed: list[int], popped: list[int]) -> bool:
    """Exercise 5 (LeetCode 946): could `popped` be produced by pushing `pushed` in order?"""
    stack: list[int] = []
    i = 0
    for value in pushed:
        stack.append(value)
        while stack and i < len(popped) and stack[-1] == popped[i]:
            stack.pop()
            i += 1
    return i == len(popped)


if __name__ == "__main__":
    m = MinStack()
    for v in (5, 3, 7, 3):
        m.push(v)
    print(m.get_min(), m.pop(), m.get_min(), m.pop(), m.pop(), m.get_min())
    print(remove_adjacent_duplicates("abbaca"), simplify_path("/zoo/./animals/../lions/"))
    print(backspace_compare("ab#c", "ad#c"), validate_pops([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]))
