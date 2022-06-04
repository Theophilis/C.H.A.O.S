
#C.H.A.O.S

import numpy as np
import pygame
import os
import pickle
import sys

pygame.font.init()

length = 8
#number of times given rule is applied and number of initial rows generated
width = length * 2 + 1
#number of cells in a row
rule = 90
#number who's x_base transformation gives the rules dictionary its values
view = 4
#size of the view window that scans a row for rule application
base = 2
#numerical base of the rule set. number of colors each cell can be
start = length
#position for a row 0 cell value 1
direction = 0
#if ^ = 0 view scans from left to right: else view scans right to left


#####to do#####
#translate complex numbers (pi, phi, e) to a base n digit sequence(where n is the number of possible rule states to be called).
##Then, trigger a rotation of a rule state based on the rule position given by the digit in the complex number

#prep journal data for analysis

#add a record feature and button to menu. allows for recorder of all key inputs in a text file.

#write a read.me and contributor guide, attatch a GNU open source license, and publish on github




#####map#####


def base_x(n, b):
    e = n//b
    q = str(n % b)
    if n == 0:
        return '0'
    elif e == 0:
        return q
    else:
        return base_x(e, b) + q


def rule_gen_2(rule, base = 2, width = 0):

    rules = dict()

    int_rule = base_x(rule, base)

    x = int_rule[::-1]

    if width == 0:
        while len(x) < base ** view:

            x += '0'

    else:
        while len(x) < width:
            x += '0'
    
    bnr = x[::-1]

    int_rule = [int(v) for v in bnr]

    for x in range(len(int_rule)):

        x = len(int_rule) - x - 1

        key = tuple(base_x(x, base)[-view:])

        if len(key) < view:

            diff = view - len(key)
            key = list(key)

            for y in range(diff):

                key.insert(0, str(0))

        key = "".join(key)

        rules[tuple(key)] = int_rule[-x - 1]

    return rules, int_rule


def fencing(zero, level = 0):
    # print(" ")
    # print("zero")
    # print(zero)
    fence = []
    for x in range(4):
        if x % 2 == 0:
            if x < 2:
                # print(x)
                for y in range(2 * (level + 1)):
                    post = (zero[0], zero[0] + (y + 1))
                    # print("post")
                    # print(post)
                    fence.append(post)
            else:
                # print(x)
                for y in range(2 * (level + 1)):
                    post = (zero[0] + 2 * (level + 1), zero[0] + 2 * (level + 1) - (y + 1))
                    fence.append(post)

        else:
            if x < 2:
                # print(x)
                for y in range(2 * (level + 1)):
                    post = (zero[0] + (y + 1), zero[0] + 2 * (level + 1))
                    fence.append(post)
            else:
                # print(x)
                for y in range(2 * (level + 1) + 1):
                    post = (zero[0] + 2 * (level + 1) - (y + 1), zero[0])
                    fence.append(post)

    return tuple(fence)


def viewer(f, canvas):
    try:
        c_1 = canvas[(f[0] - 1, f[1])]
    except:
        c_1 = 0

    try:
        c_2 = canvas[(f[0], f[1] + 1)]
    except:
        c_2 = 0

    try:
        c_3 = canvas[(f[0] + 1, f[1])]
    except:
        c_3 = 0

    try:
        c_4 = canvas[(f[0], f[1] - 1)]
    except:
        c_4 = 0
    # view = (canvas[c_1], canvas[c_2], canvas[c_3], canvas[c_4])
    view = (str(c_1), str(c_2), str(c_3), str(c_4))
    return view


def fence_map(size, start, order=0):

    if order == 0:
        fence = dict()

        for x in range(int(size/2)):
            zero = (start[0] - (x + 1), start[0] - (x + 1))
            fence[x] = fencing(zero, x)

        full_fence = []
        for k in list(fence.keys()):
            for f in fence[k][:len(fence[k]) - 1]:
                full_fence.append(f)

        canvas_f = np.zeros((size, size), dtype='int8')
        full_fence.insert(0, start)

        for f in full_fence:
            canvas_f[f] = full_fence.index(f)

        return full_fence, canvas_f

    elif order == 1:
        canvas_t = np.zeros((size, size), dtype='int8')

        t_fence = []

        for x in range(size):
            for y in range(size):
                t_fence.append((x, y))

        for t in t_fence:
            canvas_t[t] = t_fence.index(t)

        return t_fence, canvas_t

    elif order == 2:
        canvas = np.zeros((size, size), dtype='int8')

        fence = []

        for x in range(size):
            for y in range(size):
                fence.append((x, y))

        fence = sorted(fence, key=lambda x: abs(x[0] + x[1]))

        for f in fence:
            canvas[f] = fence.index(f)

        return fence, canvas



#####game#####

pygame.init()
pygame.display.init()

current_display = pygame.display.Info()
# WIDTH , HEIGHT = current_display.current_w - 50, current_display.current_h - 100
WIDTH, HEIGHT = 603, 603
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
letter_values = {'q':0, 'w':1, 'e':2, 'r':3, 't':4, 'y':5, 'u':6, 'i':7, 'o':8, 'p':9, 'a':10, 's':11, 'd':12, 'f':13,
                 'g':14, 'h':15, 'j':16, 'k':17, 'l':18, 'z':19, 'x':20, 'c':21, 'v':22, 'b':23, 'n':24, 'm':25, ' ':26}

pygame.display.set_caption("C.H.A.O.S")


click = False


def Chaos_Window(base, pixel_res):

    run, FPS, rule, clock, journal, press, view = 1, 30,  451, pygame.time.Clock(), dict(), dict(), 4

    cell_row_width, cell_rows = int(WIDTH/pixel_res), int(HEIGHT/pixel_res)

    d_rule, i_rule = rule_gen_2(rule, base)

    canvas = np.zeros((cell_rows, cell_row_width), dtype='int8')
    start = (int(cell_rows / 2), int(cell_row_width / 2))
    full_fence, canvas_f = fence_map(cell_row_width, start)
    canvas[start] = 1

    print(" ")
    print("d_rule")
    print(d_rule)
    print("i_rule")
    print(i_rule)
    print(len(i_rule))

    def redraw_window():

        rule_label_0_b = text_font.render(f"RUL3: {i_rule[0:int((base**view)/2)]}", 1, (255, 255, 255))
        rule_label_1_b = text_font.render(f"          {i_rule[int((base**view)/2):int((base**view))]}", 1, (255, 255, 255))
        #
        # step_label_b = main_font.render(f"5T3P: {step}", 1, (255, 255, 255))
        # rand_count_l = main_font.render(f"C0UNT: {rand_count}", 1, (255, 255, 255))
        #
        WIN.blit(rule_label_0_b, (10, HEIGHT - 40))
        WIN.blit(rule_label_1_b, (7, HEIGHT - 25))
        #
        # WIN.blit(step_label_b, (WIDTH - step_label_b.get_width() - 10, 10))
        # WIN.blit(rand_count_l, (WIDTH - step_label_b.get_width() - 39, 50))



        pygame.display.update()

    def input(letter, base):

        bv = base ** view

        if letter not in press:
            press[letter] = 0
        else:
            press[letter] += 1

        place = int((letter_values[letter] + ((press[letter] % (int(bv / len(letter_values)) + 2)) * int(
            (bv / int(bv / len(letter_values) + 1))))) % bv)

        if i_rule[place] == 0:

            i_rule[place] = 1
            d_rule[list(d_rule.keys())[place]] = 1

        elif i_rule[place] == 1:

            if base == 2:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 2
                d_rule[list(d_rule.keys())[place]] = 2

        elif i_rule[place] == 2:

            if base == 3:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 3
                d_rule[list(d_rule.keys())[place]] = 3

        else:
            i_rule[place] = 0
            d_rule[list(d_rule.keys())[place]] = 0

    for f in full_fence:

        cell = pygame.Rect(f[0] * pixel_res, f[1] * pixel_res, pixel_res, pixel_res)

        if canvas[f] == 0:
            pygame.draw.rect(WIN, (0, 0, 0), cell)

        if canvas[f] == 1:
            pygame.draw.rect(WIN, (255, 0, 255), cell)

        if canvas[f] == 2:
            pygame.draw.rect(WIN, (0, 255, 255), cell)

        if canvas[f] == 3:
            pygame.draw.rect(WIN, (255, 255, 0), cell)

    pygame.display.update()

    while run == 1:

        WIN.fill((0, 0, 0))
        clock.tick(FPS)

        for f in full_fence:
            views = viewer(f, canvas)
            f_0 = canvas[f]
            canvas[f] = d_rule[views]

            cell = pygame.Rect(f[0] * pixel_res, f[1] * pixel_res, pixel_res, pixel_res)

            if canvas[f] == 0:
                pygame.draw.rect(WIN, (0, 0, 0), cell)

            if canvas[f] == 1:
                pygame.draw.rect(WIN, (255, 0, 255), cell)

            if canvas[f] == 2:
                pygame.draw.rect(WIN, (0, 255, 255), cell)

            if canvas[f] == 3:
                pygame.draw.rect(WIN, (255, 255, 0), cell)

        redraw_window()
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2

            if event.type == pygame.KEYDOWN:

                if event.key == K_ESCAPE:
                    run = 2

                if event.key == pygame.K_q:

                    input('q', base)

                if event.key == pygame.K_w:

                    input('w', base)

                if event.key == pygame.K_e:

                    input('e', base)

                if event.key == pygame.K_r:

                    input('r', base)

                if event.key == pygame.K_t:

                    input('t', base)

                if event.key == pygame.K_y:

                    input('y', base)

                if event.key == pygame.K_u:

                    input('u', base)

                if event.key == pygame.K_i:

                    input('i', base)

                if event.key == pygame.K_o:

                    input('o', base)

                if event.key == pygame.K_p:

                    input('p', base)

                if event.key == pygame.K_a:

                    input('a', base)

                if event.key == pygame.K_s:

                    input('s', base)

                if event.key == pygame.K_d:

                    input('d', base)

                if event.key == pygame.K_f:

                    input('f', base)

                if event.key == pygame.K_g:

                    input('g', base)

                if event.key == pygame.K_h:

                    input('h', base)

                if event.key == pygame.K_j:

                    input('j', base)

                if event.key == pygame.K_k:

                    input('k', base)

                if event.key == pygame.K_l:

                    input('l', base)

                if event.key == pygame.K_z:

                    input('z', base)

                if event.key == pygame.K_x:

                    input('x', base)

                if event.key == pygame.K_c:

                    input('c', base)

                if event.key == pygame.K_v:

                    input('v', base)

                if event.key == pygame.K_b:

                    input('b', base)

                if event.key == pygame.K_n:

                    input('n', base)

                if event.key == pygame.K_m:

                    input('m', base)

                if event.key == pygame.K_SPACE:

                    input(' ', base)



#menus

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)



def draw_text(text, font, color_dt, surface, x, y):
    textobj = font.render(text, 1, color_dt)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



def menu():

    click = False
    input_text = ''

    while True:


        WIN.fill((0, 0, 0))
        t_line = pygame.Rect(WIDTH/2 - 633, 200, 1360, 2)
        draw_text('C311UL4R H4PT1C 4UT0M4T4 0P3R4T1NG 5Y5T3M', TITLE_FONT, (10, 100, 10), WIN, WIDTH/2 - 655, 100)
        pygame.draw.rect(WIN, (10, 100, 10), t_line)

        text_surface = main_font.render(input_text, True, (100, 10, 100))
        mx, my = pygame.mouse.get_pos()


        size_2 = pygame.Rect(WIDTH/2 - 300, 400, 200, 50)
        size_3 = pygame.Rect(WIDTH/2 - 300, 500, 200, 50)
        size_5 = pygame.Rect(WIDTH/2 - 300, 600, 200, 50)
        size_10 = pygame.Rect(WIDTH/2 - 300, 700, 200, 50)
        size_2_i = pygame.Rect(WIDTH/2 - 300, 400, 197, 43)
        size_3_i = pygame.Rect(WIDTH/2 - 300, 500, 197, 43)
        size_5_i = pygame.Rect(WIDTH/2 - 300, 600, 197, 43)
        size_10_i = pygame.Rect(WIDTH/2 - 300, 700, 197, 43)

        binary = pygame.Rect(WIDTH/2 + 100, 400, 200, 50)
        ternary = pygame.Rect(WIDTH/2 + 100, 500, 200, 50)
        quaternary = pygame.Rect(WIDTH/2 + 100, 600, 200, 50)
        binary_i = pygame.Rect(WIDTH/2 + 100, 400, 197, 43)
        ternary_i = pygame.Rect(WIDTH/2 + 100, 500, 197, 43)
        quaternary_i = pygame.Rect(WIDTH/2 + 100, 600, 197, 43)

        vel_rect = pygame.Rect(WIDTH/2 + 100, 700, 200, 50)
        vel_rect_i = pygame.Rect(WIDTH/2 + 100, 700, 197, 43)

        enter = pygame.Rect(WIDTH/2 - 100, 850, 200, 50)
        enter_i = pygame.Rect(WIDTH/2 - 100, 850, 197, 43)

        underline_1 = pygame.Rect(WIDTH/2 + 100, 385, 200, 2)
        underline_2 = pygame.Rect(WIDTH/2 - 300, 385, 200, 2)


        pygame.draw.rect(WIN, (10, 100, 10), size_2)
        pygame.draw.rect(WIN, (10, 100, 10), size_3)
        pygame.draw.rect(WIN, (10, 100, 10), size_5)
        pygame.draw.rect(WIN, (10, 100, 10), size_10)
        pygame.draw.rect(WIN, (0, 0, 0), size_2_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_3_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_5_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_10_i)
        draw_text(' small', main_font, (10, 100, 10), WIN, WIDTH/2 - 300, 400)
        draw_text(' medium', main_font, (10, 100, 10), WIN, WIDTH/2 - 300, 500)
        draw_text(' large', main_font, (10, 100, 10), WIN, WIDTH/2 - 300, 600)
        draw_text(' X-large', main_font, (10, 100, 10), WIN, WIDTH/2 - 300, 700)
        draw_text('Cell Size', main_font, (10, 100, 10), WIN, WIDTH/2 - 280, 340)
        pygame.draw.rect(WIN, (10, 100, 10), underline_2)

        pygame.draw.rect(WIN, (100, 10, 10), binary)
        pygame.draw.rect(WIN, (100, 10, 10), ternary)
        pygame.draw.rect(WIN, (100, 10, 10), quaternary)
        pygame.draw.rect(WIN, (0, 0, 0), binary_i)
        pygame.draw.rect(WIN, (0, 0, 0), ternary_i)
        pygame.draw.rect(WIN, (0, 0, 0), quaternary_i)
        draw_text(' Two', main_font, (100, 10, 10), WIN, WIDTH/2 + 100, 400)
        draw_text(' Three', main_font, (100, 10, 10), WIN, WIDTH/2 + 100, 500)
        draw_text(' Four', main_font, (100, 10, 10), WIN, WIDTH/2 + 100, 600)
        draw_text('Number of Colors', main_font, (100, 10, 10), WIN, WIDTH/2 + 80, 340)
        pygame.draw.rect(WIN, (100, 10, 10), underline_1)

        pygame.draw.rect(WIN, (100, 10, 100), vel_rect)
        pygame.draw.rect(WIN, (0, 0, 0), vel_rect_i)
        draw_text('^place mouse-pointer on box to type;', small_font, (100, 10, 100), WIN, WIDTH/2 + 200, 775)
        draw_text('numbers between 1-10 recommended', small_font, (100, 10, 100), WIN, WIDTH/2 + 210, 800)

        pygame.draw.rect(WIN, (10, 10, 100), enter)
        pygame.draw.rect(WIN, (0, 0, 0), enter_i)
        draw_text(' Enter', main_font, (10, 10, 100), WIN, WIDTH/2 - 100, 850)

        draw_text('Instructions:', small_font, (200, 200, 200), WIN, 50, 275)
        draw_text('1. Choose a cell-size. [GREEN]', small_font, (200, 200, 200), WIN, 50, 325)
        draw_text('     -Start with X-large to be safe. Smaller cells', text_font, (200, 200, 200), WIN, 50, 365)
        draw_text('         may cause issues on slower computers.', text_font, (200, 200, 200), WIN, 50, 390)
        draw_text('2. Choose the number of cell colors. [RED]', small_font, (200, 200, 200), WIN, 50, 425)
        draw_text('3. Set a desired speed. [PURPLE]', small_font, (200, 200, 200), WIN, 50, 475)
        draw_text('4. Press Enter [BLUE]', small_font, (200, 200, 200), WIN, 50, 525)
        draw_text('     The program will have loaded once you see Step & Count', text_font, (200, 200, 200), WIN, 50, 575)
        draw_text('     in the top right, and Rule in the bottom left.', text_font, (200, 200, 200), WIN, 50, 600)
        draw_text('     Typing has no effect until the first row of colored', text_font, (200, 200, 200), WIN, 50, 625)
        draw_text('     cells reach the bottom of the page.', text_font, (200, 200, 200), WIN, 50, 650)
        draw_text('     Two cell colors uses the keys (asdf-jkl;) to change the rules.', text_font, (200, 200, 200), WIN, 50, 675)
        draw_text('     For three colors+, the best effects are seen while typing full sentences', text_font, (200, 200, 200), WIN, 50, 700)
        draw_text('     Press the escape key to exit the program at any time.', text_font, (200, 200, 200), WIN, 50, 725)
        draw_text('     Enjoy!', text_font, (200, 200, 200), WIN, 50, 750)

        if size_2.collidepoint((mx, my)):
            if click:
                print("size_2")
                pixel_res = 2
                draw_text(' small', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 400)
        if size_3.collidepoint((mx, my)):
            if click:
                print("size_3")
                pixel_res = 3
                draw_text(' medium', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 500)
        if size_5.collidepoint((mx, my)):
            if click:
                print("size_5")
                pixel_res = 5
                draw_text(' large', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 600)
        if size_10.collidepoint((mx, my)):
            if click:
                print("size_10")
                pixel_res = 10
                draw_text(' X-large', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 700)

        if binary.collidepoint((mx, my)):
            if click:
                print("binary")
                base = 2
                draw_text(' Two', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 400)
        if ternary.collidepoint((mx, my)):
            if click:
                print("ternary")
                base = 3
                draw_text(' Three', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 500)
        if quaternary.collidepoint((mx, my)):
            if click:
                print("quaternary")
                base = 4
                draw_text(' Four', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 600)

        if vel_rect.collidepoint((mx, my)):
            draw_text('Speed:', main_font, (100, 10, 100), WIN, WIDTH / 2 + 100, 700)
            WIN.blit(text_surface, (WIDTH / 2 + 200, 700))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        input_text += '1'
                    if event.key == K_2:
                        input_text += '2'
                    if event.key == K_3:
                        input_text += '3'
                    if event.key == K_4:
                        input_text += '4'
                    if event.key == K_5:
                        input_text += '5'
                    if event.key == K_6:
                        input_text += '6'
                    if event.key == K_7:
                        input_text += '7'
                    if event.key == K_8:
                        input_text += '8'
                    if event.key == K_9:
                        input_text += '9'
                    if event.key == K_0:
                        input_text += '0'
                    if event.key == K_BACKSPACE:
                        input_text = input_text[:len(input_text) - 1]
                    print(input_text)

            if len(input_text) > 0:
                cell_vel = int(input_text)

        if enter.collidepoint((mx, my)):
            if click:
                print("enter")
                print("pixel_res")
                print(pixel_res)
                draw_text('Enter', main_font, (255, 255, 255), WIN, WIDTH / 2 - 100, 800)
                Chaos_Window(base, pixel_res, cell_vel)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        mainClock.tick(60)

# menu()

Chaos_Window(4, 2)
