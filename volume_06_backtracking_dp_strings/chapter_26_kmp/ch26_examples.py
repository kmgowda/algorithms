"""Volume 6, Chapter 26 - Knuth-Morris-Pratt: never look at a text letter twice.

Run:  python3 ch26_examples.py
"""

from __future__ import annotations


def failure(pattern: str) -> list:
    """fail[k] = length of the longest proper prefix of pattern[:k+1] that is also a suffix of it (Figure 26.2)."""
    fail, k = [0] * len(pattern), 0
    for i in range(1, len(pattern)):
        while k and pattern[i] != pattern[k]:
            k = fail[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        fail[i] = k
    return fail


def kmp_search(text: str, pattern: str) -> tuple[list, int]:
    """Every occurrence of pattern, with letter comparisons counted (Figure 26.3). Empty pattern: every position."""
    if not pattern:
        return list(range(len(text) + 1)), 0
    fail, found, k, comparisons = failure(pattern), [], 0, 0
    for i, ch in enumerate(text):
        while True:
            comparisons += 1
            if ch == pattern[k]:
                k += 1
                break
            if k == 0:
                break
            k = fail[k - 1]                           # slide the pattern; keep the part already known to match
        if k == len(pattern):
            found.append(i - k + 1)
            k = fail[k - 1]
    return found, comparisons


def failure_trace(pattern: str) -> list:
    """The border table built step by step (Section 26.4): for each i >= 1, (i, letter, k before, the k values
    fallen back to, k after)."""
    fail, k, steps = [0] * len(pattern), 0, []
    for i in range(1, len(pattern)):
        start, falls = k, []
        while k and pattern[i] != pattern[k]:
            k = fail[k - 1]
            falls.append(k)
        if pattern[i] == pattern[k]:
            k += 1
        fail[i] = k
        steps.append((i, pattern[i], start, falls, k))
    return steps


def kmp_trace(text: str, pattern: str) -> list:
    """The search step by step (Figure 26.3): for each text position, (i, letter, k before, fallbacks, k after,
    match reported?)."""
    fail, k, out = failure(pattern), 0, []
    for i, ch in enumerate(text):
        start, falls = k, []
        while k and ch != pattern[k]:
            k = fail[k - 1]
            falls.append(k)
        if ch == pattern[k]:
            k += 1
        hit = k == len(pattern)
        out.append((i, ch, start, falls, k, hit))
        if hit:
            k = fail[k - 1]
    return out


def automaton(pattern: str, alphabet: str) -> list:
    """The KMP automaton (Section 26.5): step[k][c] = how many pattern letters match after reading c with k matched.
    It is built from the border table, and searching then takes exactly one look-up per text letter."""
    m, fail = len(pattern), failure(pattern)
    step = [{} for _ in range(m + 1)]
    for k in range(m + 1):
        for c in alphabet:
            if k < m and c == pattern[k]:
                step[k][c] = k + 1
            elif k == 0:
                step[k][c] = 0
            else:
                step[k][c] = step[fail[k - 1]][c]
    return step


def automaton_search(text: str, pattern: str) -> list:
    if not pattern:
        return list(range(len(text) + 1))
    step, k, found = automaton(pattern, sorted(set(text + pattern))), 0, []
    for i, c in enumerate(text):
        k = step[k][c]
        if k == len(pattern):
            found.append(i - k + 1)
    return found


if __name__ == "__main__":
    print(failure("abacab"), failure("aaaab"), failure("abcd"))
    print(kmp_search("abacabacab", "abacab"))
    t = "a" * 1000
    print(kmp_search(t, "a" * 9 + "b")[1], kmp_search(t, "b" + "a" * 9)[1], len(kmp_search(t, "aaa")[0]))
    nl = "the reading club meets on monday; the club reads maps and poems at the library"
    print(kmp_search(nl, "club"))
