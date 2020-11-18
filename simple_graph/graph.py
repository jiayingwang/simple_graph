from collections import defaultdict
from math import inf
class Graph:
    
    def __init__(self, edges=None, symmetric=True, allow_self_link=False, default_weight=1, verbose=False):
        self._symmetric = symmetric
        self._default_weight = default_weight
        self._allow_self_link = allow_self_link
        self.verbose = verbose
        self.clear()
        if not edges:
            edges = {}
        if type(edges) is list:
            self.add_edges(edges)
        elif type(edges) is dict or type(edges) is defaultdict:
            for u in edges:
                self.add_node(u)
                if type(edges[u]) is list:
                    for v in edges[u]:
                        self.add_edge(u, v)
                elif type(edges[u]) is dict or type(edges) is defaultdict:
                    for v in edges[u]:
                        self.add_edge(u, v, edges[u][v])
                else:
                    raise ValueError('Edge format is not correct.')
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
        if self._symmetric:
            return [(u, v) for u in self._edges for v in self._edges[u] if u <= v]
        else:
            return [(u, v) for u in self._edges for v in self._edges[u]]
    
    @property
    def edge_weights(self):
        edges = []
        for u in self._edges:
            for v in self._edges[u]:
                edges.append((u, v, self._edges[u][v]))
        return edges
    
    def load(self, file_name):
        self.clear()
        edge_list = []
        with open(file_name) as f:
            for line in f:
                edge_list.append(line.split())
            self.add_edges(edge_list)
            
    def add_edges(self, edge_list):
        for edge in edge_list:
            u = edge[0]
            v = edge[1]
            w = self._default_weight
            if len(edge) > 2:
                w = edge[2]
            self.add_edge(u, v, w)
            
    def remove_edges(self, edge_list):
        for edge in edge_list:
            u = edge[0]
            v = edge[1]
            self.remove_edge(u, v)
    
    def add_edge(self, u, v, weight=None):
        if u == v:
            self._allow_self_link = True
        if weight == None:
            weight = self._default_weight
        if self.verbose:
            print('add edge', u, v)
        old_weight = self._edges[u].get(v, 0)
        self._edges[u][v] = weight
        self._total_node_edge_weight[v] += weight - old_weight
        self._total_edge_weight += weight - old_weight
        if u not in self._nodes:
            self.add_node(u)
        if v not in self._nodes:
            self.add_node(v)
        if self._symmetric:
            if self.verbose:
                print('add edge', v, u)
            old_weight = self._edges[v].get(u, 0)
            self._edges[v][u] = weight
            self._total_node_edge_weight[u] += weight - old_weight
            self._total_edge_weight += weight - old_weight
            
    def remove_edge(self, u, v):
        if self.verbose:
            print('remove edge', u, v)
        weight = self._edges[u].pop(v, None)
        if weight:
            self._total_node_edge_weight[v] -= weight
            self._total_edge_weight -= weight
        if self._symmetric:
            if self.verbose:
                print('remove', v, u)
            weight = self._edges[v].pop(u, None)
            if weight:
                self._total_node_edge_weight[u] -= weight
                self._total_edge_weight -= weight
            
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
        
    def remove_node(self, u, weight=None):
        weight = self._nodes.pop(u, None)
        if weight:
            for v in list(self._edges[u]):
                self.remove_edge(u, v)
            self._edges.pop(u, None)
            if not self._symmetric:
                for edge in self.edges:
                    if edge[1] == u:
                        self.remove_edge(edge[0], edge[1])
        
    def has_node(self, u):
        if u in self._nodes:
            return True
        else:
            return False
    
    def node_degree(self, u):
        neighbors = self.neighbors(u)
        return len(neighbors) + neighbors.count(u)
    
    def node_degrees(self):
        node_degrees = []
        for u in self.nodes:
            node_degrees.append(self.node_degree(u))
        node_degrees.sort(reverse=True)
        return node_degrees
    
    def min_degree(self):
        min_degree = inf
        for u in self.nodes:
            node_degree = self.node_degree(u)
            if node_degree < min_degree:
                min_degree = node_degree
        return min_degree
    
    def max_degree(self):
        max_degree = 0
        for u in self.nodes:
            node_degree = self.node_degree(u)
            if node_degree > max_degree:
                max_degree = node_degree
        return max_degree
    
    def density(self):
        V = len(self.nodes)
        E = len(self.edges)
        if self._symmetric:
            E *= 2
        return float(f'{E / V ** 2 if self._allow_self_link else E / (V * (V-1)):.4f}')
        
    def is_connected(self, vis_nodes=None, start=None):
        if vis_nodes is None:
            vis_nodes = set()
        nodes = self.nodes
        if not start:
            start = nodes[0]
        vis_nodes.add(start)
        if len(vis_nodes) == len(nodes):
            return True
        else:
            for u in self.neighbors(start):
                if u not in vis_nodes and self.is_connected(vis_nodes, u):
                    return True
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
    
    def find_isolated_nodes(self):
        isolated = []
        for n in self.nodes:
            if not self.neighbors(n):
                isolated.append(n)
        return isolated
    
    def find_path(self, start, end, path=None):
        if start not in self.nodes or end not in self.nodes:
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
        if start not in self.nodes or end not in self.nodes:
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
        nodes = self.nodes
        pairs = [(nodes[i],nodes[j]) for i in range(len(nodes)-1) for j in range(i+1, len(nodes))]
        smallest_paths = []
        for (s,e) in pairs:
            paths = self.find_all_paths(s,e)
            smallest = sorted(paths, key=len)[0]
            smallest_paths.append(smallest)
        smallest_paths.sort(key=len)
        diameter = len(smallest_paths[-1])-1
        return diameter
    
    def __repr__(self):
        return str(dict(self._edges))
