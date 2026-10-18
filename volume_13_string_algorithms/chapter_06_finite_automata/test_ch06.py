import itertools
import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


def naive(t, p):
    return [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]


class TestAutomata(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 5)))
            t = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 30)))
            self.assertEqual(ex.dfa_search(t, p, "abc"), naive(t, p))
            self.assertEqual(sol.ends_with_pattern(t, p, "abcd"), t.endswith(p))
            delta = ex.build_dfa(p, "abc")
            for q in range(len(p) + 1):
                for c in "abc":
                    s = p[:q] + c
                    expected = max(k for k in range(min(len(p), len(s)) + 1) if s.endswith(p[:k]))
                    if q == len(p):
                        s = p + c
                        expected = max(k for k in range(len(p) + 1) if k <= len(p) and s.endswith(p[:k]) and k < len(s) + 1)
                    self.assertEqual(delta[q][c], expected)
        for n in range(0, 8):
            for p in ("11", "101"):
                self.assertEqual(sol.count_avoiding(n, p, "01"), sum(1 for s in itertools.product("01", repeat=n) if p not in "".join(s)))
        for v in range(200):
            self.assertEqual(sol.divisible_by_three(bin(v)[2:]), v % 3 == 0)

    def test_examples(self) -> None:
        self.assertEqual(ex.dfa_search("abababacaba", "ababaca", "abc"), [2])
        self.assertEqual([ex.is_valid_id(x) for x in ("AB-1234", "A-1234", "AB-12x4", "ab-1234")], [True, False, False, False])
        self.assertEqual(len(ex.dfa_table("ababaca", "abc")), 9)


if __name__ == "__main__":
    unittest.main()
