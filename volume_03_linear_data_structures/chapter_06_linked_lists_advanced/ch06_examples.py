"""Volume 3, Chapter 6 - Linked Lists II: Doubly Linked, Circular, Sentinels, Fast and Slow Pointers.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

from typing import Any, Iterator


# ------------------------------------------------------------------ doubly linked list with sentinels
class DNode:
    def __init__(self, value: Any = None) -> None:
        self.value = value
        self.prev: DNode | None = None
        self.next: DNode | None = None


class DoublyLinkedList:
    """Two permanent sentinel nodes (front and back) mean there is never an 'empty list' special case.

    Invariant: front <-> item1 <-> ... <-> itemN <-> back, and every prev/next pair agrees.
    """

    def __init__(self, values: list[Any] | None = None) -> None:
        self._front, self._back = DNode(), DNode()
        self._front.next, self._back.prev = self._back, self._front
        self._size = 0
        for value in values or []:
            self.push_back(value)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        node = self._front.next
        while node is not self._back:
            assert node is not None
            yield node.value
            node = node.next

    def backwards(self) -> Iterator[Any]:
        node = self._back.prev
        while node is not self._front:
            assert node is not None
            yield node.value
            node = node.prev

    def _insert_between(self, value: Any, before: DNode, after: DNode) -> DNode:
        node = DNode(value)
        node.prev, node.next = before, after
        before.next = node
        after.prev = node
        self._size += 1
        return node

    def push_front(self, value: Any) -> DNode:
        assert self._front.next is not None
        return self._insert_between(value, self._front, self._front.next)

    def push_back(self, value: Any) -> DNode:
        assert self._back.prev is not None
        return self._insert_between(value, self._back.prev, self._back)

    def unlink(self, node: DNode) -> Any:
        """Remove a node we already hold, in O(1) - the big win over singly linked lists."""
        if node is self._front or node is self._back:
            raise ValueError("cannot remove a sentinel")
        assert node.prev is not None and node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None
        self._size -= 1
        return node.value

    def pop_front(self) -> Any:
        if not self._size:
            raise IndexError("pop from empty list")
        assert self._front.next is not None
        return self.unlink(self._front.next)

    def pop_back(self) -> Any:
        if not self._size:
            raise IndexError("pop from empty list")
        assert self._back.prev is not None
        return self.unlink(self._back.prev)


class MusicPlayer:
    """Industry example: previous/next buttons and 'remove this song' are all O(1)."""

    def __init__(self, songs: list[str]) -> None:
        self.playlist = DoublyLinkedList()
        self._nodes = [self.playlist.push_back(song) for song in songs]
        self.current: DNode | None = self._nodes[0] if self._nodes else None

    def now_playing(self) -> str | None:
        return None if self.current is None else self.current.value

    def next(self) -> str | None:
        if self.current is not None and self.current.next is not self.playlist._back:
            self.current = self.current.next
        return self.now_playing()

    def previous(self) -> str | None:
        if self.current is not None and self.current.prev is not self.playlist._front:
            self.current = self.current.prev
        return self.now_playing()

    def remove_current(self) -> str | None:
        if self.current is None:
            return None
        doomed = self.current
        self.current = doomed.next if doomed.next is not self.playlist._back else doomed.prev
        if self.current is self.playlist._front:
            self.current = None
        self.playlist.unlink(doomed)
        return self.now_playing()


# ------------------------------------------------------------------ circular list: round robin
def round_robin(players: list[str], turns: int) -> list[str]:
    """Practical example: a board game's turns go around a circle forever."""
    if not players:
        return []
    nodes = [DNode(name) for name in players]
    for i, node in enumerate(nodes):
        node.next = nodes[(i + 1) % len(nodes)]     # the last points back to the first
    order, node = [], nodes[0]
    for _ in range(turns):
        order.append(node.value)
        assert node.next is not None
        node = node.next
    return order


# ------------------------------------------------------------------ fast and slow pointers (singly linked)
class Node:
    def __init__(self, value: Any, next_node: "Node | None" = None) -> None:
        self.value = value
        self.next = next_node


def build(values: list[Any]) -> Node | None:
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def middle(head: Node | None) -> Node | None:
    """The slow pointer moves 1 step, the fast moves 2: when fast reaches the end, slow is in the middle."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        assert slow is not None
        slow, fast = slow.next, fast.next.next
    return slow


def has_cycle(head: Node | None) -> bool:
    """Floyd's tortoise and hare: in a loop, the fast pointer eventually laps the slow one."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        assert slow is not None
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False


def cycle_start(head: Node | None) -> Node | None:
    """Where does the loop begin? After they meet, restart one pointer at the head; move both 1 step."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        assert slow is not None
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            finder = head
            while finder is not slow:
                assert finder is not None and slow is not None
                finder, slow = finder.next, slow.next
            return finder
    return None


def redirect_loop(redirects: dict[str, str], start: str) -> str | None:
    """Industry example: web page A redirects to B, B to C, ... Does it loop forever? Return the loop's first page."""
    nodes: dict[str, Node] = {}
    for page in set(redirects) | set(redirects.values()) | {start}:
        nodes[page] = Node(page)
    for page, target in redirects.items():
        nodes[page].next = nodes[target]
    found = cycle_start(nodes[start])
    return None if found is None else found.value


if __name__ == "__main__":
    dll = DoublyLinkedList(["Atlas", "Birds", "Cats"])
    dll.push_front("Aesop")
    print(list(dll), list(dll.backwards()), dll.pop_back(), dll.pop_front(), list(dll))
    player = MusicPlayer(["Song A", "Song B", "Song C"])
    print(player.next(), player.next(), player.next(), player.previous(), player.remove_current(), list(player.playlist))
    print(round_robin(["Ana", "Ben", "Cy"], 7))
    print("Middle of 1..5:", middle(build([1, 2, 3, 4, 5])).value)       # type: ignore[union-attr]
    loop = build([1, 2, 3, 4, 5])
    tail = loop
    while tail.next:                                                       # type: ignore[union-attr]
        tail = tail.next                                                   # type: ignore[union-attr]
    tail.next = loop.next.next                                             # type: ignore[union-attr]  # 5 -> 3
    print("Has cycle:", has_cycle(loop), "| starts at", cycle_start(loop).value)   # type: ignore[union-attr]
    print("Redirect loop:", redirect_loop({"/a": "/b", "/b": "/c", "/c": "/d", "/d": "/b"}, "/a"))
