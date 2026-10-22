"""Volume 2, Chapter 4 - Thinking Problems.

Problem 1: the forward and backward walks of a sentinel list mirror each other (checked in the tests).
Problem 2: splice a run of nodes from one doubly linked list into another in O(1).
Problem 3: "delete without the predecessor" by copying the next value, kept here so the tests can show it fails.
"""

from __future__ import annotations

from ch04_examples import DNode, DoublyLinkedList, LinkedList, Node


def splice(first: DNode, last: DNode, after: DNode) -> None:
    """Move the run first ... last to just after node `after` (not inside the run): six link changes, O(1)."""
    before, beyond = first.prev, last.next
    before.next, beyond.prev = beyond, before          # close the gap the run leaves
    nxt = after.next
    after.next, first.prev = first, after              # hook the run in after `after`
    last.next, nxt.prev = nxt, last


def delete_by_copy(node: Node) -> None:
    """WRONG in general: overwrite node with its successor's value and unlink the successor."""
    if node.next is None:
        raise ValueError("the tail has no successor to copy")
    node.value = node.next.value
    node.next = node.next.next


if __name__ == "__main__":
    a, b = DoublyLinkedList(["Ana", "Ben", "Cai", "Dev"]), DoublyLinkedList(["Eve", "Fay"])
    splice(a.find("Ben"), a.find("Cai"), b.find("Eve"))
    print(a.values(), a.values_backward(), b.values(), b.values_backward())
    shelf = LinkedList([12, 25, 47, 63])
    held = shelf.find(47)
    delete_by_copy(shelf.find(25))
    shelf.insert_after(held, 50)
    print(shelf.values(), held.value)
