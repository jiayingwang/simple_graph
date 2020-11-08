from collections import defaultdict
class Graph:
    
    def __init__(self, edges=None, symmetric=True, default_weight=1):
        self._symmetric = symmetric
        self._default_weight = default_weight
        self.clear()
        if not edges:
            edges = {}
        for u in edges:
            if type(edges[u]) is list:
                for v in edges[u]:
                    self.add_edge(u, v)
            elif type(edges[u]) is dict:
                for v in edges[u]:
                    self.add_edge(u, v, edges[u][v])
            else:
                raise ValueError('Edge format is not correct.')
    
    def clear(self):
        self._nodes = {}
        self._edges = defaultdict(dict)
        self._total_edge_weight = 0
        self._total_node_edge_weight = defaultdict(int)
     
    @property
    def nodes(self):
        return list(self._nodes.keys())
    
    @property
    def edges(self):
        edges = []
        for u in self._edges:
            for v in self._edges[u]:
                edges.append((u, v))
        return edges
    
    @property
    def edge_weights(self):
        edges = []
        for u in self._edges:
            for v in self._edges[u]:
                edges.append((u, v, self._edges[u][v]))
        return edges
    
    def load(self, file_name):
        self.clear()
        with open(file_name) as f:
            for line in f:
                items = line.split()
                u = items[0]
                v = items[1]
                w = self._default_weight
                if len(items) > 2:
                    w = items[2]
                self.add_edge(u, v, w)
        return 
    
    def add_edge(self, u, v, weight=None):
        if weight == None:
            weight = self._default_weight
        self._edges[u][v] = weight
        self._total_node_edge_weight[v] += weight
        self._total_edge_weight += weight
        if u not in self._nodes:
            self._nodes[u] = weight
        if v not in self._nodes:
            self._nodes[v] = weight
        if self._symmetric:
            self._edges[v][u] = weight
            self._total_node_edge_weight[u] += weight
            self._total_edge_weight += weight
            
    def has_edge(self, u, v):
        if u not in self._edges:
            return False
        if v not in self._edges[u]:
            return False
        return True
            
    def add_node(self, u, weight=None):
        if weight == None:
            weight = self._default_weight
        self._nodes[u] = weight
        
    def has_node(self, u):
        if u in self._nodes:
            return True
        else:
            return False
        
    def neighbors(self, u):
        if not self.has_node(u):
            return None
        return list(self._edges[u].keys())
    
    def node_weight(self, i):
        if i not in self._nodes:
            return None
        return self._nodes[i]
        
    def edge_weight(self, u, v):
        if u not in self._edges or v not in self._edges[u]:
            return None
        return self._edges[u][v]
    
    def total_edge_weight(self, u=None):
        if u == None:
            return self._total_edge_weight
        
        if not self.has_node(u):
            return 0
        
        return self._total_node_edge_weight[u]
    
    def __repr__(self):
        return str(dict(self._edges))