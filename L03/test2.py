import os

from maxstacks import MaxStackingPairs
from utils import FastaReader, pairs2parentheses, print_matrix


if __name__ == "__main__":
    msp = MaxStackingPairs()
    #seq = "AUAUGCGC"
    #seq = "ACCAGGU"
    seq = "GCGCUCUGAUGAGGCCGCAAGGCCGAAACUGCCGCAAGGCAGUCAGCGC"
    msp.seq = seq
    msp.fill_matrix()
    print_matrix(msp.V_matrix)
    pairs = msp.get_pairs()
    print(pairs)
    print(seq)
    print(pairs2parentheses(pairs, len(seq)))
