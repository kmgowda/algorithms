import heapq
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def run_model(rng, heap, ops=2000):
    model = []
    for _ in range(ops):
        if rng.random() < 0.6 or not model:
            x = rng.randint(0, 100)
            heap.push(x)
            heapq.heappush(model, x)
        else:
            assert heap.pop() == heapq.heappop(model)
    return model


class TestAdvancedHeaps(unittest.TestCase):
    def test_against_heapq(self) -> None:
        rng = random.Random(1)
        for make in (lambda: ex.DaryHeap(2), lambda: ex.DaryHeap(3), lambda: ex.DaryHeap(8),
                     ex.BinomialHeap, ex.PairingHeap):
            h = make()
            model = run_model(rng, h)
            self.assertEqual([h.pop() for _ in range(len(model))], sorted(model))
            with self.assertRaises(IndexError):
                h.pop()
        with self.assertRaises(ValueError):
            ex.DaryHeap(1)

    def test_binomial_structure_and_merge(self) -> None:
        bh = ex.BinomialHeap()
        for x in range(13):
            bh.push(x)
        self.assertEqual(sorted(bh.trees), sol.tree_orders(13))
        for order, tree in bh.trees.items():
            def size(t):
                return 1 + sum(size(c) for c in t.children)
            self.assertEqual(size(tree), 2 ** order)
        self.assertEqual(bh.peek(), 0)
        self.assertEqual(ex.merge_hospital_queues([5, 2, 8], [3, 1, 9]), [1, 2, 3, 5, 8, 9])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.dary_height(1, 4), 0)
        self.assertEqual(sol.dary_height(5, 4), 1)
        self.assertEqual(sol.dary_height(6, 4), 2)
        self.assertEqual(sol.tree_orders(13), [0, 2, 3])
        self.assertGreater(sol.best_d(10**6, 10**3, 10**5), 2)
        self.assertEqual(sol.best_d(10, 10**6, 10**5), 3)
        self.assertGreater(sol.count_comparisons(4, 1000), 0)


if __name__ == "__main__":
    unittest.main()
