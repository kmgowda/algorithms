import unittest

import ch32_examples as ex


class TestChapter61(unittest.TestCase):
    def test_filter(self) -> None:
        b = ex.BloomFilter(16, 3)
        for t in ("Maps", "Ocean", "Clocks"):
            b.add(t)
        self.assertEqual([i for i, v in enumerate(b.bits) if v], [2, 5, 8, 11, 12, 13, 15])
        self.assertFalse(b.might_contain("Stars"))
        self.assertTrue(b.might_contain("Castles"))
        b.add("Robots")
        self.assertEqual([i for i, v in enumerate(b.bits) if v], [0, 1, 2, 5, 8, 11, 12, 13, 15])

    def test_rates(self) -> None:
        missed, false_yes, new = ex.screen(owned=20_000, proposals=3_000, already=500)
        self.assertEqual(missed, 0)
        self.assertLess(false_yes / new, 0.02)
        self.assertAlmostEqual(ex.measure(80_000, 10_000, 6, trials=10_000), ex.false_positive_rate(80_000, 10_000, 6),
                               delta=0.006)


if __name__ == "__main__":
    unittest.main()
