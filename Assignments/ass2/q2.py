from os.path import join, dirname, abspath
import sys

HERE = dirname(abspath(__file__))
sys.path.insert(0, join(HERE, "../../L04"))

from debrujin import DeBrujin

if __name__ == "__main__":
    seqs = ['ACCTCC', 'TCCGCC', 'CCGCCA']
    for k in [2, 3]:
        dbg = DeBrujin(k)
        for seq in seqs:
            dbg.build_graph(seq)

        G = dbg.graph
        dbg.draw_with_dot("img/q2-k{}.pdf".format(k))

        print("nodes when k = {}:".format(k))
        print(G.nodes)
        print("edges when k = {}:".format(k))
        print(G.edges)
        print("euler pathes when k = {}:".format(k))
        if k == 2:
            for path in dbg.euler_walk('AC'):
                print(' -> '.join(path))
        if k == 3:
            for path in dbg.euler_walk('ACC'):
                print(' -> '.join(path))

