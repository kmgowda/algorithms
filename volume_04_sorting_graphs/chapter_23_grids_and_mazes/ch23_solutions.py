"""Volume 4, Chapter 23 - Thinking Problems: model solutions that are algorithms.

Run:  python3 ch23_solutions.py
"""

from __future__ import annotations

from collections import deque

from ch23_examples import BASEMENT


def fewest_pushes(grid: list[str], start, goal) -> int | None:
    """Thinking Problem 2: the fewest shelves to push aside so that start can reach goal (0-1 BFS).
    Stepping onto an open square costs 0 pushes, onto a shelf '#' costs 1. The deque holds squares
    in non-decreasing order of pushes, so each square is settled once: O(rows x columns).
    Returns None only when start or goal lies outside the grid."""
    rows, cols = len(grid), len(grid[0]) if grid else 0
    inside = lambda r, c: 0 <= r < rows and 0 <= c < cols
    if not inside(*start) or not inside(*goal):
        return None
    best = {start: 0}
    dq = deque([start])
    done = set()
    while dq:
        r, c = dq.popleft()
        if (r, c) in done:
            continue
        done.add((r, c))
        if (r, c) == goal:
            return best[goal]
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            nr, nc = r + dr, c + dc
            if not inside(nr, nc):
                continue
            cost = best[(r, c)] + (1 if grid[nr][nc] == "#" else 0)
            if cost < best.get((nr, nc), cost + 1):
                best[(nr, nc)] = cost
                if cost == best[(r, c)]:
                    dq.appendleft((nr, nc))         # a free step: same number of pushes, front of the deque
                else:
                    dq.append((nr, nc))             # one more push: back of the deque
    return best.get(goal)


def corner_rule_rooms(grid: list[str]) -> int:
    """Thinking Problem 3: the flawed rule 'count open squares whose upper and left neighbours are walls or
    the edge'. Right for rectangular rooms, wrong for rooms of any other shape."""
    def wall(r, c):
        return r < 0 or c < 0 or grid[r][c] == "#"
    return sum(1 for r, row in enumerate(grid) for c, ch in enumerate(row)
               if ch != "#" and wall(r - 1, c) and wall(r, c - 1))


def rooms(grid: list[str]) -> int:
    """The correct count (Section 23.8): one flood fill per open square not yet marked."""
    seen, count = set(), 0
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "#" or (r, c) in seen:
                continue
            count += 1
            seen.add((r, c))
            q = deque([(r, c)])
            while q:
                y, x = q.popleft()
                for ny, nx in ((y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)):
                    if 0 <= ny < len(grid) and 0 <= nx < len(row) and grid[ny][nx] != "#" and (ny, nx) not in seen:
                        seen.add((ny, nx))
                        q.append((ny, nx))
    return count


if __name__ == "__main__":
    print(fewest_pushes(BASEMENT, (0, 0), (4, 7)))
    print(fewest_pushes(["S.#.", "..#E", "..#."], (0, 0), (1, 3)))
    print(corner_rule_rooms([".#.", "..."]), rooms([".#.", "..."]))
