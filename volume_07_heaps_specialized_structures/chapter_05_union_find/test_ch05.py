import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


def components_bfs(n, edges):
    adj = {i: set() for i in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    label, comp = {}, 0
    for s in range(n):
        if s in label:
            continue
        stack = [s]
        label[s] = comp
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in label:
                    label[y] = comp
                    stack.append(y)
        comp += 1
    return label, comp


class TestUnionFind(unittest.TestCase):
    def test_against_search(self) -> None:
        rng = random.Random(1)
        for _ in range(100):
            n = rng.randint(1, 40)
            edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 40))]
            uf = ex.UnionFind()
            for i in range(n):
                uf.add(i)
            for a, b in edges:
                uf.union(a, b)
            label, comp = components_bfs(n, edges)
            self.assertEqual(uf.groups, comp)
            for _ in range(30):
                a, b = rng.randrange(n), rng.randrange(n)
                self.assertEqual(uf.connected(a, b), label[a] == label[b])
                self.assertEqual(uf.group_size(a), sum(1 for v in label.values() if v == label[a]))

    def test_examples(self) -> None:
        people = ["Ana", "Ben", "Cy", "Dev", "Eve", "Fay"]
        self.assertEqual(ex.friend_groups([("Ana", "Ben"), ("Cy", "Dev"), ("Ben", "Eve")], people),
                         [["Ana", "Ben", "Eve"], ["Cy", "Dev"], ["Fay"]])
        self.assertEqual(ex.redundant_cable([(1, 2), (2, 3), (3, 4), (1, 4), (1, 5)]), (1, 4))
        self.assertIsNone(ex.redundant_cable([(1, 2), (2, 3)]))
        self.assertEqual(ex.count_islands(["##..#", "#...#", "..#..", "....#"]), 4)

    def test_compression_flattens(self) -> None:
        uf = ex.UnionFind()
        for i in range(1000):
            uf.union(i, i + 1)
        root = uf.find(0)
        for i in range(1001):
            uf.find(i)
        self.assertTrue(all(uf.parent[i] == root for i in range(1001)))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.provinces([[1, 1, 0], [1, 1, 0], [0, 0, 1]]), 2)
        self.assertEqual(sol.merge_accounts([["Ana", "a@x", "b@x"], ["Ana", "c@x"], ["Ana", "b@x", "d@x"], ["Ben", "e@x"]]),
                         [["Ana", "a@x", "b@x", "d@x"], ["Ana", "c@x"], ["Ben", "e@x"]])
        self.assertFalse(sol.satisfiable(["a==b", "b!=a"]))
        self.assertTrue(sol.satisfiable(["a==b", "b==c", "a!=d"]))
        self.assertEqual(sol.largest_group([("a", "b"), ("c", "d"), ("b", "e")]), 3)


if __name__ == "__main__":
    unittest.main()
