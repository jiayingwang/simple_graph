class Vertex:
  
  def __init__(self, label, weight=None):
    '''
      a vertex have a label and a weight
      and the label cann't be None
    '''
    self.label = label
    self.set_weight(weight)
    
  def set_weight(self, weight=None):
    if not weight:
      weight = 1.0
    self.weight = weight
    
  def __repr__(self):
    return f'V(label={self.label}, weight={self.weight})'
  
class Vertices:
  
  def __init__(self, verbose=False):
    self.verbose = verbose
    self.clear()
  
  def clear(self):
    self._vertices = []
    self._label2id = {}
    self.next_id = 0
    self._removed_ids = []
    
  @property
  def labels(self):
    return list(self._label2id.keys())
    
  @property
  def ids(self):
    return list(self._label2id.values())
  
  def get_next_id(self):
    vid = self.next_id
    if self._removed_ids:
      vid = self._removed_ids.pop()
    else: 
      self.next_id += 1
    return vid
  
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
  
  def get(self, label):
    vid = self.to_id(label)
    if not vid:
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
    vid = self.get_next_id()
    assert vid <= len(self._vertices), f'Error happen when insert vertex {label}'
    if vid == len(self._vertices):
      self._vertices.append(Vertex(label, weight))
    else:
      self._vertices[vid].set_weight(weight)
    self._label2id[label] = vid
    self._vertices[vid].label = label
    self._vertices[vid].set_weight(weight)
    return vid
  
  def remove(self, label):
    vid = self.to_id(label)
    if vid is not None:
      self._removed_ids.append(vid)
      self._label2id.pop(label)
    return vid
  
  def modify(self, label, weight):
    vertex = self.get(label)
    vertex.set_weight(weight)
  