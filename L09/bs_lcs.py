from bisect import bisect


class LCS(object):

    def __init__(self, A, B):
        self.A = A
        self.B = B
        n = len(A)
        assert len(B) == n
        self.tuples_table = []
        self._build_tuples_table(A, B)

    def delta(self, element):
        return self.B.index(element)

    def _build_tuples_table(self, A, B):
        delta = self.delta
        self.tuples_table.append([(delta(1), 1)])
        for i in range(2, len(A)+1):
            tree = self.tuples_table[i-2]
            tree_new = []
            for t in tree:
                j, e = t
                if not ((j >= delta(i)) and \
                        self.query(i-2, j) <= (self.query(i-2, delta(i)-1) + 1)):
                    tree_new.append(t)
            tree_new.append( (delta(i), self.query(i-2, delta(i)-1) + 1) )
            tree_new.sort(key=lambda t:t[0])
            self.tuples_table.append(tree_new)

    def query(self, i, j):
        if j < 0:
            return 0
        tree = self.tuples_table[i]
        tree_ = [idx for (idx, value) in tree]
        idx = bisect(tree_, j)
        if idx <= 0:
            return 0
        value = tree[max(idx-1,0)][1]
        return value

    def to_dense(self):
        n = len(self.A)
        res = [[0 for j in range(n)] for i in range(n)]
        for i, tree in enumerate(self.tuples_table):
            for idx, value in tree:
                for j in range(idx, n):
                    res[i][j] = value
        return res
