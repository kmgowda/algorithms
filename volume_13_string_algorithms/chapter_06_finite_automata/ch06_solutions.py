"""Volume 13, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from ch06_examples import build_dfa


def ends_with_pattern(text: str, pattern: str, alphabet: str) -> bool:
    """Exercise 1: does the text END with the pattern? Run the DFA and check the final state."""
    delta, q = build_dfa(pattern, alphabet), 0
    for ch in text:
        q = delta[q].get(ch, 0)
    return q == len(pattern)


def count_avoiding(n: int, pattern: str, alphabet: str) -> int:
    """Exercise 2: how many strings of length n do NOT contain the pattern? DP over (length, DFA state)."""
    delta = build_dfa(pattern, alphabet)
    m = len(pattern)
    ways = [1] + [0] * m
    for _ in range(n):
        nxt = [0] * (m + 1)
        for q in range(m):
            for c in alphabet:
                nxt[delta[q][c]] += ways[q]
        ways = nxt
    return sum(ways[:m])


def divisible_by_three(binary: str) -> bool:
    """Exercise 3: a 3-state automaton for 'is this binary number divisible by 3?' - state = value mod 3."""
    state = 0
    for bit in binary:
        state = (2 * state + int(bit)) % 3
    return state == 0


if __name__ == "__main__":
    print(ends_with_pattern("xxabc", "abc", "abcx"), count_avoiding(5, "11", "01"), divisible_by_three("110"))
