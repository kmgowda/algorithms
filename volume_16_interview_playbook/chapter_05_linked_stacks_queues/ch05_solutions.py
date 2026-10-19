"""Volume 16, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque

from ch05_examples import ListNode


class MinStack:
    """Exercise 1 (LeetCode 155): every stack entry also remembers the minimum at that depth - O(1) get_min."""

    def __init__(self) -> None:
        self.items: list[tuple[int, int]] = []

    def push(self, x: int) -> None:
        self.items.append((x, min(x, self.items[-1][1]) if self.items else x))

    def pop(self) -> int:
        return self.items.pop()[0]

    def top(self) -> int:
        return self.items[-1][0]

    def get_min(self) -> int:
        return self.items[-1][1]


class QueueFromStacks:
    """Exercise 2 (LeetCode 232): two stacks; pour 'in' into 'out' only when 'out' is empty - amortized O(1)."""

    def __init__(self) -> None:
        self.inbox: list[int] = []
        self.outbox: list[int] = []

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def pop(self) -> int:
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop()


def middle_node(head: ListNode | None) -> ListNode | None:
    """Exercise 3 (LeetCode 876): slow moves one, fast moves two - slow stops in the middle."""
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next                  # type: ignore[union-attr]
    return slow


def sliding_max(nums: list[int], k: int) -> list[int]:
    """Exercise 4 (LeetCode 239): a deque of indices with decreasing values - the front is the window max."""
    dq: deque[int] = deque()
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


if __name__ == "__main__":
    s = MinStack()
    for v in (5, 3, 7):
        s.push(v)
    print(s.get_min(), sliding_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
