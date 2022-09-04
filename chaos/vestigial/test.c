#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void main(){

    printf("\nstart\n\n");

    //a_rule init
    int base = 2;
    int view = 5;
    int a_rule[2][2][2][2][2];
    int a_rule_0[2][2][2][2][2];
    for (int a=0; a<base; a++){
        for (int b=0; b<base; b++){
            for (int c=0; c<base; c++){
                for (int d=0; d<base; d++){
                    for (int e=0; e<base; e++){
                        a_rule[a][b][c][d][e] = 0;
                        a_rule_0[a][b][c][d][e] = a*pow(2, 0) + b*pow(2, 1) + c*pow(2, 2) + d*pow(2, 3) + e*pow(2, 4);
                        }}}}}
    a_rule[0][0][0][0][1] = 1;
    a_rule[0][0][0][1][0] = 1;
    a_rule[0][0][1][0][0] = 1;
    a_rule[0][1][0][0][0] = 1;
    a_rule[0][1][1][1][1] = 1;

    for (int i=0; i<32; i++) {

        printf("%i ", *(a_rule_0 + i));

    }

    printf("\n");

    int rule_1d[32];

    for (int i=0; i<32; i++){
        *(rule_1d + i) = 0;

        printf("%i ", *(rule_1d + i));
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
    int length = 3;
    int width = 3;
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

    /*
    void print_board (int array[length][width], int length, int width) {
        printf("\nprint array\n");
        printf("length = %i\n", length);
        printf("width = %i\n", width);
        for (int i=0; i<length; i++) {
            for (int o=0; o<width; o++) {
                printf("%i\t", array[i][o]);
            }
        printf(" \n");
        }}
    */


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

    /*
    print_rule(a_rule, base);
    printf("\n0 instance");
    print_board(board_0, length, width);
    print_mem(memory_0, width);
    printf("\n1 instance");
    print_board_f(board_1, lw);
    print_mem(memory_1, width);
    printf("\n2 instance");
    print_board_f(board_2, lw);
    print_mem(memory_2, width);
    */


    /*mem transfers 2d
    printf("\nmem transfer");
    for (int i=0; i<length; i++) {
        printf("\ni=%i", i);
        for (int o=0; o<width; o++) {
            memory_0[1][o] = board_0[i%length][o];
            memory_0[0][o] = board_0[(i+1)%length][o];
        }
        print_mem(memory_0, width);
        for (int o=0; o<width; o++) {
            printf("o=%i: ", o);

            int c_0 = memory_0[0][o];
            int u_0 = memory_0[1][o];
            int r_0 = memory_0[(o-(o/width))/width][(o+1)%width];
            int d_0 = board_0[(i+2)%length][o];
            int l_0 = memory_0[o/(abs(o-1)+1)][(o+width-1)%width];

            memory_0[1][o] = memory_0[0][o];
            
            printf("%i %i %i %i %i\t", c_0, u_0, r_0, d_0, l_0);
        }
    }
    */

    /*mem transfer 1d
    int start_1[width];
    int start_2[width];
    
    printf("\n\nmem transfer 1d");
    for (int i=0; i<width; i++) {
        memory_1[0][i] = board_1[i];
        memory_1[1][i] = board_1[lw-width + i];
        start_1[i] = board_1[i];

        memory_2[0][i] = board_2[i];
        memory_2[1][i] = board_2[lw-width + i];
        start_2[i] = board_2[i];
    }

    print_mem(memory_1, width);
    for (int i=0; i<lw-width; i++) {
        int o = i%width;

        int c_1 = memory_1[0][o];
        int u_1 = memory_1[1][o];
        //thank you black snake
        int r_1 = memory_1[(i+1)/width - i/width][(o+1)%width];
        int d_1 = board_1[i+width];
        int l_1 = memory_1[o/(abs(o-1)+1)][(o+width-1)%width];

        int c_2 = memory_2[0][o];
        int u_2 = memory_2[1][o];
        //thank you black snake
        int r_2 = memory_2[(i+1)/width - i/width][(o+1)%width];
        int d_2 = board_2[i+width];
        int l_2 = memory_2[o/(abs(o-1)+1)][(o+width-1)%width];

        memory_1[1][o] = memory_1[0][o];
        memory_1[0][o] = d_1;

        memory_2[1][o] = memory_2[0][o];
        memory_2[0][o] = d_2;

        printf("%i %i %i %i %i\t", c_1, u_1, r_1, d_1, l_1);
        printf("%i %i %i %i %i\t", c_2, u_2, r_2, d_2, l_2);
        printf("%i\n", a_rule[c_2][u_2][r_2][d_2][l_2]);

        board_2[i] = a_rule[c_2][u_2][r_2][d_2][l_2];
    }
    for (int i=0; i<width; i++) {
        int c_1 = memory_1[0][i];
        int u_1 = memory_1[1][i];
        int r_1 = memory_1[0][(i+1)%width];
        int d_1 = start_1[i];
        int l_1 = memory_1[0][(i+width-1)%width];

        int c_2 = memory_2[0][i];
        int u_2 = memory_2[1][i];
        int r_2 = memory_2[0][(i+1)%width];
        int d_2 = start_2[i];
        int l_2 = memory_2[0][(i+width-1)%width];

        printf("%i %i %i %i %i\t", c_1, u_1, r_1, d_1, l_1);
        printf("%i %i %i %i %i\t", c_2, u_2, r_2, d_2, l_2);
        printf("%i\n", a_rule[c_2][u_2][r_2][d_2][l_2]);

        board_2[i + lw - width] = a_rule[c_2][u_2][r_2][d_2][l_2];
    }

    print_board_f(board_2, lw);
    */

    /*
    int step(int board[lw], int memory[2][width], int lw, int width) {

        int start[width];


        printf("\nmem transfer 1d\n");


        for (int i=0; i<width; i++) {
            memory[0][i] = board[i];
            memory[1][i] = board[lw-width + i];
            start[i] = board[i];
        }


        print_mem(memory, width);
        printf("\n");


        for (int i=0; i<lw-width; i++) {

            int o = i%width;

            int c = memory[0][o];
            int u = memory[1][o];
            //thank you black snake
            int r = memory[(i+1)/width - i/width][(o+1)%width];
            int d = board[i+width];
            int l = memory[o/(abs(o-1)+1)][(o+width-1)%width];

            memory[1][o] = memory[0][o];
            memory[0][o] = d;


            printf("%i %i %i %i %i\t", c, u, r, d, l);
            printf("%i\n", a_rule[c][u][r][d][l]);


            board[i] = a_rule[c][u][r][d][l];
        }
        for (int i=0; i<width; i++) {
            int c = memory[0][i];
            int u = memory[1][i];
            int r = memory[0][(i+1)%width];
            int d = start[i];
            int l = memory[0][(i+width-1)%width];


            printf("%i %i %i %i %i\t", c, u, r, d, l);
            printf("%i\n", a_rule[c][u][r][d][l]);


            board[i + lw - width] = a_rule[c][u][r][d][l];
        }

            print_board_f(board, lw);

    }

    print_board_f(board_2, lw);
    step(board_2, memory_2, lw, width);
    step(board_2, memory_2, lw, width);

    */
    
    void step_pointer(int *board, int *memory, int *lw, int *width) {

        /*
        printf("\n");

        printf("%d\n", board);
        printf("%d\n", *board);

        printf("%d\n", memory);
        printf("%d\n", *memory);

        printf("%d\n", lw);
        printf("%d\n", *lw);

        printf("%d\n", width);
        printf("%d\n", *width);
        */

        int start[*width];

        /*
        printf("\nmem transfer 1d\n");]
        */
        
        for (int i=0; i<*width; i++) {
            *(memory + i) = *(board + i);
            *(memory + *width + i) = *(board + *lw - *width + i);
            *(start + i) = *(memory + i);
        }


        for (int i=0; i<*lw-*width; i++) {
            int o = i%*width;
            
            /*
            int c = *(memory + o);
            int u = *(memory + *width + o);
            //thank you black snake
            int r = *(memory + (((i + 1)/ *width - i/ *width) * (*width)) + ((o+1) % *width));
            int d = *(board + *width + i);
            int l = *(memory + ((o/(abs(o-1)+1) * (*width))) + (o+*width-1)%*width);

            printf("%i %i %i %i %i\t",  *(memory + o), 
                                        *(memory + *width + o), 
                                        *(memory + (((i + 1)/ *width - i/ *width) * (*width)) + ((o+1) % *width)), 
                                        *(board + *width + i), 
                                        *(memory + ((o/(abs(o-1)+1) * (*width))) + (o+*width-1)%*width));
            printf("%i %i %i %i %i\t", c, u, r, d, l);

            
            printf("%i\n", a_rule[c][u][r][d][l]);
            */
            

            *(board + i)= a_rule[*(memory + o)]
                                [*(memory + *width + o)]
                                [*(memory + (((i + 1)/ *width - i/ *width) * (*width)) + ((o+1) % *width))]
                                [*(board + *width + i)]
                                [*(memory + ((o/(abs(o-1)+1) * (*width))) + (o+*width-1)%*width)];

            
            *(memory + *width + o) = *(memory + o);
            *(memory + o) = *(board + *width + i);
            
        }

        
        for (int i=0; i<*width; i++) {
            
            /*
            int c = *(memory + i);
            int u = *(memory + *width + i);
            int r = *(memory + (i + 1)%*width);
            int d = *(start + i);
            int l = *(memory + (i+*width-1)%*width);

            
            printf("%i %i %i %i %i\t", c, u, r, d, l);
            printf("%i\n", a_rule[c][u][r][d][l]);
            */
            
            *(board + i + *lw - *width) = a_rule[*(memory + i)]
                                                [*(memory + *width + i)]
                                                [*(memory + (i + 1)%*width)]
                                                [*(start + i)]
                                                [*(memory + (i+*width-1)%*width)];

        }

            //printf("\n");
            print_board_f(board, *lw);

    }

    printf("\n");
    step_pointer(board_2, memory_2, &lw, &width);
    step_pointer(board_2, memory_2, &lw, &width);
}