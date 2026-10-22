"""Volume 4, Chapter 3 - Thinking Problems (Section 3.15).

WaitingList: a queue of readers that also lets any reader leave, in O(1) amortized time per operation
(Thinking Problem 2), and NoTicketWaitingList, the plausible version that forgets who left and rejoined
(the trap discussed in its model solution).  workload_cost counts the steps of Thinking Problem 3.
"""

from __future__ import annotations

from collections import deque


class WaitingList:
    """Join at the back, leave from anywhere, serve the oldest: each O(1) amortized."""

    def __init__(self) -> None:
        self.line = deque()      # (reader, ticket) in joining order; may hold stale entries
        self.ticket = {}         # reader -> ticket of their current place, only for readers still waiting
        self.next_ticket = 0

    def join(self, reader) -> bool:
        if reader in self.ticket:
            return False                              # already waiting: keep the earlier place
        self.ticket[reader] = self.next_ticket
        self.line.append((reader, self.next_ticket))
        self.next_ticket += 1
        return True

    def leave(self, reader) -> bool:
        return self.ticket.pop(reader, None) is not None

    def serve(self):
        while self.line:
            reader, t = self.line.popleft()
            if self.ticket.get(reader) == t:          # a live entry, not one left behind by leave
                del self.ticket[reader]
                return reader
        return None                                   # nobody is waiting

    def __len__(self) -> int:
        return len(self.ticket)


class NoTicketWaitingList(WaitingList):
    """The bug: a set of waiting readers instead of tickets, so an old entry revives after a rejoin."""

    def serve(self):
        while self.line:
            reader, _ = self.line.popleft()
            if reader in self.ticket:
                del self.ticket[reader]
                return reader
        return None


def workload_cost(costs: dict, counts: dict) -> int:
    """Total steps of a workload: the sum over operations of (how often) x (steps per call)."""
    return sum(counts[op] * costs[op] for op in counts)
