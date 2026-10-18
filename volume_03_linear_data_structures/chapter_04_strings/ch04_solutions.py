"""Volume 3, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations


def is_rotation(a: str, b: str) -> bool:
    """Exercise 1: 'lion' rotated is 'onli'. b is a rotation of a exactly when b appears inside a + a."""
    return len(a) == len(b) and b in a + a


def run_length_decode(encoded: str) -> str:
    """Exercise 2: 'a3b1c2' -> 'aaabcc' (the reverse of V1-C8's compress). Digits may be several long."""
    out: list[str] = []
    i = 0
    while i < len(encoded):
        letter = encoded[i]
        i += 1
        start = i
        while i < len(encoded) and encoded[i].isdigit():
            i += 1
        out.append(letter * int(encoded[start:i]))
    return "".join(out)


def count_character_types(text: str) -> dict[str, int]:
    """Exercise 3: letters, digits, spaces, and other symbols."""
    counts = {"letters": 0, "digits": 0, "spaces": 0, "other": 0}
    for ch in text:
        if ch.isalpha():
            counts["letters"] += 1
        elif ch.isdigit():
            counts["digits"] += 1
        elif ch.isspace():
            counts["spaces"] += 1
        else:
            counts["other"] += 1
    return counts


def slugify(title: str) -> str:
    """Exercise 4 (industry): 'Top 10 Zoo Animals!' -> 'top-10-zoo-animals' for web addresses."""
    pieces: list[str] = []
    word: list[str] = []
    for ch in title.lower():
        if ch.isalnum():
            word.append(ch)
        elif word:
            pieces.append("".join(word))
            word = []
    if word:
        pieces.append("".join(word))
    return "-".join(pieces)


def wrap_text(text: str, width: int) -> list[str]:
    """Exercise 5: break text into lines of at most `width` characters, never splitting words."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


if __name__ == "__main__":
    print(is_rotation("lion", "onli"), run_length_decode("a3b1c12"), count_character_types("Bus 42 leaves!"))
    print(slugify("Top 10 Zoo Animals!"), wrap_text("the quick brown fox jumps over the lazy dog", 10))
