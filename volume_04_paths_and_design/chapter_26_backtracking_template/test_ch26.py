import unittest

import ch26_examples as ex


class TestChapter26(unittest.TestCase):
    def test_seating(self) -> None:
        a, ca, b, cb = [], [0], [], [0]
        ex.backtrack(ex.READERS, ex.FEUDS, [], a, ca)
        ex.check_at_end(ex.READERS, ex.FEUDS, [], b, cb)
        self.assertEqual((len(a), ca[0], len(b), cb[0], a == b), (140, 547, 140, 1957, True))
        self.assertEqual(ex.first_only(ex.READERS, ex.FEUDS), (["Ana", "Cai", "Ben", "Eva", "Dev", "Fay"], 10))

    def test_every_case(self) -> None:
        o, c = [], [0]
        ex.backtrack([], [], [], o, c)
        self.assertEqual((o, c[0]), ([[]], 1))
        o, c = [], [0]
        ex.backtrack(["Ana", "Ben"], [("Ana", "Ben")], [], o, c)
        self.assertEqual((o, c[0], ex.first_only(["Ana", "Ben"], [("Ana", "Ben")])), ([], 3, (None, 3)))
        o, c = [], [0]
        ex.backtrack(ex.READERS, [], [], o, c)
        self.assertEqual((len(o), c[0]), (720, 1957))
        feuds = [(x, y) for i, x in enumerate(ex.READERS) for y in ex.READERS[i + 1:] if x != "Ana"]
        o, c = [], [0]
        ex.backtrack(ex.READERS, feuds, [], o, c)
        self.assertEqual((len(o), c[0]), (0, 37))


    def test_work(self) -> None:
        self.assertEqual((ex.work(ex.READERS, ex.FEUDS, True), ex.work(ex.READERS, ex.FEUDS, False)),
                         ((547, 742), (1957, 2052)))
        self.assertEqual(ex.nodes_by_level(ex.READERS, ex.FEUDS), [1, 6, 22, 60, 126, 192, 140])
        self.assertEqual(ex.nodes_by_level(ex.READERS, []), [1, 6, 30, 120, 360, 720, 720])
        more = ex.READERS + ["Gus", "Hal"]
        feuds = ex.FEUDS + [("Gus", "Hal"), ("Ben", "Gus")]
        self.assertEqual((ex.work(more, feuds, True)[0], ex.work(more, feuds, False)[0]), (24933, 109601))
        self.assertEqual((ex.work([], [], True), ex.work(["Ana"], [], False)), ((1, 0), (2, 0)))


if __name__ == "__main__":
    unittest.main()
