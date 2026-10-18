"""Volume 13, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations

from ch04_examples import prefix_function


def repeated_substring_pattern(s: str) -> bool:
    """Exercise 1 (LeetCode 459): is s some block repeated? With border b = pi[-1], the block length n - b must divide n."""
    if not s:
        return False
    b = prefix_function(s)[-1]
    return b > 0 and len(s) % (len(s) - b) == 0


def longest_happy_prefix(s: str) -> str:
    """Exercise 2 (LeetCode 1392): the longest proper prefix that is also a suffix - exactly pi[-1]."""
    return s[:prefix_function(s)[-1]] if s else ""


def shortest_palindrome(s: str) -> str:
    """Exercise 3 (LeetCode 214): add the fewest letters in FRONT to make a palindrome.
    The longest palindromic prefix = the border of s + '#' + reverse(s)."""
    combined = s + "#" + s[::-1]
    keep = prefix_function(combined)[-1]
    return s[keep:][::-1] + s


if __name__ == "__main__":
    print(repeated_substring_pattern("abcabcabc"), repeated_substring_pattern("aba"),
          longest_happy_prefix("ababab"), shortest_palindrome("aacecaaa"), shortest_palindrome("abcd"))
