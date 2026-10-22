"""Volume 3, Chapter 14 - Binary Heaps.

Run:  python3 ch14_examples.py
"""

from __future__ import annotations


class MinHeap:
    """A complete binary tree in an array; every parent is no larger than its children (Figure 14.1)."""

    def __init__(self, items=()):
        self.a: list = []
        self.trace: list[list] = []          # array snapshots after each swap, for the figures
        for x in items:
            self.push(x)

    def push(self, x) -> None:
        """Add at the end, then sift up while smaller than the parent (Figure 14.2)."""
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0 and a[i] < a[(i - 1) // 2]:
            p = (i - 1) // 2
            a[i], a[p] = a[p], a[i]
            self.trace.append(list(a))
            i = p

    def pop(self):
        """Take the root, move the last item to the top, then sift down (Figure 14.3)."""
        a = self.a
        top = a[0]
        last = a.pop()
        if a:
            a[0] = last
            i = 0
            while True:
                small, l, r = i, 2 * i + 1, 2 * i + 2
                if l < len(a) and a[l] < a[small]:
                    small = l
                if r < len(a) and a[r] < a[small]:
                    small = r
                if small == i:
                    break
                a[i], a[small] = a[small], a[i]
                self.trace.append(list(a))
                i = small
        return top

    def peek(self):
        return self.a[0]

    def __len__(self) -> int:
        return len(self.a)


def is_heap(a: list) -> bool:
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))


if __name__ == "__main__":
    h = MinHeap([25, 47, 12, 63, 31, 58, 70])
    print("built", h.a)
    h.trace.clear()
    h.push(9)
    print("push 9", h.trace)
    h.trace.clear()
    print("pop", h.pop(), h.trace, h.a)
    print([MinHeap([5, 3, 8, 1, 9, 2]).pop() for _ in range(1)])
