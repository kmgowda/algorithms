import random
import unittest

import ch32_examples as ex
import ch32_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_linear(self) -> None:
        r = random.Random(32)
        for _ in range(200):
            t = "".join(r.choice("ab") for _ in range(r.randint(1, 60)))
            self.assertLessEqual(sol.kasai_comparisons(t), 2 * len(t))

    def test_repeat_k(self) -> None:
        self.assertEqual([sol.longest_repeat_k("banana", k) for k in (2, 3, 4)], ["ana", "a", ""])
        r = random.Random(2)
        for _ in range(150):
            t = "".join(r.choice("ab") for _ in range(r.randint(1, 14)))
            k = r.randint(2, 4)
            got = sol.longest_repeat_k(t, k)
            count = lambda s: sum(1 for i in range(len(t) - len(s) + 1) if t.startswith(s, i))
            best = max((j - i for i in range(len(t)) for j in range(i + 1, len(t) + 1) if count(t[i:j]) >= k), default=0)
            self.assertEqual(len(got), best)
            if got:
                self.assertGreaterEqual(count(got), k)

    def test_unchecked(self) -> None:
        self.assertEqual((sol.longest_common_unchecked("abcabc", "bcx"), ex.longest_common("abcabc", "bcx")), ("abc", "bc"))


if __name__ == "__main__":
    unittest.main()
