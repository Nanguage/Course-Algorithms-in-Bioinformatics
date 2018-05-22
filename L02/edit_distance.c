#include <stdio.h>

#define EMPTY_SYMBOL '-'


int edit_distance(char* source, char* target)
{
    /*
        Calculate the edit distance of an alignment result between two sequences.
    */
    int distance = 0;
    char* s_pt = source;
    char* t_pt = target;

    while (*s_pt != '\0') {
        char s = *s_pt;
        char t = *t_pt;

        if (s != t) {
            distance += 1;
        }

        ++s_pt;
        ++t_pt;
    }

    return distance;
}


int main(int argv, char** argc) {
    char* source = "--TCATAC-TCATGAACT";
    char* target = "GGTAATCCCTC---AA--";
    int distance = edit_distance(source, target);
    printf("%d\n", distance);
    return 0;
}