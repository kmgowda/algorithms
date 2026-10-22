import random
import unittest

import ch24_examples as ex


class TestChapter40(unittest.TestCase):
    def test_every_case(self) -> None:
        s = [12, 25, 31, 47, 58, 63, 70, 84, 91]
        self.assertEqual([ex.present_sorted(s, x) for x in (12, 91, 50, 5, 95)], [True, True, False, False, False])
        self.assertFalse(ex.present_sorted([], 5))
        for a, b, want in [(30, 60, [31, 47, 58]), (58, 58, [58]), (60, 30, []), (0, 100, s), (92, 99, [])]:
            self.assertEqual((ex.range_sorted(s, a, b), ex.range_hashed(set(s), a, b)), (want, want))
        self.assertEqual((ex.range_sorted([], 1, 5), ex.range_hashed(set(), 1, 5)), ([], []))

    def test_all_agree(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            data = rng.sample(range(100), rng.randint(0, 30))
            srt, st = sorted(data), set(data)
            x = rng.randint(0, 99)
            self.assertEqual(ex.present_unsorted(data, x), ex.present_sorted(srt, x))
            self.assertEqual(ex.present_sorted(srt, x), x in st)
            a = rng.randint(0, 99); b = rng.randint(a, 99)
            self.assertEqual(ex.range_sorted(srt, a, b), ex.range_hashed(st, a, b))

    def test_shape_of_timings(self) -> None:
        t = ex.measure(20_000)
        self.assertLess(t["1000 lookups: hash set"], t["1000 lookups: unsorted list"])
        self.assertLess(t["100 ranges: sorted + bisect"], t["100 ranges: hash set"])


if __name__ == "__main__":
    unittest.main()
