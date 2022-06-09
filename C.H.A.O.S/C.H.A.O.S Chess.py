# C.H.A.O.S

import numpy as np
from datetime import datetime
import random
import pygame
import os
import pickle
import sys
import pygame.midi
import time
from collections import deque

sys.setrecursionlimit(999999999)

pygame.font.init()

length = 8
# number of times given rule is applied and number of initial rows generated
width = length * 2 + 1
# number of cells in a row
rule = 90
# number who's x_base transformation gives the rules dictionary its values
view = 3
# size of the view window that scans a row for rule application
base = 3
# numerical base of the rule set. number of colors each cell can be
start = length
# position for a row 0 cell value 1
direction = 0


# if ^ = 0 view scans from left to right: else view scans right to left


#####to do#####
# translate complex numbers (pi, phi, e) to a base n digit sequence(where n is the number of possible rule states to be called).
##Then, trigger a rotation of a rule state based on the rule position given by the digit in the complex number

# add a record feature and button to menu. allows for recorder of all key inputs in a text file.


#####map#####

def base_x(n, b):
    e = n // b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def decimal(n, b):

    n = list(reversed(n))
    n = [int(v) for v in n]

    value = 0
    place = 0


    for c in n:

        value += int(c) * b ** place
        place += 1

    return value


def rule_gen(rule, base=2):

    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_x(int(rule), (base))

    x = int_rule[::-1]

    while len(x) < base ** view:
        x += '0'

    bnr = x[::-1]
    int_rul = list(bnr)
    int_rule = []
    for i in int_rul:
        int_rule.append(int(i))

    for x in reversed(range(len(int_rule))):
        key = tuple(base_x(x, base)[-view:])

        # print(" ")
        # print("key")
        # print(key)
        if len(key) < view:
            diff = view - len(key)
            key = list(key)

            for y in range(diff):
                key.insert(0, str(0))

        key = "".join(key)
        # print(" ")
        # print(x)
        # print("int_rule_x")
        # print(int_rule)
        # print(int_rule[x])
        rules[tuple(key)] = int(int_rule[-x - 1])
    # print("")
    # print("rules")
    # print(rules)

    return rules, int_rule


def rule_gen_2(rule, base, length):
    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_x(rule, base)

    x = int_rule[::-1]

    while len(x) < length:
        x += '0'

    bnr = x[::-1]
    int_rul = list(bnr)
    int_rule = []
    for i in int_rul:
        int_rule.append(int(i))

    for x in reversed(range(len(int_rule))):
        key = tuple(base_x(x, base)[-view:])

        # print(" ")
        # print("key")
        # print(key)
        if len(key) < view:
            diff = view - len(key)
            key = list(key)

            for y in range(diff):
                key.insert(0, str(0))

        key = "".join(key)
        # print(" ")
        # print(x)
        # print("int_rule_x")
        # print(int_rule)
        # print(int_rule[x])
        rules[tuple(key)] = int(int_rule[-x - 1])
    # print("")
    # print("rules")
    # print(rules)

    return rules, int_rule


def viewer_1d(row, y, view, v_0):
    # print('view')
    # print(view)
    # print("v_0_v")
    # print(v_0)
    # print(len(v_0))

    if len(v_0) % 2 == 1:

        if y + len(v_0) > len(row) - 1:

            v_0.append('0')

        else:

            v_0.append(str(row[y + int(len(v_0) / 2) + 1]))

    else:

        if y - len(v_0) < -1:

            v_0.insert(0, '1')

        else:

            v_0.insert(0, str(row[int(y - len(v_0) / 2)]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer_1d(row, y, view, v_0)

        return v_0


def Color_cells_1d(d_rule, cell_row_width, row_0):

    # print("")
    # print("row_0")
    # print(row_0)

    row_1 = np.zeros((1, cell_row_width), dtype='int8')

    row_1[0] = [d_rule[tuple(viewer_1d(row_0, x, view, []))] for x in range(len(row_0))]

    return row_1


#####game#####

pygame.init()
pygame.display.init()

current_display = pygame.display.Info()
# WIDTH , HEIGHT = current_display.current_w - 50, current_display.current_h - 100
WIDTH, HEIGHT = 1600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
letter_values = {'q': 0, 'w': 1, 'e': 2, 'r': 3, 't': 4, 'y': 5, 'u': 6, 'i': 7, 'o': 8, 'p': 9, 'a': 10, 's': 11,
                 'd': 12, 'f': 13,
                 'g': 14, 'h': 15, 'j': 16, 'k': 17, 'l': 18, 'z': 19, 'x': 20, 'c': 21, 'v': 22, 'b': 23, 'n': 24,
                 'm': 25, ' ': 26}

pygame.display.set_caption("C.H.A.O.S")

click = False


def Chaos_Window(base, pixel_res, cell_vel, analytics, device_id=-1):

    print("base")
    print(base)
    print("device_id")
    print(device_id)
    p_m_i = 0


    # color_x_size = pixel_res
    # BLACK_PIXEL = pygame.image.load(os.path.join('assets', 'black-' + str(color_x_size) + '.png')).convert()
    # GREY_D_PIXEL = pygame.image.load(os.path.join('assets', 'dark-grey-' + str(color_x_size) + '.png')).convert()
    # GREY_L_PIXEL = pygame.image.load(os.path.join('assets', 'light-grey-' + str(color_x_size) + '.png')).convert()
    # CYAN_PIXEL = pygame.image.load(os.path.join('assets', 'cyan-' + str(color_x_size) + '.png')).convert()
    # MAGENTA_PIXEL = pygame.image.load(os.path.join('assets', 'magenta-' + str(color_x_size) + '.png')).convert()
    # YELLOW_PIXEL = pygame.image.load(os.path.join('assets', 'yellow-' + str(color_x_size) + '.png')).convert()
    # BLUE_PIXEL = pygame.image.load(os.path.join('assets', 'blue-' + str(color_x_size) + '.png')).convert()
    # RED_PIXEL = pygame.image.load(os.path.join('assets', 'red-' + str(color_x_size) + '.png')).convert()
    # GREEN_PIXEL = pygame.image.load(os.path.join('assets', 'green-' + str(color_x_size) + '.png')).convert()
    #
    # color_x_size = 20
    # BLACK_PIXEL_X = pygame.image.load(os.path.join('assets', 'black-' + str(color_x_size) + '.png')).convert()
    # GREY_D_PIXEL_X = pygame.image.load(os.path.join('assets', 'dark-grey-' + str(color_x_size) + '.png')).convert()
    # GREY_L_PIXEL_X = pygame.image.load(os.path.join('assets', 'light-grey-' + str(color_x_size) + '.png')).convert()
    # CYAN_PIXEL_X = pygame.image.load(os.path.join('assets', 'cyan-' + str(color_x_size) + '.png')).convert()
    # MAGENTA_PIXEL_X = pygame.image.load(os.path.join('assets', 'magenta-' + str(color_x_size) + '.png')).convert()
    # YELLOW_PIXEL_X = pygame.image.load(os.path.join('assets', 'yellow-' + str(color_x_size) + '.png')).convert()
    # BLUE_PIXEL_X = pygame.image.load(os.path.join('assets', 'blue-' + str(color_x_size) + '.png')).convert()
    # RED_PIXEL_X = pygame.image.load(os.path.join('assets', 'red-' + str(color_x_size) + '.png')).convert()
    # GREEN_PIXEL_X = pygame.image.load(os.path.join('assets', 'green-' + str(color_x_size) + '.png')).convert()
    #
    # class Pixel:
    #
    #     __slots__ = ['x', 'y', 'img']
    #
    #     def __init__(self, x, y):
    #         self.x = x
    #         self.y = y
    #         self.img = None
    #
    #     def draw(self, window):
    #         window.blit(self.img, (self.x, self.y))
    #
    #     def get_width(self):
    #         return self.img.get_width()
    #
    #     def get_height(self):
    #         return self.img.get_height()
    #
    # class Cell(Pixel):
    #
    #     COLOR_MAP = {
    #         "black": (BLACK_PIXEL),
    #         'light-grey': (GREY_L_PIXEL),
    #         'dark-grey': (GREY_D_PIXEL),
    #         'red': (RED_PIXEL),
    #         'yellow': (YELLOW_PIXEL),
    #         'green': (GREEN_PIXEL),
    #         'blue': (BLUE_PIXEL),
    #         'magenta': (MAGENTA_PIXEL),
    #         'cyan': (CYAN_PIXEL),
    #
    #         "black_x": (BLACK_PIXEL_X),
    #         'light-grey_x': (GREY_L_PIXEL_X),
    #         'dark-grey_x': (GREY_D_PIXEL_X),
    #         'yellow_x': (YELLOW_PIXEL_X),
    #         'cyan_x': (CYAN_PIXEL_X),
    #         'magenta_x': (MAGENTA_PIXEL_X),
    #         'blue_x': (BLUE_PIXEL_X),
    #         'red_x': (RED_PIXEL_X),
    #         'green_x': (GREEN_PIXEL_X),
    #
    #     }
    #     __slots__ = ['img', 'mask', 'y']
    #
    #     def __init__(self, x, y, color):
    #         super().__init__(x, y)
    #         self.img = self.COLOR_MAP[color]
    #         self.mask = pygame.mask.from_surface(self.img)
    #
    #     def move(self, vel):
    #         self.y += vel


    def redraw_window(input_box, v_input, zero_count, step_show, triggers, dt):

        mx, my = pygame.mouse.get_pos()

        #preparation
        zero_count = int(zero_count / cell_vel)

        triggers = [int(t / cell_vel) for t in triggers][0:base - 1]


        #colors
        if base < 5:

            bar_colors = [(0, 0, 0), (255, 0, 255), (0, 255, 255), (255, 255, 0), (192, 192, 192), (255, 0, 0),
                          (0, 255, 0), (0, 0, 255)]

        else:

            bar_colors = [(0, 0, 0), (32, 32, 32), (255, 0, 255), (0, 255, 255), (255, 255, 0), (192, 192, 192), (255, 0, 0), (0, 255, 0), (0, 0, 255)]


        # cell drawing
        [pygame.draw.rect(WIN, bar_colors[cells_a[cell]], cells_rect[cell]) for cell in cells_rect]


        gv_track = 0
        tracker = -1

        for cell in rule_models:

            pygame.draw.rect(WIN, bar_colors[i_rule[rule_models.index(cell)]], cell)

            #p1_move
            if cell.collidepoint((mx, my)):

                tracker = gv_track

                if click_l:

                    print('attack')

                    p1_move[0] = ('a', gv_track)

                if click_r and i_rule[gv_track] == 0:

                    print('defend')

                    p1_move[0] = ('d', gv_track)

                    # for x in range(bv):
                    #
                    #     shields[x] = 0

                    if shields[gv_track] < 2:
                        shields[gv_track] = 2

                    elif shields[gv_track] == 2:
                        shields[gv_track] = 0

                    print(shields)

            #pointer
            if gv_track == tracker:

                # print("gv_track % 4")
                # print(gv_track % 4)

                pygame.draw.circle(WIN, (0, 0, 0), (1 * ui_scale * (gv_track % 4) + x_offset + ui_scale / 2,
                                                    1 * ui_scale + y_offset + ui_scale / 2  + ui_scale * int(gv_track / 4)),
                                   ui_scale / 2)
                pygame.draw.circle(WIN, (255, 255, 255), (
                    1 * ui_scale * (gv_track % 4) + x_offset + ui_scale / 2,
                    1 * ui_scale + y_offset + ui_scale / 2  + ui_scale * int(gv_track / 4)), ui_scale / 2 - 1)

            #shields
            for x in range(bv):

                if shields[x] == 2:

                    pygame.draw.circle(WIN, (0, 0, 0), (1 * ui_scale * (x % 4) + x_offset + ui_scale / 2,
                                                        1 * ui_scale + y_offset + ui_scale / 2 + ui_scale * int(
                                                            x / 4)),
                                       ui_scale / 2)
                    pygame.draw.circle(WIN, (0, 255, 255), (
                        1 * ui_scale * (x % 4) + x_offset + ui_scale / 2,
                        1 * ui_scale + y_offset + ui_scale / 2 + ui_scale * int(x / 4)), ui_scale / 2 - 1)

                if shields[x] == 1:

                    pygame.draw.circle(WIN, (0, 0, 0), (1 * ui_scale * (x % 4) + x_offset + ui_scale / 2,
                                                        1 * ui_scale + y_offset + ui_scale / 2 + ui_scale * int(
                                                            x / 4)),
                                       ui_scale / 2)
                    pygame.draw.circle(WIN, (255, 255, 0), (
                        1 * ui_scale * (x % 4) + x_offset + ui_scale / 2,
                        1 * ui_scale + y_offset + ui_scale / 2 + ui_scale * int(x / 4)), ui_scale / 2 - 1)



            gv_track += 1

        [pygame.draw.rect(WIN, bar_colors[int(list(d_rule.keys())[tracker][x])], precursor[x]) for x in range(view)]

        # draw_text('Rule: ' + str(decimal(i_rule, base)), main_font, (255, 255, 255), WIN, CELL_WIDTH + 38, 10)
        # draw_text('RC: ' + str(list(rc_count.values())[:4]), main_font, (255, 255, 255), WIN, CELL_WIDTH + 235, 85)
        # draw_text('RC: ' + str(list(rc_count.values())[4:]), main_font, (255, 255, 255), WIN, CELL_WIDTH + 235, 130)
        # draw_text('P1: ' + str(int(p1_score / cell_row_width)) + ' P2: ' + str(int(p2_score / cell_row_width)), main_font, (255, 255, 255), WIN, CELL_WIDTH + 235, 180)

        # for x in d_label[0]:
        #
        #     draw_text(str(x), main_font, (255, 255, 255), WIN, CELL_WIDTH + 80 + 90 * d_label[0].index(x), 330)
        #
        # for y in d_label[1]:
        #
        #     draw_text(str(y), main_font, (255, 255, 255), WIN, CELL_WIDTH + 10, 380 + 40 * d_label[1].index(y))
        #
        # for x in range(len(theory_board[:, 0, 0])):
        #
        #     draw_text(str(theory_board.tolist()[x]), main_font, (255, 255, 255), WIN, CELL_WIDTH + 30, 380 + 40 * x)

        # print('tsp-redraw')
        # print(ts_percentage)
        # print(len(ts_percentage))

        # print("triggers-redraw")
        # print(triggers)
        # print(len(triggers))

        bar_colors = bar_colors[1:]

        [pygame.draw.rect(WIN, bar_colors[x], pygame.Rect(x_offset + (bar_width * x) * 2, (y_offset + y_offset/2 - bar_height * triggers[x] / zero_out * 4) + bar_height/2 - 60, bar_width, bar_height * triggers[x] / zero_out * 4)) for x in range(len(ts_percentage) - 1)]


        #vanilla labels
        rule_label_0_b = main_font.render(f"RUL3: {i_rule[0:int((base ** view) / 2)]}", 1, (255, 255, 255))
        rule_label_1_b = main_font.render(f"          {i_rule[int((base ** view) / 2):int((base ** view))]}", 1,
                                          (255, 255, 255))

        step_label_b = main_font.render(f"5T3P: {step}", 1, (255, 255, 255))
        rand_count_l = main_font.render(f"C0UNT: {rand_count}", 1, (255, 255, 255))


        #glove labels
        zero_count = main_font.render(f"ZERO: {zero_count}", 1, (255, 255, 255))
        origin_value = main_font.render(f"ORIGIN: {origin_threshold}", 1, (255, 255, 255))

        trigger_values = main_font.render(f"TRIGGERS: {triggers}", 1, (255, 255, 255))
        tsp_values = main_font.render(f"PERCENTAGE: {ts_percentage}", 1, (255, 255, 255))
        trigger_thresholds = main_font.render(f"THRESHOLD: {thresholds}", 1, (255, 255, 255))
        tsp_view = main_font.render(f"PORTION: {tsp_portion}", 1, (255, 255, 255))

        gv = main_font.render(f"GV: {glove_value}", 1, (255, 255, 255))


        #vanilla blit
        if step_show == 1:

            WIN.blit(rule_label_0_b, (10, HEIGHT - 120))
            WIN.blit(rule_label_1_b, (7, HEIGHT - 80))

        WIN.blit(step_label_b, (WIDTH - step_label_b.get_width(), 10))
        # WIN.blit(rand_count_l, (WIDTH - rand_count_l.get_width(), 50))

        # WIN.blit(zero_count, (WIDTH - zero_count.get_width(), 90))
        # WIN.blit(origin_value, (WIDTH - origin_value.get_width(), 90))


        #glove blit
        # WIN.blit(trigger_thresholds, (WIDTH - trigger_thresholds.get_width(), HEIGHT - 50))
        # WIN.blit(trigger_values, (WIDTH - trigger_values.get_width(), HEIGHT - 100))
        # WIN.blit(tsp_values, (CELL_WIDTH + 120, 170))
        # WIN.blit(tsp_view, (CELL_WIDTH + 120, 135))

        # WIN.blit(gv, (WIDTH - gv.get_width(), 90))


        #conosle inputs
        if input_box == 1:
            v_input_r = small_font.render(v_input, 1, (0, 0, 0))

            type_box = pygame.Rect(10, 10, v_input_r.get_width() + 2, v_input_r.get_height() + 2)

            pygame.draw.rect(WIN, (255, 255, 255), type_box)

            WIN.blit(v_input_r, (11, 11))

        if list_count != 0:
            draw_text(str(list_count), small_font, (255, 255, 255), WIN, 11, 33)

        draw_text(str(dt), small_font, (255, 255, 255), WIN, WIDTH - 40, 50)

        pygame.display.update()

    # def mitosis(i, r, color, row, pixel_res):
    #
    #     if r > 0:
    #
    #         if base < 5:
    #
    #             if row[0, i] == 0:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'black')
    #             if row[0, i] == 1:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'magenta')
    #             if row[0, i] == 2:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'cyan')
    #             if row[0, i] == 3:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'yellow')
    #
    #         else:
    #
    #             if row[0, i] == 0:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'black')
    #             if row[0, i] == 1:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'dark-grey')
    #             if row[0, i] == 2:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'magenta')
    #             if row[0, i] == 3:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'cyan')
    #             if row[0, i] == 4:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'yellow')
    #             if row[0, i] == 5:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'light-grey')
    #             if row[0, i] == 6:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'red')
    #             if row[0, i] == 7:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'green')
    #             if row[0, i] == 8:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'blue')
    #
    #         # if base == 2:
    #         #
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_2')
    #         #             cells[r].append(cell)
    #         #     if pixel_res == 3:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_3')
    #         #             cells[r].append(cell)
    #         #     if pixel_res == 5:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_5')
    #         #             cells[r].append(cell)
    #         #     if pixel_res == 10:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_10')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 3:
    #         #
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_2')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 3:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_3')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 5:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_5')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 10:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_10')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 4:
    #         #
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'yellow_2')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 3:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'yellow_3')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 5:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'yellow_5')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 10:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'yellow_10')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 5:
    #         #
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'dark-grey_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 4:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'yellow_2')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 6:
    #         #
    #         #     if pixel_res == 2:
    #         #
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'dark-grey_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 4:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'yellow_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 5:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'light-grey_2')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 9:
    #         #
    #         #     if pixel_res == 2:
    #         #
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'black_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'dark-grey_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'magenta_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'cyan_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 4:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'yellow_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 5:
    #         #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                             'light-grey_' + str(pixel_res))
    #         #                 cells[r].append(cell)
    #         #         if row[0, i] == 6:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'red_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 7:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'green_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 8:
    #         #             cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #         #                         'blue_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #
    #     else:
    #
    #         if base < 5:
    #
    #             if row[0, i] == 0:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black')
    #             if row[0, i] == 1:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'magenta')
    #             if row[0, i] == 2:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'cyan')
    #             if row[0, i] == 3:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow')
    #
    #         else:
    #
    #             if row[0, i] == 0:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black')
    #             if row[0, i] == 1:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'dark-grey')
    #             if row[0, i] == 2:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'magenta')
    #             if row[0, i] == 3:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'cyan')
    #             if row[0, i] == 4:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow')
    #             if row[0, i] == 5:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'light-grey')
    #             if row[0, i] == 6:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'red')
    #             if row[0, i] == 7:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'green')
    #             if row[0, i] == 8:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'blue')
    #
    #
    #
    #         # if base == 2:
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, 0, 'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, 0, 'cyan_2')
    #         #             cells[r].append(cell)
    #         #     if pixel_res == 3:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, 0, 'black_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, 0, 'blue_3')
    #         #             cells[r].append(cell)
    #         #     if pixel_res == 5:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, 0, 'black_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, 0, 'blue_5')
    #         #             cells[r].append(cell)
    #         #     if pixel_res == 10:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, 0, 'black_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, 0, 'blue_10')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 3:
    #         #
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'purple_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'green_2')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 3:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'black_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'purple_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'green_3')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 5:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'black_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'purple_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'green_5')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 10:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'black_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'purple_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + 2, 'green_10')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 4:
    #         #
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'purple_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'green_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow_2')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 3:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'purple_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'green_3')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow_3')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 5:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'purple_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'green_5')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow_5')
    #         #             cells[r].append(cell)
    #         #
    #         #     if pixel_res == 10:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'purple_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'green_10')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow_10')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 5:
    #         #
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'white_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'green_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 4:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'purple_2')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 6:
    #         #
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'dark-grey_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'magenta_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'cyan_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 4:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow_2')
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 5:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'light-grey_2')
    #         #             cells[r].append(cell)
    #         #
    #         # elif base == 9:
    #         #
    #         #     if pixel_res == 2:
    #         #         if row[0, i] == 0:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 1:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'dark-grey_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 2:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'magenta_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 3:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'cyan_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 4:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 5:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'light-grey_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 6:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'red_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 7:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'green_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #         #         if row[0, i] == 8:
    #         #             cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'blue_' + str(pixel_res))
    #         #             cells[r].append(cell)
    #
    #     return cell
    #
    # def mitosis_cell_list(i, r, color, row, pixel_res):
    #
    #     if r > 0:
    #
    #         if base < 5:
    #
    #             if row[0, i] == 0:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'black')
    #                 cells[r].append(cell)
    #             if row[0, i] == 1:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'magenta')
    #                 cells[r].append(cell)
    #             if row[0, i] == 2:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'cyan')
    #                 cells[r].append(cell)
    #             if row[0, i] == 3:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'yellow')
    #                 cells[r].append(cell)
    #
    #         else:
    #
    #             if row[0, i] == 0:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'black')
    #                 cells[r].append(cell)
    #             if row[0, i] == 1:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'dark-grey')
    #                 cells[r].append(cell)
    #             if row[0, i] == 2:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'magenta')
    #                 cells[r].append(cell)
    #             if row[0, i] == 3:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'cyan')
    #                 cells[r].append(cell)
    #             if row[0, i] == 4:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'yellow')
    #                 cells[r].append(cell)
    #             if row[0, i] == 5:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'light-grey')
    #                 cells[r].append(cell)
    #             if row[0, i] == 6:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'red')
    #                 cells[r].append(cell)
    #             if row[0, i] == 7:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'green')
    #                 cells[r].append(cell)
    #             if row[0, i] == 8:
    #                 cell = Cell(1 * pixel_res * i, cells[r - 1][i].y - pixel_res,
    #                             'blue')
    #                 cells[r].append(cell)
    #
    #     else:
    #
    #         if base < 5:
    #
    #             if row[0, i] == 0:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black')
    #                 cells[r].append(cell)
    #             if row[0, i] == 1:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'magenta')
    #                 cells[r].append(cell)
    #             if row[0, i] == 2:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'cyan')
    #                 cells[r].append(cell)
    #             if row[0, i] == 3:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow')
    #                 cells[r].append(cell)
    #
    #         else:
    #
    #             if row[0, i] == 0:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'black')
    #                 cells[r].append(cell)
    #             if row[0, i] == 1:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'dark-grey')
    #                 cells[r].append(cell)
    #             if row[0, i] == 2:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'magenta')
    #                 cells[r].append(cell)
    #             if row[0, i] == 3:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'cyan')
    #                 cells[r].append(cell)
    #             if row[0, i] == 4:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'yellow')
    #                 cells[r].append(cell)
    #             if row[0, i] == 5:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'light-grey')
    #                 cells[r].append(cell)
    #             if row[0, i] == 6:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'red')
    #                 cells[r].append(cell)
    #             if row[0, i] == 7:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'green')
    #                 cells[r].append(cell)
    #             if row[0, i] == 8:
    #                 cell = Cell(1 * pixel_res * i, - pixel_res + cell_vel, 'blue')
    #                 cells[r].append(cell)

    def input(letter, base, page, input_box, v_input):

        if echoing == 1:

            echo = 0

        echo = 1

        if input_box == 1:
            v_input += letter

        bv = base ** view

        if letter not in press:
            press[letter] = 0
        else:
            press[letter] += 1

        if echoing == 1:

            if press[letter] % 1 ==0:

                echo = 1


        place = int((letter_values[letter] + ((press[letter] % (int(bv / len(letter_values)) + 1)) * int(
            (bv / int(bv / len(letter_values) + 1))))) % bv)

        # print(' ')
        # print("place")
        # print(place)
        # print(letter_values[letter])
        # print((press[letter] % (int(bv / len(letter_values)) + 1)))
        # print((bv / int(bv / len(letter_values) + 1)))
        # print(bv)

        if i_rule[place] == 0:

            i_rule[place] = 1
            d_rule[list(d_rule.keys())[place]] = 1

            if echo % 2 == 0:

                # print('len(i_rule)')
                # print(len(i_rule))
                # print('int(place + len(i_rule)/2 % len(i_rule)) - 1')
                # print(int((place + len(i_rule)/2) % len(i_rule)) - 1)
                # print('list(d_rule.keys()))')
                # print(len(list(d_rule.keys())))

                i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 1
                d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 1

        elif i_rule[place] == 1:

            # print("i_rule_1")
            # print(i_rule)

            if base == 2:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 2
                d_rule[list(d_rule.keys())[place]] = 2

            if echo % 2 == 0:

                # print('echo')

                if base == 2:

                    # print('len(i_rule)')
                    # print(len(i_rule))
                    # print('int(place + len(i_rule)/2 % len(i_rule)) - 1')
                    # print(int(place + len(i_rule)/2 % len(i_rule)) - 1)
                    # print('list(d_rule.keys()))')
                    # print(len(list(d_rule.keys())))

                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0

                else:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 2
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 2

                # print("i_rule_2")
                # print(i_rule)

        elif i_rule[place] == 2:

            if base == 3:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 3
                d_rule[list(d_rule.keys())[place]] = 3

            if echo % 2 == 0:

                # print('echo')

                if base == 3:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0

                else:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 3
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 3

        elif i_rule[place] == 3:

            if base == 4:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 4
                d_rule[list(d_rule.keys())[place]] = 4

            if echo % 2 == 0:

                # print('echo')

                if base == 4:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0

                else:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 4
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 4

        elif i_rule[place] == 4:

            if base == 5:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 5
                d_rule[list(d_rule.keys())[place]] = 5

            if echo % 2 == 0:

                # print('echo')

                if base == 5:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0

                else:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 5
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 5

        else:

            i_rule[place] = 0
            d_rule[list(d_rule.keys())[place]] = 0

            if echo % 2 == 0:

                print('echo')

                i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0


        if rule not in journal:
            journal[rule] = []
            journal[rule].append(page)

        else:
            journal[rule].append(page)

        return v_input

    def fibonacci(a, duration, list, calls=1, b=0):

        if b == 0:
            b = a

            list.append(a)
            list.append(b)

        c = a + b

        for x in range(calls):
            list.append(c)

        if duration != 0:
            duration -= 1

            fibonacci(c, duration, list, calls, a)

    def rl_gen(input_list):

        if input_list[0] == 'm':

            input_list = input_list[1:]

            if len(input_list) == 2:

                rule_list = [x * int(input_list[1]) for x in range(int(input_list[0]))]

            elif len(input_list) == 4:

                # print(" ")
                # print("input_list")
                # print(input_list)

                rule_list = [x * int(input_list[3]) for x in
                             range(int(input_list[0]), int(input_list[1]), int(input_list[2]))]

                # print(" ")
                # print("len() 4")
                # print(rule_list)

            elif len(input_list) == 5:

                rule_list = []

                rule_list_0 = [x * int(input_list[3]) for x in
                               range(int(input_list[0]), int(input_list[1]), int(input_list[2]))]

                for rule in rule_list_0:

                    for x in range(int(input_list[4])):
                        rule_list.append(rule)

                # print(rule_list)

            list_count = len(rule_list)

        elif input_list[0] == 'fib':

            input_list = input_list[1:]

            rule_list = []

            if len(input_list) == 1:

                fibonacci(1, int(input_list[0]), rule_list)

            elif len(input_list) == 2:

                fibonacci(1, int(input_list[0]), rule_list, int(input_list[1]))

            elif len(input_list) == 3:

                fibonacci(int(input_list[2]), int(input_list[0]), rule_list, int(input_list[1]))

            # print(" ")
            # print("rule_list")
            # print(rule_list)

            list_count = len(rule_list)

        elif input_list[0] == 'sqr':

            # print(" ")
            # print("sqr")

            input_list = input_list[1:]

            if len(input_list) == 2:
                rule_list = [x ** int(input_list[1]) for x in range(int(input_list[0]))]

                # print('rule_list')
                # print(rule_list)

            list_count = len(rule_list)

        elif input_list[0] == 'exp':

            # print(" ")
            # print("sqr")

            input_list = input_list[1:]

            rule_list = []

            if len(input_list) == 2:

                # print("")
                # print("exp len 2")
                # print(input_list)

                rule_list_0 = [x ** x for x in range(int(input_list[0]))]

                # print("rule_list_0")
                # print(rule_list_0)

                for rule in rule_list_0:

                    # print("rule")
                    # print(rule)
                    #
                    # print(input_list[1])

                    for x in range(int(input_list[1])):
                        rule_list.append(rule)

                # print('rule_list')
                # print(rule_list)

            list_count = len(rule_list)

        return rule_list, list_count

    def place_change(place):

        # print("place_change")
        # print(place)

        place = place % (base ** view)

        if i_rule[place] == 0:

            i_rule[place] = 1
            d_rule[list(d_rule.keys())[place]] = 1

        elif i_rule[place] == 1:

            # print("i_rule_1")
            # print(i_rule)

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

        elif i_rule[place] == 3:

            if base == 4:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 4
                d_rule[list(d_rule.keys())[place]] = 4

        elif i_rule[place] == 4:

            if base == 5:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 5
                d_rule[list(d_rule.keys())[place]] = 5

        else:

            i_rule[place] = 0
            d_rule[list(d_rule.keys())[place]] = 0


    #active variables
    run = 1
    FPS = 10
    rule = 21621
    ai = 2
    d_rule, i_rule = rule_gen(rule, base)
    start = 0
    step = 0
    step_show = 0
    clock = pygame.time.Clock()
    origin_rule = 0
    bv = base ** view

    if base < 5:
        cell_colors = {0:'black_x', 1:'magenta_x', 2:'cyan_x', 3:'yellow_x'}

    else:
        cell_colors = {0:'black_x', 1:'dark_grey_x', 2:'magenta_x', 3:'cyan_x', 4:'yellow_x', 5:'light_grey_x', 6:'red_x', 7:'green_x', 8:'blue_x'}

    #window
    if analytics == 1:

        CELL_WIDTH = HEIGHT

    else:

        CELL_WIDTH = WIDTH

    #chess
    p1_score = 0
    p2_score = 0

    p1_history = []
    p2_history = []

    ad = {0: 'a', 1: 'd', 2: 'a', 3: 'd', 4: 'a', 5: 'd'}
    rv = 0

    move_down = 0
    move_up = 0

    click_l = False
    click_r = False

    rc_count = {}
    for k in d_rule:

        rc_count[k] = 0

    shields = {}
    pc_count = {}
    stagnation = {}

    for x in range(bv):

        shields[x] = 0
        pc_count[x] = 0
        stagnation[x] = 0

    if ai == 1:

        last_move = -1

        #agression
        agression = 0
        momentum = 0
        attack = []
        defend = []
        committed = []
        stance = 0

        #popularity
        cool_kids = []
        cool_score = 0

        #age
        age = 999999999999999999999999999999999999999999999999999999999999999
        fresh = []

    p1_move = ('a', 0)
    p2_move = ('a', 0)

    print("")
    print("rc_count")
    print(rc_count)

    theory_board = np.zeros((base ** view, base ** view, 2), dtype='uint8')

    print("###theory_board###")
    print(theory_board)

    dominant_x = []
    dominant_y = []
    d_label = ([], [])


    #input augments
    echoing = 0
    randomizer = 0
    midi_inputs = 1

    #glove emthods
    characters_g = 0
    words_g = 2
    rules_g = 0
    digits = 1

    #glove value scales
    tplus_scale = 2
    tminus_scale = 16

    #record keeping
    journal = dict()
    page = []
    press = dict()
    press_vault = dict()

    # infile = open("cell-journal", "rb")
    # journal = pickle.load(infile)
    # infile.close

    #random
    r_c = 0
    r_i = 0
    rand_count = 0
    iterate = 0

    #glove activations
    zero_out = int(cell_vel * 4000 / pixel_res)
    zero_count = int(cell_vel * 4000 / pixel_res)
    origin_threshold = 50
    over_flow = 0

    rule_pause = 128
    gvp_threshold = 128
    gv_pause = 0

    t0_threshold = 128
    t1_threshold = 80
    t2_threshold = 80
    t3_threshold = 80
    t4_threshold = 80
    t5_threshold = 40
    t6_threshold = 40
    t7_threshold = 40
    t8_threshold = 40
    thresholds = [t0_threshold, t1_threshold, t2_threshold, t3_threshold, t4_threshold, t5_threshold, t6_threshold, t7_threshold, t8_threshold]

    trigger_0 = 0
    trigger_1 = 0
    trigger_2 = 0
    trigger_3 = 0
    trigger_4 = 0
    trigger_5 = 0
    trigger_6 = 0
    trigger_7 = 0
    trigger_8 = 0

    triggers = []
    ts_percentage = []
    tsp_portion = []
    placed = []
    glove_value = 0
    rule_window_scale = 4

    #chaos console
    input_box = 0
    list_count = 0
    v_input = ''
    write = 0
    j_name = ''
    max_rule = base ** base ** view

    #cell design

    cell_row_width = int(CELL_WIDTH / pixel_res)
    cell_rows = int(HEIGHT / pixel_res)

    print("")
    print('cells: width height')
    print((cell_row_width, cell_rows))

    cells_a = np.zeros((cell_rows, cell_row_width), dtype='int8')

    if start == 0:

        cells_a[0, int(cell_row_width / 2)] = 1

    else:

        cells_a[0] = rule_gen_2(start, base, cell_row_width)[1]

    # print("")
    # print(cells_a)

    for x in range(cell_rows - 1):

        cells_a = np.roll(cells_a, 1, 0)
        cells_a[0] = Color_cells_1d(d_rule, cell_row_width, cells_a[1])

    print("")
    print(cells_a)


    #cells_rect init
    cells_rect = dict()
    for x in range(cell_row_width):

        for y in range(cell_rows):

            cell = pygame.Rect(x * pixel_res, y * pixel_res, pixel_res, pixel_res)

            cells_rect[(y, x)] = cell


    #ui
    ui_on = 1
    ui_scale = 40

    rule_models = []
    precursor = []
    gv_mark = ()
    clunk = 0

    ir_height = base
    bar_height = 800
    bar_width = 20

    x_offset = CELL_WIDTH + 40
    y_offset = 50


    if midi_inputs == 1:

        pygame.init()
        pygame.midi.init()
        pygame.fastevent.init()
        event_get = pygame.fastevent.get
        event_post = pygame.fastevent.post

        #rtmidi init
        if device_id >= 0:

            print(" ")
            print("device info")
            _print_device_info()

            input_id = device_id
            print("input_id")
            print(input_id)

            print(' ')
            print("using input_id :%s:" % input_id)
            pygame.midi.get_device_info(input_id)
            p_m_i = pygame.midi.Input(device_id)

        ev_1 = 0
        ev_2 = 0
        ev_3 = 0
        ev_4 = 0
        ev_5 = 0
        ev_6 = 0
        ev_7 = 0
        ev_8 = 0
        ev_9 = 0
        ev_10 = 0
        ev_11 = 0

        if device_id > 0:

            if midi_inputs == 1:

                if p_m_i.poll():

                    # print(' ')
                    # print('i')
                    # print(i)

                    midi_events = p_m_i.read(999)
                    midi_evs = pygame.midi.midis2events(midi_events, p_m_i.device_id)

                    for m_e in midi_evs:
                        event_post(m_e)

    if origin_rule == 0:

        magnify = 4
        colors = 1
        step_size = int(base ** view / (base - 1) / magnify)

        # print("")
        # print("step_size")
        # print(step_size)
        # print(base ** view)
        # print(base - 1)

        o_r = rule_gen(0, base)[1]

        # print(o_r)

        for x in range(int((base ** view) / step_size) + 1):

            # print("step_size * x")
            # print(step_size * x)
            # print("current place")
            # print(-((step_size * x + 1) % bv))

            if x > 0:

                o_r[-((step_size * x + 1) % bv)] = x % colors + 1

            else:

                o_r[-((step_size * x + 1) % bv)] = 1


        o_r[-1] = 1

        origin_rule = decimal(o_r, base)

        print("")
        print("origin rule")
        print(o_r)
        print(origin_rule)

    if ui_on == 1:

        clunk = 0
        rule_models = []
        precursor = []

        ir_split = []

        [ir_split.append(i_rule[x * int(len(i_rule) / ir_height):(x + 1) * int(len(i_rule) / ir_height)]) for x in
         range(ir_height)]

        # x_offset = CELL_WIDTH + 40
        # y_offset = 20 + ui_scale + y

        [[rule_models.append(
            pygame.Rect(1 * ui_scale * x + x_offset, 1 * ui_scale + y_offset + ui_scale * y, ui_scale - 1, ui_scale - 1)) for x in
          range(len(ir_split[y]))] for y in range(ir_height)]

        # x_offset = CELL_WIDTH + 40
        # y_offset = 20 + ui_scale * (ir_height + 1)

        [precursor.append(
            pygame.Rect(1 * ui_scale * x + x_offset, 1 * ui_scale + y_offset + ui_scale * (ir_height + 1), ui_scale - 1,
                        ui_scale - 1)) for x in range(view)]

        # print("")
        # print("rule_models")
        # print(len(rule_models))
        # print(rule_models)

    print(" ")
    print("d_rule")
    print(d_rule)
    print("i_rule")
    print(i_rule)
    print(len(i_rule))


    #main loop
    while run == 1:

        # print("")
        # print("running")

        WIN.fill((32, 32, 32))
        dt = clock.tick(FPS)
        redraw_window(input_box, v_input, zero_count, step_show, triggers, dt)
        click_l = False
        click_r = False
        move_down = 1

        #mitosis
        if move_down > 0:

            # print("")
            # print("last move")
            # print(last_move)
            # print("rc_count")
            # print(rc_count)
            #
            # print("")
            # print("optimal")
            # print(optimal)
            # print(optimals)
            #
            # print("")
            # print("agression")
            # print(agression)
            # print(momentum)
            # print('aggravated')
            # print(attack)
            # print(defend)
            # print(committed)
            #
            # print("")
            # print("popularity")
            # print(pc_count)
            # print('popular')
            # print(cool_score)
            # print(cool_kids)
            #
            # print("")
            # print("age")
            # print(stagnation)
            # print(age)
            # print(fresh)

            # print("shields")
            # print(shields)
            #
            # print("")
            # print('p1_move')
            # print(p1_move)
            # print("p2_move")
            # print(p2_move)

            last_move = p2_move[-1]

            p1_history.append(p1_move[0])
            p2_history.append(p2_move)

            pc_count[p1_move[-1]] += 1
            pc_count[p2_move[-1]] += 1

            stagnation[p1_move[-1]] = 0
            stagnation[p2_move[-1]] = 0

            if p2_move[0] == 'd':

                shields[p2_move[-1]] = 2

            if p1_move[0] == 'a':

                if shields[p1_move[-1]] == 0 and i_rule[p1_move[-1]] == 1:

                    place_change(p1_move[-1])

                else:

                    shields[p1_move[-1]] = 0

            if p2_move[0] == 'a':

                if shields[p2_move[-1]] == 0:

                    place_change(p2_move[-1])

                else:

                    shields[p2_move[-1]] = 0

            for x in range(cell_vel):

                cells_a = np.roll(cells_a, 1, 0)
                cells_a[0] = Color_cells_1d(d_rule, cell_row_width, cells_a[1])
                line = tuple(cells_a[0])

            # score
            for x in line:
                if x == 0:
                    p1_score += 1
                else:
                    p2_score += 1

            if line in page:

                if r_i == 0 and list_count == 0:

                    rand_count += 1

                    # print("duplicate")

                    rand = random.randrange(0, base ** view - 1)

                else:
                    iterate += 1

                # print(" ")
                # print("rand")
                # print(rand)

                # print(rand)
                # print(i_rule)
                # print(d_rule)

                # print(" ")
                # print("rule")
                # print(rule)

                if rule not in journal:
                    journal[rule] = []
                    journal[rule].append(page)

                else:
                    journal[rule].append(page)

                page = []

                if randomizer == 1:

                    if list_count == 0:

                        # print("list_count == 0:")
                        # print("randomizer")

                        if base == 2:
                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                        if base == 3:
                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 2
                                d_rule[list(d_rule.keys())[rand]] = 2
                            elif i_rule[rand] == 2:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                        if base == 4:

                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 2
                                d_rule[list(d_rule.keys())[rand]] = 2
                            elif i_rule[rand] == 2:
                                i_rule[rand] = 3
                                d_rule[list(d_rule.keys())[rand]] = 3
                            elif i_rule[rand] == 3:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                        if base == 5:

                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 2
                                d_rule[list(d_rule.keys())[rand]] = 2
                            elif i_rule[rand] == 2:
                                i_rule[rand] = 3
                                d_rule[list(d_rule.keys())[rand]] = 3
                            elif i_rule[rand] == 3:
                                i_rule[rand] = 4
                                d_rule[list(d_rule.keys())[rand]] = 4
                            elif i_rule[rand] == 4:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                        if base == 6:

                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 2
                                d_rule[list(d_rule.keys())[rand]] = 2
                            elif i_rule[rand] == 2:
                                i_rule[rand] = 3
                                d_rule[list(d_rule.keys())[rand]] = 3
                            elif i_rule[rand] == 3:
                                i_rule[rand] = 4
                                d_rule[list(d_rule.keys())[rand]] = 4
                            elif i_rule[rand] == 4:
                                i_rule[rand] = 5
                                d_rule[list(d_rule.keys())[rand]] = 5
                            elif i_rule[rand] == 5:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                # print("change")
                # print(i_rule)
                # print(d_rule)

            else:
                page.append(line)

            step += 1
            move_down -= 1

            momentum = 0
            for i in i_rule:

                if i == 1:
                    momentum += 1

            if momentum < 4:
                agression = 1

            if momentum > 4:
                agression = 0


            # print("history")
            # print(p1_history)
            # print(p2_history)

            for x in range(bv):

                stagnation[x] += 1

                if shields[x] > 0:
                    shields[x] -= 1

            # last_move = p2_move
            # pc_count[p1_move[0]] = 0
            # pc_count[p2_move] = 0

        if move_up > 0:

            p1_history = p1_history[:-1]
            p2_history = p2_history[:-1]

            cells_a = np.roll(cells_a, -1, 0)

            # score
            for x in cells_a[-1]:
                if x == 0:
                    p1_score -= 1
                else:
                    p2_score -= 1

            cells_a[-1] = 0
            line = tuple(cells_a[0])

            # #pixel class cells
            # [cells_pixel.append(Cell(x * pixel_res, -pixel_res, cell_colors[line[x]])) for x in range(cell_row_width)]

            if line in page:

                if r_i == 0 and list_count == 0:

                    rand_count += 1

                    # print("duplicate")

                    rand = random.randrange(0, base ** view - 1)

                else:
                    iterate += 1

                # print(" ")
                # print("rand")
                # print(rand)

                # print(rand)
                # print(i_rule)
                # print(d_rule)

                # print(" ")
                # print("rule")
                # print(rule)

                if rule not in journal:
                    journal[rule] = []
                    journal[rule].append(page)

                else:
                    journal[rule].append(page)

                page = []

                if randomizer == 1:

                    if list_count == 0:

                        # print("list_count == 0:")
                        # print("randomizer")

                        if base == 2:
                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                        if base == 3:
                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 2
                                d_rule[list(d_rule.keys())[rand]] = 2
                            elif i_rule[rand] == 2:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                        if base == 4:

                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 2
                                d_rule[list(d_rule.keys())[rand]] = 2
                            elif i_rule[rand] == 2:
                                i_rule[rand] = 3
                                d_rule[list(d_rule.keys())[rand]] = 3
                            elif i_rule[rand] == 3:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                        if base == 5:

                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 2
                                d_rule[list(d_rule.keys())[rand]] = 2
                            elif i_rule[rand] == 2:
                                i_rule[rand] = 3
                                d_rule[list(d_rule.keys())[rand]] = 3
                            elif i_rule[rand] == 3:
                                i_rule[rand] = 4
                                d_rule[list(d_rule.keys())[rand]] = 4
                            elif i_rule[rand] == 4:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                        if base == 6:

                            if i_rule[rand] == 0:
                                i_rule[rand] = 1
                                d_rule[list(d_rule.keys())[rand]] = 1
                            elif i_rule[rand] == 1:
                                i_rule[rand] = 2
                                d_rule[list(d_rule.keys())[rand]] = 2
                            elif i_rule[rand] == 2:
                                i_rule[rand] = 3
                                d_rule[list(d_rule.keys())[rand]] = 3
                            elif i_rule[rand] == 3:
                                i_rule[rand] = 4
                                d_rule[list(d_rule.keys())[rand]] = 4
                            elif i_rule[rand] == 4:
                                i_rule[rand] = 5
                                d_rule[list(d_rule.keys())[rand]] = 5
                            elif i_rule[rand] == 5:
                                i_rule[rand] = 0
                                d_rule[list(d_rule.keys())[rand]] = 0

                # print("change")
                # print(i_rule)
                # print(d_rule)

            else:
                page.append(line)

            step += 1
            move_up -= 1

            for x in range(bv):

                pc_count[x] -= 1

        #chess
        row_a = cells_a[0]

        ##stats


        for k in d_rule:
            rc_count[k] = 0

        for x in range(len(row_a)):

            v_0 = tuple(viewer_1d(row_a, x, view, []))

            rc_count[v_0] += 1

        #base scores
        p1_bs = 0
        p2_bs = 0

        # print("")
        # print(i_rule)
        # print(list(rc_count.values()))

        for x in range(len(i_rule)):
            if i_rule[x] == 0:
                p1_bs += list(rc_count.values())[x]
            else:
                p2_bs += list(rc_count.values())[x]

        theory_board = np.zeros((base ** view, base**view, 2), dtype='uint8')

        for x in range(base ** view):

            for y in range(base ** view):

                #theory scores
                p1_ts = p1_bs
                p2_ts = p2_bs

                if i_rule[-(x + 1)] == 1:

                    p1_ts += list(rc_count.values())[-(x + 1)]
                    p2_ts -= list(rc_count.values())[-(x + 1)]

                if i_rule[-(y + 1)] == 0:

                    p1_ts -= list(rc_count.values())[-(y + 1)]
                    p2_ts += list(rc_count.values())[-(y + 1)]

                if x == y:

                    p1_ts = p1_bs
                    p2_ts = p2_bs

                # print('')
                # print("theory score")
                # print((x - 1, y -1))
                # print(p1_ts)
                # print(p2_ts)
                # print(theory_board)

                theory_board[y, x, 0] = p1_ts
                theory_board[y, x, 1] = p2_ts


        # print("")
        # print('rc_count')
        # print(list(rc_count.values()))
        #
        # print("base score")
        # print(p1_bs)
        # print(p2_bs)
        #
        # print("theory_board")
        # print(theory_board)

        def IEDS(theory_board, s_w, d_label=(), simple=0, label=0):

            # print("")
            # print("IEDS")
            # print(theory_board)

            dominant_x = []
            eliminate_x = []

            dominant_y = []
            eliminate_y = []

            for x in range(len(theory_board[0, :, 0])):

                for y in range(len(theory_board[0, :, 0])):

                    # print("")
                    # print("x, y")
                    # print((x, y))

                    if s_w == 's':

                        status = []

                        # print("")

                        for z in range(base ** view):

                            # print("z")
                            # print(theory_board[z + 1, x + 1, 0], theory_board[z + 1, y + 1, 0])

                            if theory_board[z + 1, x + 1, 0] > theory_board[z + 1, y + 1, 0]:

                                # print('greater')

                                status.append('g')


                        # print('status')

                        if len(status) == base ** view:

                            if y not in eliminate_x and x != y:

                                # print("elimiate")

                                eliminate_x.append(y)

                    if s_w == 'w':

                        status_x = []

                        # print("")

                        for z in range(len(theory_board[:, 0, 0])):

                            # print("z")
                            # print("x compare")
                            # print(theory_board[z, x, 0], theory_board[z, y, 0])

                            if theory_board[z, x, 0] == theory_board[z, y, 0]:

                                # print("equal_x")
                                status_x.append('e')

                            if theory_board[z, x, 0] > theory_board[z, y, 0]:

                                # print('greater_x')
                                status_x.append('g')


                        # print('status_x')
                        # print(len(status_x))
                        # print(len(theory_board[0, :, 0]))

                        if len(status_x) == len(theory_board[:, 0, 0]) and 'g' in status_x:

                            if y not in eliminate_x and x != y:

                                # print("elimiate_x")

                                eliminate_x.append(y)

            for x in range(len(theory_board[0, :, 0])):

                if x not in eliminate_x:

                    dominant_x.append(x)


            # print("")
            # print("dominant")
            # print(dominant_x)
            # print('eliminate')
            # print(eliminate_x)

            theory_board_1 = np.zeros((len(theory_board[:, 0, 0]), len(dominant_x), 2), dtype='uint8')

            for d in dominant_x:

                # print("")
                # print("d")
                # print(d)
                # print(theory_board[ :, d, :])

                theory_board_1[:, dominant_x.index(d), :] = theory_board[:, d, :]

            # print("")
            # print("theory_board_1")
            # print(theory_board_1)


            dominant_y = []
            eliminate_y = []

            for x in range(len(theory_board_1[:, 0, 0])):

                for y in range(len(theory_board_1[:, 0, 0])):

                    # print("")
                    # print("x, y")
                    # print((x, y))

                    if s_w == 's':

                        status = []

                        # print("")

                        for z in range(base ** view):

                            # print("z")
                            # print(theory_board[z + 1, x + 1, 0], theory_board[z + 1, y + 1, 0])

                            if theory_board[z + 1, x + 1, 0] > theory_board[z + 1, y + 1, 0]:
                                # print('greater')

                                status.append('g')

                        # print('status')

                        if len(status) == base ** view:

                            if y not in eliminate_x and x != y:
                                # print("elimiate")

                                eliminate_x.append(y)

                    if s_w == 'w':

                        status_y = []

                        # print("")

                        greater = 0

                        for z in range(len(dominant_x)):

                            # print('y compare')
                            # print(z)
                            # print(theory_board_1[x, z, 1], theory_board_1[y, z, 1])

                            if theory_board_1[x, z, 1] == theory_board_1[y, z, 1]:

                                # print("equal_y")

                                status_y.append('e')

                            if theory_board_1[x, z, 1] > theory_board_1[y, z, 1]:
                                # print('greater_y')
                                status_y.append('g')

                                greater += 1

                        # print('status_y')
                        # print(len(status_y))

                        if len(status_y) == len(dominant_x) and 'g' in status_y:

                            if y not in eliminate_y and x != y:

                                # print('eliminate_y')

                                eliminate_y.append(y)

            for x in range(len(theory_board_1[:, 0, 0])):

                if x not in eliminate_y:
                    dominant_y.append(x)

            # print("")
            # print("dominant_y")
            # print(dominant_y)
            # print('eliminate_y')
            # print(eliminate_y)

            theory_board_2 = np.zeros((len(dominant_y), len(dominant_x), 2), dtype='uint8')

            # print("theory_board_2")
            # print(theory_board_2)

            for d in dominant_y:

                # print("")
                # print("d")
                # print(d)
                # print(theory_board_1[d, :, :])

                theory_board_2[dominant_y.index(d), :, :] = theory_board_1[d, :, :]

            # print("")
            # print("theory_board_2")
            # print(theory_board_2)
            #
            # print(len(theory_board[:, 0, 0]))
            # print(len(theory_board_2[:, 0, 0]))
            # print(len(theory_board[0, :, 0]))
            # print(len(theory_board_2[0, :, 0]))

            if len(theory_board[:, 0, 0]) == len(theory_board_2[:, 0, 0]) and len(theory_board[0, :, 0]) == len(theory_board_2[0, :, 0]):

                # print("simple")

                simple = 1


            values = []

            for y in range(len(theory_board_2[:, 0, 0])):

                for x in range(len(theory_board_2[0, :, 0])):

                    # print(theory_board_2[y, x])
                    # print(theory_board_2[y, x, 0])
                    # print(theory_board_2[y, x, 1])

                    if theory_board_2[y, x, 0] not in values:

                        values.append(theory_board_2[y, x, 0])

                    if theory_board_2[y, x, 1] not in values:

                        values.append(theory_board_2[y, x, 1])

            values = sorted(values)

            # print("")
            # print("values")
            # print(values)
            #
            # print("theory_board_2")
            # print(theory_board_2)

            for y in range(len(theory_board_2[:, 0, 0])):

                for x in range(len(theory_board_2[0, :, 0])):

                    theory_board_2[y, x, 0] = values.index(theory_board_2[y, x, 0])
                    theory_board_2[y, x, 1] = values.index(theory_board_2[y, x, 1])

            # print("")
            # print("theory_boards 1")
            # print(theory_board)
            # print(theory_board_2)

            if len(theory_board_2[:, 0, 0]) == 0:

                theory_board_2 = theory_board

            # print("theory_boards 2")
            # print(theory_board)
            # print(theory_board_2)

            if label == 0:

                label = 1

                d_label = (dominant_x, dominant_y)

            if simple == 0:

                theory_board_2, dominant_x, dominant_y, d_label = IEDS(theory_board_2, s_w, d_label, simple, label)

                return theory_board_2, dominant_x, dominant_y, d_label

            else:

                return theory_board_2, dominant_x, dominant_y, d_label






        theory_board, dominant_x, dominant_y, d_label = IEDS(theory_board, 'w')






        ##p2 bot
        if ai == 1:

            p2_move = -1
            optimal = 0
            optimals = []

            ###value
            for r in rc_count:

                if list(rc_count.keys()).index(r) == last_move:

                    continue

                if rc_count[r] > optimal:

                    optimal = rc_count[r]

            for r in rc_count:

                if list(rc_count.keys()).index(r) == last_move:

                    continue

                if rc_count[r] == optimal:

                    optimals.append(list(rc_count.keys()).index(r))

            if len(optimals) == 1:

                if i_rule[optimals[0]] == 0:

                    p2_move = ('a', optimals[0])

                else:

                    p2_move = ('d', optimals[0])

            ###agression
            if p2_move == -1:

                attack = []
                defend = []
                committed = []
                stance = 0


                for o in optimals:

                    if i_rule[o] == 0:

                        attack.append(o)

                    else:

                        defend.append(o)

                if agression == 0 and len(defend) > 0:

                    committed = defend
                    stance = 0

                else:

                    committed = attack
                    stance = 1

                if len(committed) == 1:

                    p2_move = [ad[agression], committed[0]]

            ###popularity
            elif p2_move == -1:

                cool_kids = []
                cool_score = 0

                for c in committed:

                    if pc_count[c] > cool_score:

                        cool_score = pc_count[c]

                for c in committed:

                    if pc_count[c] == cool_score:

                        cool_kids.append(c)

                if len(cool_kids) == 1:

                    p2_move = [ad[stance], cool_kids[0]]

            ###age
            elif p2_move == -1:

                age = 99999
                fresh = []

                for c in cool_kids:

                    if stagnation[c] < age:

                        age = stagnation[c]

                for c in cool_kids:

                    if stagnation[c] == age:

                        fresh.append(c)

                if len(fresh) == 1:

                    p2_move = [ad[stance], fresh[0]]

        if ai >= 2:

            rv_1 = random.choice(d_label[0])
            rv_2 = random.choice(d_label[1])
            rv_3 = random.choice(range(2))

            if ai == 3:

                if rv_3 == 1:

                    # print("random")
                    # print(rv_3)

                    rv_1 = random.choice(range(8))
                    rv_2 = random.choice(range(8))

                    # print(rv_1)
                    # print(rv_2)

            # print(d_label[0])
            # print(d_label[1])
            # print(rv_1)
            # print(rv_2)

            p1_move = (ad[i_rule[rv_1]], rv_1)
            p2_move = (ad[i_rule[rv_2]], rv_2)




        # print("p2_move")
        # print(p2_move)



        #console rule inputs

        if list_count != 0:

            if rule_list[0] < max_rule:

                # print("")
                # print('valid')
                # print(rule_list[0])

                d_rule, i_rule = rule_gen(rule_list[0], base)

            else:

                new_rule = rule_list[0] % max_rule

                d_rule, i_rule = rule_gen(new_rule, base)

            rule_list = rule_list[1:]

            list_count -= 1


        #inputs
        for event in pygame.event.get():

            current_digit = -1

            #quit
            if event.type == pygame.QUIT:
                run = 2

            #click
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_l = True
                if event.button == 3:
                    click_r = True

            #keyboard
            if event.type == pygame.KEYDOWN:

                if event.key == K_ESCAPE:
                    run = 2


                if event.key == pygame.K_DOWN:

                    # print("down")

                    move_down += 1

                if event.key == pygame.K_UP:

                    # print("up")

                    move_up += 1


                if event.key == pygame.K_q:
                    v_input = input('q', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_w:
                    v_input = input('w', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_e:
                    v_input = input('e', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_r:
                    v_input = input('r', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_t:
                    v_input = input('t', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_y:
                    v_input = input('y', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_u:
                    v_input = input('u', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_i:
                    v_input = input('i', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_o:
                    v_input = input('o', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_p:
                    v_input = input('p', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_a:
                    v_input = input('a', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_s:
                    v_input = input('s', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_d:
                    v_input = input('d', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_f:
                    v_input = input('f', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_g:
                    v_input = input('g', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_h:
                    v_input = input('h', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_j:
                    v_input = input('j', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_k:
                    v_input = input('k', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_l:
                    v_input = input('l', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_z:
                    v_input = input('z', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_x:
                    v_input = input('x', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_c:
                    v_input = input('c', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_v:
                    v_input = input('v', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_b:
                    v_input = input('b', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_n:
                    v_input = input('n', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_m:
                    v_input = input('m', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_SPACE:
                    v_input = input(' ', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_0:

                    v = 0

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_1:

                    v = 1

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_2:

                    v = 2

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_3:

                    v = 3

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_4:

                    v = 4

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_5:

                    v = 5

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_6:

                    v = 6

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_7:

                    v = 7

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_8:

                    v = 8

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_9:

                    v = 9

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_BACKSPACE:
                    v_input = v_input[0:-1]

                if event.key == pygame.K_MINUS:
                    # print("underscore")

                    v_input += "-"

                #console commands
                if event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_SHIFT:

                    if input_box == 0:

                        input_box = 1

                    else:

                        if len(v_input) != 0:

                            input_list = v_input.split()

                            # print(" ")
                            # print("input_list")
                            # print(input_list)
                            # print(len(input_list))
                            # print(len(input_list[0]))

                            if len(input_list) > 1:

                                try:

                                    rule_list, list_count = rl_gen(input_list)

                                except:

                                    if input_list[0] == 'base':

                                        print("##########based##########")

                                        row = np.zeros((1, cell_row_width), dtype='int8')
                                        base = int(input_list[1])
                                        bv = base ** view

                                        step_size = int(base ** view / (base - 1) / magnify)
                                        o_r = rule_gen(0, base)[1]
                                        for x in range(int((base ** view) / step_size) + 1):

                                            if x > 0:

                                                o_r[-((step_size * x + 1) % bv)] = x % colors + 1

                                            else:

                                                o_r[-((step_size * x + 1) % bv)] = 1
                                        o_r[-1] = 1
                                        origin_rule = decimal(o_r, base)
                                        ir_height = base

                                        if base < 5:
                                            cell_colors = {0: 'black_x', 1: 'magenta_x', 2: 'cyan_x', 3: 'yellow_x'}

                                        else:
                                            cell_colors = {0: 'black_x', 1: 'dark_grey_x', 2: 'magenta_x', 3: 'cyan_x',
                                                           4: 'yellow_x', 5: 'light_grey_x', 6: 'red_x', 7: 'green_x',
                                                           8: 'blue_x'}

                                        print("origin rule")
                                        print(o_r)
                                        print(origin_rule)

                                        d_rule, i_rule = rule_gen(origin_rule, base)

                                        if words_g > 0:

                                            triggers = [trigger_1, trigger_2, trigger_3, trigger_4, trigger_5, trigger_6,
                                                        trigger_7, trigger_8][:base - 1]

                                            triggers.append(trigger_0)

                                            t_sum = 1

                                            for t in triggers:

                                                # print("t")
                                                # print(t)

                                                if t > triggers[-1]:
                                                    triggers[-1] = t

                                                t_sum += t

                                            rw_length = int(
                                                round(triggers[-1] / zero_out, 3) * base ** view / rule_window_scale)

                                            ts_percentage = [round((t / t_sum * 100), 0) for t in triggers]

                                            tsp_portion = [int(round((t / t_sum), 3) * rw_length) for t in triggers]

                                            for x in range(len(triggers)):

                                                if triggers[x] != 0 and tsp_portion[x] == 0:
                                                    tsp_portion[x] = 1

                                            t_dict = dict()

                                            for x in range(len(triggers)):

                                                # print("x")
                                                # print(x)

                                                if x == len(triggers) - 1:

                                                    t_dict[0] = tsp_portion[x]

                                                else:

                                                    t_dict[x + 1] = tsp_portion[x]

                                            t_dict = sorted(list(t_dict.items()), key=lambda x: x[1], reverse=True)

                                            # print("t_dict")
                                            # print(t_dict)
                                            #
                                            # print("i_rule")
                                            # print(i_rule

                                            place = (glove_value % (base ** view)) - 1
                                            glove_value = (glove_value % (base ** view)) - 1

                                            for t in t_dict:

                                                if t[1] != 0:

                                                    for x in range(t[1]):

                                                        # print("ir gv len(t)")
                                                        # print(len(i_rule))
                                                        # print(place)
                                                        # print(len(t))
                                                        # print(base ** view)

                                                        if i_rule[place % len(i_rule)] != t[0]:

                                                            # print("place")
                                                            # print(place % len(i_rule))

                                                            if place % len(i_rule) not in placed:
                                                                placed.append(place % len(i_rule))

                                                            # print("len(placed)")
                                                            # print(len(placed))

                                                            i_rule[place % len(i_rule)] = t[0] % base
                                                            d_rule[list(d_rule.keys())[place % len(i_rule)]] = t[0] % base

                                                        else:

                                                            continue

                                                        place += 1

                                    if input_list[0] == 'name':
                                        j_name = input_list[1]

                                        write = 1

                                    if input_list[0] == 't-clear':

                                        trigger_0 = 0
                                        trigger_1 = 0
                                        trigger_2 = 0
                                        trigger_3 = 0
                                        trigger_4 = 0
                                        trigger_5 = 0
                                        trigger_6 = 0
                                        trigger_7 = 0
                                        trigger_8 = 0


                                    if input_list[0] == 'characters-g':

                                        characters_g = input_list[1]

                                    if input_list[0] == 'words-g':

                                        words_g = input_list[1]

                                    if input_list[0] == 'rules-g':

                                        rules_g = input_list[1]

                                    if input_list[0] == 'digits-g':

                                        digits = input_list[1]


                                    if input_list[0] == 'tplus':

                                        tplus_scale = int(input_list[1])

                                    if input_list[0] == 'tminus':

                                        tminus_scale = int(input_list[1])


                                    if input_list[0] == 'rule-pause':

                                        rule_pause = int(input_list[1])


                                    if input_list[0] == 'threshold':

                                        origin_threshold = int(input_list[1])

                                        # print("")
                                        # print("originated")
                                        # print(origin_threshold)

                                    if input_list[0] == 'threshold-0':

                                        t0_threshold = int(input_list[1])

                                    if input_list[0] == 'threshold-1':

                                        t1_threshold = int(input_list[1])

                                    if input_list[0] == 'threshold-2':

                                        t2_threshold = int(input_list[1])

                                    if input_list[0] == 'threshold-3':

                                        t3_threshold = int(input_list[1])

                                    if input_list[0] == 'threshold-4':

                                        t4_threshold = int(input_list[1])

                                    if input_list[0] == 'threshold-5':

                                        t5_threshold = int(input_list[1])

                                    if input_list[0] == 'threshold-6':

                                        t6_threshold = int(input_list[1])

                                    if input_list[0] == 'threshold-7':

                                        t7_threshold = int(input_list[1])

                                    if input_list[0] == 'threshold-8':

                                        t8_threshold = int(input_list[1])

                                    if input_list[0] == 'threshold-all':

                                        t0_threshold = int(input_list[1])
                                        t1_threshold = int(input_list[1])
                                        t2_threshold = int(input_list[1])
                                        t3_threshold = int(input_list[1])
                                        t4_threshold = int(input_list[1])

                                    thresholds = [t0_threshold, t1_threshold, t2_threshold, t3_threshold, t4_threshold]

                            elif v_input == 'write':

                                write = 1

                            elif input_list[0] == 'invalid':

                                v_input = ''

                            else:

                                try:

                                    d_rule, i_rule = rule_gen(int(v_input), base)

                                except:

                                    v_input = 'invalid'

                                    continue

                            v_input = ''

                        input_box = 0

                elif event.key == pygame.K_PERIOD:

                    d_rule, i_rule = rule_gen(origin_rule, base)

                    for letter in press:

                        if letter in press_vault:

                            press_vault[letter] += press[letter]

                        else:
                            press_vault[letter] = press[letter]

                        press[letter] = 0

            #midi
            if event.type in [pygame.midi.MIDIIN]:

                # print(event)

                clean_e = str(event)[21:-3]
                list_e = clean_e.split(',')
                ev = []

                for l in list_e:

                    ev.append(int(l.split(':')[1]))

                # print(" ")
                # print("ev")
                # print(ev)
                # print(event)

                #x axis
                if ev[1] == 0:

                    ev_1 = ev[2]

                    if words_g > 0:

                        if ev[2] > rule_pause:

                            words_g = 3

                        else:

                            words_g = 2

                    # print("")
                    # print("ev_1")
                    # print(ev_1)

                    if ev_1 > gvp_threshold:

                        # print("gv_pause")

                        gv_pause = 1

                    else:

                        gv_pause = 0

                #y axis
                if ev[1] == 2:

                    ev_2 = ev[2]

                #z axis
                if ev[1] == 3:

                    ev_3 = ev[2]

                #pitch
                if ev[1] == 4:

                    ev_4 = ev[2]

                #yaw
                if ev[1] == 5:

                    ev_5 = ev[2]

                #roll
                if ev[1] == 6:

                    ev_6 = ev[2]

                #thumb
                if ev[1] == 7:

                    ev_7 = ev[2]

                    if words_g != 3:

                        if ev[2] > t0_threshold:

                            if trigger_0 < 0:

                                trigger_0 = 0

                            else:

                                trigger_0 += int(cell_vel * tplus_scale)

                            current_digit = 0

                    # if words_g > 0:
                    #
                    #     if ev[2] > rule_pause:
                    #
                    #         words_g = 3
                    #
                    #     else:
                    #
                    #         words_g = 2

                #pointer
                if ev[1] == 8:

                    ev_8 = ev[2]

                    if words_g != 3:

                        if ev[2] > t1_threshold:

                            if trigger_1 < 0:

                                trigger_1 = 0

                            else:

                                trigger_1 += int(cell_vel * tplus_scale)

                        if ev[2] < t5_threshold:

                            if trigger_5 < 0:

                                trigger_5 = 0

                            else:

                                trigger_5 += int(cell_vel * tplus_scale)

                            current_digit = 1

                #middle
                if ev[1] == 9:

                    ev_9 = ev[2]

                    if words_g != 3:

                        if ev[2] > t2_threshold:

                            if trigger_2 < 0:

                                trigger_2 = 0

                            else:

                                trigger_2 += int(cell_vel * tplus_scale)

                            current_digit = 2

                        if ev[2] < t6_threshold:

                            if trigger_6 < 0:

                                trigger_6 = 0

                            else:

                                trigger_6 += int(cell_vel * tplus_scale)

                            current_digit = 1

                    # if ev[2] > origin_threshold:
                    #
                    #     if zero_count > 0:
                    #
                    #         zero_count -= int(cell_vel/5)
                    #
                    #     if zero_count < 0:
                    #
                    #         zero_count = 1

                #ring
                if ev[1] == 10:

                    ev_10 = ev[2]

                    if words_g != 3:

                        if ev[2] > t3_threshold:

                            if trigger_3 < 0:

                                trigger_3 = 0

                            else:

                                trigger_3 += int(cell_vel * tplus_scale)

                            current_digit = 3

                        if ev[2] < t7_threshold:

                            if trigger_7 < 0:

                                trigger_7 = 0

                            else:

                                trigger_7 += int(cell_vel * tplus_scale)

                            current_digit = 1

                #pinky
                if ev[1] == 11:

                    ev_11 = ev[2]

                    if words_g != 3:

                        if ev[2] > t4_threshold:

                            if trigger_4 < 0:

                                trigger_4 = 0

                            else:

                                trigger_4 += int(cell_vel * tplus_scale)

                            current_digit = 4

                        if ev[2] < t8_threshold:

                            if trigger_8 < 0:

                                trigger_8 = 0

                            else:

                                trigger_8 += int(cell_vel * tplus_scale)

                            current_digit = 1



                if characters_g == 1:

                    if gv_pause == 0:

                        # print("summing")

                        if digits == 1:

                            glove_value = ev_1 + ev_2 + ev_3 + ev_4 + ev_5 + ev_6 + ev_7 + ev_8 + ev_9 + ev_10 + ev_11

                        else:

                            glove_value = ev_2 + ev_3 + ev_4 + ev_5 + ev_6

                        glove_value = glove_value % (base ** view)

                    if rule not in journal:

                        # print("############## not in ##############")

                        journal[rule] = []
                        journal[rule].append(page)

                    else:

                        # print("else")

                        journal[rule].append(page)

                    if current_digit != - 1:

                        i_rule[glove_value] = current_digit
                        d_rule[list(d_rule.keys())[glove_value]] = current_digit

                if words_g > 0:

                    if digits == 1:

                        glove_value = ev_1 + ev_2 + ev_3 + ev_4 + ev_5 + ev_6 + ev_7 + ev_8 + ev_9 + ev_10 + ev_11

                    else:

                        glove_value = ev_1 + ev_2 + ev_3 + ev_4 + ev_5 + ev_6

                    glove_value = glove_value % (base ** view)

                    # print("glove_value")
                    # print(glove_value)


                    # place_change(glove_value)
                    # place_change(glove_value + ev_7)
                    # place_change(glove_value + ev_8)
                    # place_change(glove_value + ev_9)
                    # place_change(glove_value + ev_10)
                    # place_change(glove_value + ev_11)

                    # print("")
                    # print("rule")
                    # print(rule)

                    if rule not in journal:

                        # print("############## not in ##############")

                        journal[rule] = []
                        journal[rule].append(page)

                    else:

                        # print("else")

                        journal[rule].append(page)

                    # print(len(journal))

                    if words_g == 2:

                        triggers = [trigger_1, trigger_2, trigger_3, trigger_4, trigger_5, trigger_6, trigger_7, trigger_8][:base - 1]

                        triggers.append(trigger_0)

                        t_sum = 1

                        # print(" ")
                        # print("triggers-event")
                        # print(triggers)
                        # print(len(triggers))

                        for t in triggers:

                            # print("t")
                            # print(t)

                            if t > triggers[-1]:
                                triggers[-1] = t

                            t_sum += t

                        # print("last t")
                        # print(triggers[-1])
                        #
                        # print(base ** view)
                        # print(len(i_rule))
                        #
                        # print('t-1 / zero_out')
                        # print(round(triggers[-1] / zero_out, 3) * base ** view)

                        rw_length = int(round(triggers[-1] / zero_out, 3) * base ** view / rule_window_scale)

                        # print("t_sum")
                        # print(t_sum)

                        ts_percentage = [round((t / t_sum * 100), 0) for t in triggers]

                        # largest = 0
                        #
                        # for t in ts_percentage:
                        #
                        #     if t > largest:
                        #
                        #         largest = t
                        #
                        # ts_percentage.append(largest)

                        tsp_portion = [int(round((t / t_sum), 3) * rw_length) for t in triggers]

                        # print("")
                        # print("tsp portion")
                        # print(tsp_portion)

                        for x in range(len(triggers)):

                            if triggers[x] != 0 and tsp_portion[x] == 0:

                                tsp_portion[x] = 1


                        t_dict = dict()

                        for x in range(len(triggers)):

                            # print("x")
                            # print(x)

                            if x == len(triggers) - 1:

                                t_dict[0] = tsp_portion[x]

                            else:

                                t_dict[x + 1] = tsp_portion[x]

                        t_dict = sorted(list(t_dict.items()), key=lambda x: x[1], reverse=True)

                        # print("t_dict")
                        # print(t_dict)
                        #
                        # print("i_rule")
                        # print(i_rule

                        place = (glove_value % (base ** view)) - 1

                        for t in t_dict:

                            if t[1] != 0:

                                for x in range(t[1]):

                                    # print("ir gv len(t)")
                                    # print(len(i_rule))
                                    # print(place)
                                    # print(len(t))
                                    # print(base ** view)

                                    if i_rule[place % len(i_rule)] != t[0]:

                                        # print("place")
                                        # print(place % len(i_rule))

                                        if place % len(i_rule) not in placed:
                                            placed.append(place % len(i_rule))

                                        # print("len(placed)")
                                        # print(len(placed))

                                        # print("place")
                                        # print(place)
                                        # print(len(i_rule))
                                        # print(bv)

                                        i_rule[place % len(i_rule) - 1] = t[0] % base
                                        d_rule[list(d_rule.keys())[place % len(i_rule) - 1]] = t[0] % base

                                    else:

                                        continue

                                    place += 1

                        # print(i_rule)

                        # print(ts_percentage)

                        triggers.append(t_sum)

                if rules_g == 1:

                    glove_value = ev_7 + 4 * ev_8 + 16 * ev_9 + 64 * ev_10

                    # print("")
                    # print("glove_value")
                    # print(glove_value)

                    d_rule, i_rule = rule_gen(glove_value, base)

                    if rule not in journal:
                        journal[rule] = []
                        journal[rule].append(page)

                    else:
                        journal[rule].append(page)


        #glove methods
        if words_g > 0:

            if words_g == 2:

                if trigger_0 > 0:

                    trigger_0 -= int(cell_vel * tminus_scale)

                    if trigger_0 > zero_out:
                        trigger_0 = zero_out

                    if trigger_0 < 0:
                        trigger_0 = 0

                    if trigger_0 == zero_out:

                        print("trigger0 == zero_out origin_rule")

                        d_rule, i_rule = rule_gen(origin_rule, base)

                        if over_flow == 0:

                            trigger_0 = 0

                if trigger_1 > 0:

                    trigger_1 -= int(cell_vel * tminus_scale)

                    if trigger_1 > zero_out:
                        trigger_1 = zero_out

                    if trigger_1 < 0:
                        trigger_1 = 0

                    if trigger_1 == zero_out:

                        print("trigger1 == zero_out origin_rule")

                        d_rule, i_rule = rule_gen(origin_rule, base)

                        if over_flow == 0:

                            trigger_1 = 0

                if trigger_2 > 0:

                    trigger_2 -= int(cell_vel * tminus_scale)

                    if trigger_2 > zero_out:
                        trigger_2 = zero_out

                    if trigger_2 < 0:
                        trigger_2 = 0

                    if trigger_2 == zero_out:

                        print("trigger2 == zero_out origin_rule")

                        d_rule, i_rule = rule_gen(origin_rule, base)

                        if over_flow == 0:

                            trigger_2 = 0

                if trigger_3 > 0:

                    trigger_3 -= int(cell_vel * tminus_scale)

                    if trigger_3 > zero_out:
                        trigger_3 = zero_out

                    if trigger_3 < 0:
                        trigger_3 = 0

                    if trigger_3 == zero_out:

                        print("trigger3 == zero_out origin_rule")

                        d_rule, i_rule = rule_gen(origin_rule, base)

                        if over_flow == 0:

                            trigger_3 = 0

                if trigger_4 > 0:

                    trigger_4 -= int(cell_vel * tminus_scale)

                    if trigger_4 > zero_out:
                        trigger_4 = zero_out

                    if trigger_4 < 0:
                        trigger_4 = 0

                    if trigger_4 == zero_out:

                        print("trigger4 == zero_out origin_rule")

                        d_rule, i_rule = rule_gen(origin_rule, base)

                        if over_flow == 0:

                            trigger_4 = 0

                if trigger_5 > 0:

                    trigger_5 -= int(cell_vel * tminus_scale)

                    if trigger_5 > zero_out:
                        trigger_5 = zero_out

                    if trigger_5 < 0:
                        trigger_5 = 0

                    if trigger_5 == zero_out:

                        print("trigger5 == zero_out origin_rule")

                        d_rule, i_rule = rule_gen(origin_rule, base)

                        if over_flow == 0:

                            trigger_5 = 0

                if trigger_6 > 0:

                    trigger_6 -= int(cell_vel * tminus_scale)

                    if trigger_6 > zero_out:
                        trigger_6 = zero_out

                    if trigger_6 < 0:
                        trigger_6 = 0

                    if trigger_6 == zero_out:

                        print("trigger6 == zero_out origin_rule")

                        d_rule, i_rule = rule_gen(origin_rule, base)

                        if over_flow == 0:

                            trigger_6 = 0

                if trigger_7 > 0:

                    trigger_7 -= int(cell_vel * tminus_scale)

                    if trigger_7 > zero_out:
                        trigger_7 = zero_out

                    if trigger_7 < 0:
                        trigger_7 = 0

                    if trigger_7 == zero_out:

                        print("trigger7 == zero_out origin_rule")

                        d_rule, i_rule = rule_gen(origin_rule, base)

                        if over_flow == 0:

                            trigger_7 = 0

                if trigger_8 > 0:

                    trigger_8 -= int(cell_vel * tminus_scale)

                    if trigger_8 > zero_out:
                        trigger_8 = zero_out

                    if trigger_8 < 0:
                        trigger_8 = 0

                    if trigger_8 == zero_out:

                        print("trigger8 == zero_out origin_rule")

                        d_rule, i_rule = rule_gen(origin_rule, base)

                        if over_flow == 0:

                            trigger_8 = 0

            if words_g == 1:

                if trigger_0 > 0:

                    trigger_0 -= int(cell_vel/2)

                    if trigger_0 > zero_out:

                        trigger_0 = zero_out

                    if trigger_0 < 0:

                        trigger_0 = 0

                    if trigger_0 == zero_out:

                        d_rule, i_rule = rule_gen(origin_rule, base)

                if trigger_1 > 0:

                    trigger_1 -= int(cell_vel/2)

                    if trigger_1 > zero_out:

                        trigger_1 = zero_out

                    if trigger_1 < 0:

                        trigger_1 = 0

                    if trigger_1 == zero_out:

                        d_rule, i_rule = rule_gen(origin_rule, base)

                if trigger_2 > 0:

                    trigger_2 -= int(cell_vel / 2)

                    if trigger_2 > zero_out:

                        trigger_2 = zero_out

                    if trigger_2 < 0:

                        trigger_2 = 0

                    if trigger_2 == zero_out:

                        d_rule, i_rule = rule_gen(origin_rule, base)

                if trigger_3 > 0:

                    trigger_3 -= int(cell_vel / 2)

                    if trigger_3 > zero_out:

                        trigger_3 = zero_out

                    if trigger_3 < 0:

                        trigger_3 = 0

                    if trigger_3 == zero_out:

                        d_rule, i_rule = rule_gen(origin_rule, base)

                if trigger_4 > 0:

                    trigger_4 -= int(cell_vel / 2)

                    if trigger_4 > zero_out:

                        trigger_4 = zero_out

                    if trigger_4 < 0:

                        trigger_4 = 0

                    if trigger_4 == zero_out:

                        d_rule, i_rule = rule_gen(origin_rule, base)

                triggers = [trigger_1, trigger_2, trigger_3, trigger_4, trigger_0]

                t_sum = 1

                # print(" ")
                # print("triggers")
                # print(triggers)

                for t in triggers:

                    # print("t")
                    # print(t)

                    if t > triggers[-1]:

                        triggers[-1] = t


                    t_sum += t

                # print("last t")
                # print(triggers[-1])
                #
                # print(base ** view)
                # print(len(i_rule))
                #
                # print('t-1 / zero_out')
                # print(round(triggers[-1] / zero_out, 3) * base ** view)

                rw_length = int(round(triggers[-1] / zero_out, 3) * base ** view / 2)

                # print("t_sum")
                # print(t_sum)

                ts_percentage = [round((t / t_sum * 100), 3) for t in triggers]

                # largest = 0
                #
                # for t in ts_percentage:
                #
                #     if t > largest:
                #
                #         largest = t
                #
                # ts_percentage.append(largest)

                tsp_portion = [int(round((t / t_sum), 3) * rw_length) for t in triggers]

                tspp = sum(tsp_portion)

                # print("tspp")
                # print(tspp)

                t_dict = dict()

                for x in range(len(triggers)):

                    # print("x")
                    # print(x)

                    if x == len(triggers) - 1:

                        t_dict[0] = tsp_portion[x]

                    else:

                        t_dict[x + 1] = tsp_portion[x]

                t_dict = sorted(list(t_dict.items()), key=lambda x:x[1], reverse=True)

                # print("t_dict")
                # print(t_dict)
                #
                # print("i_rule")
                # print(i_rule

                place = (glove_value % (base ** view)) - 1

                for t in t_dict:

                    if t[1] != 0:

                        for x in range(t[1]):

                            # print("ir gv len(t)")
                            # print(len(i_rule))
                            # print(place)
                            # print(len(t))
                            # print(base ** view)

                            if i_rule[place % len(i_rule)] != t[0]:

                                # print("place")
                                # print(place % len(i_rule))

                                if place % len(i_rule) not in placed:

                                    placed.append(place % len(i_rule))

                                # print("len(placed)")
                                # print(len(placed))

                                i_rule[place % len(i_rule)] = t[0]
                                d_rule[list(d_rule.keys())[place % len(i_rule)]] = t[0]

                            else:

                                continue

                            place += 1

                # print(i_rule)







                # print(ts_percentage)

                triggers.append(t_sum)


        #midi clean up
        if device_id > 0:

            if midi_inputs == 1:

                if p_m_i.poll():

                    # print(' ')
                    # print('i')
                    # print(i)

                    midi_events = p_m_i.read(999)
                    midi_evs = pygame.midi.midis2events(midi_events, p_m_i.device_id)

                    for m_e in midi_evs:
                        event_post(m_e)


    #journal write
    if write == 1:

        if len(j_name) > 0:

            filename = 'journals/journal_' + j_name

        else:

            j_num = len(os.listdir('../journals'))

            filename = 'journals/journal_' + str(j_num)

        outfile = open(filename, 'wb')
        pickle.dump(journal, outfile)
        outfile.close

        # print(len(journal))


# menus

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
    input_text_c = ''
    input_text_v = ''
    device_id = None
    analytics = 0

    pygame.init()
    pygame.fastevent.init()

    pygame.midi.init()

    print(" ")
    print("device info")
    _print_device_info()

    mc = pygame.midi.get_count()
    print("mc")
    print(mc)

    ports = dict()

    print("")
    print("mdi")
    for m in range(pygame.midi.get_count()):


        mdi = pygame.midi.get_device_info(m)
        print(mdi)

        ports[m] = str(mdi[1])




    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print(' ')
    print("using input_id :%s:" % input_id)
    p_m_i = pygame.midi.Input(input_id)
    device_id = -1

    while True:


        WIN.fill((0, 0, 0))
        t_line = pygame.Rect(WIDTH / 2 - 633, 200, 1360, 2)
        draw_text('C311UL4R H4PT1C 4UT0M4T4 0P3R4T1NG 5Y5T3M', TITLE_FONT, (10, 100, 10), WIN, WIDTH / 2 - 655, 100)
        pygame.draw.rect(WIN, (10, 100, 10), t_line)

        text_surface_c = main_font.render(input_text_c, True, (100, 10, 10))
        text_surface_v = main_font.render(input_text_v, True, (100, 10, 100))
        mx, my = pygame.mouse.get_pos()


        for p in ports:

            # print("")
            # print(p)
            # print(ports[p])

            port_button = pygame.Rect(WIDTH / 2 + 400, 600 + p * 40, 362, 34)
            pygame.draw.rect(WIN, (192, 128, 0), port_button)

            port_button = pygame.Rect(WIDTH / 2 + 400, 600 + p * 40, 360, 30)
            pygame.draw.rect(WIN, (0, 0, 0), port_button)

            if port_button.collidepoint((mx, my)):

                # print("collide")
                # print(p)

                if click:

                    print(p)

                    device_id = int(p)
                    draw_text('> ' + str(ports[p]), small_font, (255, 255, 255), WIN, WIDTH / 2 + 400, 600 + p * 40)

            draw_text('> ' + str(ports[p]), small_font, (192, 128, 0), WIN, WIDTH / 2 + 400, 600 + p * 40)

        size_2 = pygame.Rect(WIDTH / 2 - 300, 400, 200, 50)
        size_3 = pygame.Rect(WIDTH / 2 - 300, 500, 200, 50)
        size_5 = pygame.Rect(WIDTH / 2 - 300, 600, 200, 50)
        size_10 = pygame.Rect(WIDTH / 2 - 300, 700, 200, 50)
        size_2_i = pygame.Rect(WIDTH / 2 - 300, 400, 197, 43)
        size_3_i = pygame.Rect(WIDTH / 2 - 300, 500, 197, 43)
        size_5_i = pygame.Rect(WIDTH / 2 - 300, 600, 197, 43)
        size_10_i = pygame.Rect(WIDTH / 2 - 300, 700, 197, 43)

        # binary = pygame.Rect(WIDTH/2 + 100, 400, 200, 50)
        # ternary = pygame.Rect(WIDTH/2 + 100, 500, 200, 50)
        # quaternary = pygame.Rect(WIDTH/2 + 100, 600, 200, 50)
        # binary_i = pygame.Rect(WIDTH/2 + 100, 400, 197, 43)
        # ternary_i = pygame.Rect(WIDTH/2 + 100, 500, 197, 43)
        # quaternary_i = pygame.Rect(WIDTH/2 + 100, 600, 197, 43)

        color_rect = pygame.Rect(WIDTH / 2 + 100, 400, 200, 50)
        color_rect_i = pygame.Rect(WIDTH / 2 + 100, 400, 197, 43)

        vel_rect = pygame.Rect(WIDTH / 2 + 100, 500, 200, 50)
        vel_rect_i = pygame.Rect(WIDTH / 2 + 100, 500, 197, 43)

        enter = pygame.Rect(WIDTH / 2 + 100, 700, 200, 50)
        enter_i = pygame.Rect(WIDTH / 2 + 100, 700, 197, 43)

        underline_2 = pygame.Rect(WIDTH / 2 - 300, 385, 200, 2)

        analytics_button = pygame.Rect(WIDTH / 2 + 470, 300, 200, 50)
        pygame.draw.rect(WIN, (0, 192, 192), analytics_button)
        analytics_button = pygame.Rect(WIDTH / 2 + 470, 300, 197, 43)
        pygame.draw.rect(WIN, (0, 0, 0), analytics_button)
        draw_text('analytics ^ 0 off - 1 on', small_font, (0, 192, 192), WIN,WIDTH / 2 + 470, 350)


        pygame.draw.rect(WIN, (10, 100, 10), size_2)
        pygame.draw.rect(WIN, (10, 100, 10), size_3)
        pygame.draw.rect(WIN, (10, 100, 10), size_5)
        pygame.draw.rect(WIN, (10, 100, 10), size_10)
        pygame.draw.rect(WIN, (0, 0, 0), size_2_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_3_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_5_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_10_i)
        draw_text(' small', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 400)
        draw_text(' medium', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 500)
        draw_text(' large', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 600)
        draw_text(' X-large', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 700)
        draw_text('Cell Size', main_font, (10, 100, 10), WIN, WIDTH / 2 - 280, 340)
        pygame.draw.rect(WIN, (10, 100, 10), underline_2)

        # pygame.draw.rect(WIN, (100, 10, 10), binary)
        # pygame.draw.rect(WIN, (100, 10, 10), ternary)
        # pygame.draw.rect(WIN, (100, 10, 10), quaternary)
        # pygame.draw.rect(WIN, (0, 0, 0), binary_i)
        # pygame.draw.rect(WIN, (0, 0, 0), ternary_i)
        # pygame.draw.rect(WIN, (0, 0, 0), quaternary_i)
        # draw_text(' Two', main_font, (100, 10, 10), WIN, WIDTH/2 + 100, 400)
        # draw_text(' Three', main_font, (100, 10, 10), WIN, WIDTH/2 + 100, 500)
        # draw_text(' Four', main_font, (100, 10, 10), WIN, WIDTH/2 + 100, 600)
        # draw_text('Number of Colors', main_font, (100, 10, 10), WIN, WIDTH/2 + 80, 340)
        # pygame.draw.rect(WIN, (100, 10, 10), underline_1)

        pygame.draw.rect(WIN, (100, 10, 10), color_rect)
        pygame.draw.rect(WIN, (0, 0, 0), color_rect_i)
        draw_text('<place mouse-pointer on box to type;', small_font, (100, 10, 10), WIN, WIDTH / 2 + 350, 400)
        draw_text('choose a single number between 2 and 9', small_font, (100, 10, 10), WIN, WIDTH / 2 + 360, 425)

        pygame.draw.rect(WIN, (100, 10, 100), vel_rect)
        pygame.draw.rect(WIN, (0, 0, 0), vel_rect_i)
        draw_text('<place mouse-pointer on box to type;', small_font, (100, 10, 100), WIN, WIDTH / 2 + 350, 500)
        draw_text('numbers between 1-10 recommended', small_font, (100, 10, 100), WIN, WIDTH / 2 + 360, 525)

        pygame.draw.rect(WIN, (10, 10, 100), enter)
        pygame.draw.rect(WIN, (0, 0, 0), enter_i)
        draw_text(' Enter', main_font, (10, 10, 100), WIN, WIDTH / 2 + 100, 700)

        draw_text('Instructions:', small_font, (200, 200, 200), WIN, 50, 225)
        draw_text('1. Choose a cell-size. [GREEN]', small_font, (200, 200, 200), WIN, 50, 275)
        draw_text('     -Start with X-large to be safe. Smaller cells', text_font, (200, 200, 200), WIN, 50, 315)
        draw_text('         may cause issues on slower computers.', text_font, (200, 200, 200), WIN, 50, 340)
        draw_text('2. Choose the number of cell colors. [RED]', small_font, (200, 200, 200), WIN, 50, 375)
        draw_text('3. Set a desired speed. [PURPLE]', small_font, (200, 200, 200), WIN, 50, 425)
        draw_text('4. Press Enter [BLUE]', small_font, (200, 200, 200), WIN, 50, 475)
        draw_text('     The program will have loaded once you see Step & Count', text_font, (200, 200, 200), WIN, 50,
                  525)
        draw_text('     in the top right, and Rule in the bottom left.', text_font, (200, 200, 200), WIN, 50, 550)
        draw_text('     Typing has no effect until the first row of colored', text_font, (200, 200, 200), WIN, 50, 575)
        draw_text('     cells reach the bottom of the page.', text_font, (200, 200, 200), WIN, 50, 600)
        draw_text('     Two cell colors uses the keys (asdf jkl;) to change the rules.', text_font, (200, 200, 200),
                  WIN, 50, 625)
        draw_text('     For three colors+, the best effects are seen while typing full sentences', text_font,
                  (200, 200, 200), WIN, 50, 650)
        draw_text('     Press the escape key to exit the program at any time.', text_font, (200, 200, 200), WIN, 50,
                  675)
        draw_text('     Enjoy!', text_font, (200, 200, 200), WIN, 50, 700)
        draw_text('Command Menu (Advanced Technique)', small_font, (200, 200, 200), WIN, 50, 750)
        draw_text(
            '     Press shift & enter keys, at the same time, to activate. A white box will appear in the top left corner of the screen.',
            text_font, (200, 200, 200), WIN, 50, 800)
        draw_text(
            '     Once the desired command is typed into the box, press the shift & enter keys again to input the command and close the box.',
            text_font, (200, 200, 200), WIN, 50, 825)
        draw_text(
            '     All commands are lowercase or integer values, spaces matter, and invalid commands will return a warning in the type field',
            text_font, (200, 200, 200), WIN, 50, 850)
        draw_text(
            '     To save the designs found during a session input(write) or (name *desired-name*). names longer than one word must be separated by a -',
            text_font, (200, 200, 200), WIN, 50, 875)
        draw_text('     All values are accepted as inputs and will change the rule accordingly', text_font,
                  (200, 200, 200), WIN, 50, 900)

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

        # if binary.collidepoint((mx, my)):
        #     if click:
        #         print("binary")
        #         base = 2
        #         draw_text(' Two', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 400)
        # if ternary.collidepoint((mx, my)):
        #     if click:
        #         print("ternary")
        #         base = 3
        #         draw_text(' Three', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 500)
        # if quaternary.collidepoint((mx, my)):
        #     if click:
        #         print("quaternary")
        #         base = 4
        #         draw_text(' Four', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 600)

        if color_rect.collidepoint((mx, my)):
            draw_text('Colors:', main_font, (100, 10, 10), WIN, WIDTH / 2 + 100, 400)
            WIN.blit(text_surface_c, (WIDTH / 2 + 200, 400))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        input_text_c += '1'
                    if event.key == K_2:
                        input_text_c += '2'
                    if event.key == K_3:
                        input_text_c += '3'
                    if event.key == K_4:
                        input_text_c += '4'
                    if event.key == K_5:
                        input_text_c += '5'
                    if event.key == K_6:
                        input_text_c += '6'
                    if event.key == K_7:
                        input_text_c += '7'
                    if event.key == K_8:
                        input_text_c += '8'
                    if event.key == K_9:
                        input_text_c += '9'
                    if event.key == K_0:
                        input_text_c += '0'
                    if event.key == K_BACKSPACE:
                        input_text_c = input_text_c[:len(input_text_c) - 1]
                    print(input_text_c)

            if len(input_text_c) > 0:
                base = int(input_text_c)

        if vel_rect.collidepoint((mx, my)):
            draw_text('Speed:', main_font, (100, 10, 100), WIN, WIDTH / 2 + 100, 500)
            WIN.blit(text_surface_v, (WIDTH / 2 + 200, 500))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        input_text_v += '1'
                    if event.key == K_2:
                        input_text_v += '2'
                    if event.key == K_3:
                        input_text_v += '3'
                    if event.key == K_4:
                        input_text_v += '4'
                    if event.key == K_5:
                        input_text_v += '5'
                    if event.key == K_6:
                        input_text_v += '6'
                    if event.key == K_7:
                        input_text_v += '7'
                    if event.key == K_8:
                        input_text_v += '8'
                    if event.key == K_9:
                        input_text_v += '9'
                    if event.key == K_0:
                        input_text_v += '0'
                    if event.key == K_BACKSPACE:
                        input_text_v = input_text_v[:len(input_text_v) - 1]
                    print(input_text_v)

            if len(input_text_v) > 0:
                cell_vel = int(input_text_v)


        if enter.collidepoint((mx, my)):
            if click:
                print("enter")
                print("pixel_res")
                print(pixel_res)
                draw_text('Enter', main_font, (255, 255, 255), WIN, WIDTH / 2 - 100, 800)
                Chaos_Window(base, pixel_res, cell_vel, analytics, device_id)

        if analytics_button.collidepoint((mx, my)):
            if click:
                print('analytics on')

                if analytics == 0:

                    analytics = 1

                else:

                    analytics = 0

            draw_text('analytics: ' + str(analytics), main_font, (0, 192, 192), WIN, WIDTH / 2 + 480, 300)


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


#pygame.midi interface

def print_device_into():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )

def input_main(device_id=None):

    pygame.init()
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    #rtmidi init
    # midiout = rtmidi.MidiOut()
    # available_ports = midiout.get_port_name(1)
    # print(" ")
    # print("midiout")
    # print(midiout)
    # print("available ports")
    # print(available_ports)
    #
    # if available_ports:
    #     midiout.open_port(1)
    # else:
    #     midiout.open_virtual_port('My virtual output')

    pygame.midi.init()

    print(" ")
    print("device info")
    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print(' ')
    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)

    # print('i')
    # print(i)
    #
    # print(" ")
    # print("device info")
    # _print_device_info()

    pygame.display.set_mode((1, 1))
    going = True

    while going:
        events = event_get()
        for e in events:

            # print(" ")
            # print('e')
            # print(e)
            # print(type(e))


            if e.type in [pygame.QUIT]:
                going = False
            if e.type in [pygame.KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:

                # print(e)

                clean_e = str(e)[21:-3]
                list_e = clean_e.split(',')
                ev = []
                for l in list_e:
                    ev.append(int(l.split(':')[1]))

                # print(" ")
                # print("ev")
                # print(ev)
                # print(e)

                # if ev[0] == 144:
                #     midiout.send_noteon(ev[0], ev[1], ev[2])
                # elif ev[0] == 128:
                #     midiout.send_noteoff(ev[0], ev[1])

        if i.poll():

            # print(' ')
            # print('i')
            # print(i)

            midi_events = i.read(10)
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)

    del i
    pygame.midi.quit()


# input_main()


# menu()


Chaos_Window(5, 2, 1, 1, 2)




