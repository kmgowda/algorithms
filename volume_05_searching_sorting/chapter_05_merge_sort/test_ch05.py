import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


class TestMergeSort(unittest.TestCase):
    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
            self.assertEqual(ex.merge_sort(v), sorted(v))
            self.assertEqual(ex.merge_sort_bottom_up(v), sorted(v))
            brute = sum(1 for i in range(len(v)) for j in range(i + 1, len(v)) if v[i] > v[j])
            s, inv = ex.sort_and_count_inversions(v)
            self.assertEqual((s, inv), (sorted(v), brute))

    def test_stable(self) -> None:
        class Item:
            def __init__(self, key, tag):
                self.key, self.tag = key, tag

            def __le__(self, other):
                return self.key <= other.key

        items = [Item(k, t) for k, t in [(2, "a"), (1, "b"), (2, "c"), (1, "d"), (2, "e")]]
        self.assertEqual([x.tag for x in ex.merge_sort(items)], ["b", "d", "a", "c", "e"])

    def test_industry(self) -> None:
        self.assertEqual(ex.ranking_disagreement(["lion", "tiger", "zebra", "panda"], ["tiger", "lion", "panda", "zebra"]), 2)
        self.assertEqual(ex.ranking_disagreement(["a", "b"], ["a", "b"]), 0)
        logs = ex.merge_log_files([(1, "w1"), (5, "w2")], [(2, "d1"), (6, "d2")], [(3, "c1")])
        self.assertEqual([t for t, _ in logs], [1, 2, 3, 5, 6])


class TestSolutions(unittest.TestCase):
    def test_merge_into_first(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            a = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 8)))
            b = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 8)))
            first = a + [0] * len(b)
            sol.merge_into_first(first, len(a), b)
            self.assertEqual(first, sorted(a + b))

    def test_merge_k_and_linked(self) -> None:
        rng = random.Random(3)
        for _ in range(100):
            lists = [sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 6))]
            self.assertEqual(sol.merge_k_sorted(lists), sorted(x for l in lists for x in l))
            v = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
            head = None
            for x in reversed(v):
                head = sol.Node(x, head)
            node, out = sol.sort_linked_list(head), []
            while node:
                out.append(node.value)
                node = node.next
            self.assertEqual(out, sorted(v))


if __name__ == "__main__":
    unittest.main()
