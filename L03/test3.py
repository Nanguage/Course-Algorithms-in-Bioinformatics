import os

from minstackenergy import MinStackingEnergy
from utils import FastaReader, pairs2parentheses, print_matrix


if __name__ == "__main__":
    mspe = MinStackingEnergy()
    seq = "AUAUGCGC"
    #seq = "ACCAGGU"
    mspe.seq = seq
    mspe.fill_matrix()
    print_matrix(mspe.V_matrix)
    pairs = mspe.get_pairs()
    print(pairs)
    print(seq)
    print(pairs2parentheses(pairs, len(seq)))
