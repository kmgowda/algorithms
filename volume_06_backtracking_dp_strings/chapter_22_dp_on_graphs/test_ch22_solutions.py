import unittest

import ch22_examples as ex
import ch22_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_at_most_k(self) -> None:
        for k in range(0, 5):
            self.assertEqual(ex.at_most_k(ex.DEPOTS, ex.LEGS, "A", k)[-1], sol.brute_at_most(ex.DEPOTS, ex.LEGS, "A", k))

    def test_walks(self) -> None:
        self.assertEqual(sol.walks_exactly(ex.DEPOTS, ex.LEGS, "A", 2), {"A": 0, "B": 0, "C": 1, "D": 2, "E": 2})
        self.assertEqual(sol.walks_exactly(ex.DEPOTS, ex.LEGS, "A", 0), {"A": 1, "B": 0, "C": 0, "D": 0, "E": 0})
        for k in range(4):
            got = sol.walks_exactly(ex.DEPOTS, ex.LEGS, "A", k)
            self.assertEqual(sum(got.values()), sum(1 for _ in _walks(k)))

    def test_in_place_bug(self) -> None:
        bad = sol.at_most_k_in_place(ex.DEPOTS, ex.LEGS, "A", 1)
        self.assertEqual((bad["B"], bad["D"], bad["E"]), (2, 4, 2))
        self.assertEqual(ex.at_most_k(ex.DEPOTS, ex.LEGS, "A", 1)[-1]["D"], float("inf"))


def _walks(k, at="A"):
    if k == 0:
        yield ()
        return
    for a, b, _ in ex.LEGS:
        if a == at:
            for rest in _walks(k - 1, b):
                yield ((a, b),) + rest


if __name__ == "__main__":
    unittest.main()
