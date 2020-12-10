from math import inf
from .vertices import Vertices
from .edges import Edges

class Graph:
  
  def __init__(self, edges=None, symmetric=True, allow_self_link=False, verbose=False):
    '''
      init method:
      
      edges: a set of edges, default is None, which means empty graph
      symmetric: if the graph is symmetric, if so when we add <u, v> in the graph, <v, u> will be automatically added in the graph
      allow_self_link: if edge <u, u> in the graph
    '''
    self._allow_self_link = allow_self_link
    self.verbose = verbose
    self.symmetric = symmetric
    self.V = Vertices(verbose=verbose)
    self.E = Edges(symmetric, verbose=verbose)
    
    if not edges:
      edges = {}
    if type(edges) is list:
      self.add_edges(edges)
    elif type(edges) is dict or type(edges) is defaultdict:
      for u in edges:
        self.add_vertex(u)
        if type(edges[u]) is list:
          for v in edges[u]:
            self.add_edge(u, v)
        elif type(edges[u]) is dict or type(edges) is defaultdict:
          for v in edges[u]:
            self.add_edge(u, v, weight = edges[u][v])
        else:
          raise ValueError('Edge format is not correct.')
    else:
      raise ValueError('Edge format is not correct.')
    
  def clear(self):
    self.V.clear()
    self.E.clear()
     
  @property
  def vertices(self):
    return self.V.labels
    
  @property
  def edges(self):
    return [(self.V.to_label(u_id), self.V.to_label(v_id)) for (u_id, v_id) in self.eids]
  
  @property
  def vids(self):
    return self.V.ids
    
  @property
  def eids(self):
    return self.E.items
    
  def load(self, file_name):
    '''
        load the graph from file <file_name>
    '''
    self.clear()
    edge_list = []
    with open(file_name) as f:
      for line in f:
        edge_list.append(line.split())
      self.add_edges(edge_list)
            
  def add_edges(self, edge_list):
    for edge in edge_list:
      u_label = edge[0]
      v_label = edge[1]
      label = None
      weight = None
      if len(edge) > 2:
        label = edge[2]
      if len(edge) > 3:
        weight = edge[3]
      self.add_edge(u_label, v_label, label, weight)
            
  def remove_edges(self, edge_list):
    for edge in edge_list:
      u = edge[0]
      v = edge[1]
      self.remove_edge(u, v)
  
  def get_vertex(self, label):
    return self.V.get(label)
  
  def add_vertex(self, label, weight=None):
    self.V.add(label, weight)
  
  def remove_vertex(self, label):
    vid = self.V.remove(label)
    if vid is None:
      if self.verbose:
        print('Vertex', lable, 'can not be found, abort.')
    self.E.remove_vertex(vid)
    
  def has_vertex(self, label):
    vertex = self.get_vertex(label)
    return True if vertex else False
  
  def neighbors(self, label):
    vid = self.V.to_id(label)
    return [self.V.to_label(nid) for nid in self.E.neighbors(vid)]
  
  def get_edge(self, u_label, v_label):
    u_id = self.V.to_id(u_label)
    if u_id is None:
      return None
    v_id = self.V.to_id(v_label)
    if v_id is None:
      return None
    return self.E.get(u_id, v_id)
  
  def has_edge(self, u_label, v_label):
    return True if self.get_edge(u_label, v_label) else False
    
  def add_edge(self, u_label, v_label, label=None, weight=None, allow_add_vertex=True):
    if u_label == v_label:
      if not self._allow_self_link:
        if self.verbose:
          print(f'Cannot add edge <{u_label}, {v_label}>, because allow_self_link=False, abort.')
        return
    if self.verbose:
      print('add edge', u_label, v_label)
      if self.symmetric:
        print('add edge', v_label, u_label)
    u_id = self.V.to_id(u_label, allow_add_vertex)
    v_id = self.V.to_id(v_label, allow_add_vertex)
    if u_id is None:
      if self.verbose:
        print(f'Failed to find vertex {u_label}, abort.')
      return
    if v_id is None:
      if self.verbose:
        print(f'Failed to find vertex {v_label}, abort.')
      return
    self.E.add(u_id, v_id, label, weight)
            
  def remove_edge(self, u_label, v_label):
    u_id = self.V.to_id(u_label)
    v_id = self.V.to_id(v_label)
    if u_id is None:
      print(f'Failed to find vertex {u_label}, abort.')
      return
    if v_id is None:
      print(f'Failed to find vertex {v_label}, abort.')
      return
    if self.verbose:
      print('remove edge', u_label, v_label)
      if self.symmetric:
        print('remove edge', v_label, u_label)
    self.E.remove(u_id, v_id)
    
  def degree(self, label):
    neighbors = self.neighbors(label)
    return len(neighbors) + neighbors.count(label)
    
  def degrees(self):
    return sorted([self.degree(u) for u in self.vertices], reverse=True)
    
  def min_degree(self):
    return min([self.degree(u) for u in self.vertices])
    
  def max_degree(self):
    return max([self.degree(u) for u in self.vertices])
    
  def density(self):
    V = len(self.vids)
    E = len(self.eids)
    if self.symmetric:
      E *= 2
    return E / V ** 2 if self._allow_self_link else E / (V * (V-1))
        
  def is_connected(self, vis_V=None, start=None):
    if vis_V is None:
      vis_V = set()
    vids = self.vids
    if not start:
      start = vids[0]
    vis_V.add(start)
    if len(vis_V) == len(vids):
      return True
    else:
      for v_id in self.E.neighbors(start):
        if v_id not in vis_V and self.is_connected(vis_V, v_id):
          return True
      return False

  def total_edge_weight(self, label=None):
    if label is None:
      return self.E._total_edge_weight 
    vid = self.V.to_id(label)
    if vid is None:
      return 0
    return self.E._total_vertex_edge_weight[vid]

  def find_isolated_vertices(self):
    isolated = []
    for v in self.vertices:
      if not self.neighbors(v):
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
    return 'V:' + str(self.vertices) + '\n' + 'E:' + str(self.edges)
