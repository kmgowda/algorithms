"""Volume 3, Chapter 5 - Solutions to the exercises (plain Node chains, LeetCode style)."""

from __future__ import annotations

from typing import Any

from ch05_examples import Node


def build(values: list[Any]) -> Node | None:
    """Helper: make a chain of nodes from a list."""
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def to_list(head: Node | None) -> list[Any]:
    out = []
    while head is not None:
        out.append(head.value)
        head = head.next
    return out


def count_nodes_recursive(head: Node | None) -> int:
    """Exercise 1: length = 1 + length of the rest (V2-C7)."""
    return 0 if head is None else 1 + count_nodes_recursive(head.next)


def sum_values(head: Node | None) -> int:
    """Exercise 2."""
    total = 0
    while head is not None:
        total += head.value
        head = head.next
    return total


def reverse_chain(head: Node | None) -> Node | None:
    """Exercise 3 (LeetCode 206): reverse a chain and return the new head."""
    previous = None
    while head is not None:
        head.next, previous, head = previous, head, head.next
    return previous


def merge_sorted(a: Node | None, b: Node | None) -> Node | None:
    """Exercise 4 (LeetCode 21): merge two sorted chains by re-linking nodes (no new nodes)."""
    dummy = Node(None)            # a placeholder in front makes the first step like all others
    tail = dummy
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def remove_duplicates_sorted(head: Node | None) -> Node | None:
    """Exercise 5 (LeetCode 83): a sorted chain keeps one node per value."""
    node = head
    while node is not None and node.next is not None:
        if node.next.value == node.value:
            node.next = node.next.next
        else:
            node = node.next
    return head


if __name__ == "__main__":
    chain = build([3, 1, 4])
    print(count_nodes_recursive(chain), sum_values(chain), to_list(reverse_chain(build([1, 2, 3]))))
    print(to_list(merge_sorted(build([1, 4, 9]), build([2, 3, 10]))), to_list(remove_duplicates_sorted(build([1, 1, 2, 3, 3]))))
