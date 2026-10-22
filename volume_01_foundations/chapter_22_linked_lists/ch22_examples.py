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


class DNode:
    """A node of a doubly linked list: a value and links to both neighbours."""

    def __init__(self, value, prev=None, next=None):
        self.value, self.prev, self.next = value, prev, next


class DoublyLinkedList:
    """Section 22.10: header and trailer sentinels make every insert and delete the same four or two link changes."""

    def __init__(self, values=()):
        self.header, self.trailer = DNode(None), DNode(None)
        self.header.next, self.trailer.prev = self.trailer, self.header
        self.size = 0
        for v in values:
            self.push_back(v)

    def insert_between(self, value, before: DNode, after: DNode) -> DNode:
        new = DNode(value, before, after)         # changes 1 and 2: the new node's own links
        before.next = new                         # change 3
        after.prev = new                          # change 4
        self.size += 1
        return new

    def remove(self, node: DNode):
        node.prev.next = node.next                # the neighbours link past the node
        node.next.prev = node.prev
        self.size -= 1
        return node.value

    def push_front(self, value) -> DNode:
        return self.insert_between(value, self.header, self.header.next)

    def push_back(self, value) -> DNode:
        return self.insert_between(value, self.trailer.prev, self.trailer)

    def pop_front(self):
        if self.size == 0:
            raise IndexError("pop from an empty list")
        return self.remove(self.header.next)

    def pop_back(self):
        if self.size == 0:
            raise IndexError("pop from an empty list")
        return self.remove(self.trailer.prev)     # O(1): the trailer knows the last node

    def find(self, value) -> DNode | None:
        node = self.header.next
        while node is not self.trailer:
            if node.value == value:
                return node
            node = node.next
        return None

    def values(self) -> list:
        out, node = [], self.header.next
        while node is not self.trailer:
            out.append(node.value)
            node = node.next
        return out

    def values_backward(self) -> list:
        out, node = [], self.trailer.prev
        while node is not self.header:
            out.append(node.value)
            node = node.prev
        return out


class WaitingList:
    """Section 22.11: join at the end, serve from the front, cancel anyone - all O(1)."""

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
    d = DoublyLinkedList([25, 47, 63])
    d.insert_between(58, d.find(47), d.find(63))
    d.remove(d.find(47))
    print(d.values(), d.values_backward(), d.pop_back())
