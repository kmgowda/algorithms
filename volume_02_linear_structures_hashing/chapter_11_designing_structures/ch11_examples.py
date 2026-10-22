"""Volume 2, Chapter 11 - Designing Your Own Data Structure.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations


class MinStack:
    """A stack whose every item carries the minimum at or below it (Figure 11.1)."""

    def __init__(self):
        self._items: list[tuple[int, int]] = []          # (value, minimum at or below)

    def push(self, value: int) -> None:
        low = value if not self._items else min(value, self._items[-1][1])
        self._items.append((value, low))

    def pop(self) -> int:
        return self._items.pop()[0]

    def top(self) -> int:
        return self._items[-1][0]

    def min(self) -> int:
        return self._items[-1][1]

    def __len__(self) -> int:
        return len(self._items)


class BrowserHistory:
    """Back and forward with two stacks and a current page (Figure 11.2)."""

    def __init__(self, home: str):
        self.current = home
        self._back: list[str] = []
        self._forward: list[str] = []

    def visit(self, page: str) -> None:
        self._back.append(self.current)
        self.current = page
        self._forward.clear()

    def back(self) -> str:
        if self._back:
            self._forward.append(self.current)
            self.current = self._back.pop()
        return self.current

    def forward(self) -> str:
        if self._forward:
            self._back.append(self.current)
            self.current = self._forward.pop()
        return self.current


class MinQueue:
    """Exercise 4's elegant answer: a queue built from two min-stacks, min in O(1) amortized."""

    def __init__(self):
        self._in, self._out = MinStack(), MinStack()

    def enqueue(self, v: int) -> None:
        self._in.push(v)

    def dequeue(self) -> int:
        if not len(self._out):
            while len(self._in):
                self._out.push(self._in.pop())
        return self._out.pop()

    def min(self) -> int:
        candidates = [s.min() for s in (self._in, self._out) if len(s)]
        return min(candidates)


if __name__ == "__main__":
    s = MinStack()
    for b in (47, 63, 12, 25):
        s.push(b)
        print("push", b, "min", s.min())
    s.pop(); print("min", s.min()); s.pop(); print("min", s.min())
    h = BrowserHistory("A")
    h.visit("B"); h.back(); h.visit("C"); h.back(); print(h.forward())
