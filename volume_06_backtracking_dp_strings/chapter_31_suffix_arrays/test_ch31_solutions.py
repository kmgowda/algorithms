import random
import unittest

import ch31_examples as ex
import ch31_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_block(self) -> None:
        r = random.Random(31)
        for _ in range(200):
            t = "".join(r.choice("ab") for _ in range(r.randint(1, 20)))
            p = "".join(r.choice("ab") for _ in range(r.randint(1, 4)))
            sa = ex.suffix_array_simple(t)
            idx = [k for k, i in enumerate(sa) if t.startswith(p, i)]
            self.assertEqual(idx, list(range(idx[0], idx[0] + len(idx))) if idx else [])

    def test_longest_prefix(self) -> None:
        sa = ex.suffix_array_simple("banana")
        self.assertEqual((sol.longest_occurring_prefix("banana", sa, "nanny"), sol.longest_occurring_prefix("banana", sa, "xyz")), ("nan", ""))
        r = random.Random(2)
        for _ in range(200):
            t = "".join(r.choice("ab") for _ in range(r.randint(1, 15)))
            q = "".join(r.choice("ab") for _ in range(r.randint(0, 8)))
            sa = ex.suffix_array_simple(t)
            want = max(k for k in range(len(q) + 1) if q[:k] in t)
            self.assertEqual(sol.longest_occurring_prefix(t, sa, q), q[:want])

    def test_whole_suffix_bug(self) -> None:
        sa = ex.suffix_array_simple("banana")
        self.assertEqual((sol.find_all_whole_suffixes("banana", sa, "ana"), ex.find_all("banana", sa, "ana")[0]), ([3], [1, 3]))


if __name__ == "__main__":
    unittest.main()
