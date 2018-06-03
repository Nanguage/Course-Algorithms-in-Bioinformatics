import os

from minstackenergy import MinStackingEnergy
from utils import FastaReader, pairs2parentheses, view_matrix


if __name__ == "__main__":
    mspe = MinStackingEnergy()
    #seq = "AUAUGCGC"
    #seq = "ACCAGGU"
    seq = "GCGCUCUGAUGAGGCCGCAAGGCCGAAACUGCCGCAAGGCAGUCAGCGC"
    mspe.seq = seq
    mspe.fill_matrix()
    pairs = mspe.get_pairs()
    print(pairs)
    print(seq)
    print(pairs2parentheses(pairs, len(seq)))
    print(mspe.max_score())
    #view_matrix(mspe.V_matrix, seq)
