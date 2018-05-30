PAIR_SCORES = {
    ('A', 'U'): 1,
    ('U', 'A'): 1,
    ('G', 'C'): 1,
    ('C', 'G'): 1,
    ('G', 'U'): 1,
}


def score(base1, base2, pair_scores=PAIR_SCORES, default_score=0):
    if (base1, base2) in pair_scores:
        base1 = base1.upper()
        base2 = base2.upper()
        return pair_scores[(base1, base2)]
    else:
        return default_score


class FastaReader(object):
    def __init__(self, path):
        self.file_handle = open(path)

    def __iter__(self):
        name = None
        seq = None
        for line in self.file_handle:
            line = line.strip()
            if line.startswith(">"):
                name = line[1:]
                continue
            seq = line
            yield (name, seq)

    def __close__(self):
        self.file_handle.close()


def pairs2parentheses(pairs, seq_len,
                      default_symbol='.',
                      left_symbol='(', right_symbol=')'):
    parentheses = [default_symbol for _ in range(seq_len)]
    for i, j in list(pairs):
        parentheses[i] = left_symbol
        parentheses[j] = right_symbol
    parentheses = "".join(parentheses)
    return parentheses


def print_matrix(mat):
    import numpy as np
    arr = np.array(mat)
    print(arr)