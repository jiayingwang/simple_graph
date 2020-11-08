import unittest
from simple_graph import Graph


class TestGraph(unittest.TestCase):

    def test_nodes_edges(self):
        G = Graph({0: [1, 2], 1: [2]})
        self.assertEqual(G.nodes, [0, 1, 2])
        self.assertEqual(G.edges, [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)])

    def test_edge_weight(self):
        G = Graph({0: [1, 2], 1: [2]})
        self.assertEqual(G.total_edge_weight(1), 2)
        self.assertEqual(G.total_edge_weight(), 6)
        
    def test_neighbors(self):
        G = Graph({0: [1, 2], 1: [2]})
        self.assertEqual(G.neighbors(1), [0, 2])
        
    def test_add_edge(self):
        G = Graph({0: [1, 2], 1: [2]})
        G.add_edge(2, 3)
        self.assertEqual(G.has_edge(2, 3), True)
        

if __name__ == '__main__':
    unittest.main()
