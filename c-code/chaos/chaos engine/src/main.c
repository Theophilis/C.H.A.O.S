//standard
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
//sdl
#define SDL_MAIN_HANDLED
#include <SDL2/SDL.h>
//server
#include <WinSock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif

#pragma comment(lib, "Ws2_32.lib")

#define BUFFLEN 64
#define PORT 21621
#define ADDRESS "127.0.0.1" //local host

static bool should_quit = false;

void chaomize(int *chaos_board, int *a_rule, int lw, int ww, int b_width, int base) {

    int *b_memory = malloc((ww * sizeof(int)));
    int *row_0 = malloc((b_width * sizeof(int)));
    int *base_scale = malloc((5 * sizeof(int)));

    // //memory init
    // for (int i=0; i<ww; i++){
    // b_memory[i] = 0;
    // }

    // //row_0
    // for (int i=0; i<b_width; i++){
    //     row_0[i] = 0;
    // }
    
    //base scale
    for (int i=0; i<5; i++) {
    double a = pow(base, i);
    int b;
    b=a;
    // printf("%i ", b);
    *(base_scale + i) = b;
    }


    // printf("\nboard\n");
    // for (int i=0; i<lw; i++){
    //     printf("%i ", *(chaos_board + i));
    // } printf("\n");


    for (int i=0; i<b_width; i++) {
        *(b_memory + i) = *(chaos_board + i);
        *(b_memory + b_width + i) = *(chaos_board + lw - b_width + i);
        *(row_0 + i) = *(b_memory + i);
        }

    for (int i=0; i<lw-b_width; i++) {
        int o = i%b_width;
        //Center, Up, Right, Down, Left: neighbors
        *(chaos_board + i) = *(a_rule + 
                        (*(b_memory + o) * *(base_scale + 4)) + 
                        (*(b_memory + b_width + o) * *(base_scale + 3)) + 
                        (*(b_memory + (((i + 1)/ b_width - i/ b_width) * (b_width)) + ((o+1) % b_width)) * *(base_scale + 2)) +
                        (*(chaos_board + b_width + i) * *(base_scale + 1)) +
                        (*(b_memory + ((o/(abs(o-1)+1) * (b_width))) + (o+b_width-1)%b_width) * *(base_scale + 0)));
        *(b_memory + b_width + o) = *(b_memory + o);
        *(b_memory + o) = *(chaos_board + b_width + i);
        }

    for (int i=0; i<b_width; i++) {
        *(chaos_board + i + lw - b_width) = *(a_rule +
                                        (*(b_memory + i) * *(base_scale + 4)) + 
                                        (*(b_memory + b_width + i) * *(base_scale + 3)) + 
                                        (*(b_memory + (i + 1)%b_width) * *(base_scale + 2)) + 
                                        (*(row_0 + i) * *(base_scale + 1)) + 
                                        (*(b_memory + (i+b_width-1)%b_width) * *(base_scale + 0)));
        }

    free(b_memory);
    free(row_0);
    free(base_scale);
}

void key_input (int *a_rule, int *key_counter, int val, int bv, int base) {
    
    // printf("\ninput val = %i\n", val);
    // printf("\n%i\n", *(key_counter + val));
    // printf("\n%i\n", *(a_rule + val));
    // printf("\n%i\n", (val + (27 * *(key_counter + val))) % bv);

    *(a_rule + (val + (27 * *(key_counter + val))) % bv) = (*(a_rule + (val + (27 * *(key_counter + val))) % bv) + 1) % base;
    *(key_counter + val) += 1;

    // printf("\nrule\n");
    for (int i=0; i<bv; i++){
        //printf("%i ", a_rule[i]);
    }
    //printf("\n");
}

void value_color(int *board,  int *colors, uint8_t *pixels, int lw, int color_step, int color_on){


    uint8_t rgb[3] = {0, 0, 0};
    int layer_size = 255;

    // for (int i=0; i<lw; i++) {
    //     *(board + i) = 1;
    // }

    // printf("\n");
    // for (int i=0; i<3; i++) {
    //     printf("%i ", *(rgb + i));
    // } printf("\n");

    

    for (int i=0; i<lw; i++) {

        // printf("\n\nnew board %i = %i\n", i, *(board + i));
        // printf("colors %i\n ", *(colors + i));
        //RGBA

        *(rgb) = 0;
        *(rgb + 1) = 0;
        *(rgb + 2) = 0;

        if (color_on > 0) {
            //red
            if (*(colors + i) < layer_size) {
                // printf("red\n");
                *(rgb) = *(colors + i);
            }
            //red green
            else if (*(colors + i) < layer_size * 2) {
                // printf("red green\n");
                *(rgb) = 255;
                *(rgb + 1) = (*(colors + i) - layer_size) % 255;
            }
            //green
            else if (*(colors + i) < layer_size * 3) {
                // printf("green\n");
                *(rgb) = 255 - (*(colors + i) - (layer_size * 2)) % 255;
                *(rgb + 1) = 255;
            }
            //green blue
            else if (*(colors + i) < layer_size * 4) {
                // printf("green blue\n");
                *(rgb + 1) = 255;
                *(rgb + 2) = (*(colors + i) - (layer_size * 3)) % 255;
            }
            //blue
            else if (*(colors + i) < layer_size * 5) {
                // printf("blue\n");
                *(rgb + 1) =  255 - (*(colors + i) - (layer_size * 4)) % 255;
                *(rgb + 2) = 255;
            }
            //blue red
            else if (*(colors + i) < layer_size * 6) {
                // printf("blue red\n");
                *(rgb + 2) = 255;
                *(rgb) = (*(colors + i) - (layer_size * 5)) % 255;
            }
            //white
            else if (*(colors + i) < layer_size * 7) {
                // printf("white\n");
                *(rgb) = 255;
                *(rgb + 2) = 255;
                *(rgb + 1) = (*(colors + i) - (layer_size * 2)) % 255;
            }
            //black
            else if (*(colors + i) < layer_size * 8) {
                // printf("black\n");
                *(rgb) = 255 - *(colors + i) - (layer_size * 7);
                *(rgb + 1) = 255 - *(colors + i) - (layer_size * 7);
                *(rgb + 2) = 255 - *(colors + i) - (layer_size * 7);
            }
            
            // for (int i=0; i<3; i++) {
            //     printf("%i ", *(rgb + i));
            // } 
            // printf("\ncolor_step %i\n", color_step);

        } else {
            *(rgb) = *(colors + i) % 255;
            *(rgb + 1) = *(colors + i) % 255;
            *(rgb + 2) = *(colors + i) % 255;

            color_step = 1;
        }

        // if (*(board + i) == 0){
        //     if (*(colors + i) > 0) {
        //     *(colors + i) -= color_step;
        //     }
        // }
        // else {
        //     *(colors + i) = *(colors + i) + 1;
        //     // printf("\ncolors %i\n", *(colors + i));
        //     *(colors + i) = *(colors + i) % (layer_size * 10);
        //     // printf("colors %i\n\n", *(colors + i));
        // }


        *(pixels + (i * 4)) = *(rgb + 2);
        *(pixels + (i * 4) + 1) = *(rgb + 1);
        *(pixels + (i * 4) + 2) = *(rgb);
        *(pixels + (i * 4) + 3) = 255;

        


    }
}

void value_color_s(int *board, uint8_t *pixels, int lw){   

    for (int i=0; i<lw; i++) {
        // printf("%i  ", *(board + i));
        //RGBA

        if (*(board + i) == 0) {
            // printf("zero\n");
            *(pixels + (i * 4)) = 0;
            *(pixels + (i * 4) + 1) = 0;
            *(pixels + (i * 4) + 2) = 0;
            *(pixels + (i * 4) + 3) = 0;
        }

        else if (*(board + i) == 2) {
            // printf("one\n");
            *(pixels + (i * 4)) = 255;
            *(pixels + (i * 4) + 1) = 0;
            *(pixels + (i * 4) + 2) = 255;
            *(pixels + (i * 4) + 3) = 255;
        }

        else if (*(board + i) == 3) {
            // printf("two\n");
            *(pixels + (i * 4)) = 255;
            *(pixels + (i * 4) + 1) = 255;
            *(pixels + (i * 4) + 2) = 0;
            *(pixels + (i * 4) + 3) = 255;
        }

        else if (*(board + i) == 4) {
            // printf("three\n");
            *(pixels + (i * 4)) = 0;
            *(pixels + (i * 4) + 1) = 255;
            *(pixels + (i * 4) + 2) = 255;
            *(pixels + (i * 4) + 3) = 255;
        }

        else if (*(board + i) == 1) {
            // printf("four\n");
            *(pixels + (i * 4)) = 128;
            *(pixels + (i * 4) + 1) = 128;
            *(pixels + (i * 4) + 2) = 128;
            *(pixels + (i * 4) + 3) = 255;
        }
        


    }
}


int main(int argc, char *argv[]) {
    
    puts("Hello there\n");
    puts("\tspread some chaos\n");

    //--------------------START--------------------//

        //standard
    printf("standard\n");
    int base = 2;
    int view = 5;

    int b_length = 1001;
    int b_width = 1001;
    int bb_length = b_length;
    int bb_width = b_length;
    int s_length = 512;
    int s_width = 256;
    int c_length = b_length;
    int c_width = b_length;

    int gv = 0;
    int glove = 3;
    int rule_value = 0;
    int character_size = 64;
    int color_on = 1;
    int brush_stroke = 9;
    int layer_size = 255;
    int bb_convert = 0;



        //calculated
    printf("calculated\n");
    float bv_0 = pow(base, view);
    int bv = bv_0;
    int lw_bb = bb_length * bb_width;
    int ww_bb = bb_width * 2;
    int lw = b_length * b_width;
    int ww = 2 * b_width;
    int pinpoint = (lw/2);
    int lw_s = s_length * s_width;

        //arrays
    printf("arrays\n");
    int *a_rule = malloc((bv * sizeof(int)));
    int *brush_board = malloc((lw * sizeof(int)));
    int *chaos_board = malloc((lw * sizeof(int)));
    int *chaos_colors = malloc((lw * sizeof(int)));
    int *side_board = malloc((s_length * s_width) * sizeof(int));
    int *key_counter = malloc((27 * sizeof(int)));
    int *glove_values = malloc(12 * sizeof(long));
    //x=0, y=1, z=2, pitch=3, yaw=4, roll=5, thumb=6, pointer=7, middle=8, ring=9, pinky=10, elbow=11

        //glove methods
    printf("glove methods\n");
    int thumb_trigger = 16;
    int index_trigger = 64;
    int middle_trigger = 64;
    int ring_trigger = 64;
    int pinky_trigger = 64;
    int last_value = 0;

            //colors
    printf("colors\n");
    float drain_level = 60;
    float c_max = drain_level * 5;
    float step_up = .05;
    float step_down = .03;
    int color_step = 1;
    int color_step_scale = 12;

    float window_scale = 5;
    float window_max = bv / window_scale;
    float window = 0;
    int place = 0;
    int skip_scale = 16;

    float c_ratio = 0;
    float c_total = 0;
    float c_0 = 0;
    float c_1 = 0;
    float c_2 = 0;
    float c_3 = 0;
    float c_4 = 0;

    int ci_0 = 0;
    int ci_1 = 0;
    int ci_2 = 0;
    int ci_3 = 0;
    int ci_4 = 0;
    

        //zero out
    for (int i=0; i<27; i++) {
        *(key_counter + i) = 0;
    }

    for (int i=0; i<bv; i++){
        *(a_rule + i) = 0;
    }

    *(a_rule + 1) = 1;
    *(a_rule + 2) = 1;
    *(a_rule + 4) = 1;
    *(a_rule + 8) = 1;
    *(a_rule + 15) = 1;
    
        //board init
    printf("board init\n");
    for (int i=0; i<lw; i++) {
        *(chaos_board + i) = 0;
        *(chaos_colors + i) = 0;
        *(brush_board + i) = 0;
    }
    *(chaos_board + pinpoint) = 1;
    *(brush_board + lw_bb/2) = 1;

        //side board init
    for (int i=0; i<(s_length * s_width)/2; i++) {
        *(side_board + i) = 0;
        *(side_board + i + (s_length * s_width)/2) = 0;

    }   

    for (int i=0; i<12; i++) {
        *(glove_values + i) = 0;
    }



    //--------------------END--------------------//
    
    //----------------sdl shit----------------//
    
    //init
    printf("sdl init\n");
    SDL_Init(SDL_INIT_VIDEO);
    //main
    SDL_Window *win;
    SDL_Renderer *rend;
    SDL_Texture *texture;
    //side
    SDL_Window *win_s;
    SDL_Renderer *rend_s;
    SDL_Texture *texture_s;

    //define
        //window_1
    win = SDL_CreateWindow("C.H.A.O.S.", 
                SDL_WINDOWPOS_CENTERED, 
                SDL_WINDOWPOS_CENTERED, 
                b_width, b_length, 
                SDL_WINDOW_SHOWN);

    rend = SDL_CreateRenderer(win, 
                            -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);

    texture = SDL_CreateTexture(rend, 
                    SDL_PIXELFORMAT_ARGB8888, 
                    SDL_TEXTUREACCESS_STREAMING, 
                    b_length, 
                    b_width);

    // SDL_ShowCursor(false);

        //window_2
    win_s = SDL_CreateWindow("C.H.A.O.S. side", 
                SDL_WINDOWPOS_CENTERED, 
                SDL_WINDOWPOS_CENTERED, 
                s_width, s_length, 
                SDL_WINDOW_SHOWN);

    rend_s = SDL_CreateRenderer(win_s, 
                            -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);

    texture_s = SDL_CreateTexture(rend_s, 
                    SDL_PIXELFORMAT_ARGB8888, 
                    SDL_TEXTUREACCESS_STREAMING, 
                    s_width, 
                    s_length);


    //pixels
    int pitch = lw * 4;
    uint8_t *pixels = malloc((pitch * sizeof(uint8_t)));

    int pitch_s = lw_s * 4;
    uint8_t *pixels_s = malloc((pitch * sizeof(uint8_t)));

        //main
    SDL_LockTexture(texture, NULL, (void **)&pixels, &pitch);
    value_color(chaos_board, chaos_colors, pixels, lw, color_step, 0);
    SDL_UnlockTexture(texture);

    SDL_RenderClear(rend);
    SDL_RenderCopy(rend, texture, NULL, NULL);
    SDL_RenderPresent(rend);

        //side

    int x_s = 0;
    int y_s = 0;
    for (int i=0; i<(bv); i++) {
        
        y_s = (i/4) * character_size * s_width;
        x_s = i%4 * character_size;

        // printf("%i %i\n", y_s, x_s);

        for (int o=0; o<character_size; o++) {
            *(side_board + ((x_s + o) + (y_s + (1 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (2 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (3 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (4 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (5 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (6 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (7 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (8 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (9 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (10 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (11 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (12 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (13 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (14 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (15 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (16 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (17 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (18 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (19 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (20 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (21 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (22 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (23 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (24 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (25 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (26 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (27 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (28 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (29 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (30 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (31 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (32 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (33 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (34 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (35 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (36 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (37 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (38 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (39 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (40 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (41 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (42 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (43 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (44 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (45 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (46 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (47 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (48 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (49 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (50 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (51 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (52 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (53 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (54 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (55 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (56 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (57 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (58 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (59 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (60 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (61 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (62 * s_width)))) = i%4 + 1;
            *(side_board + ((x_s + o) + (y_s + (63 * s_width)))) = i%4 + 1;

        }
    }
    SDL_LockTexture(texture_s, NULL, (void **)&pixels_s, &pitch_s);
    value_color_s(side_board, pixels_s, lw_s);
    SDL_UnlockTexture(texture_s);

    SDL_RenderClear(rend_s);
    SDL_RenderCopy(rend_s, texture_s, NULL, NULL);
    SDL_RenderPresent(rend_s);
    

   //rule organizer//
   /*
   int *val_occ = malloc((5 * sizeof(int)));
   int *place_track = malloc((6 * sizeof(int)));
   int *pop_track = malloc((6 * sizeof(int)));
   int *c1_growth = malloc((6 * 32 * sizeof(int)));
   int *c2_growth = malloc((6 * 32 * sizeof(int)));
   int dec;


   for (int i=0; i<6; i++) {
        for (int o=0; o<32; o++) {
            *(c1_growth + (i*32) + o) = 0; 
            
            // printf("%i ", o);
        } 
        *(pop_track + i) = 0;
   }



        for (int ee=0; ee<6; ee++) {
            *(place_track + ee) = 0;
        }

    for (int a=0; a<base; a++) {
        *(val_occ + 0) = a;
        for (int b=0; b<base; b++) {
            *(val_occ + 1) = b;
            for (int c=0; c<base; c++) {
                *(val_occ + 2) = c;
                for (int d=0; d<base; d++) {
                    *(val_occ + 3) = d;
                    for (int e=0; e<base; e++) {
                        *(val_occ + 4) = e;

                        int zeros = 0;
                        int ones = 0;


                        for (int f=0; f<5; f++) {
                            printf("%i ", *(val_occ + f));
                            
                            if (*(val_occ + f) ==  0) {
                                zeros += 1;}
                            if (*(val_occ + f) == 1) {
                                ones += 1;}
                        
                        }   

                        double val = *(val_occ + 0) * pow(base, 4) + 
                                        *(val_occ + 1) * pow(base, 3) +
                                        *(val_occ + 2) * pow(base, 2) +
                                        *(val_occ + 3) * pow(base, 1) +
                                        *(val_occ + 4);
                                
                        dec=val + 1;  
                        
                        if (zeros == 5) {
                            
                            printf("\n zero is five\n");
                            *(c1_growth + (5 * 32) + *(place_track + 5)) = dec;
                            *(c2_growth + (0 * 32) + *(place_track + 5)) = dec;

                            *(place_track + 5) += 1;
                            *(pop_track + 5) += 1;
                        }

                        if (zeros == 4) {
                            
                            printf("\n zero is four\n");
                            *(c1_growth + (4 * 32) + *(place_track + 4)) = dec;
                            *(c2_growth + (1 * 32) + *(place_track + 4)) = dec;

                            *(place_track + 4) += 1;
                            *(pop_track + 4) += 1;
                        }

                        if (zeros == 3) {
                            
                            printf("\n zero is three\n");
                            *(c1_growth + (3 * 32) + *(place_track + 3)) = dec;
                            *(c2_growth + (2 * 32) + *(place_track + 3)) = dec;

                            *(place_track + 3) += 1;
                            *(pop_track + 3) += 1;
                        }

                        if (zeros == 2) {
                            
                            printf("\n zero is two\n");
                            *(c1_growth + (2 * 32) + *(place_track + 2)) = dec;
                            *(c2_growth + (3 * 32) + *(place_track + 2)) = dec;

                            *(place_track + 2) += 1;
                            *(pop_track + 2) += 1;
                        }

                        if (zeros == 1) {
                            
                            printf("\n zero is one\n");
                            *(c1_growth + (1 * 32) + *(place_track + 1)) = dec;
                            *(c2_growth + (4 * 32) + *(place_track + 1)) = dec;

                            *(place_track + 1) += 1;
                            *(pop_track + 1) += 1;
                        }

                        if (zeros == 0) {
                            
                            printf("\n zero is zero\n");
                            *(c1_growth + (0 * 32) + *(place_track + 0)) = dec;
                            *(c2_growth + (5 * 32) + *(place_track + 0)) = dec;

                            *(place_track + 0) += 1;
                            *(pop_track + 0) += 1;
                        }

                        printf("\t");
                        printf("Zeros: %i\tOnes %i\t%i", zeros, ones, dec);
                        printf("\n");

                    }
                }
            }
        }
    }

    int *character_board = malloc((32 * sizeof(int)));
    for (int i=0; i<32; i++) {
        *(character_board + i) = 0;
    }

    printf("\n");
    for (int i=0; i<6; i++) {
    printf("%i ", *(pop_track + i));
    }

    printf("\n\n");
    int clink = 0;
    for (int i=0; i<6; i++) {
        for (int o=0; o<*(pop_track + i); o++) {
            printf("\n%i %i", i, o);
            printf("\t%i", *(c1_growth + (i*32) + o));
            printf("\t%i",  clink);
            *(character_board + clink) = *(c1_growth + (i*32) + o);
            clink += 1;
            
            
        }
        // clink += *(pop_track + i);
    }
    
    printf("\n");
    for (int i=0; i<32; i++) {
        printf("%i ", *(character_board + i));
    }

    */
    
    //lever//
    int c_lever = 16;

    //----------------Server----------------//

    int res, sendRes;
    WSADATA wsaData; //config data
    SOCKET listener;
    struct sockaddr_in address;
    SOCKET client;
    struct sockaddr_in clientAddr;
    int clientAddrlen;
    char *welcome = "Embrace Chaos";
    char recvbuf[BUFFLEN];
    int recvbuflen = BUFFLEN;

    //server
    if (glove > 1) {
    


        //init
    res = WSAStartup(MAKEWORD(2, 2), &wsaData);

    if (res) {
        printf("Startup failed %d\n", res);
        return 1;
    }


        //setup
            //construct socket
    listener = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    if (listener == INVALID_SOCKET) {
        printf("Error with construction %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }


            //bind
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = inet_addr(ADDRESS);
    address.sin_port = htons(PORT);
    res = bind(listener, (struct sockaddr*)&address, sizeof(address));

    if (res == SOCKET_ERROR) {
        printf("Bind failed: %d\n", WSAGetLastError());
        closesocket(listener);
        WSACleanup();
        return 1;
    }


            //set to listen
    res = listen(listener, SOMAXCONN);
    if (res == SOCKET_ERROR) {
        printf("Listen failed %d\n", WSAGetLastError());
        closesocket(listener);
        WSACleanup();
        return 1;
    }

    printf("Listening on %s:%d\n", ADDRESS, PORT);

        //handle a client
            //accept
    client = accept(listener, NULL, NULL);
    if (client == INVALID_SOCKET) {
        printf("Could not accept: %d\n", WSAGetLastError());
        close(listener);
        WSACleanup();
        return 1;
    }

            //get info
    getpeername(client, (struct sockaddr*)&clientAddr, &clientAddrlen);
    printf("Client connected at %s:%d\n", inet_ntoa(address.sin_addr), ntohs(address.sin_port));

            //send welcome message
    sendRes = send(client, welcome, strlen(welcome), 0);
    if (sendRes != strlen(welcome)) {
        printf("Error sending: %d\n", WSAGetLastError());
        shutdown(client, SD_BOTH);
        closesocket(client);
    }

            //receive messages

    }
    /*
    do {
        res = recv(client, recvbuf, recvbuflen, 0);
        if (res > 0) {
            recvbuf[res] = "\0";
            printf("\nMessage received: %s\n", recvbuf);
            printf("len %zi\n", sizeof(recvbuf));

            for (int i=0; i<12; i++) {
                uint32_t myInt1 = recvbuf[0 + (i*4)] + 
                                 (recvbuf[1 + (i*4)] << 8) + 
                                 (recvbuf[2 + (i*4)] << 16) + 
                                 (recvbuf[3 + (i*4)] << 24);

                *(glove_values + i) = myInt1;
            } printf("\n");

            for (int i=0; i<12; i++) {
                printf("%zi ", *(glove_values + i));
            } printf("\n");

            //echo message
            sendRes = send(client, recvbuf, res, 0);
                if (sendRes != res) {
                    printf("Error sending: %d\n", WSAGetLastError());
                    shutdown(client, SD_BOTH);
                    closesocket(client);
                    break;
                    }
        }
    } while (res > 0);

            //shutdown client
    res = shutdown(client, SD_BOTH);
    if (res == SOCKET_ERROR) {
        printf("Client shutdown failed: %d\n", WSAGetLastError());
    }
    closesocket(client);

        //clean up//
            //shut down
    closesocket(listener); 

            //clean up
    res = WSACleanup();

    if (res) {
        printf("Cleanup failed %d\n", res);
        return 1;
    }
    */


//--------------------MAIN-----LOOP--------------------//
    while (!should_quit) {

        //board to brush
        for (int l=0; l<bb_length; l++) {
            for (int w=0; w<bb_width; w++) {
                *(brush_board + ((l * (bb_width)) + w) % lw_bb) = *(chaos_board + 
                (((b_length - (l + (*(glove_values + 1) % 128) * brush_stroke) % b_length) * b_width) + 
                (w + (*(glove_values) % 128) * brush_stroke)) % lw);
        }} 

        if (glove == 2) {
        *(brush_board + lw_bb/2) = 1; 
        }

        //chaomize
        chaomize(brush_board, a_rule, lw_bb, ww_bb, bb_width, base);

        //brush to board
        if (glove == 2) {
            for (int l=0; l<bb_length; l++) {
                for (int w=0; w<bb_width; w++) {
                    
                    bb_convert = (((b_length - (l + (*(glove_values + 1) % 128) * brush_stroke) % b_length) * b_width) + 
                                (w + (*(glove_values) % 128) * brush_stroke)) % lw;

                    *(chaos_board + 
                    bb_convert) = 
                    *(brush_board + ((l * (bb_width)) + w) % lw_bb);

                if (*(brush_board + ((l * (bb_width)) + w) % lw_bb) == 0){
                    if (*(chaos_colors + bb_convert) > 0) {
                    *(chaos_colors + bb_convert) -= color_step;
                    }
                }
                else {
                *(chaos_colors + bb_convert) = *(chaos_colors + bb_convert) + 1;
                // printf("\ncolors %i\n", *(colors + i));
                *(chaos_colors + bb_convert) = *(chaos_colors + bb_convert) % (layer_size * 10);
                // printf("colors %i\n\n", *(colors + i));
            }
        }}}

        if (glove == 3) {
            for (int l=0; l<bb_length; l++) {
                for (int w=0; w<bb_width; w++) {
                    
                    bb_convert = (((b_length - (l + (*(glove_values + 1) % 128) * brush_stroke) % b_length) * b_width) + 
                                (w + (*(glove_values) % 128) * brush_stroke)) % lw;

                    *(chaos_board + 
                    bb_convert) = 
                    *(brush_board + ((l * (bb_width)) + w) % lw_bb);

                if (*(brush_board + ((l * (bb_width)) + w) % lw_bb) == 0){
                    if (*(chaos_colors + bb_convert) > 0) {
                    *(chaos_colors + bb_convert) -= color_step;
                    if (*(chaos_colors + bb_convert) < 0) {
                        *(chaos_colors + bb_convert) = 0;
                    }
                    }
                }
                else {
                *(chaos_colors + bb_convert) = *(chaos_colors + bb_convert) + color_step;
                *(chaos_colors + bb_convert) = *(chaos_colors + bb_convert) % (layer_size * 10);

                // printf("\ncolors %i\n", *(chaos_colors + bb_convert));
                // printf("colors %i\n\n", *(chaos_colors + bb_convert));
            }
        }}}


        //render
            //thank you Sanette
            //main render
        SDL_LockTexture(texture, NULL, (void **)&pixels, &pitch);
        value_color(chaos_board, chaos_colors, pixels, lw, color_step, color_on);
        SDL_UnlockTexture(texture);

        SDL_RenderClear(rend);
        SDL_RenderCopy(rend, texture, NULL, NULL);
        SDL_RenderPresent(rend);

            //side render
        for (int i=0; i<(bv); i++) {
            
            y_s = (i/4) * character_size * s_width;
            x_s = i%4 * character_size;

            // printf("%i %i\n", y_s, x_s);

            for (int o=0; o<character_size; o++) {
                *(side_board + ((x_s + o) + (y_s + (1 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (2 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (3 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (4 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (5 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (6 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (7 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (8 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (9 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (10 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (11 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (12 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (13 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (14 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (15 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (16 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (17 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (18 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (19 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (20 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (21 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (22 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (23 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (24 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (25 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (26 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (27 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (28 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (29 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (30 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (31 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (32 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (33 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (34 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (35 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (36 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (37 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (38 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (39 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (40 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (41 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (42 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (43 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (44 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (45 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (46 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (47 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (48 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (49 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (50 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (51 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (52 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (53 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (54 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (55 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (56 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (57 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (58 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (59 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (60 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (61 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (62 * s_width)))) = *(a_rule + i);
                *(side_board + ((x_s + o) + (y_s + (63 * s_width)))) = *(a_rule + i);

            }
        }
        SDL_LockTexture(texture_s, NULL, (void **)&pixels_s, &pitch_s);
        value_color_s(side_board, pixels_s, (s_length * s_width));
        SDL_UnlockTexture(texture_s);

        SDL_RenderClear(rend_s);
        SDL_RenderCopy(rend_s, texture_s, NULL, NULL);
        SDL_RenderPresent(rend_s);


        //events
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
            case SDL_QUIT:
                should_quit = true;
                break;

            case SDL_MOUSEBUTTONDOWN:
                if (event.button.button == SDL_BUTTON_LEFT) {
                    printf("Click!\n");
                }
                break;
            
            case SDL_KEYDOWN:
                switch(event.key.keysym.scancode){
                    case SDL_SCANCODE_ESCAPE:
                        should_quit = true;
                        break;

                    case SDL_SCANCODE_RETURN:
                        for (int i=0; i<lw; i++) {
                            *(chaos_board + i) = 0;
                            *(chaos_colors + i) = 0;
                            }
                            *(chaos_board + (lw/2)) = 1;
                        break;

                    case SDL_SCANCODE_DOWN:
                        c_lever -=1;
                        printf("%i\n", c_lever);
                        break;
                    case SDL_SCANCODE_UP:
                        c_lever += 1;
                        printf("%i\n", c_lever);
                        break;

                    case SDL_SCANCODE_Q:
                        // printf("q\n");
                        key_input(a_rule, key_counter, 0, bv, base);
                        break;

                    case SDL_SCANCODE_W:
                        //printf("w\n");
                        key_input(a_rule, key_counter, 1, bv, base);
                        break;

                    case SDL_SCANCODE_E:
                        //printf("e\n");
                        key_input(a_rule, key_counter, 2, bv, base);
                        break;

                    case SDL_SCANCODE_R:
                        //printf("r\n");
                        key_input(a_rule, key_counter, 3, bv, base);
                        break;

                    case SDL_SCANCODE_T:
                        //printf("t\n");
                        key_input(a_rule, key_counter, 4, bv, base);
                        break;

                    case SDL_SCANCODE_Y:
                        //printf("y\n");
                        key_input(a_rule, key_counter, 5, bv, base);
                        break;

                    case SDL_SCANCODE_U:
                        //printf("u\n");
                        key_input(a_rule, key_counter, 6, bv, base);
                        break;

                    case SDL_SCANCODE_I:
                        //printf("i\n");
                        key_input(a_rule, key_counter, 7, bv, base);
                        break;

                    case SDL_SCANCODE_O:
                        //printf("o\n");
                        key_input(a_rule, key_counter, 8, bv, base);
                        break;

                    case SDL_SCANCODE_P:
                        //printf("p\n");
                        key_input(a_rule, key_counter, 9, bv, base);
                        break;

                    case SDL_SCANCODE_A:
                        //printf("a\n");
                        key_input(a_rule, key_counter, 10, bv, base);
                        break;

                    case SDL_SCANCODE_S:
                        //printf("s\n");
                        key_input(a_rule, key_counter, 11, bv, base);
                        break;

                    case SDL_SCANCODE_D:
                        //printf("d\n");
                        key_input(a_rule, key_counter, 12, bv, base);
                        break;
                        
                    case SDL_SCANCODE_F:
                        //printf("f\n");
                        key_input(a_rule, key_counter, 13, bv, base);
                        break;

                    case SDL_SCANCODE_G:
                        //printf("g\n");
                        key_input(a_rule, key_counter, 14, bv, base);
                        break;

                    case SDL_SCANCODE_H:
                        //printf("h\n");
                        key_input(a_rule, key_counter, 15, bv, base);
                        break;

                    case SDL_SCANCODE_J:
                        //printf("j\n");
                        key_input(a_rule, key_counter, 16, bv, base);
                        break;

                    case SDL_SCANCODE_K:
                        //printf("k\n");
                        key_input(a_rule, key_counter, 17, bv, base);
                        break;

                    case SDL_SCANCODE_L:
                        //printf("l\n");
                        key_input(a_rule, key_counter, 18, bv, base);
                        break;

                    case SDL_SCANCODE_Z:
                        //printf("z\n");
                        key_input(a_rule, key_counter, 19, bv, base);
                        break;

                    case SDL_SCANCODE_X:
                        //printf("x\n");
                        key_input(a_rule, key_counter, 20, bv, base);
                        break;

                    case SDL_SCANCODE_C:
                        //printf("c\n");
                        key_input(a_rule, key_counter, 21, bv, base);
                        break;

                    case SDL_SCANCODE_V:
                        //printf("v\n");
                        key_input(a_rule, key_counter, 22, bv, base);
                        break;

                    case SDL_SCANCODE_B:
                        //printf("b\n");
                        key_input(a_rule, key_counter, 23, bv, base);
                        break;

                    case SDL_SCANCODE_N:
                        //printf("n\n");
                        key_input(a_rule, key_counter, 24, bv, base);
                        break;

                    case SDL_SCANCODE_M:
                        //printf("m\n");
                        key_input(a_rule, key_counter, 25, bv, base);
                        break;

                    case SDL_SCANCODE_SPACE:
                        //printf(" \n");
                        key_input(a_rule, key_counter, 26, bv, base);
                        break;
                    
                }

            default:
                break;
            }
        }
        

        //glove
        if (glove > 0) {
            //glove values

            res += 1;
            gv=0;
            do {
                res = recv(client, recvbuf, recvbuflen, 0);
                if (res > 0) {
                    recvbuf[res] = "\0";
                    // printf("\nMessage received: %s\n", recvbuf);
                    // printf("len %zi\n", sizeof(recvbuf));

                    for (int i=0; i<12; i++) {
                        uint32_t myInt1 = recvbuf[0 + (i*4)] + 
                                        (recvbuf[1 + (i*4)] << 8) + 
                                        (recvbuf[2 + (i*4)] << 16) + 
                                        (recvbuf[3 + (i*4)] << 24);

                        *(glove_values + i) = myInt1;
                        } 
                        //printf("\n");

                    for (int i=0; i<12; i++) {
                        // printf("%zi ", *(glove_values + i));
                        gv += *(glove_values + i);
                        } 
                        // printf("\n");

                    //echo message
                    // printf("[DEBUG0] ### sendRes value = %d\n", sendRes);
                    sendRes = send(client, recvbuf, res, 0);
                    if (sendRes != res) {
                        printf("Error sending: %d\n", WSAGetLastError());
                        shutdown(client, SD_BOTH);
                        closesocket(client);
                        break;
                        }
                    // printf("[DEBUG0] ### Respond value is: %d\n", res);
                    res=0;
                }
            } while (res > 0);


                //glove methods
            if (glove == 1) {
            if (*(glove_values + 7) > index_trigger) {
                if (c_1 < drain_level) {
                    c_1 += step_up;
                } else {
                    c_1 = 0;
                    c_0 = 0;
                    for (int i=0; i<bv; i++) {
                        if (*(a_rule + i) == 1) {
                            *(a_rule + i) = 0;
                        }
                    }
                }
            } else {
                if (c_1 > 0) {
                    c_1 -= step_down;
                }
            }

            if (*(glove_values + 8) > middle_trigger) {
                if (c_2 < drain_level) {
                    c_2 += step_up;
                } else {
                    c_2 = 0;
                    c_0 = 0;
                    for (int i=0; i<bv; i++) {
                        if (*(a_rule + i) == 2) {
                            *(a_rule + i) = 0;
                        }
                    }
                }
            } else {
                if (c_2 > 0) {
                    c_2 -= step_down;
                }
            }

            if (*(glove_values + 9) > ring_trigger) {
                if (c_3 < drain_level) {
                    c_3 += step_up;
                } else {
                    c_3 = 0;
                    c_0 = 0;
                    for (int i=0; i<bv; i++) {
                        if (*(a_rule + i) == 3) {
                            *(a_rule + i) = 0;
                        }
                    }
                }
            } else {
                if (c_3 > 0) {
                    c_3 -= step_down;
                }
            }

            if (*(glove_values + 10) > pinky_trigger) {
                if (c_4 < drain_level) {
                    c_4 += step_up;
                } else {
                    c_4 = 0;
                    c_0 = 0;
                    for (int i=0; i<bv; i++) {
                        if (*(a_rule + i) == 4) {
                            *(a_rule + i) = 0;
                        }
                    }
                }
            } else {
                if (c_4 > 0) {
                    c_4 -= step_down;
                }
            }

            if (c_0 < c_1) {
                c_0 = c_1;
            }

            if (c_0 < c_2) {
                c_0 = c_2;
            }

            if (c_0 < c_3) {
                c_0 = c_3;
            }

            if (c_0 < c_4) {
                c_0 = c_4;
            }

            if (c_0 > 0) {
                c_0 -= step_down;
            }

            c_total = c_0 + c_1 + c_2 + c_3 + c_4;
            c_ratio = c_total / c_max;
            window = c_ratio * window_max;

            printf("\n%f\t%f\t%f\t%f\t%f\t%f\t%f\n", c_0, c_1, c_2, c_3, c_4, c_ratio, window);

            place = 0;
            if (c_total < 1) {
                c_total = 1;
            }
            ci_0 = (c_0/c_total) * window;
            ci_1 = (c_1/c_total) * window;
            ci_2 = (c_2/c_total) * window;
            ci_3 = (c_3/c_total) * window;
            ci_4 = (c_4/c_total) * window;

            if(ci_0 > drain_level) {
                ci_0 = drain_level;
            }
            if(ci_1 > drain_level) {
                ci_1 = drain_level;
            }
            if(ci_2 > drain_level) {
                ci_2 = drain_level;
            }
            if(ci_3 > drain_level) {
                ci_3 = drain_level;
            }
            if(ci_4 > drain_level) {
                ci_4 = drain_level;
            }

            printf("\n%i\t%i\t%i\t%i\t%i\n", ci_0, ci_1, ci_2, ci_3, ci_4);

            for (int i=0; i<ci_0; i++) {
                *(a_rule + (gv + place)) = 0;
                place += *(glove_values + 6)/skip_scale;
            }

            for (int i=0; i<ci_1; i++) {
                *(a_rule + (gv + place)) = 1;
                place += *(glove_values + 6)/skip_scale;
            }

            if (base > 2) {
            for (int i=0; i<ci_2; i++) {
                *(a_rule + (gv + place)) = 2;
                place += *(glove_values + 6)/skip_scale;
            }}

            if (base > 3) {
            for (int i=0; i<ci_3; i++) {
                *(a_rule + (gv + place)) = 3;
                place += *(glove_values + 6)/skip_scale;
            }}

            if (base > 4) {
            for (int i=0; i<ci_4; i++) {
                *(a_rule + (gv + place)) = 4;
                place += *(glove_values + 6)/skip_scale;
            }}}
            
            else if (glove == 2) {
                
                //rule calc
                rule_value = ((*(glove_values + 6)/64) + 
                            (*(glove_values + 7)/64) * 2 + 
                            (*(glove_values + 8)/64) * 4 + 
                            (*(glove_values + 9)/64) * 8 +
                            (*(glove_values + 10)/64) * 16);

                //single change check
                if (rule_value % bv != last_value) {
                    if (*(a_rule + (rule_value % bv)) == 0) {
                        *(a_rule + (rule_value % bv)) = 1;
                    } else {
                        *(a_rule + (rule_value % bv)) = 0;
                    }} else {
                    }
                last_value = (rule_value % bv);


                //wrist activation
                if (*(glove_values + 3)/64 == 1) {

                    for (int i=0; i<lw; i++) {
                        *(chaos_board + i) = 0;
                        *(brush_board + i%lw_bb) = 0;
                    }

                    color_on += 1;
                    color_on = color_on % 2;
                }

                //brush size
                bb_length = ((*(glove_values + 2) % 128) * 4 + 9) % (b_length - 1) + 1;
                bb_width = bb_length;
                lw_bb = bb_length * bb_width;
                ww_bb = bb_width * bb_width;

                // printf("\n%i %i %i %i\n", bb_length, bb_width, lw_bb, ww_bb);
                
            }

            else if (glove == 3) {
                
                //rule calc
                rule_value = ((*(glove_values + 6)/64) + 
                            (*(glove_values + 7)/64) * 2 + 
                            (*(glove_values + 8)/64) * 4 + 
                            (*(glove_values + 9)/64) * 8 +
                            (*(glove_values + 10)/64) * 16);

                //single change check
                if (rule_value % bv != last_value) {
                    if (*(a_rule + (rule_value % bv)) == 0) {
                        *(a_rule + (rule_value % bv)) = 1;
                    } else {
                        *(a_rule + (rule_value % bv)) = 0;
                    }} else {
                    }
                last_value = (rule_value % bv);


                //wrist activation
                if (*(glove_values + 3)/64 == 1) {

                    for (int i=0; i<lw; i++) {
                        *(chaos_board + i) = 0;
                        *(chaos_colors + i) = 0;
                        *(brush_board + i%lw_bb) = 0;

                    }

                    color_on += 1;
                    color_on = color_on % 2;
                }
                
                //color_step
                color_step = (*(glove_values + 2) / color_step_scale) + 1;
                
            }

        }
        
        int pin_y = lw - (((((*(glove_values + 1) * b_width/128) % b_width) * b_width) % lw) - 1);
        int pin_x = (*(glove_values) * b_width/128) % b_width;
        int pin_test = (pin_x + pin_y) % lw;

        // printf("\npin_test %i %i %i", pin_test, pin_y, pin_x);

        if (*(chaos_board + pin_test) == 0) {
            *(chaos_board + pin_test) = 1;
        }
        else {
            *(chaos_board + pin_test) = 0;
        }
        

        
    }

    return 0;
}