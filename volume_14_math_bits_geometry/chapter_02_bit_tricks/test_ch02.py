import itertools
import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestBitTricks(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            n = rng.randint(0, 2 ** 20)
            i = rng.randint(0, 20)
            self.assertEqual(ex.get_bit(n, i), int(format(n, "021b")[::-1][i]))
            self.assertEqual(ex.get_bit(ex.set_bit(n, i), i), 1)
            self.assertEqual(ex.get_bit(ex.clear_bit(n, i), i), 0)
            self.assertEqual(ex.toggle_bit(ex.toggle_bit(n, i), i), n)
            self.assertEqual(ex.count_bits(n), bin(n).count("1"))
            self.assertEqual(ex.is_power_of_two(n), n > 0 and bin(n).count("1") == 1)
            if n:
                self.assertEqual(ex.lowest_set_bit(n), 1 << (len(bin(n)) - len(bin(n).rstrip("0"))))
            self.assertEqual(sol.reverse_bits(n), int(format(n, "032b")[::-1], 2))
            a, b = rng.randint(-1000, 1000), rng.randint(-1000, 1000)
            self.assertEqual(sol.add_without_plus(a, b), a + b)
        for _ in range(100):
            vals = rng.sample(range(1, 100), 6)
            single, pair = vals[0], vals[1:]
            nums = pair + pair + [single]
            rng.shuffle(nums)
            self.assertEqual(ex.single_number(nums), single)
            x, y = vals[0], vals[1]
            nums2 = vals[2:] * 2 + [x, y]
            self.assertEqual(sol.two_singles(nums2), sorted([x, y]))
            n = rng.randint(1, 20)
            miss = rng.randint(0, n)
            self.assertEqual(ex.missing_number([v for v in range(n + 1) if v != miss]), miss)
        self.assertEqual(ex.bits_table(20), [bin(i).count("1") for i in range(21)])
        subs = ex.all_subsets(["a", "b", "c", "d"])
        self.assertEqual(sorted(map(tuple, subs)), sorted(c for r in range(5) for c in itertools.combinations("abcd", r)))

    def test_examples(self) -> None:
        user = ex.grant(0, "read", "write")
        self.assertEqual(user, 3)
        self.assertTrue(ex.can(user, "write"))
        self.assertFalse(ex.can(user, "delete"))
        self.assertEqual(sol.reverse_bits(0b00000010100101000001111010011100), 964176192)


if __name__ == "__main__":
    unittest.main()
