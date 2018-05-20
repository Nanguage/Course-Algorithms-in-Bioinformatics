#define EMPTY_SYMBOL '-'
#define INSERT_SYMBOL '+'
#define DELETE_SYMBOL '-'
#define MATCH_SYMBOL '|'
#define MISMATCH_SYMBOL 'x'

int maximum_idx(float* arr, int size);

void print_alignment(char* source, char* target, char* track_res);

float base_similar_score(char s, char t,
                         float match_score, float penalty_mismatch,
                         float penalty_insert, float penalty_delete);


typedef struct Pos {
    int x;
    int y;
} Pos;


typedef struct Node {
    Pos pos;
    struct Node * next;
} Node;


/*
Denote one route in the backtrack.

  Head                                                  Tail
    \                                                    \
    Node1   ->   Node2   ->  Node3  -> ... ->  NodeN  ->  NULL
    (x1, y1)     ...                           (xN, yN)

*/
typedef struct Route {
    Node* head;
    char* track_result;
    float score;
} Route;


Route* track_result_to_route(char* track_result, Pos start_pos);
void destruct_route(Route* route);
void print_route(Route* route);
