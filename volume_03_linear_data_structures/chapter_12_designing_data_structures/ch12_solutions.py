"""Volume 3, Chapter 12 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque
from typing import Any


class UniqueQueue:
    """Exercise 1: a queue that ignores items already waiting (e.g. a crawler's 'pages to visit')."""

    def __init__(self) -> None:
        self._order: deque[Any] = deque()
        self._waiting: set[Any] = set()

    def enqueue(self, item: Any) -> bool:
        if item in self._waiting:
            return False
        self._order.append(item)
        self._waiting.add(item)
        return True

    def dequeue(self) -> Any:
        item = self._order.popleft()
        self._waiting.remove(item)
        return item

    def __len__(self) -> int:
        return len(self._order)

    def check_invariants(self) -> None:
        assert len(self._order) == len(self._waiting) == len(set(self._order))


class CircularPlaylist:
    """Exercise 2: next() loops forever; remove(song) works anywhere."""

    def __init__(self, songs: list[str]) -> None:
        self._songs = list(songs)
        self._position = 0

    def next(self) -> str:
        if not self._songs:
            raise IndexError("empty playlist")
        song = self._songs[self._position]
        self._position = (self._position + 1) % len(self._songs)
        return song

    def remove(self, song: str) -> None:
        index = self._songs.index(song)
        self._songs.pop(index)
        if index < self._position:
            self._position -= 1
        if self._songs:
            self._position %= len(self._songs)
        else:
            self._position = 0


class SnapshotCounter:
    """Exercise 3: a counter you can snapshot and roll back (an undo stack of values)."""

    def __init__(self) -> None:
        self.value = 0
        self._snapshots: list[int] = []

    def add(self, amount: int) -> None:
        self.value += amount

    def snapshot(self) -> int:
        self._snapshots.append(self.value)
        return len(self._snapshots) - 1

    def rollback(self) -> None:
        if not self._snapshots:
            raise IndexError("no snapshot to roll back to")
        self.value = self._snapshots.pop()


if __name__ == "__main__":
    q = UniqueQueue()
    print([q.enqueue(u) for u in ("/home", "/zoo", "/home")], q.dequeue(), len(q))
    p = CircularPlaylist(["A", "B", "C"])
    print([p.next() for _ in range(4)])
    p.remove("C")
    print([p.next() for _ in range(3)])
    c = SnapshotCounter()
    c.add(5)
    c.snapshot()
    c.add(10)
    c.rollback()
    print(c.value)
