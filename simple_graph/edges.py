from collections import defaultdict
class Edge:

  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      if key == 'weight':
        self.__dict__[key] = float(value)
      else:
        self.__dict__[key] = value
    
  def __repr__(self):
    return str(self.to_dict())
    
  def to_dict(self):
    return self.__dict__
    
class Edges:
  
  def __init__(self, undirected=True, verbose=False):
    self.undirected = undirected
    self.verbose = verbose
    self.clear()
  
  def clear(self):
    self._neighbors = defaultdict(dict)
    self._reverse_neighbors = defaultdict(dict)
    
  @property
  def items(self):
    return [(u, v) for u in self._neighbors for v in self._neighbors[u]]
  
  def neighbors(self, u):
    neighbors = []
    if u in self._neighbors:
      neighbors += list(self._neighbors[u].keys())
    if self.undirected and u in self._reverse_neighbors:
      neighbors += list(self._reverse_neighbors[u].keys())
    return neighbors
  
  def reverse_neighbors(self, u):
    reverse_neighbors = []
    if u in self._reverse_neighbors:
      reverse_neighbors += list(self._reverse_neighbors[u].keys())
    if self.undirected and u in self._neighbors:
      reverse_neighbors += list(self._neighbors[u].keys())
    return reverse_neighbors
  
  def __getitem__(self, items):
    u, v = items[0], items[1]
    if self.undirected and u > v:
      u, v = v, u
    if u not in self._neighbors:
      return None
    return self._neighbors[u].get(v, None)
  
  def remove(self, u, v):
    if self.undirected and u > v:
      u, v = v, u
    if u not in self._neighbors:
      return
    self._neighbors[u].pop(v)
    self._reverse_neighbors[v].pop(u)
    
  def remove_vertex(self, x):
    '''
      remove a vertex needs to remove the related edges 
    '''
    for n in self._neighbors[x]:
      # remove link in reverse_neighors
      if n in self._reverse_neighbors and x in self._reverse_neighbors[n]:
        self._reverse_neighbors[n].pop(x)
    self._neighbors.pop(x)
    for n in self._reverse_neighbors[x]:
      # remove link in neighbors
      if n in self._neighbors and x in self._neighbors[n]:
        self._neighbors[n].pop(x, None)
    self._reverse_neighbors.pop(x)
      
  def add(self, u, v, **kwargs):
    if self.undirected and u > v:
      u, v = v, u
    edge = self[u, v]
    if edge:
      if self.verbose:
        print(f'Edge ({u},{v}) already exists.')
        return
    edge = Edge(**kwargs)
    self._neighbors[u][v] = edge
    if u == v and self.undirected:
      return
    self._reverse_neighbors[v][u] = edge