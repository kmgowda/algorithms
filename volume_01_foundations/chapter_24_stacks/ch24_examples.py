"""Volume 1, Chapter 24 - Stacks.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations


class Stack:
    """Last in, first out, kept in a Python list with the top at the end (Figure 24.3)."""

    def __init__(self):
        self._items = []

    def push(self, item) -> None:
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items


class _Node:
    def __init__(self, value, next=None):
        self.value, self.next = value, next


class LinkedStack:
    """The same promise with the top at the head of a linked chain (Figure 24.4)."""

    def __init__(self):
        self._top = None

    def push(self, item) -> None:
        self._top = _Node(item, self._top)

    def pop(self):
        if self._top is None:
            raise IndexError("pop from an empty stack")
        node, self._top = self._top, self._top.next
        return node.value

    def peek(self):
        if self._top is None:
            raise IndexError("peek at an empty stack")
        return self._top.value

    def is_empty(self) -> bool:
        return self._top is None


class BoundedStack:
    """A stack in a fixed array of `capacity` slots (Section 24.5): push on a full stack is an overflow."""

    def __init__(self, capacity: int):
        self._slots = [None] * capacity
        self._size = 0                            # slots[0 .. size-1] hold the items; the top is slots[size-1]

    def push(self, item) -> None:
        if self._size == len(self._slots):
            raise OverflowError("push onto a full stack")
        self._slots[self._size] = item
        self._size += 1

    def pop(self):
        if self._size == 0:
            raise IndexError("pop from an empty stack")
        self._size -= 1
        item, self._slots[self._size] = self._slots[self._size], None
        return item

    def is_empty(self) -> bool:
        return self._size == 0


def sort_with_stacks(returns: list[int]) -> list[int]:
    """Section 24.7: load a trolley (a stack) so books come off smallest first, using one spare stack.
    `returns` lists the pile bottom to top. Returns the order books come off the trolley."""
    pile, trolley, spare = Stack(), Stack(), Stack()
    for b in returns:
        pile.push(b)
    while not pile.is_empty():
        book = pile.pop()
        while not trolley.is_empty() and trolley.peek() < book:
            spare.push(trolley.pop())
        trolley.push(book)
        while not spare.is_empty():
            trolley.push(spare.pop())
    out = []
    while not trolley.is_empty():
        out.append(trolley.pop())
    return out


def reverse_word(word: str) -> str:
    s = Stack()
    for ch in word:
        s.push(ch)
    return "".join(s.pop() for _ in range(len(word)))


if __name__ == "__main__":
    s = Stack()
    for b in (47, 12, 63):
        s.push(b)
    print(s.pop(), end=" ")
    s.push(25)
    print(s.pop(), s.peek())
    print(sort_with_stacks([47, 12, 63, 25, 84]), sort_with_stacks([3, 1, 2]), reverse_word("STACK"))
