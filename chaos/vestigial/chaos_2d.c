#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <Python.h>


void step(int *board, int *a_rule, int *base, int *lw, int *width) {

    int memory[2][width];
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
    return NULL;
    }

