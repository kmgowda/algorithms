import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


def naive(t, p):
    return [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]


class TestZBoyerMoore(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 20)))
            z = ex.z_array(s)
            for i in range(1, len(s)):
                k = 0
                while i + k < len(s) and s[k] == s[i + k]:
                    k += 1
                self.assertEqual(z[i], k)
            p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
            t = "".join(rng.choice("abc") for _ in range(rng.randint(0, 30)))
            self.assertEqual(ex.z_search(t, p), naive(t, p))
            self.assertEqual(ex.horspool(t, p)[0], naive(t, p))
            self.assertEqual(sol.count_distinct_substrings(s), len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)}))
            if s:
                per = sol.string_period(s)
                self.assertTrue(all(s[i] == s[i % per] for i in range(len(s))))
                self.assertFalse(any(all(s[i] == s[i % q] for i in range(len(s))) for q in range(1, per)))

    def test_examples(self) -> None:
        self.assertEqual(ex.z_array("aabxaab"), [7, 1, 0, 0, 3, 1, 0])
        doc = ex.english_like(20000) + " needle in a haystack"
        found, bm = ex.horspool(doc, "needle in a haystack")
        self.assertEqual(len(found), 1)
        self.assertLess(bm * 5, ex.naive_comparisons(doc, "needle in a haystack"))
        self.assertEqual(ex.find_in_document("To be, or not to be, that is the question", "to be"), [14])
        self.assertEqual(sol.bad_character_table("needle"), {"n": 5, "e": 3, "d": 2, "l": 1})


if __name__ == "__main__":
    unittest.main()
