"""Tests for ch06_compare (Section 6.11)."""
import unittest

import ch06_compare as c
import ch06_examples as e


class TestCompare(unittest.TestCase):
    def test_trial_formula(self):
        for p in (2, 3, 5, 97, 1009, 100003):
            self.assertEqual(c.trial_divisions(p), c.trial_divisions_counted(p))

    def test_power_mults(self):
        for exp in (1, 2, 3, 10, 1000, 12345):
            # count by running square-and-multiply
            bits, count, acc = bin(exp)[3:], 0, 1
            for b in bits:
                count += 1 + (b == "1")
            self.assertEqual(c.power_mults(exp), count)

    def test_table_printed(self):
        rows = {r[0]: r for r in c.table()}
        self.assertEqual(rows[12][1], 100000000003)
        self.assertEqual((rows[12][2], rows[12][3], rows[12][4]), (316226, 51, 600))
        self.assertEqual((rows[20][2], rows[20][4]), (3162277659, 996))
        for d, p, *_ in rows.values():
            self.assertTrue(e.miller_rabin(p))

    def test_fooled(self):
        for n in (561, 1105, 41041):
            self.assertEqual(c.fooled(n), {"trial division": False, "Fermat, base 2": True, "Miller-Rabin": False})

    def test_every_case(self):
        self.assertEqual(c.trial_divisions(2), 0)
        self.assertEqual(c.power_mults(1), 0)
        self.assertEqual(c.fermat_mults(3), 1)


if __name__ == "__main__":
    unittest.main()
