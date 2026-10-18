import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def naive(t, p):
    return [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]


def brute_pi(p):
    return [max((k for k in range(i + 1) if p[:k] == p[i + 1 - k:i + 1] and k <= i), default=0) for i in range(len(p))]


class TestKMP(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            t = "".join(rng.choice("ab") for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 6)))
            self.assertEqual(ex.prefix_function(p), brute_pi(p))
            found, comps = ex.kmp_search(t, p)
            self.assertEqual(found, naive(t, p))
            self.assertLessEqual(comps, 2 * len(t))
            cuts = sorted(rng.sample(range(len(t) + 1), min(3, len(t) + 1)))
            chunks = [t[a:b] for a, b in zip([0] + cuts, cuts + [len(t)])]
            self.assertEqual(ex.stream_alarm(chunks, p), naive(t, p))
            s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 10)))
            self.assertEqual(sol.repeated_substring_pattern(s),
                             any(len(s) % k == 0 and s[:k] * (len(s) // k) == s for k in range(1, len(s))))
            pal = sol.shortest_palindrome(s)
            self.assertEqual(pal, pal[::-1])
            self.assertTrue(pal.endswith(s))
            best = min(len(s) - k for k in range(len(s) + 1) if s[:k] == s[:k][::-1])
            self.assertEqual(len(pal) - len(s), best)

    def test_examples(self) -> None:
        self.assertEqual(ex.prefix_function("ababaca"), [0, 0, 1, 2, 3, 0, 1])
        self.assertEqual(ex.kmp_search("abababa", "aba")[0], [0, 2, 4])
        t, p = "a" * 10000, "a" * 49 + "b"
        self.assertLess(ex.kmp_search(t, p)[1] * 20, ex.naive_comparisons(t, p))
        self.assertEqual(ex.stream_alarm(["GET /ind", "ex.html?id=1 UNI", "ON SELECT pass"], "UNION SELECT"), [21])
        self.assertEqual(sol.longest_happy_prefix("ababab"), "abab")
        self.assertEqual(sol.shortest_palindrome("aacecaaa"), "aaacecaaa")
        self.assertEqual(sol.shortest_palindrome("abcd"), "dcbabcd")


if __name__ == "__main__":
    unittest.main()
