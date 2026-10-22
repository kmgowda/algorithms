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
    """True if word reads the same both ways, ignoring case: two pointers moving inward (Figure 21.7)."""
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


def compare(a: str, b: str) -> tuple[int, int]:
    """Dictionary order by code points: (-1, 0 or 1, character pairs looked at). Stops at the first difference."""
    looked = 0
    for x, y in zip(a, b):
        looked += 1
        if x != y:
            return (-1 if x < y else 1), looked
    return (len(a) > len(b)) - (len(a) < len(b)), looked


def substrings(text: str) -> list[str]:
    """Every non-empty run of neighbouring characters, by start and length: n(n + 1)/2 of them (Figure 21.6)."""
    return [text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1)]


def subsequences(text: str) -> list[str]:
    """Every way of keeping some characters in their order, gaps allowed: 2^n of them, the empty one included."""
    if not text:
        return [""]
    rest = subsequences(text[1:])
    return [text[0] + s for s in rest] + rest


def utf8_lengths(text: str) -> list[int]:
    """Bytes that UTF-8 uses for each character of text."""
    return [len(ch.encode("utf-8")) for ch in text]


if __name__ == "__main__":
    print([ord(c) for c in "MAPS & MAYA"], find_all("a map of maps", "map"), find_all("banana", "ana"))
    print(is_palindrome("RACECAR"), is_palindrome("Never odd or even".replace(" ", "")), is_palindrome("BOOKS"))
    print(compare("map", "maps"), compare("Maya", "maya"), compare("library", "librarian"), compare("", ""))
    print(substrings("MAP"), subsequences("MAP"), len(substrings("LIBRARY")), len(subsequences("LIBRARY")))
    print(utf8_lengths("café 😀"), len("café"), len("café".encode("utf-8")))
    print(copies_with_plus(["x" * 10] * 200), len(build_newsletter(["x" * 10] * 200)), letter_counts("Maya maps"))
