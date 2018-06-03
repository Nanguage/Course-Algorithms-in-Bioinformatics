import math
from math import floor
from functools import reduce

from energy import stacking_pair_free_energy
from utils import score



def logistic(x, n, x0=6, a=1, b=math.e, c=3, L=1):
    return L / (a + b**(-c*(x-x0)))

def linear(x, n):
    return x / n

def relu(x, n, cut=5):
    if x <= cut:
        return 0
    else:
        return 1


class MinStackingEnergy(object):
    """
    Dynamic programming,
    minimize the stacking pairs energy.
    """

    def __init__(self, score_func=score,
                 energy_func=stacking_pair_free_energy):
        self.score_func = score_func
        self.energy_func = energy_func
        self.V_matrix = None
        self.seq = None

    def predict(self, seq):
        """
        Predict the second structure.
        Return a set of pairs.
        """
        self.seq = seq
        self.fill_matrix()
        return self.get_pairs()

    def free_energy_of_stacking_pairs_with_length(self, i, j, h, penalty_func=logistic):
        seq = self.seq

        matchs = []
        for t in range(h+1):
            matchs.append(score(seq[i+t], seq[j-t]))
        all_match = reduce(lambda a,b:a*b, matchs)
        if all_match:
            energys = []
            for t in range(h):
                e = stacking_pair_free_energy(seq[i+t], seq[j-t], seq[i+t+1], seq[j-t-1])
                if penalty_func:
                    d = float(j - i - 2*t)
                    r = penalty_func(d, len(seq))
                    e = e * r
                energys.append(e)
            eS = -sum(energys)
            return eS
        else:
            return 0

    def free_energy_of_stacking_pairs_at(self, i, j):
        V = self.V_matrix
        m = floor((j - i + 1) / 2.0) - 1
        v2_possible = []
        for h in range(1, m+1):
            eS = self.free_energy_of_stacking_pairs_with_length(i, j, h)
            v2_possible.append(V[i+h+1][j-h-1] + eS)
        v2 = max(v2_possible + [0])
        return v2

    def fill_matrix(self):
        seq = self.seq
        n = len(seq)
        V = [[0 for j in range(n)] for i in range(n)]
        self.V_matrix = V
        for offset in range(3, n):
            for i in range(n - offset):
                j = i + offset
                # no stacking pair at position j
                v0 = V[i][j-1]
                # no stacking pair at position i
                v1 = V[i+1][j]
                # form a length 'h' stacking pair at (k, j)
                v2 = self.free_energy_of_stacking_pairs_at(i, j)
                # form a stacking pairs at (i, k) and (k, j)
                v3 = max([V[i][k] + V[k+1][j]
                          for k in range(i+3, j)]) if j > i+3 else 0

                V[i][j] = max([v0, v1, v2, v3])

    def get_pairs(self):
        n = len(self.V_matrix)
        V = self.V_matrix
        pairs = set()
        def traceback(i, j):
            if j <= i+2:
                return
            elif V[i][j] == V[i][j-1]:
                traceback(i, j-1)
            elif V[i][j] == V[i+1][j]:
                traceback(i+1, j)
            else:
                for k in range(i, j):
                    if V[i][j] == V[i][k] + V[k+1][j] :
                        traceback(i, k)
                        traceback(k+1, j)
                        return
                    else:
                        m = floor((j - k + 1)/2) - 1
                        for h in range(m, 0, -1):
                            score = self.free_energy_of_stacking_pairs_with_length(k, j, h)
                            if score != 0 and V[i][j] == V[k+h+1][j-h-1] + score:
                                for t in range(h+1):
                                    pairs.add((k+t, j-t))
                                traceback(i, k-1)
                                traceback(k+h+1, j-h-1)
                                return
        traceback(0, n-1)
        return pairs

    def max_score(self):
        n = len(self.V_matrix)
        return self.V_matrix[0][n-1]
