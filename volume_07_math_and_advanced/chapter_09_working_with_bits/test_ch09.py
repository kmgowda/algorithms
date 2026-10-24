import random
import unittest

import ch09_examples as ex


class TestChapter9(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.to_binary(5), ex.to_binary(84), ex.to_binary(255)), ("00000101", "01010100", "11111111"))
        a, b = ex.make_set(["large print", "audio", "kids"]), ex.make_set(["audio", "e-book", "kids"])
        self.assertEqual((a, b, ex.members(a & b), ex.members(a ^ b), ex.members(a & ~b)), (19, 26, ["audio", "kids"], ["large print", "e-book"], ["large print"]))
        self.assertEqual((ex.popcount(84), ex.popcount(2 ** 40 - 1), len(ex.subsets(a))), ((3, 3), (40, 40), 8))

    def test_every_case(self) -> None:
        self.assertEqual((ex.to_binary(0), ex.members(0), ex.subsets(0), ex.make_set([]), 84 >> 2, 84 << 1), ("00000000", [], [0], 0, 21, 168))
        with self.assertRaises(ValueError):
            ex.to_binary(-1)
        r = random.Random(9)
        for _ in range(300):
            n = r.randint(0, 2 ** 20)
            self.assertEqual(ex.popcount(n)[0], bin(n).count("1"))
            m = r.randint(0, 63)
            self.assertEqual(len(ex.subsets(m)), 2 ** bin(m).count("1"))


class TestDepth(unittest.TestCase):
    def test_subsets_order_and_tables(self) -> None:
        self.assertEqual(ex.subsets(19), [19, 18, 17, 16, 3, 2, 1, 0])
        import random
        r = random.Random(9)
        for _ in range(200):
            m = r.randint(0, 2 ** 12)
            subs = ex.subsets(m)
            self.assertEqual(subs, sorted(subs, reverse=True))
            self.assertEqual(len(subs), 2 ** bin(m).count("1"))
            self.assertTrue(all(x & ~m == 0 for x in subs))
            self.assertEqual(ex.popcount_by_table(m)[0], bin(m).count("1"))
        self.assertEqual((ex.popcount_by_table(2 ** 40 - 1), ex.popcount_by_table(0)), ((40, 5), (0, 0)))

    def test_chapter_numbers(self) -> None:
        self.assertEqual((ex.subsets(10), ex.popcount(200), divmod(200, 64)), ([10, 8, 2, 0], (3, 3), (3, 8)))
        seq, x = [], 3
        for _ in range(5):
            seq.append(x)
            x = ex.next_same_popcount(x)
        self.assertEqual(seq, [3, 5, 6, 9, 10])
        import itertools
        for k in range(1, 6):
            walk, x = [], (1 << k) - 1
            while x < 1 << 8:
                walk.append(x)
                x = ex.next_same_popcount(x)
            self.assertEqual(len(walk), len(list(itertools.combinations(range(8), k))))

    def test_bitset(self) -> None:
        a, b = ex.Bitset(1000), ex.Bitset(1000)
        for x in range(0, 1000, 7):
            a.add(x)
        for x in range(0, 1000, 11):
            b.add(x)
        self.assertEqual((a.count(), b.count(), a.intersection(b).count(), a.union(b).count(), len(a.words)), (143, 91, 13, 221, 16))
        self.assertTrue(77 in a.intersection(b))
        self.assertFalse(1000 in a)
        self.assertEqual((ex.Bitset(0).count(), ex.Bitset(0).words), (0, []))

    def test_fewest_branches(self) -> None:
        self.assertEqual(ex.fewest_branches_covering(0b111111), (["East", "South"], 32))
        self.assertEqual(ex.fewest_branches_covering(0), ([], 32))
        self.assertEqual(ex.fewest_branches_covering(0b1000000), ([], 32))


    def test_nim_and_grundy(self) -> None:
        from functools import lru_cache
        import itertools
        self.assertEqual(ex.nim_winner([3, 4, 5]), (True, [0, 1]))
        self.assertEqual(ex.nim_winner([1, 2, 3])[0], False)
        self.assertEqual([ex.grundy(n, [1, 2, 3]) for n in range(9)], [0, 1, 2, 3, 0, 1, 2, 3, 0])

        @lru_cache(None)
        def wins(state, moves):                  # plain game search: can the mover force the last move?
            for i, p in enumerate(state):
                for m in moves:
                    if m <= p:
                        nxt = tuple(sorted(state[:i] + (p - m,) + state[i + 1:]))
                        if not wins(nxt, moves):
                            return True
            return False
        for piles in itertools.product(range(5), repeat=3):
            st = tuple(sorted(piles))
            self.assertEqual(ex.nim_winner(list(piles))[0], wins(st, (1, 2, 3, 4)))
            self.assertEqual(ex.sum_winner(list(piles), [1, 3, 4]), wins(st, (1, 3, 4)))


if __name__ == "__main__":
    unittest.main()
