"""Volume 5, Chapter 10 - Matching and Assignment: pair people with jobs.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import itertools

# Which festival desks each volunteer is trained for.
CAN_DO = {"Ana": ["Tickets", "Cafe"], "Ben": ["Tickets"], "Cai": ["Cafe", "Stage", "Signs"], "Dev": ["Stage"],
          "Eva": ["Signs", "First aid"]}


def max_matching(can_do: dict, log: list | None = None, calls: list | None = None) -> dict:
    """Augmenting paths (Figure 10.2): give each volunteer a desk, moving earlier volunteers along if needed.
    Returns {desk: volunteer}. calls, if given, records (newcomer, depth, person, desk, what happened) for every desk
    a TryAssign call looks at (Figure 10.3)."""
    owner: dict = {}

    def try_assign(person, seen, depth, newcomer):
        for desk in can_do[person]:
            if desk in seen:
                if calls is not None:
                    calls.append((newcomer, depth, person, desk, "seen"))
                continue
            seen.add(desk)
            if desk not in owner:
                if calls is not None:
                    calls.append((newcomer, depth, person, desk, "free"))
                owner[desk] = person
                return True
            if calls is not None:
                calls.append((newcomer, depth, person, desk, "ask " + owner[desk]))
            if try_assign(owner[desk], seen, depth + 1, newcomer):
                owner[desk] = person                  # take the desk; its old owner moved elsewhere
                return True
        return False

    for person in can_do:
        ok = try_assign(person, set(), 0, person)
        if log is not None:
            log.append((person, ok, dict(owner)))
    return owner


def greedy_matching(can_do: dict) -> dict:
    """Each volunteer takes their first free desk and never moves: can leave people out."""
    owner = {}
    for person, desks in can_do.items():
        for d in desks:
            if d not in owner:
                owner[d] = person
                break
    return owner


# Minutes each driver needs to reach each branch (an assignment problem).
DRIVERS = ["Ana", "Ben", "Cai", "Dev"]
BRANCHES = ["North", "East", "South", "West"]
MINUTES = [[2, 9, 8, 9], [1, 3, 5, 2], [3, 2, 8, 7], [7, 1, 1, 5]]


def best_assignment(cost: list) -> tuple[int, tuple]:
    """Try every way of giving each driver a different branch (n! ways); keep the cheapest."""
    n = len(cost)
    return min((sum(cost[i][p[i]] for i in range(n)), p) for p in itertools.permutations(range(n)))


def greedy_assignment(cost: list) -> tuple[int, list]:
    """Repeatedly take the cheapest remaining driver-branch pair."""
    n, used_r, used_c, total, pairs = len(cost), set(), set(), 0, []
    cells = sorted((cost[i][j], i, j) for i in range(n) for j in range(n))
    for c, i, j in cells:
        if i not in used_r and j not in used_c:
            used_r.add(i)
            used_c.add(j)
            total += c
            pairs.append((i, j))
    return total, pairs


def konig_cover(can_do: dict) -> tuple[dict, list]:
    """A maximum matching and a smallest vertex cover of the same size (Konig's theorem, Figure 10.6).
    From every unmatched person, follow alternating paths (any trained desk, then that desk's owner). Z = everyone
    and every desk reached. The cover is the people NOT in Z plus the desks in Z."""
    owner = max_matching(can_do)
    matched = set(owner.values())
    z_people = [p for p in can_do if p not in matched]
    z_desks: set = set()
    stack = list(z_people)
    seen_people = set(z_people)
    while stack:
        p = stack.pop()
        for d in can_do[p]:
            if d not in z_desks:
                z_desks.add(d)
                q = owner.get(d)
                if q is not None and q not in seen_people:
                    seen_people.add(q)
                    stack.append(q)
    desks = list(dict.fromkeys(d for ds in can_do.values() for d in ds))
    cover = [p for p in can_do if p not in seen_people] + [d for d in desks if d in z_desks]
    return owner, cover


def hopcroft_karp(can_do: dict, log: list | None = None) -> dict:
    """Hopcroft-Karp (Figure 10.4): in each phase, a breadth-first search finds the length of the shortest augmenting
    paths, then depth-first searches use a whole set of such paths that share no vertex. O(E sqrt V).
    Returns {desk: person}; log gets one list of augmenting paths per phase."""
    owner: dict = {}                                   # desk -> person
    mine: dict = {}                                    # person -> desk
    people = list(can_do)
    inf = float("inf")
    while True:
        layer = {p: 0 for p in people if p not in mine}
        queue, found, i = [p for p in people if p not in mine], inf, 0
        while i < len(queue):                          # breadth-first search in layers
            p = queue[i]
            i += 1
            if layer[p] >= found:
                continue
            for d in can_do[p]:
                q = owner.get(d)
                if q is None:
                    found = min(found, layer[p] + 1)   # a free desk: shortest augmenting paths have this length
                elif q not in layer:
                    layer[q] = layer[p] + 1
                    queue.append(q)
        if found == inf:
            return owner
        used_desks: set = set()
        paths = []

        def dfs(p, path):
            for d in can_do[p]:
                if d in used_desks:
                    continue
                q = owner.get(d)
                if q is None and layer[p] + 1 == found or q is not None and layer.get(q) == layer[p] + 1:
                    used_desks.add(d)
                    if q is None or dfs(q, path + [d, q]):
                        owner[d], mine[p] = p, d
                        if q is None:
                            paths.append(path + [d])
                        return True
            layer[p] = inf                              # a dead end: do not try it again in this phase
            return False

        for p in people:
            if p not in mine and layer.get(p) == 0:
                dfs(p, [p])
        if log is not None:
            log.append(paths)


def hungarian(cost: list, log: list | None = None) -> tuple[int, list]:
    """The Hungarian method on a square table (Figures 10.8 and 10.9), in its table-and-lines form.
    1. Subtract each row's smallest number, then each column's. 2. Find the largest set of zeros with no two in a
    row or column. 3. If it has n zeros, they are the answer. Otherwise cover every zero with the fewest lines,
    subtract the smallest uncovered number from every uncovered cell, add it where two lines cross, and repeat.
    Returns (total cost, column chosen for each row). log gets (step, table) snapshots."""
    n = len(cost)
    if n == 0:
        return 0, []
    a = [row[:] for row in cost]
    for row in a:
        m = min(row)
        for j in range(n):
            row[j] -= m
    if log is not None:
        log.append(("rows reduced", [r[:] for r in a]))
    for j in range(n):
        m = min(a[i][j] for i in range(n))
        for i in range(n):
            a[i][j] -= m
    if log is not None:
        log.append(("columns reduced", [r[:] for r in a]))
    while True:
        zeros = {i: [j for j in range(n) if a[i][j] == 0] for i in range(n)}
        owner = max_matching(zeros)                     # column -> row: the most independent zeros
        if len(owner) == n:
            pick = [0] * n
            for j, i in owner.items():
                pick[i] = j
            return sum(cost[i][pick[i]] for i in range(n)), pick
        line_rows, line_cols = _lines(zeros, owner, n)  # fewest lines covering every zero
        m = min(a[i][j] for i in range(n) for j in range(n) if i not in line_rows and j not in line_cols)
        for i in range(n):
            for j in range(n):
                if i not in line_rows and j not in line_cols:
                    a[i][j] -= m
                elif i in line_rows and j in line_cols:
                    a[i][j] += m
        if log is not None:
            log.append((f"lines: rows {sorted(line_rows)}, columns {sorted(line_cols)}; adjust by {m}",
                        [r[:] for r in a]))


def _lines(zeros: dict, owner: dict, n: int) -> tuple[set, set]:
    """The fewest lines covering every zero (Konig): rows not reached from unmatched rows, columns reached."""
    matched_rows = set(owner.values())
    reached_rows = {i for i in range(n) if i not in matched_rows}
    reached_cols: set = set()
    stack = list(reached_rows)
    while stack:
        i = stack.pop()
        for j in zeros[i]:
            if j not in reached_cols:
                reached_cols.add(j)
                k = owner.get(j)
                if k is not None and k not in reached_rows:
                    reached_rows.add(k)
                    stack.append(k)
    return set(range(n)) - reached_rows, reached_cols


# Three shelvers and three trolleys: minutes for each shelver to empty each trolley (needs one adjustment).
SHELVING = [[4, 1, 3], [2, 0, 5], [3, 2, 2]]

# The festival with a sixth volunteer and a sixth desk: Fay can do only Tickets or the Cafe.
CAN_DO_SIX = {**CAN_DO, "Eva": ["Signs", "First aid", "Lost property"], "Fay": ["Tickets", "Cafe"]}

if __name__ == "__main__":
    log = []
    print(max_matching(CAN_DO, log))
    for row in log:
        print(row)
    print(greedy_matching(CAN_DO))
    print(best_assignment(MINUTES), greedy_assignment(MINUTES))
