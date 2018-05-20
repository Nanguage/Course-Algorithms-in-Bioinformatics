#include <stdio.h>

#define EMPTY_SYMBOL '-'


int similarity_score(char* source, char* target,
               int match_score, int penalty_mismatch,
               int penalty_insert, int penalty_delete)
/*
    Calculate the edit distance of an alignment result.
    The length of source and target sequences are same.
*/
{
    int score = 0;
    char* s_pt = source;
    char* t_pt = target;

    while (*s_pt != '\0') {
        char s = *s_pt;
        char t = *t_pt;

        if (s == t) {
            /* Matched */
            score += match_score;
        } else {

            if (s == EMPTY_SYMBOL && t != EMPTY_SYMBOL) {
                /* Deletion */
                score += penalty_delete;
            } else if (s != EMPTY_SYMBOL && t == EMPTY_SYMBOL) {
                /* Insertion */
                score += penalty_insert;
            } else {
                /* Mismatch */
                score += penalty_mismatch;
            }
        }

        ++s_pt;
        ++t_pt;
    }

    return score;
}


int main(int argv, char** argc) {
    char* source = "--TCATAC-TCATGAACT";
    char* target = "GGTAATCCCTC---AA--";
    int score = similarity_score(source, target, 1, -1, -1, -1);
    printf("%d\n", score);
    return 0;
}
