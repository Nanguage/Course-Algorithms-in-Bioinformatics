from utils import score


class Nussinov(object):
    """
    Dynamic Programming,
    maxmize the number of base pairs in an RNA sequence.
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
        for m in range(n - 1):
            for i in range(n - m - 1):
                j = i + m + 1
                v0 = V[i+1][j-1] + score(seq[i], seq[j])
                v1 = max([V[i][k] + V[k+1][j] for k in range(i, j)])
                V[i][j] = max(v0, v1)
        self.V_matrix = V

    def get_pairs(self):
        seq = self.seq
        n = len(self.V_matrix)
        V = self.V_matrix
        pairs = set()
        def traceback(i, j):
            if j <= i:
                return
            elif V[i][j] == V[i][j-1]:
                traceback(i, j-1)
            else:
                for k in range(i, j+1):
                    if self.score_func(seq[k], seq[j]) != 0:
                        if V[i][j] == V[i][k-1 if k-1 >= 0 else 0] + V[k+1][j-1] + 1:
                            pairs.add((k, j))
                            traceback(i, k-1)
                            traceback(k+1, j-1)
                            return
        traceback(0, n-1)
        return pairs

    def max_score(self):
        n = len(self.V_matrix)
        return self.V_matrix[0][n-1]
