"""Volume 3, Chapter 4 - Strings: Characters, Encodings, Immutability, and String Building.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

import unicodedata


# ------------------------------------------------------------------ characters are numbers
def code_points(text: str) -> list[int]:
    """Every character is stored as a number called its code point."""
    return [ord(ch) for ch in text]


def utf8_size(text: str) -> tuple[int, int]:
    """(characters, bytes when saved as UTF-8). English letters take 1 byte; others take 2-4."""
    return len(text), len(text.encode("utf-8"))


def caesar_shift(text: str, shift: int) -> str:
    """Beginner example: a secret-message wheel. Shift letters, keep everything else."""
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)


# ------------------------------------------------------------------ building strings
class StringBuilder:
    """Collect pieces cheaply, then join once. Mirrors Java's StringBuilder / C#'s StringBuilder."""

    def __init__(self) -> None:
        self._pieces: list[str] = []
        self._length = 0

    def add(self, piece: str) -> "StringBuilder":
        self._pieces.append(piece)
        self._length += len(piece)
        return self                     # returning self allows chaining: sb.add("a").add("b")

    def __len__(self) -> int:
        return self._length

    def build(self) -> str:
        return "".join(self._pieces)


def receipt(items: list[tuple[str, int, float]]) -> str:
    """Practical example: a shop receipt built with StringBuilder."""
    sb = StringBuilder()
    total = 0.0
    for name, qty, price in items:
        line_total = qty * price
        total += line_total
        sb.add(f"{name:<10}{qty:>3} x {price:>6.2f} = {line_total:>7.2f}\n")
    sb.add(f"{'TOTAL':<23}{total:>8.2f}\n")
    return sb.build()


# ------------------------------------------------------------------ classic string problems
def reverse_words(sentence: str) -> str:
    """LeetCode 151: words in reverse order, single spaces."""
    return " ".join(reversed(sentence.split()))


def longest_common_prefix(words: list[str]) -> str:
    """LeetCode 14: e.g. the shared start of file names or URLs. O(total characters)."""
    if not words:
        return ""
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def is_palindrome_two_pointers(text: str) -> bool:
    """Index-based check without building a reversed copy: O(1) extra space."""
    i, j = 0, len(text) - 1
    while i < j:
        if text[i] != text[j]:
            return False
        i, j = i + 1, j - 1
    return True


# ------------------------------------------------------------------ industry
def normalize_username(name: str) -> str:
    """Industry example: 'Zoë', 'Zoe\u0308' and ' ZOË ' must be the SAME account.

    NFC normalization merges characters that can be written in two ways; casefold() is a
    stronger lower() designed for comparing text in many languages.
    """
    return unicodedata.normalize("NFC", name.strip()).casefold()


def mask_card_number(card: str) -> str:
    """Industry example: show only the last 4 digits on receipts and screens."""
    digits = [ch for ch in card if ch.isdigit()]
    if len(digits) < 4:
        raise ValueError("card number too short")
    return "**** " * 3 + "".join(digits[-4:])


if __name__ == "__main__":
    print("Code points of 'Zoo':", code_points("Zoo"), "| chr(90) =", chr(90))
    for word in ("zebra", "Zoë", "动物园", "🦁"):
        print(f"{word!r}: (characters, UTF-8 bytes) = {utf8_size(word)}")
    secret = caesar_shift("Meet at the Lion Gate!", 3)
    print(secret, "->", caesar_shift(secret, -3))
    print(receipt([("Mango", 3, 40.0), ("Bread", 1, 55.5), ("Milk", 2, 30.25)]))
    print(reverse_words("  the  quick brown   fox "), "|", longest_common_prefix(["flower", "flow", "flight"]))
    print(normalize_username(" ZOË ") == normalize_username("zoe\u0308"), mask_card_number("4111 1111 1111 1234"))
