from collections import defaultdict
class Edge:

  def __init__(self, label=None, weight=None):
    '''
      an edge can have label and weight
      the label can be None
    '''
    self.label = label
    self.set_weight(weight)

  def set_weight(self, weight=None):
    if not weight:
      weight = 1.0
    self.weight = weight
    
  def __repr__(self):
    if self.label:
      return f'edge(label={self.label}, weight={self.weight})'
    else:
      return f'edge(weight={self.weight})'
    
class Edges:
  
  def __init__(self, symmetric=True, verbose=False):
    self.symmetric = symmetric
    self.verbose = verbose
    self.clear()
  
  def clear(self):
    self._edges = defaultdict(dict)
    self._total_edge_weight = 0
    self._total_vertex_edge_weight = defaultdict(float)
    
  @property
  def items(self):
    if self.symmetric:
      return [(u, v) for u in self._edges for v in self._edges[u] if u <= v]
    else:
      return [(u, v) for u in self._edges for v in self._edges[u]]
    
  def remove_vertex(self, x):
    if self.symmetric:
      for n in self.neighbors(x):
        self.remove(x, n)
        self.remove(n, x)
    else:
      for u, v in self.items:
        if u == x or v == x:
          self.remove(u, v)
    self._edges.pop(x)
    
  def neighbors(self, u):
    if u is None:
      return None
    return list(self._edges[u].keys())
  
  def _upsert(self, u, v, label=None, weight=None):
    '''
      insert/update an edge <u, v> with label and weight
      if edge <u, v> exist, update it
      else insert it
    '''
    edge = self.get(u, v)
    
    if edge:
      # update
      if weight is not None:
        weight_diff = weight - edge.weight
        self._total_vertex_edge_weight[v] += weight_diff
        self._total_edge_weight += weight_diff
        edge.weight = weight
      if label:
        edge.label = label
    else:
      # insert
      edge = Edge(label, weight)
      self._edges[u][v] = edge
      self._total_vertex_edge_weight[v] += edge.weight
      self._total_edge_weight += edge.weight
      
  def _remove(self, u, v):
    if not self.get(u, v):
      return
    edge = self._edges[u].pop(v)
    self._total_vertex_edge_weight[v] -= edge.weight
    self._total_edge_weight -= edge.weight
      
  def add(self, u, v, label=None, weight=None):
    self._upsert(u, v, label, weight)
    if self.symmetric:
      self._upsert(v, u, label, weight)
      
  def modify(self, u, v, label=None, weight=None):
    self.add(u, v, label, weight)
      
  def remove(self, u, v):
    self._remove(u, v)
    if self.symmetric:
      self._remove(v, u)
      
  def get(self, u, v):
    if u not in self._edges:
      return None
    return self._edges[u].get(v, None)