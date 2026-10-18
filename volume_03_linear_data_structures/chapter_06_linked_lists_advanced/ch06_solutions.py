"""Volume 3, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from ch06_examples import Node, middle


def kth_from_end(head: Node | None, k: int) -> Node | None:
    """Exercise 1 (LeetCode 19 idea): move a 'lead' pointer k steps ahead, then move both."""
    lead = head
    for _ in range(k):
        if lead is None:
            return None
        lead = lead.next
    trail = head
    while lead is not None:
        assert trail is not None
        lead, trail = lead.next, trail.next
    return trail


def is_palindrome_list(head: Node | None) -> bool:
    """Exercise 2 (LeetCode 234): find the middle, reverse the second half, compare. O(1) extra space."""
    mid = middle(head)
    previous = None
    while mid is not None:                      # reverse from the middle onward
        mid.next, previous, mid = previous, mid, mid.next
    left, right = head, previous
    while right is not None:
        assert left is not None
        if left.value != right.value:
            return False
        left, right = left.next, right.next
    return True


def josephus(people: int, step: int) -> int:
    """Exercise 3: people in a circle; every `step`-th person leaves. Who remains? (positions 1..n)."""
    nodes = [Node(i + 1) for i in range(people)]
    for i, node in enumerate(nodes):
        node.next = nodes[(i + 1) % people]
    previous = nodes[-1]
    current = nodes[0]
    while current.next is not current:
        for _ in range(step - 1):
            previous, current = current, current.next      # type: ignore[assignment]
        previous.next = current.next                       # current leaves the circle
        current = current.next                             # type: ignore[assignment]
    return current.value


def cycle_length(head: Node | None) -> int:
    """Exercise 4: once the pointers meet, walk around the loop once and count."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        assert slow is not None
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            length, node = 1, slow.next
            while node is not slow:
                assert node is not None
                length, node = length + 1, node.next
            return length
    return 0


if __name__ == "__main__":
    from ch06_examples import build
    print(kth_from_end(build([1, 2, 3, 4, 5]), 2).value, is_palindrome_list(build([1, 2, 2, 1])))  # type: ignore[union-attr]
    print(josephus(7, 3))
