"""Volume 1, Chapter 23 - Linked-List Techniques.

Run:  python3 ch23_examples.py
"""

from __future__ import annotations


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def build(values) -> Node | None:
    head = None
    for v in reversed(list(values)):
        head = Node(v, head)
    return head


def values_of(head, limit: int = 1000) -> list:
    out = []
    while head is not None and len(out) < limit:
        out.append(head.value)
        head = head.next
    return out


def reverse(head):
    """Turn every link around with prev, current and next (Figure 23.1); returns the new head."""
    prev, current = None, head
    while current is not None:
        nxt = current.next
        current.next = prev
        prev, current = current, nxt
    return prev


def reverse_recursive(head):
    """Section 23.4: reverse the rest by trusting the smaller call, then turn one link (O(n) stack depth)."""
    if head is None or head.next is None:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head                         # the old second node now points back at head
    head.next = None
    return new_head


def middle(head):
    """The middle node, in one pass: the hare moves two nodes for each one the tortoise moves (Figure 23.2)."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


def has_cycle(head) -> tuple[bool, int]:
    """Floyd's tortoise and hare (Figure 23.3). Returns (cycle found, steps taken)."""
    slow = fast = head
    steps = 0
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        steps += 1
        if slow is fast:
            return True, steps
    return False, steps


def loop_start(head):
    """Section 23.6: where the loop begins and how long it is, or None if there is no loop.
    Returns (start node, loop length, steps to meet, steps from the head to the start)."""
    slow = fast = head
    meet = 0
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        meet += 1
        if slow is fast:
            break
    else:
        return None
    a, b, to_start = head, slow, 0                # one pointer back to the head, one at the meeting node
    while a is not b:
        a, b = a.next, b.next
        to_start += 1
    length, cur = 1, a.next                       # walk once round the loop
    while cur is not a:
        cur, length = cur.next, length + 1
    return a, length, meet, to_start


def merge(a, b):
    """Merge two sorted lists by relinking nodes, using a dummy node (Figure 23.5)."""
    dummy = tail = Node(None)
    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def with_loop(values, back_to: int):
    """A list whose last node links back to position back_to (Figure 23.3)."""
    head = build(values)
    nodes, cur = [], head
    while cur is not None:
        nodes.append(cur)
        cur = cur.next
    nodes[-1].next = nodes[back_to]
    return head


if __name__ == "__main__":
    print(values_of(reverse(build([12, 25, 47, 63]))))
    print(middle(build([12, 25, 47, 58, 63, 70, 84])).value, middle(build(range(1, 7))).value)
    print(has_cycle(with_loop([12, 25, 47, 58, 63, 70, 84, 91], 3)), has_cycle(build(range(8))))
    print(values_of(merge(build([12, 47, 63]), build([25, 58, 84, 91]))))
    print(has_cycle(with_loop(list(range(7)), 3)))
    node, length, meet, to_start = loop_start(with_loop([12, 25, 47, 58, 63, 70, 84, 91], 3))
    print(node.value, length, meet, to_start)
    node, length, meet, to_start = loop_start(with_loop([12, 25, 31, 47, 58], 1))
    print(node.value, length, meet, to_start)
    print(values_of(reverse_recursive(build([12, 25, 47, 63]))))
