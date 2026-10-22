import random
import unittest

import ch20_examples as ex
import ch20_solutions as sol


def brute_cover(log):
    need, best = set(log), (0, 0)
    for i in range(len(log)):
        for j in range(i + 1, len(log) + 1):
            if set(log[i:j]) == need and (best[0] == 0 or j - i < best[0]):
                best = (j - i, i)
    return best


class TestShortestCovering(unittest.TestCase):
    def test_smallest(self) -> None:
        self.assertEqual(sol.shortest_covering(""), (0, 0))
        self.assertEqual(sol.shortest_covering("A"), (1, 0))
        self.assertEqual(sol.shortest_covering("AAAA"), (1, 0))
        self.assertEqual(sol.shortest_covering("AB"), (2, 0))

    def test_examples(self) -> None:
        self.assertEqual(sol.shortest_covering("ABCBDAEFB"), (6, 2))
        self.assertEqual(sol.shortest_covering("ABBACBA"), (3, 2))

    def test_random(self) -> None:
        rng = random.Random(20)
        for _ in range(1500):
            s = "".join(rng.choice("ABCD") for _ in range(rng.randint(0, 12)))
            got, want = sol.shortest_covering(s), brute_cover(s)
            self.assertEqual(got[0], want[0])
            self.assertEqual(set(s[got[1]:got[1] + got[0]]), set(s))


class TestIfBug(unittest.TestCase):
    def test_counterexample(self) -> None:
        self.assertEqual(ex.shortest_stretch([1, 1, 1, 12], 10), 1)
        self.assertEqual(sol.shortest_stretch_if([1, 1, 1, 12], 10), 3)

    def test_count_window_moves(self) -> None:
        rng = random.Random(7)
        for _ in range(300):
            c = [rng.randint(0, 9) for _ in range(rng.randint(1, 15))]
            t = rng.randint(1, 40)
            lengths = [j - i for i in range(len(c)) for j in range(i + 1, len(c) + 1) if sum(c[i:j]) >= t]
            self.assertEqual(ex.shortest_stretch(c, t), min(lengths) if lengths else 0)


if __name__ == "__main__":
    unittest.main()
