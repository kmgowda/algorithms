import itertools
import math
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


def brute_ip(s):
    out = []
    for cuts in itertools.combinations(range(1, len(s)), 3):
        parts = [s[a:b] for a, b in zip((0,) + cuts, cuts + (len(s),))]
        if all(p and (p == "0" or p[0] != "0") and int(p) <= 255 and len(p) <= 3 for p in parts):
            out.append(".".join(parts))
    return sorted(out)


class TestValidStructures(unittest.TestCase):
    def test_parentheses(self) -> None:
        for n in range(0, 7):
            got = ex.balanced_parentheses(n)
            self.assertEqual(len(got), math.comb(2 * n, n) // (n + 1))          # Catalan numbers
            brute = sorted("".join(p) for p in set(itertools.product("()", repeat=2 * n)) if sol.is_balanced("".join(p)))
            self.assertEqual(sorted(got), brute)

    def test_phone_ip_palindromes(self) -> None:
        self.assertEqual(ex.phone_words("23"), ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"])
        self.assertEqual(ex.phone_words(""), [])
        self.assertEqual(len(ex.phone_words("79")), 16)
        rng = random.Random(1)
        for _ in range(100):
            s = "".join(rng.choice("0123456789") for _ in range(rng.randint(1, 13)))
            self.assertEqual(sorted(ex.restore_ip_addresses(s)), brute_ip(s))
        for _ in range(50):
            s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 8)))
            parts = ex.palindrome_partitions(s)
            self.assertTrue(all("".join(p) == s and all(x == x[::-1] for x in p) for p in parts))
            brute = 0
            for mask in range(1 << (len(s) - 1)):
                pieces, cur = [], s[0]
                for i in range(1, len(s)):
                    if mask >> (i - 1) & 1:
                        pieces.append(cur)
                        cur = s[i]
                    else:
                        cur += s[i]
                pieces.append(cur)
                brute += all(x == x[::-1] for x in pieces)
            self.assertEqual(len(parts), brute)
        self.assertEqual(ex.vanity_numbers("4357", {"help", "gelp", "hello", "idea"}), ["gelp", "help"])

    def test_solutions(self) -> None:
        self.assertEqual(sol.letter_case_permutations("a1b"), ["A1B", "A1b", "a1B", "a1b"])
        self.assertEqual(sorted(sol.add_operators("123", 6)), ["1*2*3", "1+2+3"])
        self.assertEqual(sorted(sol.add_operators("232", 8)), ["2*3+2", "2+3*2"])
        self.assertEqual(sol.add_operators("105", 5), ["1*0+5", "10-5"])
        for e in sol.add_operators("1234", 10):
            self.assertEqual(eval(e), 10)


if __name__ == "__main__":
    unittest.main()
