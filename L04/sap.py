"""
Spectral alignment problem (SAP) Dynamic Programming solving.
"""

import math

import networkx as nx
import pydot


def hamming_distance(s, t):
    """
    return the hamming distance bwtween two sequences.
    """
    assert len(s) == len(t)
    distance = 0
    for i in range(len(s)):
        if s[i] != t[i]:
            distance += 1
    return distance


def base_similarity(s, t):
    return 1 if s == t else 0


class SAP(object):
    CHAR_SET = ['A', 'T', 'C', 'G']
    
    def __init__(self, T_kmers):
        self.T_kmers = T_kmers
        T = list(T_kmers)        
        k = len(T[0])
        assert all([len(t) == k for t in T]), \
            "All kmers must with same k."
        self.k = k
        self.dependency_graph = nx.DiGraph()

    def build_dependency_graph(self, seq, distance_func=hamming_distance):
        self._seq = seq
        self._start_node = 'start'
        self.__build_nodes(seq)
        self.__build_edges(seq, distance_func)
    
    def __build_nodes(self, seq):
        G = self.dependency_graph
        T = self.T_kmers
        k = self.k
        start_layer = [self._start_node]
        num_layers = len(seq) - self.k + 1
        layers = [start_layer]
        G.add_node(self._start_node)
        for i in range(num_layers):
            layer = []
            for t in list(T):
                node = (i+k, t)
                G.add_node(node)
                layer.append(node)
            layers.append(layer)
        self.layers = layers
    
    def __build_edges(self, seq, distance_func):
        G = self.dependency_graph
        T = self.T_kmers
        k = self.k
        # build first layer edge
        prefix = seq[:k]
        for t in list(T):
            w = distance_func(prefix, t)
            G.add_edge(self._start_node, (k, t), weight=w)
        # build middle layers
        match_and_insert_edges = {}
        for t in list(T):
            match_and_insert_edges.setdefault(t, [])
            for char in SAP.CHAR_SET:
                t_ = t[1:] + char
                if t_ in T and t_ != t:
                    match_and_insert_edges[t].append(t_)

        for l_idx in range(k, len(seq)+1):
            for t in list(T):
                # add verticle edge (delete)
                G.add_edge((l_idx, t), (l_idx+1, t), weight=1)
                # add skew edge (match)
                if l_idx != len(seq):
                    for t_ in match_and_insert_edges.get(t):
                        w = 0 if seq[l_idx] == t_[-1] else 1
                        G.add_edge((l_idx, t), (l_idx+1, t_), weight=w)
                # add horizontal edges (insert)
                if l_idx != k:
                    for t_ in match_and_insert_edges.get(t):
                        G.add_edge((l_idx, t), (l_idx, t_), weight=1)
    
    def min_distance(self):
        G = self.dependency_graph
        T = self.T_kmers
        paths = []
        for t in T:
            p = nx.shortest_path_length(G,
                    source=self._start_node,
                    target=(len(self._seq), t),
                    weight='weight')
            paths.append(p)
        return min(paths)
    
    def write_dependency_graph(self, path, fig_format='pdf'):
        G = self.dependency_graph
        for u,v,d in G.edges(data=True):
            d['label'] = d.get('weight','')
        dotg = nx.drawing.nx_pydot.to_pydot(G)
        cmd = "dotg.write_{}('{}')".format(fig_format, path)
        exec(cmd)
