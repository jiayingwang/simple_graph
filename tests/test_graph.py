import unittest
from simple_graph import Graph

class TestGraph(unittest.TestCase):

  def test_vertices_edges(self):
    G = Graph()
    self.assertEqual(G.vertices, [])
    G = Graph({0: [1, 2], 1: [2]})
    self.assertEqual(G.vertices, [0, 1, 2])
    self.assertEqual(G.edges, [(0, 1), (0, 2), (1, 2)])

  def test_edge_weight(self):
    G = Graph({0: [1, 2], 1: [2]})
    self.assertEqual(G.total_edge_weight(1), 2)
    self.assertEqual(G.total_edge_weight(), 6)
    G = Graph({1: {1: {'weight': 6}, 2: {'weight': 2}, 0: {'weight': 2}}, 2: {1: {'weight': 2}, 2: {'weight': 6}, 0: {'weight': 2}}, 0: {1: {'weight': 2}, 2: {'weight': 2}, 0: {'weight': 6}}})
    self.assertEqual(G.total_edge_weight(), 30)
    self.assertEqual(G.total_edge_weight(1), 10)
    G = Graph(undirected=False)
    G.add_edge(1, 2)
    self.assertEqual(G.total_edge_weight(1), 0)
    self.assertEqual(G.total_edge_weight(), 1)
        
  def test_to_dict(self):
    G = Graph({1: {1: {'weight': 6}, 2: {'weight': 2}, 0: {'weight': 2}}, 2: {1: {'weight': 2}, 2: {'weight': 6}, 0: {'weight': 2}}, 0: {1: {'weight': 2}, 2: {'weight': 2}, 0: {'weight': 6}}})
    self.assertEqual(G.to_dict(), 
  {'V': [(1, {}), (2, {}), (0, {})],
 'E': [(1, 1, {'weight': 6}),
  (1, 2, {'weight': 2}),
  (0, 1, {'weight': 2}),
  (0, 2, {'weight': 2}),
  (0, 0, {'weight': 6}),
  (2, 2, {'weight': 6})]})
      
  def test_edges(self):
    G = Graph({1: {1: {'weight': 6}, 2: {'weight': 2}, 0: {'weight': 2}}, 2: {1: {'weight': 2}, 2: {'weight': 6}, 0: {'weight': 2}}, 0: {1: {'weight': 2}, 2: {'weight': 2}, 0: {'weight': 6}}})
    self.assertEqual(G.edges, [(1, 1), (1, 2), (0, 1), (0, 2), (0, 0), (2, 2)])
      
  def test_vertices(self):
    G = Graph({1: {1: {'weight': 6}, 2: {'weight': 2}, 0: {'weight': 2}}, 2: {1: {'weight': 2}, 2: {'weight': 6}, 0: {'weight': 2}}, 0: {1: {'weight': 2}, 2: {'weight': 2}, 0: {'weight': 6}}})
    self.assertEqual(set(G.vertices), {1, 2, 0})
    G = Graph(undirected=False)
    G.add_edge(1, 2)
    self.assertEqual(set(G.vertices), {1, 2})
      
  def test_add_vertex(self):
    G = Graph({'E':[[0, 1], [1, 2], [0, 2]]})
    G.add_vertex(3)
    self.assertEqual(G.find_isolated_vertices(), [3])
    
      
  def test_remove_vertex(self):
    G = Graph(undirected=False)
    G.add_edge(1, 2)
    G.remove_vertex(1)
    self.assertEqual(set(G.vertices), {2})
    G.remove_edge(1, 2)
    G = Graph({'V': ['1', '2', '0', '4', '3', '7', '6', '5', '11', '10', '8', '15', '14', '9', '12', '13'], 'E': [('1', '2'), ('1', '4'), ('1', '7'), ('2', '0'), ('2', '4'), ('2', '6'), ('0', '3'), ('0', '5'), ('7', '5'), ('7', '6'), ('5', '11'), ('4', '10'), ('8', '15'), ('8', '14'), ('8', '9'), ('14', '9'), ('9', '12'), ('10', '14'), ('10', '13'), ('11', '10'), ('6', '11'), ('3', '7')]})
    G.remove_vertex('1')
    self.assertNotIn('1', G.vertices)
    self.assertNotIn(('1', '2'), G.edges)
    self.assertNotIn(('1', '4'), G.edges)
    self.assertNotIn(('1', '7'), G.edges)
    G.remove_vertex('4')
    self.assertNotIn('4', G.vertices)
    self.assertNotIn(('2', '4'), G.edges)
    self.assertNotIn(('4', '10'), G.edges)
    G = Graph({'E':{ "a" : ["d"],
      "b" : ["c"],
      "c" : ["b", "c", "d", "e"],
      "d" : ["a", "c"],
      "e" : ["c"],
      "f" : []
    }})
    G.remove_vertex('a')
    G.remove_vertex('c')
    self.assertEqual(set(G.vertices), {'d', 'b', 'e', 'f'})
    self.assertEqual(G.edges, [])
    
  def test_neighbors(self):
    G = Graph({0: [1, 2], 1: [2]})
    self.assertEqual(set(G.neighbors(1)), {0, 2})
        
  def test_add_edge(self):
    G = Graph()
    self.assertEqual(G.has_edge(1, 2), False)
    G = Graph({0: [1, 2], 1: [2]})
    self.assertEqual(G.has_edge(2, 3), False)
    G.add_edge(2, 3)
    self.assertEqual(G.has_edge(2, 3), True)
    self.assertEqual(G.total_edge_weight(), 8)
    G.add_edge(2, 3)
    self.assertEqual(G.total_edge_weight(), 8)
    G = Graph()
    G.add_edge('a', 'z')
    G.add_edge('x', 'y')
    self.assertEqual(G.has_edge('a', 'z'), True)
    self.assertEqual(G.has_edge('x', 'y'), True)
        
  def test_isolate(self):
    G = Graph({
      "a" : ["c"],
      "b" : ["c", "e"],
      "c" : ["a", "b", "d", "e"],
      "d" : ["c"],
      "e" : ["c", "b"],
      "f" : []
    })
    self.assertEqual(G.find_isolated_vertices(), ['f'])
    G = Graph({1: [2, 3], 2: [3]}, undirected = False)
    self.assertEqual(G.find_isolated_vertices(), [])
        
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
    self.assertEqual(G.find_path('a', 'f'), None)
    self.assertEqual(G.find_path('c', 'c'), ['c'])
        
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
    self.assertEqual(G.find_all_paths('a', 'f'), [['a', 'd', 'f'], ['a', 'f']])
    self.assertEqual(G.find_all_paths('c', 'c'), [['c']])
        
  def test_degree(self):
    G = Graph(
{'V': ['a', 'd', 'b', 'c', 'e', 'f'], 'E': [('a', 'd'), ('b', 'c'), ('c', 'c'), ('c', 'e'), ('d', 'c')]})
    self.assertEqual(G.degree('a'), 1)
    self.assertEqual(G.degree('c'), 5)
    self.assertEqual(G.degree('d'), 2)
    self.assertEqual(G.degree('f'), 0)
      
  def test_max_degree(self):
    G = Graph(
{'V': ['a', 'd', 'b', 'c', 'e', 'f'], 'E': [('a', 'd'), ('b', 'c'), ('c', 'c'), ('c', 'e'), ('d', 'c')]})
    self.assertEqual(G.max_degree(), 5)
      
  def test_min_degree(self):
    G = Graph(
{'V': ['a', 'd', 'b', 'c', 'e', 'f'], 'E': [('a', 'd'), ('b', 'c'), ('c', 'c'), ('c', 'e'), ('d', 'c')]})
    self.assertEqual(G.min_degree(), 0)
      
  def test_degrees(self):
    G = Graph(
{'V': ['a', 'd', 'b', 'c', 'e', 'f'], 'E': [('a', 'd'), ('b', 'c'), ('c', 'c'), ('c', 'e'), ('d', 'c')]})
    self.assertEqual(G.degrees(), [5, 2, 1, 1, 1, 0])
        
  def test_density(self):
    G = Graph({ 
      "a" : ["d","f"],
      "b" : ["c","b"],
      "c" : ["b", "c", "d", "e"],
      "d" : ["a", "c"],
      "e" : ["c"],
      "f" : ["a"]
    })
    self.assertEqual(float(f"{G.density():.4f}"), 0.3889)
    G = Graph(
{'V': ['a', 'd', 'b', 'c', 'e', 'f'], 'E': [('a', 'd'), ('b', 'c'), ('c', 'c'), ('c', 'e'), ('d', 'c')]})
    self.assertEqual(float(f"{G.density():.4f}"), 0.2778)
    complete_graph = { 
      "a" : ["b","c"],
      "b" : ["a","c"],
      "c" : ["a","b"]
    }
    G = Graph(complete_graph)
    self.assertEqual(float(f"{G.density():.4f}"), 1.0)
    isolated_graph = { 
      "a" : [],
      "b" : [],
      "c" : []
    }
    G = Graph(isolated_graph)
    self.assertEqual(float(f"{G.density():.4f}"), 0.0)
        
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
    G = Graph({ "a" : ["d","f"],
      "b" : ["c"],
      "c" : ["b", "c", "d", "e"],
      "d" : ["a", "c"],
      "e" : ["c"],
      "f" : ["a"]
    })
    self.assertEqual(G.is_connected(), True)
    G = Graph({ "a" : ["d","f"],
      "b" : ["c","b"],
      "c" : ["b", "c", "d", "e"],
      "d" : ["a", "c"],
      "e" : ["c"],
      "f" : ["a"]
    })
    self.assertEqual(G.is_connected(), True)
        
        
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
    
  def test_edge_betweenness(self):
    G = Graph({'s': {'u':{'weight': 10}, 'x':{'weight': 5}},
    'u': {'v':{'weight': 1}, 'x':{'weight': 2}},
    'v': {'y':{'weight': 4}},
    'x':{'u':{'weight': 3},'v':{'weight': 9},'y':{'weight': 2}},
    'y':{'s':{'weight': 7},'v':{'weight': 6}}}, undirected=False)
    self.assertDictEqual(G.edge_betweenness(), {('s', 'u'): 0.0,
 ('s', 'x'): 0.4,
 ('u', 'v'): 0.15000000000000002,
 ('u', 'x'): 0.15000000000000002,
 ('v', 'y'): 0.2,
 ('x', 'u'): 0.30000000000000004,
 ('x', 'v'): 0.0,
 ('x', 'y'): 0.25,
 ('y', 's'): 0.4,
 ('y', 'v'): 0.05})
    
  def test_connected_components(self):
    G = Graph({'E':[(1, 2), (2, 3), (4, 5)] })
    self.assertEqual(G.connected_components, [[1, 2, 3], [4, 5]])
    
  def test_max_cliques(self):
    G = Graph({'E': [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (3, 4), (4, 5)]})
    self.assertEqual(G.max_cliques, [[1, 4, 2, 3], [1, 4, 5]])

if __name__ == '__main__':
    unittest.main()
