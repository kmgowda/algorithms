import random
import unittest

import ch16_examples as ex


class TestChapter19(unittest.TestCase):
    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            a = [rng.randint(0, 50) for _ in range(rng.randint(0, 60))]
            for fan in (2, 3, None):
                block = rng.randint(1, 4)
                out, _, _ = ex.external_sort(a, block * rng.randint(3, 10), block, fan)
                self.assertEqual(out, sorted(a))

    def test_fan_in(self) -> None:
        rng = random.Random(1)
        big = [rng.randrange(10 ** 6) for _ in range(100_000)]
        for fan, passes, io in [(2, 7, 8000), (4, 4, 5000), (9, 3, 4000), (None, 3, 4000), (50, 3, 4000)]:
            out, d, p = ex.external_sort(big, 1000, 100, fan)
            self.assertEqual((p, d.reads, d.writes), (passes, io, io))

    def test_every_case(self) -> None:
        p = ex.PILE
        rows = [(p, 9, 1, 0, 9), (p, 20, 1, 0, 9), (p + [40], 9, 2, 1, 20), (p, 4, 3, 1, 18), (sorted(p), 4, 3, 1, 18),
                ([47] * 9, 4, 3, 1, 18), ([47], 4, 1, 0, 1), ([], 4, 0, 0, 0)]
        for a, mem, runs, passes, io in rows:
            out, d, ps = ex.external_sort(a, mem, 1)
            self.assertEqual(out, sorted(a))
            self.assertEqual((len(ex.make_runs(a, mem, ex.Disk(1))), ps, d.reads, d.writes), (runs, passes, io, io))

    def test_fan_in_limits(self) -> None:
        self.assertEqual(ex.max_fan_in(1000, 100), 9)
        self.assertEqual(ex.max_fan_in(1000, 100, double_buffer=True), 4)
        self.assertEqual(ex.max_fan_in(5000, 1000), 4)
        self.assertEqual(ex.max_fan_in(2_000_000, 10_000), 199)
        self.assertEqual(ex.max_fan_in(3, 1), 2)
        self.assertEqual([ex.merge_passes(r, k) for r, k in [(0, 2), (1, 2), (2, 2), (100, 9), (100, 4), (6, 4), (6, 2),
                                                             (25, 199), (51, 9)]], [0, 0, 1, 3, 4, 2, 3, 1, 2])
        with self.assertRaises(ValueError):
            ex.merge_passes(5, 1)
        with self.assertRaises(ValueError):
            ex.external_sort(list(range(10)), 2, 1)
        rng = random.Random(5)
        a = [rng.random() for _ in range(30_000)]
        for fan, passes, io in [(2, 3, 120), (None, 2, 90)]:
            out, d, p = ex.external_sort(a, 5000, 1000, fan)
            self.assertEqual((out == sorted(a), p, d.reads, d.writes), (True, passes, io, io))

    def test_replacement_selection(self) -> None:
        self.assertEqual(ex.replacement_selection([], 3), [])
        self.assertEqual(ex.replacement_selection([5], 3), [[5]])
        self.assertEqual(ex.replacement_selection(list(range(10)), 2), [list(range(10))])
        self.assertEqual(ex.replacement_selection([3, 1, 2], 1), [[3], [1, 2]])
        rng = random.Random(1)
        big = [rng.randrange(10 ** 6) for _ in range(100_000)]
        runs = ex.replacement_selection(big, 1000)
        self.assertEqual(len(runs), 51)
        self.assertTrue(all(r == sorted(r) for r in runs))
        self.assertEqual(sorted(x for r in runs for x in r), sorted(big))

    def test_polyphase(self) -> None:
        log = ex.polyphase(8, 5)
        self.assertEqual(log, [((3, 0, 5), 10), ((0, 3, 2), 9), ((2, 1, 0), 10), ((1, 0, 1), 8), ((0, 1, 0), 13)])
        self.assertEqual(sum(w for _, w in log), 50)
        self.assertEqual(ex.polyphase(1, 0), [])
        self.assertEqual(ex.polyphase(1, 1), [((0, 0, 1), 2)])

    def test_merge_trace(self) -> None:
        log = []
        ex.merge_runs([[4, 9], [1, 6], [3, 8]], ex.Disk(1), log)
        self.assertEqual(log[:4], [(1, 1), (3, 2), (4, 0), (6, 1)])
        disk, log = ex.Disk(1), []
        runs = ex.make_runs(ex.PILE, 4, disk)
        self.assertEqual(runs, [[12, 25, 58, 91], [31, 47, 70, 84], [63]])
        ex.merge_runs(runs, disk, log)
        self.assertEqual(log[:5], [(12, 0), (25, 0), (31, 1), (47, 1), (58, 0)])


if __name__ == "__main__":
    unittest.main()
