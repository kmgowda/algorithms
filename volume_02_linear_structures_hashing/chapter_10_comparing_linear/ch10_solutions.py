"""Volume 2, Chapter 10 - Thinking Problems.

Problem 1: the fewest moves to insert at position k of a ring-buffer deque, min(k, n - k).
Problem 2: a gap buffer for the text editor: typing and deleting at the cursor in O(1) amortized,
moving the cursor d places in O(d).
"""

from __future__ import annotations


def ring_insert_moves(n: int, k: int) -> int:
    """Shift the shorter side: the k items before position k back one cell, or the n - k after it forward."""
    return min(k, n - k)


class GapBuffer:
    """The text lives at both ends of one array; the free cells (the gap) sit at the cursor."""

    def __init__(self, capacity: int = 8):
        self.buf: list = [None] * capacity
        self.gap_start, self.gap_end = 0, capacity     # free cells are buf[gap_start:gap_end]

    def insert(self, ch: str) -> None:
        if self.gap_start == self.gap_end:
            self._grow()
        self.buf[self.gap_start] = ch
        self.gap_start += 1

    def delete(self) -> str | None:
        """Backspace: remove the character before the cursor."""
        if self.gap_start == 0:
            return None
        self.gap_start -= 1
        return self.buf[self.gap_start]

    def move_to(self, pos: int) -> None:
        pos = max(0, min(pos, len(self)))
        while self.gap_start > pos:                    # one character hops from before the gap to after it
            self.gap_start -= 1
            self.gap_end -= 1
            self.buf[self.gap_end] = self.buf[self.gap_start]
        while self.gap_start < pos:
            self.buf[self.gap_start] = self.buf[self.gap_end]
            self.gap_start += 1
            self.gap_end += 1

    def _grow(self) -> None:
        old, tail = self.buf, len(self.buf) - self.gap_end
        self.buf = [None] * max(1, 2 * len(old))
        self.buf[:self.gap_start] = old[:self.gap_start]
        self.buf[len(self.buf) - tail:] = old[self.gap_end:]
        self.gap_end = len(self.buf) - tail

    def __len__(self) -> int:
        return len(self.buf) - (self.gap_end - self.gap_start)

    def text(self) -> str:
        return "".join(self.buf[:self.gap_start] + self.buf[self.gap_end:])


if __name__ == "__main__":
    g = GapBuffer(4)
    for ch in "SHELF":
        g.insert(ch)
    g.move_to(0)
    g.insert("A")
    g.insert(" ")
    print(g.text(), g.gap_start, len(g), ring_insert_moves(9, 4))
