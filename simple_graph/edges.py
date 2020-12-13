from elegant_structure import Pool
from collections import defaultdict
class Edge:

  def __init__(self, label=None, weight=None):
    '''
      an edge can have label and weight
      the label can be None
    '''
    self.label = label
    if not weight:
      weight = 1.0
    self.weight = weight
    
  def __repr__(self):
    return str(self.to_json())
    
  def to_json(self):
    if self.label:
      return {'label': self.label, 'weight': self.weight}
    else:
      return {'weight': self.weight}
    
class Edges:
  
  def __init__(self, symmetric=True, verbose=False):
    self.symmetric = symmetric
    self.verbose = verbose
    self.clear()
  
  def clear(self):
    self._edges = Pool(Edge)
    self._neighbors = defaultdict(dict)
    self._reverse_neighbors = defaultdict(dict)
    
  @property
  def items(self):
    return [(u, v) for u in self._neighbors for v in self._neighbors[u]]
  
  def neighbors(self, u):
    neighbors = []
    if u in self._neighbors:
      neighbors += list(self._neighbors[u].keys())
    if self.symmetric and u in self._reverse_neighbors:
      neighbors += list(self._reverse_neighbors[u].keys())
    return neighbors
  
  def reverse_neighbors(self, u):
    reverse_neighbors = []
    if u in self._reverse_neighbors:
      reverse_neighbors += list(self._reverse_neighbors[u].keys())
    if self.symmetric and u in self._neighbors:
      reverse_neighbors += list(self._neighbors[u].keys())
    return reverse_neighbors
  
  def _get(self, u, v):
    if self.symmetric and u > v:
      u, v = v, u
    if u not in self._neighbors:
      return None
    eid = self._neighbors[u].get(v, None)
    return eid
  
  def __getitem__(self, items):
    u, v = items[0], items[1]
    eid = self._get(u, v)
    if eid is not None:
      return self._edges[eid]
    else:
      return None
  
  def remove(self, u, v):
    if self.symmetric and u > v:
      u, v = v, u
    if u not in self._neighbors:
      return
    self._neighbors[u].pop(v)
    eid = self._reverse_neighbors[v].pop(u)
    self._edges.remove(eid)
    
  def remove_vertex(self, x):
    '''
      remove a vertex needs to remove the related edges 
    '''
    for n in self._neighbors[x]:
      eid = self._neighbors[x][n]
      self._edges.remove(eid)
      # remove link in reverse_neighors
      if n in self._reverse_neighbors and x in self._reverse_neighbors[n]:
        self._reverse_neighbors[n].pop(x)
    self._neighbors.pop(x)
    for n in self._reverse_neighbors[x]:
      eid = self._reverse_neighbors[x][n]
      self._edges.remove(eid)
      # remove link in neighbors
      if n in self._neighbors and x in self._neighbors[n]:
        self._neighbors[n].pop(x, None)
    self._reverse_neighbors.pop(x)
      
  def add(self, u, v, label=None, weight=None):
    if self.symmetric and u > v:
      u, v = v, u
    eid = self._get(u, v)
    if eid:
      edge = self._edges[eid]
      if weight:
        edge.weight = weight
      if label:
        edge.label = label
    else:
      eid = self._edges.add(label, weight)
    self._neighbors[u][v] = eid
    if u == v and self.symmetric:
      return
    self._reverse_neighbors[v][u] = eid
      
  def modify(self, u, v, label=None, weight=None):
    self.add(u, v, label, weight)