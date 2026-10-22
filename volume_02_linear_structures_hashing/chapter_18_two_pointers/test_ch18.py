import itertools
import random
import unittest

import ch18_examples as ex


class TestChapter34(unittest.TestCase):
    def test_every_case(self) -> None:
        for a, want in [([], []), ([7], [7]), ([5, 5, 5], [5]), ([1, 2, 3], [1, 2, 3]),
                        ([12, 12, 25, 31, 31, 31, 47, 63, 63], [12, 25, 31, 47, 63])]:
            b = list(a)
            self.assertEqual(b[:ex.dedupe_sorted(b)], want)
        self.assertEqual([ex.merge_sorted(a, b) for a, b in [([], [1, 2]), ([], []), ([1, 2], [3, 4]), ([3, 4], [1, 2]), ([5, 5], [5])]],
                         [([1, 2], 0), ([], 0), ([1, 2, 3, 4], 2), ([1, 2, 3, 4], 2), ([5, 5, 5], 2)])
        self.assertEqual([ex.best_bookends(h)[0] for h in ([], [4], [4, 4], [1, 2, 3, 4], [5, 5, 5, 5])], [0, 0, 4, 4, 15])
        self.assertEqual([ex.common_sorted(a, b) for a, b in [([], [1]), ([1, 2], [3, 4]), ([1, 2, 3], [1, 2, 3]), ([2, 2, 3], [2, 3, 3])]],
                         [[], [], [1, 2, 3], [2, 3]])

    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 12)))
            b = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 12)))
            c = a[:]
            k = ex.dedupe_sorted(c)
            self.assertEqual(c[:k], sorted(set(a)))
            self.assertEqual(ex.merge_sorted(a, b)[0], sorted(a + b))
            self.assertEqual(ex.common_sorted(sorted(set(a)), sorted(set(b))), sorted(set(a) & set(b)))
            h = [rng.randint(1, 10) for _ in range(rng.randint(2, 10))]
            brute = max((j - i) * min(h[i], h[j]) for i, j in itertools.combinations(range(len(h)), 2))
            self.assertEqual(ex.best_bookends(h)[0], brute)

    def test_examples(self) -> None:
        a = [5, 5, 5, 8, 9, 9]
        self.assertEqual(ex.dedupe_sorted(a), 3)
        self.assertEqual(a, [5, 8, 9, 8, 9, 9])
        self.assertEqual(ex.merge_sorted([3, 9, 14], [1, 4, 9, 20]), ([1, 3, 4, 9, 9, 14, 20], 6))
        self.assertEqual([v for *_, v in ex.best_bookends([3, 7, 2, 6, 4, 8, 5])[1]], [18, 25, 28, 6, 12, 4])
        self.assertEqual(ex.common_sorted([2, 4, 6, 8, 10], [3, 4, 5, 8, 11]), [4, 8])


class TestNewPractice(unittest.TestCase):
    def test_remove_value(self) -> None:
        a = [7, 0, 3, 0, 0, 9]
        self.assertEqual((ex.remove_value(a, 0), a[:3]), (3, [7, 3, 9]))
        self.assertEqual(ex.remove_value([], 0), 0)
        self.assertEqual(ex.remove_value([0, 0], 0), 0)
        self.assertEqual(ex.remove_value([1, 2], 0), 2)

    def test_palindrome(self) -> None:
        self.assertEqual(ex.is_palindrome("RACECAR"), (True, 3))
        self.assertEqual(ex.is_palindrome("LIBRARY"), (False, 1))
        self.assertEqual((ex.is_palindrome(""), ex.is_palindrome("A")), ((True, 0), (True, 0)))


if __name__ == "__main__":
    unittest.main()
