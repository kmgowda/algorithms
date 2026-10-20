"""Volume 1, Chapter 22 - Linked Lists.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations


class Node:
    """One link of the chain: a value and the next node (or None)."""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def to_list(head: Node | None) -> list:
    """Walk from the head to the end, collecting the values (Figure 22.6)."""
    values, current = [], head
    while current is not None:
        values.append(current.value)
        current = current.next
    return values


class LinkedList:
    """A singly linked list with the operations of Figures 22.3 to 22.5."""

    def __init__(self, values=()):
        self.head: Node | None = None
        for v in reversed(list(values)):
            self.push_front(v)

    def push_front(self, value) -> None:
        self.head = Node(value, self.head)        # link first, then move the head

    def find(self, value) -> Node | None:
        current = self.head
        while current is not None and current.value != value:
            current = current.next
        return current

    def insert_after(self, node: Node, value) -> None:
        node.next = Node(value, node.next)        # new.next = node.next; node.next = new

    def delete(self, value) -> bool:
        """Remove the first node holding value; True if one was removed."""
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            return True
        prev = self.head
        while prev.next is not None and prev.next.value != value:
            prev = prev.next
        if prev.next is None:
            return False
        prev.next = prev.next.next                # bypass (Figure 22.5)
        return True

    def values(self) -> list:
        return to_list(self.head)


class WaitingList:
    """Section 22.10: join at the end, serve from the front, cancel anyone - all O(1)."""

    def __init__(self):
        self.sentinel = Node(None)                # a dummy node before the first reader
        self.tail = self.sentinel
        self.before: dict[str, Node] = {}

    def join(self, name: str) -> None:
        self.before[name] = self.tail
        self.tail.next = Node(name)
        self.tail = self.tail.next

    def cancel(self, name: str) -> None:
        prev = self.before.pop(name)
        node = prev.next
        prev.next = node.next
        if node.next is not None:
            self.before[node.next.value] = prev
        else:
            self.tail = prev

    def serve(self) -> str:
        first = self.sentinel.next
        self.cancel(first.value)
        return first.value

    def names(self) -> list[str]:
        return to_list(self.sentinel.next)


if __name__ == "__main__":
    shelf = LinkedList([25, 47, 63])
    shelf.push_front(12)
    shelf.insert_after(shelf.find(47), 58)
    print(shelf.values())
    shelf.delete(47)
    print(shelf.values())
    w = WaitingList()
    for n in ("Ana", "Ben", "Cai"):
        w.join(n)
    w.cancel("Ben")
    print(w.names(), w.serve(), w.names())
    w.join("Dev")
    print(w.names())
