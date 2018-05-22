/*
Implementation of the Needleman-Wunsch algorithm.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utilities.h"
#include "matrix.h"

#define DEBUG 1


void init_score_matrix(float** mat, int dimx, int dimy,
                       float penalty_insert, float penalty_delete)
/*
    Initialize the score matrix for perform the N-W algorithm

        V(0, 0) = 0
        V(0, j) = V(0, j-1) + delta(_, T[j])
        V(i, 0) = V(i-1, 0) + delta(S[i], _)

*/
{
    mat[0][0] = 0;

    for (int j = 1; j < dimy; j++) {
        // Insertion at the begining position
        mat[0][j] = mat[0][j-1] + penalty_insert;
    }

    for (int i = 1; i < dimx; i++) {
        // Deletion at the begining position
        mat[i][0] = mat[i-1][0] + penalty_delete;
    }
}


void fill_score_matrix(float** mat, char* source, char* target,
                       float match_score, float penalty_mismatch,
                       float penalty_insert, float penalty_delete)
/*
    Fill the score matrix.

    Dynamic Programing process:

        V(i, j) = max(
            V(i-1, j-1) + delta(S[i], T[j]), # Match/Mismatch
            V(i-1, j) + delta(S[i], _), # Delete
            V(i, j-1) + delta(_, T[j])  # Insert
        )
*/
{
    int dimx = strlen(source) + 1;
    int dimy = strlen(target) + 1;

    float score_match, score_insert, socre_delete;
    float simi_score_m, simi_score_i, simi_score_d;

    for (int i = 1; i < dimx; i++) {
        for (int j = 1; j < dimy; j++) {

            char s = source[i-1];
            char t = target[j-1];

            simi_score_m = base_similar_score(s, t, match_score, penalty_mismatch,
                                                    penalty_insert, penalty_delete);
            score_match = mat[i-1][j-1] + simi_score_m;


            simi_score_i = base_similar_score(s, EMPTY_SYMBOL, match_score, penalty_mismatch,
                                                               penalty_insert, penalty_delete);
            score_insert = mat[i][j-1] + simi_score_i;


            simi_score_d = base_similar_score(EMPTY_SYMBOL, t, match_score, penalty_mismatch,
                                                               penalty_insert, penalty_delete);
            socre_delete = mat[i-1][j] + simi_score_d;

            float arr[3] = {score_match, score_insert, socre_delete};

            mat[i][j] = arr[maximum_idx(arr, 3)];
        }
    }
}


char* backtrack(float** mat, char* source, char* target)
/*
    Do backtrack, find one optimal path from the matrix.
*/
{
    int dimx = strlen(source) + 1;
    int dimy = strlen(target) + 1;

    char* track_res = malloc((dimx + dimy + 1)*sizeof(char));
    char* res_ptr = track_res;

    int x = dimx - 1;
    int y = dimy - 1;
    float s_left, s_up, s_lu;

    while (x != 0 || y != 0) {

        if (x == 0) {
            // arrive at the top border
            *res_ptr = DELETE_SYMBOL;
            y--;
        } else if (y == 0) {
            // arrive at the left border
            *res_ptr = INSERT_SYMBOL;
            x--;
        } else {
            s_left = mat[x][y-1];
            s_up = mat[x-1][y];
            s_lu = mat[x-1][y-1];

            float arr[4] = {s_lu, s_left, s_up};
            //if (DEBUG) { printf("%d, %d\n", x, y); printf("%f, %f, %f\n", s_lu, s_left, s_up); }
            switch (maximum_idx(arr, 3)) {
                case 0 :
                    // go left up
                    if (source[x-1] == target[y-1]) {
                        *res_ptr = MATCH_SYMBOL; 
                    } else {
                        *res_ptr = MISMATCH_SYMBOL;
                    }
                    x--; y--;
                    break;
                case 1 :
                    // go left
                    *res_ptr = DELETE_SYMBOL;
                    y--;
                    break;
                case 2 :
                    // go up
                    *res_ptr = INSERT_SYMBOL;
                    x--;
                    break; 
            }
        }
        res_ptr++;
    }

    *res_ptr = '\0';

    return track_res;

}


float alignment_score(char* track_res,
                      float match_score, float penalty_mismatch,
                      float penalty_insert, float penalty_delete)
/*
    Calculate the alignment score from the backtrack result string.
*/
{
    float score = 0;
    int size = strlen(track_res);
    char c;
    for (int i = 0; i < size; i++) {
        c = track_res[i];
        switch (c) {
            case MATCH_SYMBOL :
                score += match_score;
                break;
            case MISMATCH_SYMBOL :
                score += penalty_mismatch;
                break;
            case INSERT_SYMBOL :
                score += penalty_insert;
                break;
            case DELETE_SYMBOL :
                score += penalty_delete;
                break;
        }
    }

    return score;
}


char* align_NW(char* source, char* target,
              float match_score, float penalty_mismatch,
              float penalty_insert, float penalty_delete)
/*
    Perform the NW algorirhm.
*/
{
    int dimx = strlen(source) + 1;
    int dimy = strlen(target) + 1;

    float** mat = create_matrix(dimx, dimy, 0);

    if (DEBUG) {
        printf("matrix size: %d, %d\n\n", dimx, dimy);
        printf("empty matrix:\n");
        print_matrix(mat, dimx, dimy);
    }

    init_score_matrix(mat, dimx, dimy, penalty_insert, penalty_delete);

    if (DEBUG) {
        printf("initialized matrix:\n");
        print_matrix(mat, dimx, dimy);
    }

    fill_score_matrix(mat, source, target, match_score, penalty_mismatch, penalty_insert, penalty_delete);

    if (DEBUG) {
        printf("filled matrix:\n");
        print_matrix(mat, dimx, dimy);
    }

    char* track_res = backtrack(mat, source, target);

    free(mat);

    return track_res;
}


int main(int argv, char** argc)
{
    char* source = "AATTAAAAAAG";
    char* target = "AAATTTAAGGGGC";

    char* track_res = align_NW(source, target, 1, -1, -2, -2);
    printf("backtrack result: ");
    printf("%s\n", track_res);

    int dimx = strlen(source) + 1;
    int dimy = strlen(target) + 1;
    Pos start_pos = {dimx, dimy};
    Route* route = track_result_to_route(track_res, start_pos);
    print_route(route);

    print_alignment(source, target, track_res);
    float score = alignment_score(track_res, 1, -1, -2, -2);
    printf("score: %.2f\n", score);

    free(track_res);

}