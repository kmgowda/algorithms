"""Volume 3, Chapter 12 - Designing Your Own Data Structure: Interfaces, Invariants, and Tests.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Any, Iterator, Protocol


# ------------------------------------------------------------------ step 1: write the interface first
class Inbox(Protocol):
    """The interface: anything with these methods can be used as an Inbox."""

    def add(self, message: str) -> None: ...
    def latest(self, k: int) -> list[str]: ...
    def __len__(self) -> int: ...


class BoundedHistory:
    """Design example 1: keep only the last `capacity` messages (a chat app's recent history).

    Interface: add, latest(k), len, iteration oldest -> newest.
    Invariant: len(self) <= capacity, and items are in arrival order.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._items: deque[str] = deque(maxlen=capacity)

    def add(self, message: str) -> None:
        self._items.append(message)

    def latest(self, k: int) -> list[str]:
        if k < 0:
            raise ValueError("k must be non-negative")
        return list(self._items)[-k:] if k else []

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[str]:
        return iter(self._items)

    def check_invariants(self) -> None:
        assert len(self._items) <= self.capacity


def show_latest(inbox: Inbox, k: int) -> str:
    """Code written against the Protocol works with ANY class that has the right methods."""
    return " | ".join(inbox.latest(k))


# ------------------------------------------------------------------ design example 2: a gap buffer for a text editor
class GapBuffer:
    """Industry example: text editors keep a 'gap' of empty slots at the cursor.

    Typing fills the gap (O(1)); moving the cursor by d characters moves d characters across the gap (O(d)).
    Invariants: 0 <= gap_start <= gap_end <= len(slots); text = slots[:gap_start] + slots[gap_end:].
    """

    def __init__(self, text: str = "", gap: int = 8) -> None:
        self._slots: list[str] = list(text) + [""] * gap
        self._gap_start = len(text)
        self._gap_end = len(self._slots)

    def __str__(self) -> str:
        return "".join(self._slots[:self._gap_start] + self._slots[self._gap_end:])

    def __len__(self) -> int:
        return len(self._slots) - (self._gap_end - self._gap_start)

    @property
    def cursor(self) -> int:
        return self._gap_start

    def _grow(self) -> None:
        extra = max(8, len(self._slots))
        self._slots[self._gap_end:self._gap_end] = [""] * extra
        self._gap_end += extra

    def insert(self, text: str) -> None:
        for ch in text:
            if self._gap_start == self._gap_end:
                self._grow()
            self._slots[self._gap_start] = ch
            self._gap_start += 1

    def delete_before(self, count: int = 1) -> None:
        """Backspace: just widen the gap to the left."""
        self._gap_start = max(0, self._gap_start - count)

    def move_cursor(self, position: int) -> None:
        position = max(0, min(position, len(self)))
        while self._gap_start > position:                  # move characters from before the gap to after it
            self._gap_start -= 1
            self._gap_end -= 1
            self._slots[self._gap_end] = self._slots[self._gap_start]
        while self._gap_start < position:                  # move characters from after the gap to before it
            self._slots[self._gap_start] = self._slots[self._gap_end]
            self._gap_start += 1
            self._gap_end += 1

    def check_invariants(self) -> None:
        assert 0 <= self._gap_start <= self._gap_end <= len(self._slots)


# ------------------------------------------------------------------ design example 3: a queue with O(1) max
class MaxQueue:
    """Practical example: a queue of order values that can always report its largest value in O(1) amortized.

    Combines a normal queue (for FIFO order) with a monotonic deque (Chapter 10, for the max).
    """

    def __init__(self) -> None:
        self._items: deque[Any] = deque()
        self._maxes: deque[Any] = deque()

    def enqueue(self, value: Any) -> None:
        self._items.append(value)
        while self._maxes and self._maxes[-1] < value:
            self._maxes.pop()
        self._maxes.append(value)

    def dequeue(self) -> Any:
        if not self._items:
            raise IndexError("dequeue from empty queue")
        value = self._items.popleft()
        if value == self._maxes[0]:
            self._maxes.popleft()
        return value

    def max(self) -> Any:
        if not self._items:
            raise IndexError("max of empty queue")
        return self._maxes[0]

    def __len__(self) -> int:
        return len(self._items)


if __name__ == "__main__":
    chat = BoundedHistory(3)
    for msg in ("hi", "lunch?", "zoo at 2", "bring snacks"):
        chat.add(msg)
    print(list(chat), show_latest(chat, 2))
    editor = GapBuffer("Hello zoo")
    editor.move_cursor(6)
    editor.insert("city ")
    editor.move_cursor(len(editor))
    editor.insert("!")
    editor.delete_before(1)
    editor.insert("!!")
    print(repr(str(editor)), "cursor at", editor.cursor)
    q = MaxQueue()
    for v in (3, 1, 4, 1, 5):
        q.enqueue(v)
    print(q.max(), q.dequeue(), q.dequeue(), q.dequeue(), q.max(), q.dequeue(), q.dequeue())
