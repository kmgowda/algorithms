"""Volume 3, Chapter 5 - Linked Lists I: Nodes and Pointers.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

from typing import Any, Iterator


class Node:
    """One clue in the treasure hunt: a value plus a pointer to the next node (or None)."""

    def __init__(self, value: Any, next_node: "Node | None" = None) -> None:
        self.value = value
        self.next = next_node


class LinkedList:
    """A singly linked list. Invariants: `_size` equals the number of reachable nodes;
    `_tail` is the last node (None when empty)."""

    def __init__(self, values: list[Any] | None = None) -> None:
        self._head: Node | None = None
        self._tail: Node | None = None
        self._size = 0
        for value in values or []:
            self.append(value)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        node = self._head
        while node is not None:                 # follow the pointers until the end
            yield node.value
            node = node.next

    def __repr__(self) -> str:
        return " -> ".join(repr(v) for v in self) + " -> None" if self._size else "None"

    # -------------------------------------------------- O(1) operations at the ends
    def push_front(self, value: Any) -> None:
        self._head = Node(value, self._head)
        if self._tail is None:
            self._tail = self._head
        self._size += 1

    def append(self, value: Any) -> None:
        node = Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def pop_front(self) -> Any:
        if self._head is None:
            raise IndexError("pop from empty list")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value

    # -------------------------------------------------- O(n) operations that must walk
    def _node_at(self, index: int) -> Node:
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        node = self._head
        for _ in range(index):
            assert node is not None
            node = node.next
        assert node is not None
        return node

    def __getitem__(self, index: int) -> Any:
        return self._node_at(index).value

    def find(self, value: Any) -> int:
        for index, item in enumerate(self):
            if item == value:
                return index
        return -1

    def insert_after(self, index: int, value: Any) -> None:
        """Walking to `index` is O(index); the insertion itself is O(1)."""
        node = self._node_at(index)
        node.next = Node(value, node.next)
        if node is self._tail:
            self._tail = node.next
        self._size += 1

    def remove(self, value: Any) -> bool:
        """Remove the first node holding value. Needs the node BEFORE it, so walk with two pointers."""
        previous, node = None, self._head
        while node is not None and node.value != value:
            previous, node = node, node.next
        if node is None:
            return False
        if previous is None:
            self._head = node.next
        else:
            previous.next = node.next
        if node is self._tail:
            self._tail = previous
        self._size -= 1
        return True

    def reverse(self) -> None:
        """Reverse in place by turning every arrow around. O(n) time, O(1) extra space."""
        previous, node = None, self._head
        self._tail = self._head
        while node is not None:
            following = node.next
            node.next = previous
            previous, node = node, following
        self._head = previous


# ------------------------------------------------------------------ examples
def treasure_hunt(clues: list[str]) -> list[str]:
    """Beginner example: each clue only knows where the next one is."""
    hunt = LinkedList(clues)
    return [f"step {i + 1}: {clue}" for i, clue in enumerate(hunt)]


def train_after_coupling(cars: list[str], new_engine: str, dining_after: str) -> list[str]:
    """Practical example: couple an engine at the front and a dining car after a given car."""
    train = LinkedList(cars)
    train.push_front(new_engine)
    train.insert_after(train.find(dining_after), "Dining car")
    return list(train)


def browser_tabs_closed(tabs: list[str], closed: list[str]) -> list[str]:
    """Industry example: closing tabs unlinks nodes; nothing has to shift."""
    tab_list = LinkedList(tabs)
    for tab in closed:
        tab_list.remove(tab)
    return list(tab_list)


if __name__ == "__main__":
    print("\n".join(treasure_hunt(["under the oak", "behind the fountain", "inside the library", "TREASURE"])))
    stops = LinkedList(["Depot", "Library", "Market"])
    stops.append("School")
    stops.push_front("Garage")
    print(stops, "| length", len(stops), "| stops[2] =", stops[2])
    print(train_after_coupling(["Car 1", "Car 2", "Car 3"], "Engine", "Car 2"))
    print(browser_tabs_closed(["Mail", "News", "Maps", "Music"], ["News", "Music"]))
    stops.reverse()
    print("Reversed:", stops)
