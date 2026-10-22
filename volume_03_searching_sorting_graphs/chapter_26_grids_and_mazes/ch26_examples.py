"""Volume 3, Chapter 26 - Grids and Mazes: graphs that are never written down.

Run:  python3 ch26_examples.py
"""

from __future__ import annotations

import random
from collections import deque

# the library basement: '#' wall, '.' open floor, 'S' start (stairs), 'E' exit (the archive door)
BASEMENT = ["S..#....",
            ".#.#.##.",
            ".#...#..",
            ".####.#.",
            "......#E"]


def find(grid: list[str], ch: str) -> tuple[int, int]:
    for r, row in enumerate(grid):
        if ch in row:
            return r, row.index(ch)
    raise ValueError(ch)


def neighbours(grid: list[str], r: int, c: int):
    """Up, right, down, left: the four squares that share a side and are not walls (Figure 26.2)."""
    for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
            yield nr, nc


def bfs_grid(grid: list[str], start, goal) -> tuple[list | None, dict]:
    """Fewest steps from start to goal; returns (path or None, distance table)."""
    dist, parent = {start: 0}, {start: None}
    q = deque([start])
    while q:
        cell = q.popleft()
        if cell == goal:
            break
        for nxt in neighbours(grid, *cell):
            if nxt not in dist:
                dist[nxt] = dist[cell] + 1
                parent[nxt] = cell
                q.append(nxt)
    if goal not in parent:
        return None, dist
    path, cell = [], goal
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    return path[::-1], dist


def flood_fill(grid: list[str], start) -> set:
    """Every open square reachable from start (BFS without a goal)."""
    _, dist = bfs_grid(grid, start, None)
    return set(dist)


def generate_maze(rows: int, cols: int, seed: int = 1) -> list[str]:
    """A random perfect maze (exactly one route between any two rooms) by randomized DFS (Figure 26.5).
    Rooms sit at odd coordinates of a (2*rows+1) x (2*cols+1) grid; DFS knocks down the wall between rooms."""
    rng = random.Random(seed)
    h, w = 2 * rows + 1, 2 * cols + 1
    g = [["#"] * w for _ in range(h)]
    stack, seen = [(0, 0)], {(0, 0)}
    g[1][1] = "."
    while stack:
        r, c = stack[-1]
        options = [(r + dr, c + dc) for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1))
                   if 0 <= r + dr < rows and 0 <= c + dc < cols and (r + dr, c + dc) not in seen]
        if not options:
            stack.pop()
            continue
        nr, nc = rng.choice(options)
        g[2 * r + 1 + (nr - r)][2 * c + 1 + (nc - c)] = "."
        g[2 * nr + 1][2 * nc + 1] = "."
        seen.add((nr, nc))
        stack.append((nr, nc))
    return ["".join(row) for row in g]


def bfs_states(start, goal, moves) -> list | None:
    """BFS on an implicit state graph (Section 26.5, Figure 26.4): moves(state) yields the states one move away.
    Returns the fewest-moves list of states from start to goal, or None if the goal can never be reached."""
    parent = {start: None}
    q = deque([start])
    while q:
        s = q.popleft()
        if s == goal:
            path = []
            while s is not None:
                path.append(s)
                s = parent[s]
            return path[::-1]
        for t in moves(s):
            if t not in parent:
                parent[t] = s
                q.append(t)
    return None


def lock_moves(jammed: set):
    """The archive cabinet's lock: three dials 0-9; one move turns one dial one step up or down (9 wraps to 0).
    Combinations in `jammed` stick the lock, so the search must never pass through them."""
    def moves(code: str):
        for i in range(len(code)):
            for step in (1, -1):
                d = (int(code[i]) + step) % 10
                nxt = code[:i] + str(d) + code[i + 1:]
                if nxt not in jammed:
                    yield nxt
    return moves


def count_states(start, moves) -> int:
    """How many states the search can reach at all (flood fill on the state graph)."""
    seen, q = {start}, deque([start])
    while q:
        for t in moves(q.popleft()):
            if t not in seen:
                seen.add(t)
                q.append(t)
    return len(seen)


if __name__ == "__main__":
    s, e = find(BASEMENT, "S"), find(BASEMENT, "E")
    path, dist = bfs_grid(BASEMENT, s, e)
    print(len(path) - 1, path)
    print(len(flood_fill(BASEMENT, s)), sum(row.count("#") for row in BASEMENT), sum(len(r) for r in BASEMENT))
    m = generate_maze(4, 6)
    print("\n".join(m))
    mp, _ = bfs_grid(m, (1, 1), (len(m) - 2, len(m[0]) - 2))
    print(len(mp) - 1)
