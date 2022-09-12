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

void value_color(int *board, uint8_t *pixels, int lw){

    for (int i=0; i<lw; i++) {
        // printf("%i  ", *(board + i));
        //ARGB

        if (*(board + i) == 0) {
            // printf("zero\n");
            *(pixels + (i * 4)) = 0;
            *(pixels + (i * 4) + 1) = 0;
            *(pixels + (i * 4) + 2) = 0;
            *(pixels + (i * 4) + 3) = 0;
        }

        if (*(board + i) == 1) {
            // printf("one\n");
            *(pixels + (i * 4)) = 255;
            *(pixels + (i * 4) + 1) = 0;
            *(pixels + (i * 4) + 2) = 255;
            *(pixels + (i * 4) + 3) = 255;
        }

        if (*(board + i) == 2) {
            // printf("two\n");
            *(pixels + (i * 4)) = 255;
            *(pixels + (i * 4) + 1) = 255;
            *(pixels + (i * 4) + 2) = 0;
            *(pixels + (i * 4) + 3) = 255;
        }

        if (*(board + i) == 3) {
            // printf("three\n");
            *(pixels + (i * 4)) = 255;
            *(pixels + (i * 4) + 1) = 255;
            *(pixels + (i * 4) + 2) = 255;
            *(pixels + (i * 4) + 3) = 0;
        }
        


    }
}

int main(int argc, char *argv[]) {
    
    puts("Hello there\n");
    puts("\tspread some chaos\n");

    //--------------------START--------------------//

        //standard
    int base = 4;
    int view = 5;
    int b_length = 1001;
    int b_width = 1001;
    int gv = 0;

        //calculated
    float bv_0 = pow(base, view);
    int bv = bv_0;
    int lw = b_length * b_width;
    int ww = 2 * b_width;

        //arrays
    int *a_rule = malloc((bv * sizeof(int)));
    int *chaos_board = malloc((lw * sizeof(int)));
    int *key_counter = malloc((27 * sizeof(int)));
    int *glove_values = malloc(12 * sizeof(long));
    //x=0, y=1, z=2, pitch=3, yaw=4, roll=5, thumb=6, pointer=7, middle=8, ring=9, pinky=10, elbow=11

        //glove methods

    int thumb_trigger = 64;
    int index_trigger = 64;
    int middle_trigger = 64;
    int ring_trigger = 64;
    int pinky_trigger = 64;


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
    for (int i=0; i<lw; i++) {
        *(chaos_board + i) = 0;
    }
    *(chaos_board + (lw/2)) = 1;

    //--------------------END--------------------//
    
    //----------------sdl shit----------------//
    
    //init
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window *win;
    SDL_Renderer *rend;
    SDL_Texture *texture;

    //define
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

    SDL_ShowCursor(false);


    //pixels
    int pitch = lw * 4;
    uint8_t *pixels = malloc((pitch * sizeof(uint8_t)));

    SDL_LockTexture(texture, NULL, (void **)&pixels, &pitch);
    value_color(chaos_board, pixels, lw);
    SDL_UnlockTexture(texture);

    SDL_RenderClear(rend);
    SDL_RenderCopy(rend, texture, NULL, NULL);
    SDL_RenderPresent(rend);
    

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


        //init
    WSADATA wsaData; //config data
    res = WSAStartup(MAKEWORD(2, 2), &wsaData);

    if (res) {
        printf("Startup failed %d\n", res);
        return 1;
    }


        //setup
            //construct socket
    SOCKET listener;
    listener = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    if (listener == INVALID_SOCKET) {
        printf("Error with construction %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }


            //bind
    struct sockaddr_in address;
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
    SOCKET client;
    struct sockaddr_in clientAddr;
    int clientAddrlen;
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
    char *welcome = "Embrace Chaos";
    sendRes = send(client, welcome, strlen(welcome), 0);
    if (sendRes != strlen(welcome)) {
        printf("Error sending: %d\n", WSAGetLastError());
        shutdown(client, SD_BOTH);
        closesocket(client);
    }

            //receive messages
    char recvbuf[BUFFLEN];
    int recvbuflen = BUFFLEN;

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

        //chaomize
        chaomize(chaos_board, a_rule, lw, ww, b_width, base);


        //render
            //thank you Sanette
        SDL_LockTexture(texture, NULL, (void **)&pixels, &pitch);
        value_color(chaos_board, pixels, lw);
        SDL_UnlockTexture(texture);

        SDL_RenderClear(rend);
        SDL_RenderCopy(rend, texture, NULL, NULL);
        SDL_RenderPresent(rend);


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
                //printf("%zi ", *(glove_values + i));
                gv += *(glove_values + i);
                } 
                //printf("\n");

            //echo message
            sendRes = send(client, recvbuf, res, 0);
                if (sendRes != res) {
                    printf("Error sending: %d\n", WSAGetLastError());
                    shutdown(client, SD_BOTH);
                    closesocket(client);
                    break;
                    }
                res=0;
                }
            } while (res > 0);


        //glove methods
        
    }

    return 0;
}