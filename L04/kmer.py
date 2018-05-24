def jellyfish_count(k, seqs):
    for seq in seqs:
        count_table = {}
        for i in range(len(seq) - k):
            kmer = seq[i:i+k]
            count_table.setdefault(kmer, 0)
            count_table[kmer] += 1
    return count_table


def select_solid(count_table, m):
    return {k: v for k, v in count_table.items() if v > m}
