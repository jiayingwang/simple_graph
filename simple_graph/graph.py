from math import inf
import random
from collections import defaultdict
from .vertices import Vertices
from .edges import Edges

class Graph:
  
  def __init__(self, graph=None, undirected=True, verbose=False):
    '''
      init method:
      
      edges: a set of edges, default is None, which means empty graph
      undirected: if the graph is undirected/directed, default it is a undirected graph
    '''
    self.has_self_link = False
    self.verbose = verbose
    self.undirected = undirected
    self.V = Vertices(verbose=verbose)
    self.E = Edges(undirected, verbose=verbose)
    if graph:
      if type(graph) is str:
        self.parse_txt(graph)
      else:
        if 'V' in graph:
          self.parse_vertices(graph['V'])
        if 'E' in graph:
          self.parse_edges(graph['E'])
        else:
          self.parse_edges(graph)
      
  def parse_vertices(self, vertices):
    for u in vertices:
      if type(u) is list:
        self.add_vertex(u[0], **u[1])
      else:
        self.add_vertex(u)
      
  def parse_edges(self, edges):
    if edges is None:
        return
    if type(edges) is list:
      self.add_edges(edges)
    elif type(edges) is dict or type(edges) is defaultdict:
      for u in edges:
        self.add_vertex(u)
        if type(edges[u]) is list or type(edges[u]) is set:
          for v in edges[u]:
            self.add_edge(u, v)
        elif type(edges[u]) is dict or type(edges) is defaultdict:
          for v in edges[u]:
            e = edges[u][v]
            self.add_edge(u, v, **e)
        else:
          raise ValueError('Edge format is not correct.')
    else:
      raise ValueError('Edge format is not correct.')
    
  def clear(self):
    self.V.clear()
    self.E.clear()
     
  @property
  def vertices(self):
    return list(self.V._vertices.keys())
  
  @property
  def detailed_vertices(self):
    return [(v, self.V[v].to_dict()) for v in self.V._vertices]
  
  @property
  def detailed_edges(self):
    return [(u, v, self.E[u, v].to_dict()) for (u, v) in self.edges]
    
  @property
  def edges(self):
    return self.E.items
  
  def parse_txt(self, txt):
    '''
        load the graph from txt
    '''
    self.clear()
    mode = 'edge'
    options = []
    edge_list = []
    lines = [line.strip() for line in txt.split('\n') if line.strip()]
    for line in lines:
      p = line.find('#')
      if p != -1:
        command_line = line[p+1:].strip()
        commands = command_line.split()
        command = commands[0]
        options = []
        if len(commands) > 1:
          options = commands[1].split(',')
        if command == 'V':
          mode = 'vertex'
          continue
        if command == 'E':
          mode = 'edge'
          continue
      x = line.split(',')
      if mode == 'vertex':
        self.add_vertex(x[0], **{key: value for key, value in zip(options, x[1:])})
      elif mode == 'edge':
        self.add_edge(x[0], x[1], **{key: value for key, value in zip(options, x[2:])})
    
  def load(self, file_name):
    '''
        load the graph from file <file_name>
    '''
    with open(file_name) as f:
      txt = f.read()
      self.parse_txt(txt)
            
  def add_edges(self, edge_list):
    for edge in edge_list:
      u = edge[0]
      v = edge[1]
      e = {}
      if len(edge) > 2:
        e = edge[2]
        
      self.add_edge(u, v, **e)
            
  def remove_edges(self, edge_list):
    for edge in edge_list:
      u = edge[0]
      v = edge[1]
      self.remove_edge(u, v)
  
  def vertex(self, v):
    return self.V[v]
  
  def add_vertex(self, v, **kwargs):
    if self.verbose:
      print('add vertex', v)
    self.V.add(v, **kwargs)
  
  def remove_vertex(self, v):
    vertex = self.V.remove(v)
    if vertex is None:
      if self.verbose:
        print('Vertex', v, 'can not be found, abort.')
    self.E.remove_vertex(v)
    
  def has_vertex(self, v):
    vertex = self.vertex(v)
    return True if vertex else False
  
  def neighbors(self, v):
    return [n for n in self.E.neighbors(v)]
  
  def reverse_neighbors(self, v):
    return [n for n in self.E.reverse_neighbors(v)]
  
  def edge(self, u, v):
    return self.E[u, v]
  
  def has_edge(self, u, v):
    return True if self.edge(u, v) else False
    
  def add_edge(self, u, v, allow_add_vertex=True, **kwargs):
    if u == v:
      self.has_self_link = True
    if self.verbose:
      print(f'add edge ({u}, {v})')
    if not self.has_vertex(u):
      if allow_add_vertex:
        self.add_vertex(u)
      else:
        if self.verbose:
          print(f'Failed to find vertex {u}, abort.')
        return
    if not self.has_vertex(v):
      if allow_add_vertex:
        self.add_vertex(v)
      else:
        if self.verbose:
          print(f'Failed to find vertex {v}, abort.')
        return
    self.E.add(u, v, **kwargs)
            
  def remove_edge(self, u, v):
    if self.verbose:
      print('remove edge', u, v)
    self.E.remove(u, v)
    
  def degree(self, v):
    neighbors = self.neighbors(v)
    return len(neighbors) + neighbors.count(v)
    
  def degrees(self):
    return sorted([self.degree(u) for u in self.vertices], reverse=True)
    
  def min_degree(self):
    return min([self.degree(u) for u in self.vertices])
    
  def max_degree(self):
    return max([self.degree(u) for u in self.vertices])
    
  def density(self):
    V = len(self.vertices)
    E = len(self.edges)
    if self.undirected:
      E *= 2
    return E / V ** 2 if self.has_self_link else E / (V * (V-1))
        
  def is_connected(self, vis=None, start=None):
    if vis is None:
      vis = set()
    if not start:
      start = self.vertices[0]
    vis.add(start)
    if len(vis) == len(self.vertices):
      return True
    else:
      for v in self.E.neighbors(start):
        if v not in vis and self.is_connected(vis, v):
          return True
      return False

  def edge_weight(self, u, v):
    return self.E[u, v].weight if hasattr(self.E[u, v], 'weight') else 1.0

  def vertex_weight(self, v):
    return self.vertex(v).weight if hasattr(self.vertex(v), 'weight') else 1.0

  def total_edge_weight(self, v=None):
    if v is None:
        return sum([self.total_edge_weight(v) for v in self.vertices])
    if not self.has_vertex(v):
      return 0
    return sum([self.edge_weight(n, v) for n in self.E.reverse_neighbors(v)])

  def total_vertex_weight(self):
    return sum([self.vertex_weight(v) for v in self.vertices])

  def generate_random_graph(self, n, p):
    for i in range(n):
      self.add_vertex(str(i+1))
    for i in self.vertices:
      for j in self.vertices:
        if (i != j and random.random() < p):
          self.add_edge(i, j)

  def find_isolated_vertices(self):
    isolated = []
    for v in self.vertices:
      if not self.neighbors(v) and not self.reverse_neighbors(v):
        isolated.append(v)
    return isolated
    
  def find_path(self, start, end, path=None):
    if start not in self.vertices or end not in self.vertices:
      return None
    if not path:
      path = []

    path = path + [start]
    if start == end:
      return path
    for n in self.neighbors(start):
      if n not in path:
        extend_path = self.find_path(n, end, path)
        if extend_path:
          return extend_path        
    return None
    
  def find_all_paths(self, start, end, path=None):
    if start not in self.vertices or end not in self.vertices:
      return []
    if not path:
      path = []

    path = path + [start]
    if start == end:
      return [path]
    paths = []
    for n in self.neighbors(start):
      if n not in path:
        for p in self.find_all_paths(n, end, path):
          paths.append(p)
    return paths
    
  def diameter(self):
    if not self.is_connected():
      return inf
    V = self.vertices
    pairs = [(V[i], V[j]) for i in range(len(V)-1) for j in range(i+1, len(V))]
    smallest_paths = []
    for (s,e) in pairs:
      paths = self.find_all_paths(s,e)
      smallest = sorted(paths, key=len)[0]
      smallest_paths.append(smallest)
    smallest_paths.sort(key=len)
    diameter = len(smallest_paths[-1])-1
    return diameter
    
  def __repr__(self):
    return str({'V': self.vertices, 'E': self.edges})
  
  def to_dict(self):
    return {'V': self.detailed_vertices, 'E': self.detailed_edges}
