"""Volume 1, Chapter 21 - Text and Strings.

Run:  python3 ch21_examples.py
"""

from __future__ import annotations


def build_newsletter(pieces: list[str]) -> str:
    """Join many pieces with one copy of each character (Figure 21.4), instead of text = text + piece."""
    return "".join(pieces)


def copies_with_plus(pieces: list[str]) -> int:
    """Characters copied when building text with text = text + piece (Section 21.6)."""
    total, length = 0, 0
    for piece in pieces:
        length += len(piece)
        total += length
    return total


def find_all(text: str, word: str) -> list[int]:
    """Every starting position where word occurs in text, by sliding it along (Figure 21.5)."""
    matches = []
    for start in range(len(text) - len(word) + 1):
        k = 0
        while k < len(word) and text[start + k] == word[k]:
            k += 1
        if k == len(word):
            matches.append(start)
    return matches


def is_palindrome(word: str) -> bool:
    """True if word reads the same both ways, ignoring case: two pointers moving inward (Figure 21.6)."""
    left, right = 0, len(word) - 1
    while left < right:
        if word[left].lower() != word[right].lower():
            return False
        left, right = left + 1, right - 1
    return True


def letter_counts(text: str) -> dict[str, int]:
    """How often each letter appears, ignoring case and non-letters."""
    counts: dict[str, int] = {}
    for ch in text.lower():
        if ch.isalpha():
            counts[ch] = counts.get(ch, 0) + 1
    return counts


if __name__ == "__main__":
    print([ord(c) for c in "MAPS & MAYA"], find_all("a map of maps", "map"), find_all("banana", "ana"))
    print(is_palindrome("RACECAR"), is_palindrome("Never odd or even".replace(" ", "")), is_palindrome("BOOKS"))
    print(copies_with_plus(["x" * 10] * 200), len(build_newsletter(["x" * 10] * 200)), letter_counts("Maya maps"))
