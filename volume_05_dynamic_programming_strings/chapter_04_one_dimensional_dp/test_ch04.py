import itertools
import unittest

import ch04_examples as ex


class TestChapter4(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(ex.fewest_coins(6, ex.ODD), (2, [3, 3], [0, 1, 2, 1, 1, 2, 2]))
        self.assertEqual(ex.fewest_coins(30, [25, 10, 1])[:2], (3, [10, 10, 10]))
        self.assertEqual(ex.best_evenings(ex.TALKS), (23, [1, 3, 6], [0, 6, 6, 15, 15, 18, 23, 23]))

    def test_every_case(self) -> None:
        self.assertEqual([ex.fewest_coins(a, c)[:2] for a, c in ((0, ex.ODD), (7, [5, 2]), (3, [5, 2]), (5, []))],
                         [(0, []), (2, [5, 2]), (None, []), (None, [])])
        self.assertEqual([ex.best_evenings(t)[:2] for t in ([], [5], [5, 9], [4, 4, 4, 4])],
                         [(0, []), (5, [1]), (9, [2]), (8, [1, 3])])
        self.assertEqual((ex.fewest_coins(8, ex.ODD)[0], ex.fewest_coins(14, [1, 7, 10, 22])[1], ex.best_evenings(ex.TALKS + [5])[0]), (2, [7, 7], 28))
        t = list(ex.TALKS)
        t[3] = 20
        self.assertEqual(ex.best_evenings(t)[:2], (34, [1, 4, 6]))
        self.assertEqual(max(a for a in range(40) if ex.fewest_coins(a, [4, 7])[0] is None), 17)
        for n in range(1, 9):
            talks = [(i * 7) % 10 + 1 for i in range(n)]
            brute = max(sum(talks[i] for i in s) for k in range(n + 1) for s in itertools.combinations(range(n), k)
                        if all(b - a > 1 for a, b in zip(s, s[1:])))
            self.assertEqual(ex.best_evenings(talks)[0], brute)


if __name__ == "__main__":
    unittest.main()
