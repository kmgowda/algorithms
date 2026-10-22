"""Volume 2, Chapter 5 - Thinking Problems.

Problem 1: a hare three nodes per step still meets the tortoise on every loop (first meeting step computed here).
Problem 2: does the train read the same both ways? O(n) time, O(1) extra space, and the train is put back.
Problem 3: the speed-3 hare with the unchanged phase 2, which can walk round the loop forever.
"""

from __future__ import annotations

from ch05_examples import reverse


def first_meeting(head, speed: int = 2, limit: int = 10_000) -> int | None:
    """Steps until a tortoise (1 per step) and a hare (speed per step) first share a node; None if the hare ends."""
    slow = fast = head
    for step in range(1, limit + 1):
        for _ in range(speed):
            if fast is None:
                return None
            fast = fast.next
        if fast is None:
            return None
        slow = slow.next
        if slow is fast:
            return step
    return None


def is_palindrome_train(head) -> bool:
    """True if the values read the same both ways; reverses the second half, compares, then restores it."""
    if head is None:
        return True
    slow = fast = head
    while fast.next is not None and fast.next.next is not None:
        slow, fast = slow.next, fast.next.next            # slow stops at the end of the first half
    second = reverse(slow.next)
    a, b, answer = head, second, True
    while b is not None:
        if a.value != b.value:
            answer = False
            break
        a, b = a.next, b.next
    slow.next = reverse(second)                            # put the train back as it was
    return answer


def loop_start_speed3(head, limit: int = 1000):
    """WRONG: meets with a speed-3 hare, then runs the usual phase 2. Returns the start, or None after limit steps."""
    d = first_meeting(head, speed=3)
    if d is None:
        return None
    meet = head
    for _ in range(d):
        meet = meet.next
    a, b = head, meet
    for _ in range(limit):
        if a is b:
            return a
        a, b = a.next, b.next
    return None


if __name__ == "__main__":
    from ch05_examples import build, values_of, with_loop
    train = with_loop([12, 25, 31, 47, 58], 1)
    print(first_meeting(train), first_meeting(train, 3), loop_start_speed3(train))
    t = build([12, 25, 47, 25, 12])
    print(is_palindrome_train(t), values_of(t), is_palindrome_train(build([12, 25, 25, 13])))
