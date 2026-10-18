"""Volume 12, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

from ch07_examples import longest_palindromic_subsequence, palindrome_table


def min_palindrome_cuts(s: str) -> int:
    """Exercise 1 (LeetCode 132): fewest cuts so every piece is a palindrome. cuts[i] for the prefix s[:i]."""
    if not s:
        return 0
    pal = palindrome_table(s)
    cuts = [-1] + [0] * len(s)
    for i in range(1, len(s) + 1):
        cuts[i] = min(cuts[j] + 1 for j in range(i) if pal[j][i - 1])
    return cuts[len(s)]


def all_sentences(text: str, words: list[str]) -> list[str]:
    """Exercise 2 (LeetCode 140): every way to split the text into words - memoize the suffix answers."""
    vocab = set(words)
    memo: dict[int, list[str]] = {len(text): [""]}

    def from_pos(i: int) -> list[str]:
        if i not in memo:
            out = []
            for j in range(i + 1, len(text) + 1):
                if text[i:j] in vocab:
                    out += [text[i:j] + (" " + rest if rest else "") for rest in from_pos(j)]
            memo[i] = out
        return memo[i]

    return sorted(from_pos(0))


def min_insertions_to_palindrome(s: str) -> int:
    """Exercise 3 (LeetCode 1312): letters to insert to make a palindrome = length - longest palindromic subsequence."""
    return len(s) - longest_palindromic_subsequence(s)


if __name__ == "__main__":
    print(min_palindrome_cuts("aab"), all_sentences("catsanddog", ["cat", "cats", "and", "sand", "dog"]),
          min_insertions_to_palindrome("mbadm"))
