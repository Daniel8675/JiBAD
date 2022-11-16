from unittest import TestCase
import Graphs as G


class TestGraph(TestCase):  # Testy nie są obfite z tego wzgledu ze chcialem sporowac nowego rodzaju assertRaises z
    # blokiem with takze mozna je nazwac testem testow :)
    def test_add_vertex(self):
        g = G.Graph()
        with self.assertRaises(TypeError):
            g.add_vertex([1, 2, 3])

    def test_add_edge(self):
        g = G.Graph()
        g.add_vertex(1)
        g.add_vertex(2)
        with self.assertRaises(KeyError):
            g.add_edge((1, 3))



