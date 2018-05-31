import os

from maxstacks import MaxStackingPairs
from utils import FastaReader, pairs2parentheses, print_matrix


if __name__ == "__main__":
    msp = MaxStackingPairs()
    #seq = "AUAUGCGC"
    #seq = "ACCAGGU"
    seq = "GCGCUCUGAUGAGGCCGCAAGGCCGAAACUGCCGCAAGGCAGUCAGCGC"
    #seq = "AGGCCGCAAGGCCGAAACUGCCG"
    #seq = "CAUCGAACGUCCUCAAGACAGCUCUCU"
    msp.seq = seq
    msp.fill_matrix()
    print_matrix(msp.V_matrix, seq=seq)
    pairs = msp.get_pairs()
    print(pairs)
    print(seq)
    parentheses = pairs2parentheses(pairs, len(seq))
    print(parentheses)
    assert parentheses.count("(") == parentheses.count(")")
