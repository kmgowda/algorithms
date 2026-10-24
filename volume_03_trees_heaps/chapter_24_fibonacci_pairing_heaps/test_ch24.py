import heapq
import random
import unittest

import ch24_examples as ex


def keys_of(forest):
    return [r[0] for r in forest]


def run_against_heapq(test, cls, seed, check_amortized=False):
    """A seeded random workload; heapq with lazy deletion is the reference (Volume 5, Chapter 2)."""
    rng = random.Random(seed)
    h, ref, live = cls(), [], {}                         # live: item -> (node, current key)
    for step in range(400):
        r = rng.random()
        if r < 0.45:
            k = rng.randrange(1000)
            live[step] = (h.insert(k, step), k)
            heapq.heappush(ref, (k, step))
        elif r < 0.7 and live:
            while ref[0][1] not in live or live[ref[0][1]][1] != ref[0][0]:
                heapq.heappop(ref)                       # stale reference entry
            k, item = h.delete_min()
            test.assertEqual(k, ref[0][0])
            del live[item]
        elif live:
            item = rng.choice(list(live))
            x, k = live[item]
            new = k - rng.randrange(50)
            phi, cuts = (h.potential(), h.cuts) if check_amortized else (0, 0)
            h.decrease_key(x, new)
            if check_amortized:                          # cuts + change in potential <= 4: O(1) amortized
                test.assertLessEqual(h.cuts - cuts + h.potential() - phi, 4)
            live[item] = (x, new)
            heapq.heappush(ref, (new, item))
        test.assertTrue(h.valid())
        test.assertEqual(len(h), len(live))
        if live:
            test.assertEqual(h.find_min()[0], min(k for _, k in live.values()))


class TestFibonacciHeap(unittest.TestCase):
    def test_every_case(self) -> None:
        h = ex.FibHeap()                                    # empty heap
        self.assertIsNone(h.find_min())
        self.assertRaises(IndexError, h.delete_min)
        self.assertTrue(h.valid())
        x = h.insert(7)                                     # one item
        self.assertEqual((h.find_min(), h.potential()), ((7, None), 1))
        self.assertEqual(h.delete_min(), (7, None))         # delete-min with no children: nothing to link
        self.assertEqual((len(h), h.links, h.forest()), (0, 0, []))
        self.assertTrue(h.valid())
        h = ex.FibHeap([5, 3])                              # consolidation with equal degrees
        h.insert(9)
        h.delete_min()
        self.assertEqual((h.forest(), h.links), ([(5, False, [(9, False, [])])], 1))
        h = ex.FibHeap()
        nodes = {k: h.insert(k) for k in [1, 4, 6, 8, 9]}
        h.delete_min()                                      # 4 with children 6 and 8(9)
        self.assertEqual(h.forest(), [(4, False, [(6, False, []), (8, False, [(9, False, [])])])])
        h.decrease_key(nodes[9], 8)                         # no violation: equal to the parent is allowed
        self.assertEqual((h.cuts, h.marked), (0, 0))
        h.decrease_key(nodes[6], 5)                         # still above 4: nothing moves
        self.assertEqual(h.cuts, 0)
        h.decrease_key(nodes[9], 2)                         # cut; the unmarked parent 8 is marked
        self.assertEqual((h.cuts, h.cascading, nodes[8].mark), (1, 0, True))
        self.assertEqual(h.find_min(), (2, None))
        h.decrease_key(nodes[8], 3)                         # cutting a marked node itself just unmarks it
        self.assertEqual((h.cuts, h.marked), (2, 0))
        self.assertRaises(ValueError, h.decrease_key, nodes[8], 10)
        self.assertTrue(h.valid())
        h = ex.FibHeap([3, 3, 3])                           # ties
        self.assertEqual(h.find_min()[0], 3)
        self.assertEqual([h.delete_min()[0] for _ in range(3)], [3, 3, 3])

    def test_reservation_story(self) -> None:
        steps, h = ex.reservation_story()
        self.assertEqual([phi for _, _, phi in steps], [9, 1, 4, 4])
        self.assertEqual(keys_of(steps[1][1]), [25])
        self.assertEqual(h.link_log, [(58, 25), (91, 70), (70, 25), (84, 47), (63, 31), (47, 31), (31, 25)])
        self.assertEqual(keys_of(steps[3][1]), [25, 20, 15, 31])
        self.assertEqual((h.links, h.cuts, h.cascading), (7, 3, 1))
        self.assertEqual(h.find_min()[0], 15)
        self.assertTrue(h.valid())

    def test_meld_and_delete(self) -> None:
        a, b = ex.FibHeap(ex.BRANCH_A), ex.FibHeap(ex.BRANCH_B)
        a.meld(b)
        self.assertEqual((len(a), len(b), a.find_min()[0]), (9, 0, 12))
        self.assertTrue(a.valid() and b.valid())
        a.meld(ex.FibHeap())                                # meld with an empty heap
        ex.FibHeap().meld(a)
        h = ex.FibHeap()
        nodes = [h.insert(k) for k in range(20)]
        h.delete_min()
        h.delete(nodes[13])
        h.delete(nodes[1])                                  # the current minimum
        self.assertTrue(h.valid())
        self.assertEqual([h.delete_min()[0] for _ in range(len(h))], [k for k in range(2, 20) if k != 13])

    def test_against_heapq(self) -> None:
        for seed in range(30):
            run_against_heapq(self, ex.FibHeap, seed, check_amortized=True)

    def test_amortized_delete_min(self) -> None:
        rng = random.Random(9)
        h = ex.FibHeap()
        nodes = [h.insert(rng.randrange(10**6)) for _ in range(3000)]
        for x in rng.sample(nodes, 1000):
            h.decrease_key(x, x.key - rng.randrange(10**5))
        while len(h) > 1:
            n, phi = len(h), h.potential()
            h.delete_min()
            self.assertLessEqual(h.work + h.potential() - phi, 2 * ex.degree_bound(n) + 2)

    def test_degree_bound(self) -> None:
        self.assertEqual([ex.fib(k) for k in range(8)], [0, 1, 1, 2, 3, 5, 8, 13])
        self.assertEqual([ex.degree_bound(n) for n in (0, 1, 2, 3, 5, 8, 1000)], [0, 0, 1, 2, 3, 4, 14])
        degree, size, bound = ex.degree_experiment()
        self.assertEqual((degree, size, bound), (12, 3946, 17))
        self.assertLessEqual(degree, bound)
        h = ex.FibHeap(range(1025))                         # 1,024 items left: one binomial tree B10
        h.delete_min()
        self.assertEqual((len(h.roots), h.max_degree()), (1, 10))


class TestPairingHeap(unittest.TestCase):
    def test_every_case(self) -> None:
        p = ex.PairingHeap()
        self.assertIsNone(p.find_min())
        self.assertRaises(IndexError, p.delete_min)
        x = p.insert(4)
        self.assertEqual(p.delete_min(), (4, None))         # only the root: nothing to pair
        self.assertTrue(p.valid())
        p = ex.PairingHeap([58, 25, 91, 12, 70, 47, 84, 31, 63])
        self.assertEqual(p.shape(), (12, [(25, [(58, []), (91, [])]), (70, []), (47, []), (84, []), (31, []),
                                          (63, [])]))
        p.delete_min()
        self.assertEqual(p.passes[-1], ([31, 47, 25], 25))
        self.assertEqual(p.shape(), (25, [(58, []), (91, []), (70, []), (47, [(84, [])]), (31, [(63, [])])]))
        q = ex.PairingHeap([2, 9])
        nine = q.root.children and list(q.root.children)[0]
        q.decrease_key(nine, 1)                             # cut the subtree, meld it with the root
        self.assertEqual(q.shape(), (1, [(2, [])]))
        q.decrease_key(q.root, 0)                           # the root itself: nothing to cut
        self.assertEqual(q.find_min()[0], 0)
        self.assertRaises(ValueError, q.decrease_key, q.root, 5)
        self.assertTrue(q.valid())
        a, b = ex.PairingHeap([5]), ex.PairingHeap()
        a.meld(b)
        b.meld(a)
        self.assertEqual((len(a), len(b), b.find_min()[0]), (0, 1, 5))

    def test_against_heapq(self) -> None:
        for seed in range(30):
            run_against_heapq(self, ex.PairingHeap, 100 + seed)

    def test_sorting(self) -> None:
        rng = random.Random(2)
        keys = [rng.randrange(100) for _ in range(500)]
        for cls in (ex.FibHeap, ex.PairingHeap):
            self.assertEqual(ex.heap_sort_with(cls, keys), sorted(keys))
            self.assertEqual(ex.heap_sort_with(cls, []), [])


class TestDijkstra(unittest.TestCase):
    def test_town(self) -> None:
        adj = {"A": [("B", 4), ("C", 1)], "B": [("D", 1)], "C": [("B", 2), ("D", 5)], "D": []}
        for cls in (ex.FibHeap, ex.PairingHeap):
            dist, counts = ex.dijkstra(adj, "A", cls)
            self.assertEqual(dist, {"A": 0, "B": 3, "C": 1, "D": 4})
            self.assertEqual(counts, {"insert": 4, "delete_min": 4, "decrease_key": 2})
        dist, counts = ex.dijkstra_heapq(adj, "A")
        self.assertEqual(dist, {"A": 0, "B": 3, "C": 1, "D": 4})
        self.assertEqual((counts["push"], counts["stale"]), (6, 2))
        self.assertEqual(ex.dijkstra({"A": []}, "A")[0], {"A": 0})          # a single place

    def test_random_graphs(self) -> None:
        for seed in range(5):
            adj = ex.random_graph(300, 2000, seed)
            d1 = ex.dijkstra(adj, 0, ex.FibHeap)[0]
            d2 = ex.dijkstra(adj, 0, ex.PairingHeap)[0]
            d3 = ex.dijkstra_heapq(adj, 0)[0]
            self.assertEqual(d1, d2)
            self.assertEqual(d1, d3)

    def test_report(self) -> None:
        r = ex.dijkstra_report()
        self.assertEqual(r["fibonacci"], {"insert": 10000, "delete_min": 10000, "decrease_key": 9495,
                                          "links": 67324, "cuts": 3405, "cascading": 170})
        self.assertEqual(r["pairing"]["links"], 188835)
        self.assertEqual(r["heapq"], {"push": 19528, "pop": 19528, "stale": 9528, "largest heap": 12401})


    def test_leftist_and_skew(self) -> None:
        import math
        import random
        pile = [58, 25, 91, 12, 70, 47, 84, 31, 63]
        self.assertEqual(ex.meld_sort(ex.leftist_meld, pile, lambda x: (x, None, None, 1)), sorted(pile))
        self.assertEqual(ex.meld_sort(ex.skew_meld, pile, lambda x: (x, None, None)), sorted(pile))
        r = random.Random(24)
        for _ in range(100):
            xs = [r.randint(0, 50) for _ in range(r.randint(0, 40))]
            self.assertEqual(ex.meld_sort(ex.leftist_meld, xs, lambda x: (x, None, None, 1)), sorted(xs))
            self.assertEqual(ex.meld_sort(ex.skew_meld, xs, lambda x: (x, None, None)), sorted(xs))
            h = None
            for x in xs:
                h = ex.leftist_meld(h, (x, None, None, 1))
            self.assertLessEqual(ex.right_spine(h), math.log2(len(xs) + 1) + 1e-9)


if __name__ == "__main__":
    unittest.main()
