/*
A little matrix operation library.
*/

#include <stdlib.h>
#include <stdio.h>


void print_matrix(float** mat, int dimx, int dimy)
/*
    Heleper function for log matrix, for debug.
*/
{
    for (int i = 0; i < dimx; i++) {
        for (int j = 0; j < dimy; j++) {
            float value = mat[i][j];
            printf("%5.2f", value);
            if (j != dimy - 1) {
                printf("\t");
            }
        }
        printf("\n\n");
    }
}


float** create_matrix(int dimx, int dimy, float init_value)
/*
    Create a float matrix with init value filled.
*/
{
    float** mat = (float **)malloc(dimx * sizeof(float*));
    for(int i = 0; i < dimx; i++){
        mat[i] = (float *)malloc(dimy * sizeof(float));
    }

    for (int i = 0; i < dimx; i++) {
        for (int j = 0; j < dimy; j++) {
            mat[i][j] = init_value;
        }
    }
    return mat;
}


float find_matrix_max(float** mat, int dimx, int dimy)
/*
    Find the max value in the matrix.
*/
{
    float max = mat[0][0];
    float value;

    for (int i = 0; i < dimx; i++) {
        for (int j = 0; j < dimy; j++) {
            value = mat[i][j]; 
            if (value > max) {
                max = value;
            }
        }
    }

    return max;
}
