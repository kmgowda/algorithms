"""Volume 5, Chapter 16 - Scheduling and Intervals: earliest finish first, and counting rooms.

Run:  python3 ch16_examples.py
"""

from __future__ import annotations

import heapq
import itertools

# Requests for the library's one meeting room: (group, start hour, end hour).
REQUESTS = [("Chess", 9, 11), ("Poetry", 10, 12), ("Knitting", 11, 13), ("Coding", 9, 15), ("Maps", 12, 14),
            ("Choir", 13, 16), ("Writers", 14, 15), ("Film", 15, 17)]


def by_rule(requests: list, key) -> list:
    """Greedy: take requests in the order given by key, keeping each that does not clash with those kept."""
    kept = []
    for r in sorted(requests, key=key):
        if all(r[2] <= k[1] or r[1] >= k[2] for k in kept):
            kept.append(r)
    return sorted(kept, key=lambda r: r[1])


def earliest_finish(requests: list) -> list:
    """The greedy rule that is always best (Figure 16.2): next, the request that ends soonest."""
    kept, free_at = [], float("-inf")
    for r in sorted(requests, key=lambda r: r[2]):
        if r[1] >= free_at:
            kept.append(r)
            free_at = r[2]
    return kept


def most_by_brute_force(requests: list) -> int:
    best = 0
    for k in range(len(requests) + 1):
        for combo in itertools.combinations(requests, k):
            s = sorted(combo, key=lambda r: r[1])
            if all(a[2] <= b[1] for a, b in zip(s, s[1:])):
                best = max(best, k)
    return best


def rooms_needed(requests: list) -> tuple[int, dict]:
    """Give every request a room, reusing a room as soon as it is free (Figure 16.5). Returns (rooms, room of each)."""
    free, room_of, busy = [], {}, []                     # busy: (end, room)
    count = 0
    for name, s, e in sorted(requests, key=lambda r: r[1]):
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            count += 1
            room = count
        room_of[name] = room
        heapq.heappush(busy, (e, room))
    return count, room_of


def max_overlap(requests: list) -> int:
    events = sorted([(s, 1) for _, s, _ in requests] + [(e, -1) for _, _, e in requests])
    now = best = 0
    for _, d in events:
        now += d
        best = max(best, now)
    return best


# Section 16.6: four volunteers rank four desks, and each desk leader ranks the volunteers (best first).
VOLUNTEERS = {"Ana": ["Cafe", "Tickets", "Stage", "Signs"], "Ben": ["Cafe", "Stage", "Tickets", "Signs"],
              "Cai": ["Tickets", "Cafe", "Signs", "Stage"], "Dev": ["Cafe", "Tickets", "Signs", "Stage"]}
DESKS = {"Tickets": ["Ben", "Dev", "Ana", "Cai"], "Cafe": ["Cai", "Ana", "Dev", "Ben"],
         "Stage": ["Ana", "Ben", "Cai", "Dev"], "Signs": ["Dev", "Cai", "Ben", "Ana"]}


def gale_shapley(proposers: dict, receivers: dict, log: list | None = None) -> dict:
    """Stable matching (Figure 16.6): a free proposer asks the best receiver not yet asked; the receiver keeps
    whichever of the asker and its current partner it ranks higher. Returns {proposer: receiver}."""
    rank = {r: {p: i for i, p in enumerate(prefs)} for r, prefs in receivers.items()}
    next_choice = {p: 0 for p in proposers}
    partner = {}                                      # receiver -> proposer
    free = list(proposers)
    while free:
        p = free.pop(0)
        r = proposers[p][next_choice[p]]
        next_choice[p] += 1
        held = partner.get(r)
        if held is None:
            partner[r] = p
            outcome = "accepts"
        elif rank[r][p] < rank[r][held]:
            partner[r] = p
            free.append(held)
            outcome = f"swaps {held} for"
        else:
            free.append(p)
            outcome = "rejects"
        if log is not None:
            log.append((p, r, outcome))
    return {p: r for r, p in partner.items()}


def blocking_pairs(match: dict, proposers: dict, receivers: dict) -> list:
    """Pairs (p, r) not matched together who both prefer each other to their partners: what 'unstable' means."""
    owner = {r: p for p, r in match.items()}
    out = []
    for p, prefs in proposers.items():
        for r in prefs[:prefs.index(match[p])]:       # receivers p likes better than its own
            if receivers[r].index(p) < receivers[r].index(owner[r]):
                out.append((p, r))
    return out


def all_stable(proposers: dict, receivers: dict) -> list:
    """Brute force: every perfect matching (n! of them) that has no blocking pair."""
    ps, rs = sorted(proposers), sorted(receivers)
    out = []
    for perm in itertools.permutations(rs):
        m = dict(zip(ps, perm))
        if not blocking_pairs(m, proposers, receivers):
            out.append(m)
    return out


if __name__ == "__main__":
    log = []
    print(gale_shapley(VOLUNTEERS, DESKS, log), log)
    print(all_stable(VOLUNTEERS, DESKS))
    print(earliest_finish(REQUESTS), most_by_brute_force(REQUESTS))
    print(len(by_rule(REQUESTS, lambda r: r[1])), len(by_rule(REQUESTS, lambda r: r[2] - r[1])))
    print(rooms_needed(REQUESTS), max_overlap(REQUESTS))
