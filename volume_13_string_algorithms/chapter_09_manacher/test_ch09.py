import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


def is_pal(x):
    return x == x[::-1]


class TestManacher(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 15)))
            subs = [s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]
            best = max((len(x) for x in subs if is_pal(x)), default=0)
            self.assertEqual(len(ex.longest_palindrome(s)), best)
            self.assertTrue(is_pal(ex.longest_palindrome(s)))
            self.assertEqual(len(ex.expand_around_centers(s)), best)
            self.assertEqual(ex.count_palindromes(s), sum(map(is_pal, subs)))
            if s:
                i = rng.randrange(len(s))
                j = rng.randrange(i, len(s))
                self.assertEqual(sol.is_palindrome_query(s, i, j), is_pal(s[i:j + 1]))
                self.assertEqual(len(sol.longest_palindromic_prefix(s)), max(k for k in range(1, len(s) + 1) if is_pal(s[:k])))
                for k, r in enumerate(sol.palindrome_lengths_at_centres(s)):
                    self.assertEqual(r, max(2 * d + 1 for d in range(len(s)) if k - d >= 0 and k + d < len(s) and is_pal(s[k - d:k + d + 1])))

    def test_examples(self) -> None:
        self.assertEqual(ex.manacher_radii("abaaba"), [0, 1, 0, 3, 0, 1, 6, 1, 0, 3, 0, 1, 0])
        self.assertEqual(ex.longest_palindrome("forgeeksskeegfor"), "geeksskeeg")
        self.assertEqual(ex.count_palindromes("aaa"), 6)
        r = ex.race("a" * 1500)
        self.assertLess(r["Manacher"], r["expand around centres"])
        self.assertEqual(ex.palindromic_sites("TTGAATTCAAGGATCC", 6), ["GAATTC", "GGATCC", "TGAATTCA", "TTGAATTCAA"])


if __name__ == "__main__":
    unittest.main()
