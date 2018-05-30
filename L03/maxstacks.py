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

    def fill_matrix(self):
        seq = self.seq
        score = self.score_func
        n = len(seq)
        V = [[0 for j in range(n)] for i in range(n)]
        for offset in range(3, n):
            for i in range(n - offset):
                j = i + offset
                v0 = V[i][j-1]
                v1 = V[i+1][j]
                v2 = V[i+1][j-1] + score(seq[i], seq[j]) * score(seq[i+1], seq[j-1])
                v3 = max([V[i][k] + V[k+1][j] for k in range(i+3, j)]) if j > i+3 else 0
                V[i][j] = max([v0, v1, v2, v3])
        self.V_matrix = V

    def get_pairs(self):
        seq = self.seq
        n = len(self.V_matrix)
        V = self.V_matrix
        score_func = self.score_func
        pairs = set()
        cache = set()
        def traceback(i, j):
            if (i, j) in cache:
                return
            if j <= i+2:
                cache.add((i, j))
                return
            elif V[i][j] == V[i][j-1]:
                traceback(i, j-1)
            elif V[i][j] == V[i+1][j]:
                traceback(i+1, j)
            else:
                score = score_func(seq[i], seq[j]) * score_func(seq[i+1], seq[j-1])
                if score != 0:
                    pairs.add((i, j))
                    pairs.add((i+1, j-1))
                    traceback(i+1, j)
                    traceback(i, j-1)
                    cache.add((i, j))
                    return
                else:
                    for k in range(i+3, j):
                        traceback(i, k)
                        traceback(k+1, j)
        traceback(0, n-1)
        return pairs

    def max_score(self):
        n = len(self.V_matrix)
        return self.V_matrix[0][n-1]