import random
import unittest

import ch19_examples as ex


class TestChapter19(unittest.TestCase):
    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            a = [rng.randint(0, 50) for _ in range(rng.randint(0, 60))]
            for fan in (2, 3, None):
                out, _, _ = ex.external_sort(a, rng.randint(1, 10), rng.randint(1, 4), fan)
                self.assertEqual(out, sorted(a))

    def test_fan_in(self) -> None:
        rng = random.Random(1)
        big = [rng.randrange(10 ** 6) for _ in range(100_000)]
        for fan, passes, io in [(2, 7, 8000), (4, 4, 5000), (10, 2, 3000), (None, 1, 2000)]:
            out, d, p = ex.external_sort(big, 1000, 100, fan)
            self.assertEqual((p, d.reads, d.writes), (passes, io, io))

    def test_every_case(self) -> None:
        p = ex.PILE
        rows = [(p, 9, 1, 0, 9), (p, 20, 1, 0, 9), (p + [40], 9, 2, 1, 20), (p, 3, 3, 1, 18), (sorted(p), 3, 3, 1, 18),
                ([47] * 9, 3, 3, 1, 18), ([47], 3, 1, 0, 1), ([], 3, 0, 0, 0)]
        for a, mem, runs, passes, io in rows:
            out, d, ps = ex.external_sort(a, mem, 1)
            self.assertEqual(out, sorted(a))
            self.assertEqual((len(ex.make_runs(a, mem, ex.Disk(1))), ps, d.reads, d.writes), (runs, passes, io, io))

    def test_merge_trace(self) -> None:
        log = []
        ex.merge_runs([[4, 9], [1, 6], [3, 8]], ex.Disk(1), log)
        self.assertEqual(log[:4], [(1, 1), (3, 2), (4, 0), (6, 1)])


if __name__ == "__main__":
    unittest.main()
