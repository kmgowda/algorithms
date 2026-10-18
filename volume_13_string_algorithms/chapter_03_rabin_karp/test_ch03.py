import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


def naive(t, p):
    return [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]


class TestRabinKarp(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            t = "".join(rng.choice("abc") for _ in range(rng.randint(0, 30)))
            p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
            self.assertEqual(ex.rabin_karp(t, p)[0], naive(t, p))
            self.assertEqual(ex.rabin_karp(t, p, mod=7)[0], naive(t, p))       # collisions must not cause errors
            pats = list({"".join(rng.choice("abc") for _ in range(2)) for _ in range(3)})
            got = ex.multi_pattern(t, pats)
            self.assertEqual(got, {q: naive(t, q) for q in pats})
            s = "".join(rng.choice("ab") for _ in range(rng.randint(2, 12)))
            best = max((s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s.count(s[i:j]) > 1 or
                        any(s[k:k + j - i] == s[i:j] for k in range(len(s)) if k != i)), key=len, default="")
            self.assertEqual(len(sol.longest_duplicate_substring(s)), len(best))
            k = rng.randint(1, 4)
            self.assertEqual(sol.count_distinct_windows(s, k), len({s[i:i + k] for i in range(len(s) - k + 1)}))

    def test_examples(self) -> None:
        self.assertEqual(ex.rabin_karp("abracadabra", "abra"), ([0, 7], 0))
        found, spurious = ex.rabin_karp("abracadabra" * 50, "cad", mod=31)
        self.assertEqual(len(found), 50)
        self.assertGreater(spurious, 0)
        self.assertEqual(sorted(ex.shared_passages("to be or not to be", "not to be outdone", 8)), ["not to b", "ot to be"])
        self.assertEqual(sol.longest_duplicate_substring("banana"), "ana")
        self.assertTrue(sol.is_rotation("waterbottle", "erbottlewat"))
        self.assertFalse(sol.is_rotation("abc", "acb"))


if __name__ == "__main__":
    unittest.main()
