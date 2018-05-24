from copy import copy

import networkx as nx
import matplotlib.pyplot as plt

class DeBrujin(object):
    
    def __init__(self, k):
        self.k = k
        self.graph = nx.DiGraph()

    def build_graph(self, seq):
        G = self.graph
        k = self.k

        last_kmer = None
        for i in range(len(seq) - k + 1):
            kmer = seq[i:i+k]
            if kmer not in G.nodes:
                G.add_node(kmer)
                G.nodes[kmer]['count'] = 0
            else:
                G.nodes[kmer]['count'] += 1
            
            if last_kmer is not None:
                G.add_edge(last_kmer, kmer)
            
            last_kmer = kmer
            
    def get_contigs(self):
        pass

    def draw(self, path):
        nx.draw(self.graph, with_labels=True,
                node_color='w', node_size=600)
        plt.savefig(path)

    def draw_with_dot(self, path, fig_format='pdf'):
        dotg = nx.drawing.nx_pydot.to_pydot(self.graph)
        dotg.set_rankdir('LR')
        cmd = "dotg.write_{}('{}')".format(fig_format, path)
        exec(cmd)

    def euler_walk(self, start_node):
        G = self.graph
        paths = []

        def walk(node, path, visited_edges=set()):

            path.append(node)

            destinations = G[node]
            possible_dests = [dest for dest in destinations
                                   if (node, dest) not in visited_edges]

            if len(possible_dests) == 0:
                # arrived at the end
                if visited_edges == set(G.edges):
                    return path
                else:
                    return

            for dest in possible_dests:
                visited = copy(visited_edges)
                path = copy(path)
                edge = (node, dest)
                visited.add(edge)

                res = walk(dest, copy(path), copy(visited))

                if res is not None:
                    paths.append(res)

        walk(start_node, [], set())
        return paths
