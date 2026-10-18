"""Volume 5, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

from typing import Any

from ch05_examples import merge


def merge_into_first(first: list[int], m: int, second: list[int]) -> None:
    """Exercise 1 (LeetCode 88): first has m real items followed by len(second) spare slots.
    Fill from the BACK so nothing is overwritten. O(m + n), no extra list."""
    i, j, write = m - 1, len(second) - 1, m + len(second) - 1
    while j >= 0:
        if i >= 0 and first[i] > second[j]:
            first[write] = first[i]
            i -= 1
        else:
            first[write] = second[j]
            j -= 1
        write -= 1


def merge_k_sorted(lists: list[list[Any]]) -> list[Any]:
    """Exercise 2 (LeetCode 23 idea): merge lists in pairs, like a tournament. O(N log k) for N items."""
    if not lists:
        return []
    while len(lists) > 1:
        lists = [merge(lists[i], lists[i + 1]) if i + 1 < len(lists) else lists[i] for i in range(0, len(lists), 2)]
    return lists[0]


class Node:
    def __init__(self, value: Any, next_node: "Node | None" = None) -> None:
        self.value, self.next = value, next_node


def sort_linked_list(head: Node | None) -> Node | None:
    """Exercise 3 (LeetCode 148): merge sort a linked list - split with fast/slow pointers, merge by re-linking."""
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next          # type: ignore[assignment]
    second, slow.next = slow.next, None
    a, b = sort_linked_list(head), sort_linked_list(second)
    dummy = tail = Node(None)
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


if __name__ == "__main__":
    f = [1, 4, 7, 0, 0]
    merge_into_first(f, 3, [2, 9])
    print(f, merge_k_sorted([[1, 5], [2, 6], [0, 9], [3]]))
    head = Node(4, Node(2, Node(1, Node(3))))
    node, out = sort_linked_list(head), []
    while node:
        out.append(node.value)
        node = node.next
    print(out)
