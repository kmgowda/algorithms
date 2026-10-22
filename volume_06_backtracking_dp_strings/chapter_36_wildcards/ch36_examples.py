"""Volume 6, Chapter 36 - Matching Patterns with Wildcards: ? is any one letter, * is any run of letters.

Run:  python3 ch36_examples.py
"""

from __future__ import annotations

import fnmatch

TITLES = ["treasure island", "the treasure map", "trees of britain", "a tale of two cities", "tress", "island"]


def wildcard(pattern: str, text: str) -> tuple[bool, list]:
    """M[i][j]: does pattern[:i] match text[:j]? (Figure 36.2). Returns (answer, table)."""
    n, m = len(pattern), len(text)
    M = [[False] * (m + 1) for _ in range(n + 1)]
    M[0][0] = True
    for i in range(1, n + 1):
        if pattern[i - 1] == "*":
            M[i][0] = M[i - 1][0]                     # * can match nothing
    for i in range(1, n + 1):
        p = pattern[i - 1]
        for j in range(1, m + 1):
            if p == "*":
                M[i][j] = M[i - 1][j] or M[i][j - 1]   # * matches nothing, or one more letter
            else:
                M[i][j] = M[i - 1][j - 1] and (p == "?" or p == text[j - 1])
    return M[n][m], M


def plain_recursion(pattern: str, text: str, calls: list) -> bool:
    """The same rules without a table: tries every way a * could stretch."""
    calls[0] += 1
    if not pattern:
        return not text
    if pattern[0] == "*":
        return plain_recursion(pattern[1:], text, calls) or (bool(text) and plain_recursion(pattern, text[1:], calls))
    return bool(text) and pattern[0] in ("?", text[0]) and plain_recursion(pattern[1:], text[1:], calls)


# ---- regular expressions (Section 36.6): letters, '.', '*', '|' and parentheses, by Thompson's construction

def _postfix(regex: str) -> list:
    """Insert explicit concatenation ('&') and convert to postfix order (shunting-yard)."""
    out, ops, prev = [], [], None
    prec = {"|": 1, "&": 2}
    tokens = []
    for ch in regex:                                   # add '&' between two pieces that follow each other
        if prev is not None and prev not in "(|" and ch not in "|)*":
            tokens.append("&")
        tokens.append(ch)
        prev = ch
    for t in tokens:
        if t == "(":
            ops.append(t)
        elif t == ")":
            while ops[-1] != "(":
                out.append(ops.pop())
            ops.pop()
        elif t in prec:
            while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[t]:
                out.append(ops.pop())
            ops.append(t)
        else:                                          # a letter, '.', or '*' (a postfix operator already)
            out.append(t)
    while ops:
        out.append(ops.pop())
    return out


def build_nfa(regex: str) -> tuple[int, int, dict, dict]:
    """Thompson's NFA: states are numbers; letter[s] = (symbol, next) for a state that reads one symbol;
    free[s] = states reachable without reading (empty moves). Returns (start, accept, letter, free)."""
    letter, free, count = {}, {}, [0]

    def new() -> int:
        count[0] += 1
        free[count[0]] = []
        return count[0]

    stack = []
    for t in _postfix(regex):
        if t == "&":
            b, a = stack.pop(), stack.pop()
            free[a[1]].append(b[0])
            stack.append((a[0], b[1]))
        elif t == "|":
            b, a = stack.pop(), stack.pop()
            s0, s1 = new(), new()
            free[s0] += [a[0], b[0]]
            free[a[1]].append(s1)
            free[b[1]].append(s1)
            stack.append((s0, s1))
        elif t == "*":
            a = stack.pop()
            s0, s1 = new(), new()
            free[s0] += [a[0], s1]
            free[a[1]] += [a[0], s1]
            stack.append((s0, s1))
        else:
            s0, s1 = new(), new()
            letter[s0] = (t, s1)
            stack.append((s0, s1))
    if not stack:                                      # the empty regex matches only the empty text
        s0 = new()
        return s0, s0, letter, free
    start, accept = stack.pop()
    return start, accept, letter, free


def nfa_match(regex: str, text: str) -> tuple[bool, int]:
    """Does regex match the whole text? Keep the SET of states the NFA could be in; each text letter moves every
    state at once. Returns (match?, state visits), at most about (text length + 1) x (states)."""
    start, accept, letter, free = build_nfa(regex)
    visits = [0]

    def close(states: set) -> set:
        todo, seen = list(states), set(states)
        while todo:
            s = todo.pop()
            visits[0] += 1
            for t in free.get(s, ()):
                if t not in seen:
                    seen.add(t)
                    todo.append(t)
        return seen

    current = close({start})
    for ch in text:
        current = close({nxt for s in current if s in letter for sym, nxt in [letter[s]] if sym in (ch, ".")})
    return accept in current, visits[0]


def backtrack_match(regex: str, text: str) -> tuple[bool, int]:
    """The same question answered by trying one path through the NFA at a time, backing up on failure, as
    backtracking engines do. Returns (match?, steps); the steps can grow exponentially."""
    start, accept, letter, free = build_nfa(regex)
    steps = [0]

    def go(s: int, i: int, seen: frozenset) -> bool:
        steps[0] += 1
        if s == accept and i == len(text):
            return True
        if s in letter:
            sym, nxt = letter[s]
            if i < len(text) and sym in (text[i], "."):
                return go(nxt, i + 1, frozenset())
            return False
        for t in free.get(s, ()):
            if t not in seen and go(t, i, seen | {s}):
                return True
        return False

    return go(start, 0, frozenset()), steps[0]


def search(pattern: str, titles: list) -> list:
    return [t for t in titles if wildcard(pattern, t)[0]]


if __name__ == "__main__":
    print(search("tre?s*", TITLES), search("*island", TITLES), search("*of*", TITLES), search("t?e *", TITLES))
    print(wildcard("t*s", "tress")[0], wildcard("t*s", "trees")[0], wildcard("t*s", "tree")[0])
    c = [0]
    print(plain_recursion("*a*a*a*b", "a" * 20, c), c[0], wildcard("*a*a*a*b", "a" * 20)[0], 9 * 21)
