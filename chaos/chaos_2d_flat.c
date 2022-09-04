#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void main(){

    printf("\nstart\n\n");

    //a_rule init
    int base = 2;
    int view = 5;
    int a_rule[2][2][2][2][2];
    for (int a=0; a<base; a++){
        for (int b=0; b<base; b++){
            for (int c=0; c<base; c++){
                for (int d=0; d<base; d++){
                    for (int e=0; e<base; e++){
                        a_rule[a][b][c][d][e] = 0;
                        }}}}}
    a_rule[0][0][0][0][1] = 1;
    a_rule[0][0][0][1][0] = 1;
    a_rule[0][0][1][0][0] = 1;
    a_rule[0][1][0][0][0] = 1;
    a_rule[0][1][1][1][1] = 1;


    printf("\n");

    int rule_1d[32];

    for (int i=0; i<32; i++){
        *(rule_1d + i) = 0;
    }

    *(rule_1d + 1) = 1;
    *(rule_1d + 2) = 1;
    *(rule_1d + 4) = 1;
    *(rule_1d + 8) = 1;
    *(rule_1d + 15) = 1;

    printf("\n");
    for (int i=0; i<32; i++){
    printf("%i ", *(rule_1d + i));
    }


    printf("\n");

    //board init
    int length = 5;
    int width = 5;
    int lw = length * width;
    int board_0[length][width];
    int board_1[lw];
    int board_2[lw];
    for (int i=0; i<length; i++) {
        for (int o=0; o<width; o++) {
            board_0[i][o] = i*(width) + o + 1;
        }}
    for (int i=0; i<lw; i++) {
        board_1[i] = i + 1;
        board_2[i] = 0;
    }
    board_2[lw/2] = 1;

    //memory init
    int memory_0[2][width];
    int memory_1[2][width];
    int memory_2[2][width];
    for (int i=0; i<2; i++){
        for (int o=0; o<width; o++){
        memory_0[i][o] = 0;
        memory_1[i][o] = 0;
        memory_2[i][o] = 0;
        }}


    void print_rule (int a_rule[base][base][base][base][base], int base) {
        printf("\nprint a_rule\n");
        printf("base = %i\n", base);
        for (int a=0; a<base; a++){
            for (int b=0; b<base; b++){
                for (int c=0; c<base; c++){
                    for (int d=0; d<base; d++){
                        for (int e=0; e<base; e++){
                            printf("%i ", a_rule[a][b][c][d][e]);
                        }}}}}
        printf("\n");
    }



    void print_board_f (int array[lw], int lw) {
        /*
        printf("\nprint array\n");
        printf("lw = %i\n", lw);
        */
        for (int i=0; i<lw; i++) {
            printf("%i ", array[i]);
            }
        printf("\n");
        }



    void print_mem (int memory[2][width], int width) {
        printf("\nprint mem\n");
        for (int i=0; i<2; i++) {
            for (int o=0; o<width; o++) {
                printf("%i\t", memory[i][o]);
            }
        printf(" \n");
        }}

    
    
    void step_pointer(int *board, int *a_rule, int *base, int *lw, int *width) {
        
        int memory_0[2][*width];
        int *memory = memory_0;
        int start[*width];
        int base_scale[5];

        for (int i=0; i<5; i++) {
            double a = pow(*base, i);
            int b;
            b=a;
            *(base_scale + i) = b;
            }

        for (int i=0; i<*width; i++) {
            *(memory + i) = *(board + i);
            *(memory + *width + i) = *(board + *lw - *width + i);
            *(start + i) = *(memory + i);
            }

        for (int i=0; i<*lw-*width; i++) {
            int o = i%*width;
            *(board + i) = *(a_rule + 
                            (*(memory + o) * *(base_scale + 4)) + 
                            (*(memory + *width + o) * *(base_scale + 3)) + 
                            (*(memory + (((i + 1)/ *width - i/ *width) * (*width)) + ((o+1) % *width)) * *(base_scale + 2)) +
                            (*(board + *width + i) * *(base_scale + 1)) +
                            (*(memory + ((o/(abs(o-1)+1) * (*width))) + (o+*width-1)%*width) * *(base_scale + 0)));
            *(memory + *width + o) = *(memory + o);
            *(memory + o) = *(board + *width + i);
            }

        for (int i=0; i<*width; i++) {
            *(board + i + *lw - *width) = *(a_rule +
                                           (*(memory + i) * *(base_scale + 4)) + 
                                           (*(memory + *width + i) * *(base_scale + 3)) + 
                                           (*(memory + (i + 1)%*width) * *(base_scale + 2)) + 
                                           (*(start + i) * *(base_scale + 1)) + 
                                           (*(memory + (i+*width-1)%*width) * *(base_scale + 0)));
            }
            print_board_f(board, *lw);
        }

    printf("\n");
    print_board_f(board_2, lw);
    step_pointer(board_2, rule_1d, &base, &lw, &width);
    step_pointer(board_2, rule_1d, &base, &lw, &width);
}
