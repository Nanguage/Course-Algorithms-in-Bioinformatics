from time import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from nussinov import Nussinov
from maxstacks import MaxStackingPairs
from minstackenergy import MinStackingEnergy
ALGs = [Nussinov, MaxStackingPairs, MinStackingEnergy]

seq1 = "GCGCUCUGAUGAGGCCGCAAGGCCGAAACUGCCGCAAGGCAGUCAGCGC"
seq2 = "GGCGCGUUAACAAAGCGGUUAUGUAGCGGAUUGCAAAUCCGUCUAGUCCGGUUCGACUCCGGAACGCGCCUCCA"
seq3 = "GGGAGGUUGGUGGUGGACGAGCCACUCGCCAACCGGGUCAGGUCCGGAAGGAAGCAGCCCUAACGAGCCAGGCACGGGUCGCCGUGCCAGCCUCCCACCUUUU"
SEQs = [seq1, seq2, seq3]
SEQs_NAME = ["hammerhead_ribozyme", "PDB_00313", "SRP_00004"]

N = 100

def run_alg(alg, seq):
    start = time()
    alg_ = alg()
    alg_.predict(seq)
    end = time()
    comsume = end - start
    return comsume

def benchmark(n=N):
    res = []
    for alg in ALGs:
        for seq, seqname in zip(SEQs, SEQs_NAME):
            seqlen = len(seq)
            for _ in range(n):
                time_c = run_alg(alg, seq)
                res.append([alg.__name__, seqname, seqlen, time_c])
    res_df = pd.DataFrame(res, columns=["Algorithm", "Sequence", "Sequence length", "Time"])
    return res_df

if __name__ == "__main__":
    df = benchmark(10)
    fig, ax = plt.subplots()

    sns.stripplot(ax=ax, data=df, x="Sequence", y="Time",
        hue="Algorithm", jitter=True, size=4, palette="Set2")
    with plt.rc_context({'lines.linewidth': 0.8}):
        sns.pointplot(ax=ax, data=df, x="Sequence", y="Time",
            hue="Algorithm", linestyles='--', markers='x', palette="Set2")
    plt.xlabel("")
    plt.ylabel("Time Consume(s)", fontsize=12)
    handles, labels = ax.get_legend_handles_labels()
    l = plt.legend(handles[:3], labels[:3], loc=2)

    plt.savefig("time_consume.pdf")
