import os

from nussinov import Nussinov
from utils import FastaReader, pairs2parentheses, print_matrix


if __name__ == "__main__":
    nus = Nussinov()
    #seq = "ACCAGCU"
    seq = "GCGCUCUGAUGAGGCCGCAAGGCCGAAACUGCCGCAAGGCAGUCAGCGC"
    nus.seq = seq
    nus.fill_matrix()
    print_matrix(nus.V_matrix, seq=seq)
    pairs = nus.get_pairs()
    print(pairs)
    print(seq)
    parentheses = pairs2parentheses(pairs, len(seq))
    print(parentheses)
    print(parentheses.count("("))
