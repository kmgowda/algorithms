import random
import unittest

import ch16_examples as ex
import ch16_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_last_match(self) -> None:
        r = random.Random(16)
        for _ in range(200):
            a = "".join(r.choice("ABC") for _ in range(r.randint(1, 8)))
            b = "".join(r.choice("ABC") for _ in range(r.randint(1, 8)))
            if a[-1] == b[-1]:
                self.assertEqual(ex.lcs(a, b)[0], ex.lcs(a[:-1], b[:-1])[0] + 1)

    def test_super(self) -> None:
        s = sol.shortest_super(ex.ANA, ex.BEN)
        self.assertEqual(len(s), 9)
        r = random.Random(2)
        for _ in range(200):
            a = "".join(r.choice("ABC") for _ in range(r.randint(0, 8)))
            b = "".join(r.choice("ABC") for _ in range(r.randint(0, 8)))
            s = sol.shortest_super(a, b)
            self.assertTrue(sol.is_subsequence(a, s) and sol.is_subsequence(b, s))
            self.assertEqual(len(s), len(a) + len(b) - ex.lcs(a, b)[0])

    def test_greedy(self) -> None:
        self.assertEqual(sol.greedy_trap(), ("ABA", "BBA"))
        self.assertEqual((sol.greedy_common(ex.ANA, ex.BEN), ex.lcs(ex.ANA, ex.BEN)[0]), (3, 4))


if __name__ == "__main__":
    unittest.main()
