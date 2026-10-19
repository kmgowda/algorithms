"""Volume 16, Chapter 5 - Linked Lists, Stacks, and Queues: Interview Drill.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations


class ListNode:
    def __init__(self, val: int, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next


def build(values: list[int]) -> ListNode | None:
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head: ListNode | None) -> list[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reverse_list(head: ListNode | None) -> ListNode | None:
    """LeetCode 206: walk once, turning each arrow around. Keep three names: prev, current, next."""
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


def merge_two(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    """LeetCode 21: a dummy head removes the 'is the result empty?' special case."""
    dummy = tail = ListNode(0)
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def has_cycle(head: ListNode | None) -> bool:
    """LeetCode 141: Floyd's tortoise and hare (V3-C6) - a fast pointer laps a slow one inside any cycle."""
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    """LeetCode 19: move a lead pointer n steps ahead, then move both; when the lead ends, the trailer is
    just before the node to delete."""
    dummy = ListNode(0, head)
    lead = trail = dummy
    for _ in range(n):
        lead = lead.next                                        # type: ignore[assignment]
    while lead.next:
        lead, trail = lead.next, trail.next                    # type: ignore[assignment]
    trail.next = trail.next.next                                # type: ignore[union-attr]
    return dummy.next


def valid_brackets(s: str) -> bool:
    """LeetCode 20: push openers; every closer must match the most recent opener."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack


def daily_temperatures(temps: list[int]) -> list[int]:
    """LeetCode 739: days to wait for a warmer day - a monotonic stack of unresolved days (V3-C8)."""
    wait = [0] * len(temps)
    stack: list[int] = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            wait[j] = i - j
        stack.append(i)
    return wait


def undo_editor(ops: list[str]) -> str:
    """Industry example: a text editor's undo is a stack of previous states."""
    text, history = "", []
    for op in ops:
        if op == "UNDO":
            text = history.pop() if history else text
        else:
            history.append(text)
            text += op
    return text


if __name__ == "__main__":
    print(to_list(reverse_list(build([1, 2, 3, 4, 5]))), to_list(merge_two(build([1, 2, 4]), build([1, 3, 4]))))
    loop = build([3, 2, 0, -4])
    loop.next.next.next.next = loop.next                        # type: ignore[union-attr]
    print(has_cycle(loop), has_cycle(build([1, 2])), to_list(remove_nth_from_end(build([1, 2, 3, 4, 5]), 2)))
    print(valid_brackets("()[]{}"), valid_brackets("(]"), daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
    print(repr(undo_editor(["Hel", "lo", " wrld", "UNDO", " world"])))
