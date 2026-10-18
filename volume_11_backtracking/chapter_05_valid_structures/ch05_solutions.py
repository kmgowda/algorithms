"""Volume 11, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations


def letter_case_permutations(s: str) -> list[str]:
    """Exercise 1 (LeetCode 784): every way to change the case of each letter (digits stay)."""
    out: list[str] = []
    path: list[str] = []

    def go(i: int) -> None:
        if i == len(s):
            out.append("".join(path))
            return
        options = {s[i].lower(), s[i].upper()} if s[i].isalpha() else {s[i]}
        for ch in sorted(options):
            path.append(ch)
            go(i + 1)
            path.pop()

    go(0)
    return out


def add_operators(num: str, target: int) -> list[str]:
    """Exercise 2 (LeetCode 282): insert +, -, * between digits to reach a target.
    Keep the last multiplied term so '*' can 'undo' it: value - last + last * piece."""
    out: list[str] = []

    def go(i: int, expr: str, value: int, last: int) -> None:
        if i == len(num):
            if value == target:
                out.append(expr)
            return
        for j in range(i + 1, len(num) + 1):
            piece = num[i:j]
            if len(piece) > 1 and piece[0] == "0":
                break
            n = int(piece)
            if i == 0:
                go(j, piece, n, n)
            else:
                go(j, expr + "+" + piece, value + n, n)
                go(j, expr + "-" + piece, value - n, -n)
                go(j, expr + "*" + piece, value - last + last * n, last * n)

    go(0, "", 0, 0)
    return out


def is_balanced(s: str) -> bool:
    """Exercise 3: check a parentheses string with a counter."""
    depth = 0
    for ch in s:
        depth += 1 if ch == "(" else -1
        if depth < 0:
            return False
    return depth == 0


if __name__ == "__main__":
    print(letter_case_permutations("a1b"), add_operators("123", 6), add_operators("232", 8), is_balanced("(()())"))
