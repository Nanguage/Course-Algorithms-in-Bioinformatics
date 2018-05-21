/*
Implementation of the Smith-Waterman algorithm.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utilities.h"
#include "matrix.h"

#define DEBUG 1


void fill_score_matrix(float** mat, char* source, char* target,
                       float match_score, float penalty_mismatch,
                       float penalty_insert, float penalty_delete)
/*
    Fill the score matrix.

    Dynamic Programing process:

        V(i, j) = max(
            0, # Align empty string
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

            float arr[4] = {0, score_match, score_insert, socre_delete};

            mat[i][j] = arr[maximum_idx(arr, 4)];
        }
    }
}


void move(char dire, int match,
          Node** current_node, char* track_res_ptr,
          int* x, int* y)
{
    char symbol;
    if (dire == 'l') {
        // move left
        symbol = DELETE_SYMBOL; 
        (*y)--;
    } else if (dire == 'u') {
        // move up
        symbol = INSERT_SYMBOL;
        (*x)--;
    } else {
        // move left up
        (*x)--; (*y)--; 
        if (match) {
            symbol = MATCH_SYMBOL;
        } else {
            symbol = MISMATCH_SYMBOL;
        }
    }
    *track_res_ptr = symbol;
    Node* next_node = malloc(sizeof(Node));
    next_node->pos.x = *x;
    next_node->pos.y = *y;
    (*current_node)->next = next_node;
    (*current_node) = next_node;
}


void move_left(Node** current_node, char* track_res_ptr, int* x, int* y)
{
    move('l', 1, current_node, track_res_ptr, x, y);
}

void move_up(Node** current_node, char* track_res_ptr, int* x, int* y)
{
    move('u', 1, current_node, track_res_ptr, x, y);
}

void move_left_up(int match, Node** current_node, char* track_res_ptr, int* x, int* y)
{
    move('-', match, current_node, track_res_ptr, x, y);
}


Route* backtrack(float** mat, char* source, char* target)
/*
    Backtrack matrix, find one optimal route.
*/
{
    int dimx = strlen(source) + 1;
    int dimy = strlen(target) + 1;

    char* track_res = malloc((dimx+dimy)*sizeof(char));
    char* track_res_ptr = track_res;
    Pos start = find_matrix_max_pos(mat, dimx, dimy);

    int x = start.x;
    int y = start.y;
    float value_l, value_u, value_lu;
    int match;

    Node* head_node;
    Node* current_node;
    head_node = malloc(sizeof(Node));
    head_node->pos.x = x;
    head_node->pos.y = y;
    current_node = head_node;

    while (mat[x][y] != 0) {
        if (x == 0) {
            move_left(&current_node, track_res_ptr, &x, &y);
        } else if (y == 0) {
            move_up(&current_node, track_res_ptr, &x, &y);
        } else {
            value_lu = mat[x-1][y-1];
            value_l  = mat[x][y-1];
            value_u  = mat[x-1][y];
            float arr[3] = {value_lu, value_l, value_u};
            switch(maximum_idx(arr, 3)) {
                case 0 :
                    if (source[x] == target[y]) {
                        match = 1;
                    } else {
                        match = 0;
                    }
                    move_left_up(match, &current_node, track_res_ptr, &x, &y);
                    break;
                case 1 :
                    move_left(&current_node, track_res_ptr, &x, &y);
                    break;
                case 2 :                
                    move_up(&current_node, track_res_ptr, &x, &y);
                    break;
            }
        }
        track_res_ptr++;
    }

    current_node->next = NULL;
    *track_res_ptr = '\0';

    Route* route = malloc(sizeof(Route));
    route->track_result = track_res;
    route->head = head_node;
    return route;
}


int main(int argv, char** argc)
{
    char* source = "AATTAAAAAAG";
    char* target = "AATTAAAACGC";

    int dimx = strlen(source) + 1;
    int dimy = strlen(target) + 1;
    float** mat = create_matrix(dimx, dimy, 0);

    fill_score_matrix(mat, source, target, 1, -3, -2, -2);
    printf("filled matrix:\n");
    print_matrix(mat, dimx, dimy);

    printf("backtrack result:\n");
    Route* route = backtrack(mat, source, target);
    printf("%s\n", route->track_result);
    print_route(route);
}
