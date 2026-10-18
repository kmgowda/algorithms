"""Volume 13, Chapter 6 - String Matching With Finite Automata.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations


def build_dfa(pattern: str, alphabet: str) -> list[dict[str, int]]:
    """State q = how many pattern letters are currently matched (0..m). delta[q][c] = the next state after
    reading c. Built in O(m x |alphabet|) using the 'restart' state x (KMP's fall-back, precomputed)."""
    m = len(pattern)
    delta = [{c: 0 for c in alphabet} for _ in range(m + 1)]
    if m == 0:
        return delta
    delta[0][pattern[0]] = 1
    x = 0                                            # the state we would be in after reading pattern[1:q]
    for q in range(1, m + 1):
        for c in alphabet:
            delta[q][c] = delta[x][c]                # on a mismatch, behave like state x
        if q < m:
            delta[q][pattern[q]] = q + 1             # on a match, move forward
            x = delta[x][pattern[q]]
    return delta


def dfa_search(text: str, pattern: str, alphabet: str) -> list[int]:
    """Read each letter once and follow ONE table entry - no comparisons, no fall-back loops."""
    delta = build_dfa(pattern, alphabet)
    m, q, found = len(pattern), 0, []
    for i, ch in enumerate(text):
        q = delta[q].get(ch, 0)                      # letters outside the alphabet reset to 0
        if q == m:
            found.append(i - m + 1)
    return found


def dfa_table(pattern: str, alphabet: str) -> list[str]:
    """Pretty-print the transition table, one row per state."""
    delta = build_dfa(pattern, alphabet)
    header = "state " + " ".join(alphabet)
    rows = [f"{q:>5} " + " ".join(str(delta[q][c]) for c in alphabet) for q in range(len(pattern) + 1)]
    return [header] + rows


def is_valid_id(code: str) -> bool:
    """Industry example: a hand-written automaton validating an ID like 'AB-1234' (2 capitals, dash, 4 digits)."""
    state = 0
    for ch in code:
        if state in (0, 1) and ch.isupper():
            state += 1
        elif state == 2 and ch == "-":
            state = 3
        elif 3 <= state < 7 and ch.isdigit():
            state += 1
        else:
            return False
    return state == 7


if __name__ == "__main__":
    print("\n".join(dfa_table("ababaca", "abc")))
    print(dfa_search("abababacaba", "ababaca", "abc"))
    print([is_valid_id(x) for x in ("AB-1234", "A-1234", "AB-12x4", "ab-1234")])
