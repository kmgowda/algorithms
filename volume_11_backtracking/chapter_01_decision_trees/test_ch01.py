import itertools
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestDecisionTrees(unittest.TestCase):
    def test_outfits_and_bits(self) -> None:
        wardrobe = [["a", "b"], ["c", "d", "e"], ["f"]]
        self.assertEqual(ex.all_outfits(wardrobe), list(itertools.product(*wardrobe)))
        self.assertEqual(ex.all_bit_strings(4), ["".join(p) for p in itertools.product("01", repeat=4)])
        self.assertEqual(ex.count_tree_nodes([2, 2, 2]), 15)
        self.assertEqual(len(ex.draw_tree([["x", "y"], ["p", "q"]])), 7)

    def test_picnic(self) -> None:
        prices = {"chips": 30, "juice": 40, "cake": 60, "fruit": 20}
        sets, visited, full = ex.picnic_within_budget(prices, 70)
        brute = [set(c) for r in range(5) for c in itertools.combinations(prices, r) if sum(prices[i] for i in c) <= 70]
        self.assertEqual(sorted(map(sorted, sets)), sorted(map(sorted, brute)))
        self.assertLess(visited, full)

    def test_solutions(self) -> None:
        brute = [p for p in itertools.product(range(1, 7), repeat=3) if sum(p) == 10]
        self.assertEqual(sol.dice_rolls_with_total(3, 10), brute)
        self.assertEqual(sol.leaves_and_nodes(3, 2), (8, 15))
        self.assertEqual(sol.pin_codes(4), 10000)
        self.assertEqual(ex.password_space(8, 26), 208827064576)


if __name__ == "__main__":
    unittest.main()
