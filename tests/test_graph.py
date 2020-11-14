import unittest
from simple_graph import Graph


class TestGraph(unittest.TestCase):

    def test_nodes_edges(self):
        G = Graph()
        self.assertEqual(G.nodes, [])
        G = Graph({0: [1, 2], 1: [2]})
        self.assertEqual(G.nodes, [0, 1, 2])
        self.assertEqual(G.edges, [(0, 1), (0, 2), (1, 2)])

    def test_edge_weight(self):
        G = Graph({0: [1, 2], 1: [2]})
        self.assertEqual(G.total_edge_weight(1), 2)
        self.assertEqual(G.total_edge_weight(), 6)
        
    def test_neighbors(self):
        G = Graph({0: [1, 2], 1: [2]})
        self.assertEqual(G.neighbors(1), [0, 2])
        
    def test_add_edge(self):
        G = Graph()
        self.assertEqual(G.has_edge(1, 2), False)
        G = Graph({0: [1, 2], 1: [2]})
        self.assertEqual(G.has_edge(2, 3), False)
        G.add_edge(2, 3)
        self.assertEqual(G.has_edge(2, 3), True)
        
    def test_isolate(self):
        G = Graph({
            "a" : ["c"],
            "b" : ["c", "e"],
            "c" : ["a", "b", "d", "e"],
            "d" : ["c"],
            "e" : ["c", "b"],
            "f" : []
        })
        self.assertEqual(G.find_isolated_nodes(), ['f'])
        
    def test_find_path(self):
        G = Graph({ 
            "a" : ["d"],
            "b" : ["c"],
            "c" : ["b", "c", "d", "e"],
            "d" : ["a", "c"],
            "e" : ["c"],
            "f" : []
        })
        self.assertEqual(G.find_path('a', 'b'), ['a', 'd', 'c', 'b'])
        
    def test_find_all_paths(self):
        G = Graph({ 
            "a" : ["d", "f"],
            "b" : ["c"],
            "c" : ["b", "c", "d", "e"],
            "d" : ["a", "c"],
            "e" : ["c"],
            "f" : ["d"]
        })
        self.assertEqual(G.find_all_paths('a', 'b'), [['a', 'd', 'c', 'b'], ['a', 'f', 'd', 'c', 'b']])
        
    def test_density(self):
        G = Graph({ 
            "a" : ["d","f"],
            "b" : ["c","b"],
            "c" : ["b", "c", "d", "e"],
            "d" : ["a", "c"],
            "e" : ["c"],
            "f" : ["a"]
        })
        self.assertEqual(G.density(),0.3889)
        
        
    def test_is_connected(self):
        G = Graph({ 
            "a" : ["d"],
            "b" : ["c"],
            "c" : ["b", "c", "d", "e"],
            "d" : ["a", "c"],
            "e" : ["c"],
            "f" : []
        })
        self.assertEqual(G.is_connected(), False)
        
    def test_diameter(self):
        G = Graph({ 
            "a" : ["c"],
            "b" : ["c","e","f"],
            "c" : ["a","b","d","e"],
            "d" : ["c"],
            "e" : ["b","c","f"],
            "f" : ["b","e"]
        })
        self.assertEqual(G.diameter(), 3)

if __name__ == '__main__':
    unittest.main()
