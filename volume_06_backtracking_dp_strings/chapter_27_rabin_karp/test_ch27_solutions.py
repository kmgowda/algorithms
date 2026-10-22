import random
import unittest

import ch27_examples as ex
import ch27_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_rolling(self) -> None:
        t = ex.NEWSLETTER
        for m in (1, 3, 7):
            for mod in (7, 101, 1_000_000_007):
                self.assertEqual(sol.rolled(t, m, mod), [ex.fingerprint(t[s:s + m], mod) for s in range(len(t) - m + 1)])

    def test_distinct(self) -> None:
        r = random.Random(27)
        for _ in range(100):
            t = "".join(r.choice("ab") for _ in range(r.randint(1, 30)))
            m = r.randint(1, len(t))
            self.assertEqual(sol.distinct_windows(t, m, mod=7), len({t[i:i + m] for i in range(len(t) - m + 1)}))
        self.assertEqual(sol.distinct_windows(ex.NEWSLETTER, 4), 67)

    def test_trusting(self) -> None:
        self.assertEqual(sol.trusting_search(ex.NEWSLETTER, "club", 101), [12, 23, 38, 48, 52])
        self.assertEqual(ex.rabin_karp(ex.NEWSLETTER, "club", 101)[0], [12, 38])


if __name__ == "__main__":
    unittest.main()
