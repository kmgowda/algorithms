"""Volume 11, Chapter 5 - Generating Valid Structures: Parentheses, Phone Letter Combinations, IP Addresses.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

KEYPAD = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def balanced_parentheses(pairs: int) -> list[str]:
    """LeetCode 22: every well-formed string of n pairs. Rules checked while building:
    add '(' if any are left; add ')' only if it closes an open one. Never builds an invalid prefix."""
    out: list[str] = []
    path: list[str] = []

    def go(opened: int, closed: int) -> None:
        if len(path) == 2 * pairs:
            out.append("".join(path))
            return
        if opened < pairs:
            path.append("(")
            go(opened + 1, closed)
            path.pop()
        if closed < opened:
            path.append(")")
            go(opened, closed + 1)
            path.pop()

    go(0, 0)
    return out


def phone_words(digits: str) -> list[str]:
    """LeetCode 17: every letter string a keypad number could spell (one level per digit)."""
    if not digits:
        return []
    out: list[str] = []
    path: list[str] = []

    def go(i: int) -> None:
        if i == len(digits):
            out.append("".join(path))
            return
        for letter in KEYPAD[digits[i]]:
            path.append(letter)
            go(i + 1)
            path.pop()

    go(0)
    return out


def restore_ip_addresses(s: str) -> list[str]:
    """LeetCode 93: split a digit string into 4 parts, each 0-255 with no leading zeros.
    Prune when the digits left can't fill the remaining parts (each part takes 1 to 3 digits)."""
    out: list[str] = []
    parts: list[str] = []

    def go(start: int) -> None:
        left = len(s) - start
        need = 4 - len(parts)
        if left < need or left > 3 * need:
            return                                        # impossible to finish: prune
        if need == 0:
            out.append(".".join(parts))
            return
        for length in (1, 2, 3):
            piece = s[start:start + length]
            if len(piece) < length or (piece[0] == "0" and length > 1) or int(piece) > 255:
                break
            parts.append(piece)
            go(start + length)
            parts.pop()

    go(0)
    return out


def palindrome_partitions(s: str) -> list[list[str]]:
    """LeetCode 131: cut a string into pieces that are all palindromes - only cut off palindromic prefixes."""
    out: list[list[str]] = []
    path: list[str] = []

    def go(start: int) -> None:
        if start == len(s):
            out.append(list(path))
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece == piece[::-1]:
                path.append(piece)
                go(end)
                path.pop()

    go(0)
    return out


def vanity_numbers(digits: str, dictionary: set[str]) -> list[str]:
    """Industry example: which dictionary words can a business phone number spell? (1-800-FLOWERS style)"""
    return [w for w in phone_words(digits) if w in dictionary]


if __name__ == "__main__":
    print(balanced_parentheses(3))
    print(phone_words("23"))
    print(restore_ip_addresses("25525511135"), restore_ip_addresses("101023"))
    print(palindrome_partitions("aab"))
    print(vanity_numbers("4357", {"help", "gelp", "hello", "idea"}))
