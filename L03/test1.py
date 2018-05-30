import os

from nussinov import Nussinov
from utils import FastaReader, pairs2parentheses, print_matrix


if __name__ == "__main__":
    nus = Nussinov()
    seq = "ACCAGCU"
    nus.seq = seq
    nus.fill_matrix()
    print_matrix(nus.V_matrix)
    pairs = nus.get_pairs()
    print(pairs)
    print(seq)
    print(pairs2parentheses(pairs, len(seq)))
