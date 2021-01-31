class Vertex:
  
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
  
class Vertices:
  
  def __init__(self, verbose=False):
    self.verbose = verbose
    self.clear()
  
  def clear(self):
    self._vertices = {}
  
  def __getitem__(self, v):
    if v not in self._vertices:
      if self.verbose:
        print(f'Vertex {v} is not found.')
      return None
    return self._vertices[v]
  
  def add(self, v, **kwargs):
    if v in self._vertices:
      if self.verbose:
        print('Vertex', v, 'already exists.')
        return
    self._vertices[v] = Vertex(**kwargs)
  
  def remove(self, v):
    return self._vertices.pop(v, None)
  