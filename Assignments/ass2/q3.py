from os.path import join, dirname, abspath
import sys

HERE = dirname(abspath(__file__))
sys.path.insert(0, join(HERE, "../../L04"))

from sap import SAP

if __name__ == "__main__":
    sequence = "CTGCACT"
    T = set(["ACT", "CAC", "CTG", "CTT", "TCA", "TTC"])
    sap = SAP(T)
    sap.build_dependency_graph(sequence)
    sap.write_dependency_graph("./img/q3-graph.pdf")
    min_distance = sap.min_distance()
    print("The minimium edit distance is {}.".format(min_distance))
