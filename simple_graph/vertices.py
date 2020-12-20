class Vertex:
  
  def __init__(self, label=None, weight=None):
    '''
      a vertex have a label and a weight
    '''
    self.label = label
    self.set_weight(weight)
    
  def set_weight(self, weight):
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
  
class Vertices:
  
  def __init__(self, verbose=False):
    self.verbose = verbose
    self.clear()
  
  def clear(self):
    self._vertices = {}
  
  def to_label(self, v):
    return self._vertices[v].label
  
  def __getitem__(self, v):
    if v not in self._vertices:
      if self.verbose:
        print(f'Vertex {v} is not found.')
      return None
    return self._vertices[v]
  
  def add(self, v, label=None, weight=None):
    if v in self._vertices:
      if self.verbose:
        print('Vertex', v, 'already exists.')
    if self.verbose:
      print('add vertex', v)
    self._vertices[v] = Vertex(label, weight)
  
  def remove(self, v):
    return self._vertices.pop(v, None)
  