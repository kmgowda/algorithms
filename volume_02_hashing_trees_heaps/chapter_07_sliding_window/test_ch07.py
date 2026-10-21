import random
import unittest

import ch07_examples as ex


class TestChapter36(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(400):
            c = [rng.randint(0, 9) for _ in range(rng.randint(1, 12))]
            k = rng.randint(1, len(c))
            self.assertEqual(ex.window_totals(c, k), [sum(c[i:i + k]) for i in range(len(c) - k + 1)])
            t = rng.randint(1, 40)
            lengths = [j - i for i in range(len(c)) for j in range(i + 1, len(c) + 1) if sum(c[i:j]) >= t]
            self.assertEqual(ex.shortest_stretch(c, t), min(lengths) if lengths else 0)
            quiet = [j - i for i in range(len(c)) for j in range(i + 1, len(c) + 1) if sum(c[i:j]) <= t]
            self.assertEqual(ex.longest_quiet(c, t)[0], max(quiet) if quiet else 0)
            s = "".join(rng.choice("ABCD") for _ in range(rng.randint(0, 12)))
            clean = [j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if len(set(s[i:j])) == j - i]
            self.assertEqual(ex.longest_without_repeats(s)[0], max(clean) if clean else 0)

    def test_examples(self) -> None:
        self.assertEqual(ex.shortest_stretch(ex.VISITS, 15), 3)
        self.assertEqual(ex.shortest_stretch(ex.VISITS, 20), 4)
        self.assertEqual(ex.longest_without_repeats("ABCBDAEFB"), (6, 2))
        self.assertEqual(ex.longest_without_repeats("LIBRARIAN"), (5, 0))
        self.assertEqual(ex.longest_quiet([2, 4, 1, 0, 3, 7, 1, 1, 2, 5], 12), (5, 0))
        self.assertEqual(ex.longest_quiet([2, 4, 1, 0, 3, 7, 1, 1, 2, 5], 6), (3, 1))


if __name__ == "__main__":
    unittest.main()
