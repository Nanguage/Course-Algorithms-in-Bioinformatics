CC=gcc

global_align: global_alignment.c matrix.c utilities.c
	$(CC) -Wall matrix.c utilities.c global_alignment.c; ./a.out ;rm ./a.out

local_align: local_alignment.c matrix.c utilities.c
	$(CC) -Wall matrix.c utilities.c local_alignment.c; ./a.out; rm ./a.out