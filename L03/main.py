import argparse
from collections import namedtuple

from utils import FastaReader, pairs2parentheses
from nussinov import Nussinov
from maxstacks import MaxStackingPairs
from minstackenergy import MinStackingEnergy


def argument_parser():
    parser = argparse.ArgumentParser(
        prog="RNA-2nd-structure-predictor",
        description="Predict the secondary structure of an RNA sequence.")

    parser.add_argument("input", 
                        help="Path to input fasta file.")
    parser.add_argument("--method",
                        default="nussinov",
                        const="nussinov",
                        nargs="?",
                        choices=["nussinov", "maxstacks", "minstackenergy"],
                        help="Algorithm used for predict.")
    parser.add_argument("--print_max_score", "-v",
                        action="store_true",
                        default=False,
                        help="Print the max score.")

    return parser


ResultTuple = namedtuple("ResultTuple", ["name", "seq", "parentheses", "max_score"])


def run_algorithm(algorithm, reader):
    algo = algorithm()
    for name, seq in reader:
        pairs = algo.predict(seq)
        max_score = algo.max_score()
        parentheses = pairs2parentheses(pairs, len(seq))
        result = ResultTuple(name, seq, parentheses, max_score)
        yield result


def main(args):

    fa_reader = FastaReader(args.input)

    method = args.method
    if method == "nussinov":
        algo = Nussinov
    elif method == "maxstacks":
        algo = MaxStackingPairs
    else:
        algo = MinStackingEnergy
    results = run_algorithm(algo, fa_reader)

    for res in results:
        print("> {}".format(res.name))
        print(res.seq)
        print(res.parentheses)
        if args.print_max_score:
            print(res.max_score)


if __name__ == "__main__":
    parser = argument_parser()
    args = parser.parse_args()
    main(args)

