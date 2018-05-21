#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utilities.h"


int max_align_len(char* track_res, int max_seq_len)
{
    int len_i = 0;
    int len_d = 0;
    int len = max_seq_len;

    for (char* ptr = track_res; *ptr != '\0'; ptr++) {
        switch (*ptr) {
            case INSERT_SYMBOL :
                len_i++;
                break;
            case DELETE_SYMBOL :
                len_d++;
                break;
        }
    }

    if (len_i > len_d) {
        len += len_i;
    } else {
        len += len_d;
    }

    return len;
}


void print_alignment_side(char* source, char* target, char* track_res, char choice)
{
    int seq_len;
    char* seq;
    char flag;

    int r_len = strlen(track_res);

    int max_seq_len;
    int len_sou = strlen(source);
    int len_tar = strlen(target);
    if (len_tar > len_sou) {
        max_seq_len = len_tar;
    } else {
        max_seq_len = len_sou;
    }

    int max_len = max_align_len(track_res, max_seq_len);

    if (choice == 'u' || choice == 't') {
        seq_len = len_tar;
        seq = target;
        flag = DELETE_SYMBOL;
    } else {
        seq_len = len_sou;
        seq = source;
        flag = INSERT_SYMBOL;
    }

    char* r = track_res + r_len -1;
    int i = 0;
    int idx = 0;

     // print sequence
     while (r >= track_res) {
         if (*r == flag) {
             putchar(EMPTY_SYMBOL);
         } else {
             if (idx >= seq_len) {
                 break;
             }
             putchar(seq[idx]);
             idx++;
         }
         r--;
         i++;
     }

    while (idx < seq_len) {
        putchar(seq[idx]);
        idx++;
        i++;
    }

    while (i < max_len) {
        putchar(EMPTY_SYMBOL);
        i++;
    }
}


void print_alignment_middle(char* track_res)
{
    int r_len = strlen(track_res);
    char* r = track_res + r_len -1;

    while (r != track_res) {
        if (*r == MATCH_SYMBOL) {
            putchar(MATCH_SYMBOL);
        } else {
            putchar(' ');
        }
        r--;
    }
}


void print_alignment(char* source, char* target, char* track_res)
/*
    Print the alignment result to a easy to read format.
*/
{
    print_alignment_side(source, target, track_res, 't');
    printf("\n");
    print_alignment_middle(track_res);
    printf("\n");
    print_alignment_side(source, target, track_res, 's');
    printf("\n");
}


float base_similar_score(char s, char t,
                         float match_score, float penalty_mismatch,
                         float penalty_insert, float penalty_delete)
/*
    Get the similarity score between two base.
*/
{
    float score;

    if (s != EMPTY_SYMBOL && t != EMPTY_SYMBOL) {
        if (s == t) {
            score = match_score;
        } else {
            score = penalty_mismatch;
        }
    } else if (s == EMPTY_SYMBOL && t != EMPTY_SYMBOL) {
        // Deletion
        score = penalty_delete;
    } else if (s != EMPTY_SYMBOL && t == EMPTY_SYMBOL) {
        // Insertion
        score = penalty_insert;
    } else {
        score = 0;
    }

    return score;
}


int maximum_idx(float* arr, int size)
/*
    Find the maximum number in an array. return the index.
*/
{
    float max = arr[0];
    int max_idx = 0;

    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
            max_idx = i;
        }
    }

    return max_idx;
}


Route* track_result_to_route(char* track_res, Pos start_pos)
/*
    Construct the Route from track object.
*/
{
    Route* route = malloc(sizeof(Route));
    Node* curr_node = malloc(sizeof(Node));
    Node* next_node;

    int x = start_pos.x;
    int y = start_pos.y;

    curr_node->pos.x = x;
    curr_node->pos.y = y;

    route -> head = curr_node;

    for (char* ptr = track_res; *ptr != '\0'; ptr++) {
        switch (*ptr) {
            case INSERT_SYMBOL :
                x--;
                break;
            case DELETE_SYMBOL :
                y--;
                break;
            default :
                x--; y--;
        }

        next_node = malloc(sizeof(Node));
        next_node->pos.x = x;
        next_node->pos.y = y;
        curr_node->next = next_node;
        curr_node = next_node;
    }

    curr_node->next = NULL;

    route->track_result = track_res;
    route->score = 0;

    return route;
}


void destruct_route(Route* route)
/*
    Destruct the Route.
*/
{
    Node* curr_node = route->head;
    Node* previous_node;
    while (curr_node->next != NULL) {
        previous_node = curr_node;
        curr_node = curr_node->next;
        free(previous_node);
    }
    free(curr_node);
    free(route->track_result);
    free(route);
}


void print_route(Route* route)
/*
    Print the route in a readable format.
*/
{
    int x, y;
    Node* curr_node = route->head;

    while (curr_node->next != NULL) {
        x = curr_node->pos.x;
        y = curr_node->pos.y;
        printf("(%d, %d) -> ", x, y);
        curr_node = curr_node->next;
    }

    printf("|Tail|\n");
}
