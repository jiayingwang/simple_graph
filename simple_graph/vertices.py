from elegant_structure import Pool

class Vertex:
  
  def __init__(self, label, weight=None):
    '''
      a vertex have a label and a weight
      and the label cann't be None
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
    return {'label': self.label, 'weight': self.weight}
  
class Vertices:
  
  def __init__(self, verbose=False):
    self.verbose = verbose
    self.clear()
  
  def clear(self):
    self._vertices = Pool(Vertex)
    self._label2id = {}
    
  @property
  def labels(self):
    return list(self._label2id.keys())
    
  @property
  def ids(self):
    return list(self._label2id.values())
  
  def to_id(self, label, allow_new=False):
    '''
      label -> id
    '''
    vid = self._label2id.get(label, None)
    if vid is None:
      if allow_new:
        vid = self.add(label)
    return vid
  
  def to_label(self, n_id):
    return self._vertices[n_id].label
  
  def __getitem__(self, label):
    vid = self.to_id(label)
    if vid is None:
      if self.verbose:
        print(f'Vertex {label} is not found.')
      return None
    return self._vertices[vid]
  
  def add(self, label, weight=None):
    vid = self.to_id(label)
    if vid is not None:
      if self.verbose:
        print('Vertex', label, 'already exists.')
      return vid
    if self.verbose:
      print('add vertex', label)
    vid = self._vertices.add(label, weight)
    self._label2id[label] = vid
    self._vertices[vid].label = label
    self._vertices[vid].set_weight(weight)
    return vid
  
  def remove(self, label):
    vid = self.to_id(label)
    if vid is not None:
      self._vertices.remove(vid)
      self._label2id.pop(label)
    return vid
  