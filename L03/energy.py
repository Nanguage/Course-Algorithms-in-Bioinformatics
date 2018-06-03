
STACKING_PAIR_FREE_ENERGY_MAT = \
    [[-0.9, -2.2, -2.1, -1.1, -0.6, -1.4],
     [-2.1, -3.3, -2.4, -2.1, -1.4, -2.1],
     [-2.4, -3.4, -3.3, -2.2, -1.5, -2.5],
     [-1.3, -2.4, -2.1, -0.9, -1.0, -1.3],
     [-1.3, -2.5, -2.1, -1.4, -0.5,  1.3],
     [-1.0, -1.5, -1.4, -0.6,  0.3, -0.5]]

STACKING_PAIR_FREE_ENERGY_ORDER = \
    [('A', 'U'), ('C', 'G'), ('G', 'C'),
     ('U', 'A'), ('G', 'U'), ('U', 'G')]

PAIR2ORDER = {pair: i for (i, pair) in enumerate(STACKING_PAIR_FREE_ENERGY_ORDER)}

def stacking_pair_free_energy(p, q, x, y):
    p, q, x, y = [i.upper() for i in (p, q, x, y)]
    mat = STACKING_PAIR_FREE_ENERGY_MAT
    pair2order = PAIR2ORDER
    if (x, y) in pair2order and (p, q) in pair2order:
        xy_pos = pair2order[(x, y)]
        pq_pos = pair2order[(p, q)]
        energy = mat[pq_pos][xy_pos]
        return energy
    else:
        return None


TURNER_TABLE = \
    [['.',    3.8,     '.'],
     ['.',    2.8,     '.'],
     ['.',    3.2,    5.4],
     [1.1,    3.6,    5.6],
     [2.0,    4.0,    5.7],
     [2.0,    4.4,    5.4],
     [2.1,    4.6,    6.0],
     [2.3,    4.7,    5.5],
     [2.4,    4.8,    6.4],
     [2.5,    4.9,    6.5],
     [2.6,    5.0,    6.6],
     [2.7,    5.1,    6.7],
     [2.8,    5.2,    6.8],
     [2.9,    5.3,    6.9],
     [2.9,    5.4,    6.9],
     [3.0,    5.4,    7.0],
     [3.1,    5.5,    7.1],
     [3.1,    5.5,    7.1],
     [3.2,    5.6,    7.2],
     [3.3,    5.7,    7.2],
     [3.3,    5.7,    7.3],
     [3.4,    5.8,    7.3],
     [3.4,    5.8,    7.4],
     [3.5,    5.8,    7.4],
     [3.5,    5.9,    7.5],
     [3.5,    5.9,    7.5],
     [3.6,    6.0,    7.5],
     [3.6,    6.0,    7.6],
     [3.7,    6.0,    7.6],
     [3.7,    6.1,    7.7]]

def loop_energy(type_, size):
    table = TURNER_TABLE
    order = ['internal', 'bulge', 'hairpin']
    type2order = {v:i for i,v in enumerate(order)}
    idx = type2order[type_]
    if size > 30:
        return table[-1][idx]
    else:
        return table[size][idx]

def internal_loop_energy(size):
    if size <= 3:
        raise ValueError("Size of internal loop must large than 3.")
    else:
        return loop_energy('internal', size)

def bulge_energy(size):
    return loop_energy('bulge', size)

def hairpin_energy(size):
    if size <= 2:
        raise ValueError("Size of internal loop must large than 2.")
    else:
        return loop_energy('hairpin', size)

