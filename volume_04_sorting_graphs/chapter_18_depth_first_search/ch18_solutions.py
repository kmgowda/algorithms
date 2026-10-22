"""Volume 4, Chapter 18 - Thinking Problems: model solutions (Section 18.15).

Run:  python3 ch18_solutions.py
"""

from __future__ import annotations


def dfs_times_iterative(adj: dict, start) -> dict:
    """Thinking Problem 2: discovery and finish times with no recursion, equal to the recursive dfs.
    Each stack entry is (place, bookmark); a place gets its finish time when its entry is popped. O(V + E)."""
    time, disc, fin, parent = 1, {start: 1}, {}, {start: None}
    stack = [(start, 0)]
    while stack:
        v, i = stack[-1]
        if i == len(adj[v]):
            stack.pop()
            time += 1
            fin[v] = time                       # every road from v tried: v finishes
        else:
            stack[-1] = (v, i + 1)              # move the bookmark past this road
            w = adj[v][i]
            if w not in disc:
                time += 1
                disc[w], parent[w] = time, v    # step along the road: w is discovered
                stack.append((w, 0))
    return {"disc": disc, "fin": fin, "parent": parent}


def has_cycle_undirected(adj: dict, start) -> bool:
    """Thinking Problem 3, repaired: a cycle test for two-way roads that allows parallel roads.
    It skips the road it arrived by ONCE, instead of skipping every road that leads to the parent."""
    seen, stack = {start}, [(start, None)]
    while stack:
        v, came_from = stack.pop()
        skipped = False
        for w in adj[v]:
            if w == came_from and not skipped:
                skipped = True                  # the road we arrived by: ignore it, but only once
            elif w in seen:
                return True                     # any other road to a seen place closes a cycle
            else:
                seen.add(w)
                stack.append((w, v))
    return False


if __name__ == "__main__":
    import ch18_examples as ex
    print(dfs_times_iterative(ex.adjacency(), "Library"))
    two = {"A": ["B", "B"], "B": ["A", "A"]}
    print([e for e in ex.dfs(two, "A")["edges"] if e[2] == "back"], has_cycle_undirected(two, "A"))
