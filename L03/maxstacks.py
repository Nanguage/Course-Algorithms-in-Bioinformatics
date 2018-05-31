from math import floor
from functools import reduce

from utils import score


class MaxStackingPairs(object):
    """
    Dynamic programming,
    mixmize the number of stacking pairs in an RNA sequence.
    """

    def __init__(self, score_func=score):
        self.score_func = score_func
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

    def can_form_stacking_pair_at(self, i, j):
        if j <= i + 2:
            return False
        else:
            S = self.seq
            score = self.score_func
            if score(S[i], S[j]) * score(S[i+1], S[j-1]) != 0:
                return True
            else:
                return False

    def fill_matrix(self):
        seq = self.seq
        score = self.score_func
        n = len(seq)
        V = [[0 for j in range(n)] for i in range(n)]
        for offset in range(3, n):
            for i in range(n - offset):
                j = i + offset
                # no stacking pair at position j
                v0 = V[i][j-1]
                # no stacking pair at position i
                v1 = V[i+1][j]
                m = floor((j - i + 1) / 2.0) - 1
                # form a length 'h' stacking pair at (k, j)
                v2 = max([V[i+h+1][j-h-1] + \
                          h*reduce(
                              lambda a,b:a*b,
                              [score(seq[i+t], seq[j-t]) for t in range(h+1)])
                          for h in range(1, m+1)] + [0])
                # form a stacking pairs at (i, k) and (k, j)
                v3 = max([V[i][k] + V[k+1][j]
                          for k in range(i+3, j)]) if j > i+3 else 0

                V[i][j] = max([v0, v1, v2, v3])
        self.V_matrix = V

    def get_pairs(self):
        seq = self.seq
        n = len(self.V_matrix)
        V = self.V_matrix
        score_func = self.score_func
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
                            score = h * reduce(lambda a,b:a*b, [score_func(seq[k+t], seq[j-t]) for t in range(h+1)])
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
