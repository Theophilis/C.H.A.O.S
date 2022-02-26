import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import matplotlib
import pandas as pd
from datetime import datetime
import random
import pygame
pygame.font.init()
import os
import sqlite3
import pickle
import time


length = 8
#number of times given rule is applied and number of initial rows generated
width = length * 2 + 1
#number of cells in a row
rule = 90
#number who's x_base transformation gives the rules dictionary its values
view = 3
#size of the view window that scans a row for rule application
base = 2
#numerical base of the rule set. number of colors each cell can be
start = length
#position for a row 0 cell value 1
direction = 0
#if ^ = 0 view scans from left to right: else view scans right to left

# conn = sqlite3.connect("database.db")
# c = conn.cursor()

#####to do#####
#translate complex numbers (pi, phi, e) to a base n digit sequence(where n is the number of possible rule states to be called).
#Then, trigger a rotation of a rule state based on the rule position given by the digit in the complex number


#####map#####
def base_x(n, b):
    e = n//b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def rule_gen(rule, base = 2):
    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_x(rule, base)

    x = int_rule[::-1]

    while len(x) < base ** view:
        x += '0'

    bnr = x[::-1]
    int_rul = list(bnr)
    # print(" ")
    # print("int_rule")
    # [print(int_rule)]
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


def viewer(c_a, y, view, v_0):

    # print('view')
    # print(view)
    # print("v_0_v")
    # print(v_0)
    # print(len(v_0))

    if len(v_0) % 2 == 1:

        if y + len(v_0) > len(c_a) - 1:

            v_0.append('0')

        else:

            v_0.append(str(c_a[y + int(len(v_0) / 2) + 1]))

    else:

        if y - len(v_0) < 0:

            v_0.insert(0, '0')

        else:

            v_0.insert(0, str(c_a[int(y - len(v_0) / 2)]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer(c_a, y, view, v_0)

        return v_0


def Color(color, d_rule, cell_row_width, base, row_0):

    color_n = []
    rc = []
    if base == 2:
        row_0 = np.zeros((1, cell_row_width), dtype='int8')
        for c in color:
            row_0[0, c] = 1
    row_1 = np.zeros((1, cell_row_width), dtype='int8')


    for y in range(len(row_0[0])):

        if direction != 0:
            y = len(row_0) - y - 1

        v_0 = []

        # print(" ")
        # print("y")
        # print(y)

        v_0 = tuple(viewer(row_0[0], y, view, v_0))

        # print("v_0")
        # print(v_0)
        #
        # print("rule")
        # print(d_rule[v_0])

        rc.append(list(d_rule.keys()).index(v_0))

        row_1[0, y] = d_rule[v_0]
        if int(d_rule[v_0]) == 1:
            # print("bingo")
            # print(y)
            color_n.append(y)
            rc.append(list(d_rule.keys()).index(v_0))

    record.append(color_n)
    # print("Color")
    # print(row_1)
    # print(type(row_1))
    # print(rc)

    return color_n, rc, row_1


#####game#####

WIDTH, HEIGHT = 1750, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK_PIXEL_1 = pygame.image.load(os.path.join('assets', 'black-2.png')).convert()
M_GREEN_PIXEL_1 = pygame.image.load(os.path.join('assets', 'cyan-d-2.png')).convert()
PURPLE_PIXEL_1 = pygame.image.load(os.path.join('assets', 'magenta-d-2.png')).convert_alpha()
YELLOW_PIXEL_1 = pygame.image.load(os.path.join('assets', 'yellow-d-2.png'))
BLUE_PIXEL_0 = pygame.image.load(os.path.join('assets', 'black-2.png')).convert_alpha()


pygame.init()

pygame.display.set_caption("C311UL4R H4PT1C 4T0M4T4 0P3R4T1NG 5Y5T3M")

record = []

class Pixel:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

class Player(Pixel):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health

class Cell(Pixel):
    COLOR_MAP = {
                'blue_0' : (BLUE_PIXEL_0),

                "black_1": (BLACK_PIXEL_1),
                'yellow_1': (YELLOW_PIXEL_1),
                'green_1': (M_GREEN_PIXEL_1),
                'purple_1': (PURPLE_PIXEL_1)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, vel):
        self.y += vel

def main():

    run = True
    FPS = 30
    rule = 21621
    step = 0
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("arial", 32)
    journal = dict()
    page = []
    press = dict()

    # infile = open("cell-journal", "rb")
    # journal = pickle.load(infile)
    # infile.close

    print("journal type")
    print(type(journal))

    r_c = 0
    base = 3
    haptic = 0
    held = 1

    cells = []
    cell_row_width = int(WIDTH/BLUE_PIXEL_0.get_width())
    cell_rows = int(HEIGHT/BLUE_PIXEL_0.get_height()) + 1
    cell_vel = 5

    d_rule, i_rule = rule_gen(rule, base)


    print(" ")
    print("d_rule")
    print(d_rule)
    print("i_rule")
    print(i_rule)
    print(len(i_rule))


    def redraw_window():

        for r in range(cell_rows):
            for cell in cells[r]:
                cell.draw(WIN)

        rule_label_0 = main_font.render(f"RUL3: {i_rule[0:int((base**view)/2)]}", 1, (130, 130, 130))
        rule_label_1 = main_font.render(f"            {i_rule[int((base**view)/2):int((base**view))]}", 1, (130, 130, 130))

        step_label = main_font.render(f"5T3P: {step}", 1, (255, 255, 255))

        WIN.blit(rule_label_0, (10,  HEIGHT - 120))
        WIN.blit(rule_label_1, (10, HEIGHT - 80))
        WIN.blit(step_label, (WIDTH - step_label.get_width()-10, 10))

        pygame.display.update()

    def mitosis(i, r, color, rc, row):

        if r > 0:

            if r_c == 1:
                # full rc spectrum
                if i in color:
                    if rc[i] == 0:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'black_1')
                        cells[r].append(cell)
                    if rc[i] == 1:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'white_1')
                        cells[r].append(cell)
                    if rc[i] == 2:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'red_1')
                        cells[r].append(cell)
                    if rc[i] == 3:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'orange_1')
                        cells[r].append(cell)
                    if rc[i] == 4:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'yellow_1')
                        cells[r].append(cell)
                    if rc[i] == 5:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'green_1')
                        cells[r].append(cell)
                    if rc[i] == 6:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'blue_1')
                        cells[r].append(cell)
                    if rc[i] == 7:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'purple_1')
                        cells[r].append(cell)
                else:
                    if rc[i] == 0:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'black_0')
                        cells[r].append(cell)
                    if rc[i] == 1:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'white_0')
                        cells[r].append(cell)
                    if rc[i] == 2:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'red_0')
                        cells[r].append(cell)
                    if rc[i] == 3:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'orange_0')
                        cells[r].append(cell)
                    if rc[i] == 4:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'yellow_0')
                        cells[r].append(cell)
                    if rc[i] == 5:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'green_0')
                        cells[r].append(cell)
                    if rc[i] == 6:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'blue_0')
                        cells[r].append(cell)
                    if rc[i] == 7:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'purple_0')
                        cells[r].append(cell)

            elif r_c == 2:
                # positive rc
                if i in color:
                    if rc[i] == 0:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'black_0')
                        cells[r].append(cell)
                    if rc[i] == 1:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'white_1')
                        cells[r].append(cell)
                    if rc[i] == 2:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'red_1')
                        cells[r].append(cell)
                    if rc[i] == 3:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'orange_1')
                        cells[r].append(cell)
                    if rc[i] == 4:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'yellow_1')
                        cells[r].append(cell)
                    if rc[i] == 5:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'green_1')
                        cells[r].append(cell)
                    if rc[i] == 6:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'blue_1')
                        cells[r].append(cell)
                    if rc[i] == 7:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                    'purple_1')
                        cells[r].append(cell)
                else:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'black_1')
                    cells[r].append(cell)

            elif base == 2:
                if row[0, i] == 0:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'black_1')
                    cells[r].append(cell)
                if row[0, i] == 1:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'blue_1')
                    cells[r].append(cell)

            elif base == 3:
                if row[0, i] == 0:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'black_1')
                    cells[r].append(cell)
                if row[0, i] == 1:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'purple_1')
                    cells[r].append(cell)
                if row[0, i] == 2:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'green_1')
                    cells[r].append(cell)

            elif base == 4:
                if row[0, i] == 0:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'black_1')
                    cells[r].append(cell)
                if row[0, i] == 1:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'purple_1')
                    cells[r].append(cell)
                if row[0, i] == 2:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'green_1')
                    cells[r].append(cell)
                if row[0, i] == 3:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, cells[r - 1][i].y - BLUE_PIXEL_0.get_height(),
                                'yellow_1')
                    cells[r].append(cell)

        else:

            if r_c == 1:
                # full rc spectrum
                if i in color:
                    # print(type(cells[0]))
                    if rc[i] == 0:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'black_1')
                        cells[r].append(cell)
                    if rc[i] == 1:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'white_1')
                        cells[r].append(cell)
                    if rc[i] == 2:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'red_1')
                        cells[r].append(cell)
                    if rc[i] == 3:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'orange_1')
                        cells[r].append(cell)
                    if rc[i] == 4:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'yellow_1')
                        cells[r].append(cell)
                    if rc[i] == 5:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'green_1')
                        cells[r].append(cell)
                    if rc[i] == 6:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'blue_1')
                        cells[r].append(cell)
                    if rc[i] == 7:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'purple_1')
                        cells[r].append(cell)
                else:
                    if rc[i] == 0:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'black_0')
                        cells[r].append(cell)
                    if rc[i] == 1:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'white_0')
                        cells[r].append(cell)
                    if rc[i] == 2:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'red_0')
                        cells[r].append(cell)
                    if rc[i] == 3:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'orange_0')
                        cells[r].append(cell)
                    if rc[i] == 4:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'yellow_0')
                        cells[r].append(cell)
                    if rc[i] == 5:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'green_0')
                        cells[r].append(cell)
                    if rc[i] == 6:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'blue_0')
                        cells[r].append(cell)
                    if rc[i] == 7:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'purple_0')
                        cells[r].append(cell)

            elif r_c == 2:
                # positive rc
                if i in color:
                    # print(type(cells[0]))
                    if rc[i] == 0:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'black_0')
                        cells[r].append(cell)
                    if rc[i] == 1:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'white_1')
                        cells[r].append(cell)
                    if rc[i] == 2:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'red_1')
                        cells[r].append(cell)
                    if rc[i] == 3:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'orange_1')
                        cells[r].append(cell)
                    if rc[i] == 4:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'yellow_1')
                        cells[r].append(cell)
                    if rc[i] == 5:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'green_1')
                        cells[r].append(cell)
                    if rc[i] == 6:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'blue_1')
                        cells[r].append(cell)
                    if rc[i] == 7:
                        cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'purple_1')
                        cells[r].append(cell)
                # full rc spectrum
                else:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'black_1')
                    cells[r].append(cell)

            elif base == 2:
                if row[0, i] == 0:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'black_1')
                    cells[r].append(cell)
                if row[0, i] == 1:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'blue_1')
                    cells[r].append(cell)

            elif base == 3:
                if row[0, i] == 0:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, -BLUE_PIXEL_0.get_height() + 2, 'black_1')
                    cells[r].append(cell)
                if row[0, i] == 1:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, -BLUE_PIXEL_0.get_height() + 2, 'purple_1')
                    cells[r].append(cell)
                if row[0, i] == 2:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, -BLUE_PIXEL_0.get_height() + 2, 'green_1')
                    cells[r].append(cell)

            elif base == 4:
                if row[0, i] == 0:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, -BLUE_PIXEL_0.get_height() + 2, 'black_1')
                    cells[r].append(cell)
                if row[0, i] == 1:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, -BLUE_PIXEL_0.get_height() + 2, 'purple_1')
                    cells[r].append(cell)
                if row[0, i] == 2:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, -BLUE_PIXEL_0.get_height() + 2, 'green_1')
                    cells[r].append(cell)
                if row[0, i] == 3:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, -BLUE_PIXEL_0.get_height() + 2, 'yellow_1')
                    cells[r].append(cell)


    last_step = 0

    for r in range(cell_rows):
        cells.append([])

    color =[int(cell_row_width/2)]
    row = np.zeros((1, cell_row_width), dtype='int8')
    for c in color:
        row[0, c] = 1

    # print(" ")
    # print("color")
    # print(color)
    while run:

        redraw_window()

        clock.tick(FPS)
        # print("")
        # print("cell_rows")
        # print(cell_rows)
        for r in range(cell_rows):

            if len(cells[r]) == 0:

                color, rc, row = Color(color, d_rule, cell_row_width, base, row)

                row_l = np.ndarray.tolist(row)
                line = (row_l, rc)

                if line in page:

                    # print("duplicate")

                    rand = random.randrange(0, 26)

                    # print(rand)
                    # print(i_rule)
                    # print(d_rule)

                    if rule not in journal:
                        journal[rule] = []
                        journal[rule].append(page)
                    else:
                        journal[rule].append(page)
                    page = []

                    if i_rule[rand] == 0:

                        i_rule[rand] = 1
                        d_rule[list(d_rule.keys())[rand]] = 1

                    elif i_rule[rand] == 1:
                        i_rule[rand] = 2
                        d_rule[list(d_rule.keys())[rand]] = 2

                    else:
                        i_rule[rand] = 0
                        d_rule[list(d_rule.keys())[rand]] = 0

                    # print("change")
                    # print(i_rule)
                    # print(d_rule)

                else:
                    page.append((row_l, rc))

                step += 1

                for i in range(cell_row_width):

                    mitosis(i, r, color, rc, row)



        #keyboard inputs

        delay = 1
        keys = pygame.key.get_pressed()

        if base == 2:

            if keys[pygame.K_a] and step - last_step > delay:
                if i_rule[0] == 0:

                    i_rule[0] = 1
                    d_rule[list(d_rule.keys())[0]] = 1

                else:
                    i_rule[0] = 0
                    d_rule[list(d_rule.keys())[0]] = 0

                last_step = step

            if keys[pygame.K_s] and step - last_step > delay:
                if i_rule[1] == 0:

                    i_rule[1] = 1
                    d_rule[list(d_rule.keys())[1]] = 1

                else:
                    i_rule[1] = 0
                    d_rule[list(d_rule.keys())[1]] = 0

                last_step = step

            if keys[pygame.K_d] and step - last_step > delay:
                if i_rule[2] == 0:

                    i_rule[2] = 1
                    d_rule[list(d_rule.keys())[2]] = 1

                else:
                    i_rule[2] = 0
                    d_rule[list(d_rule.keys())[2]] = 0

                last_step = step

            if keys[pygame.K_f] and step - last_step > delay:
                if i_rule[3] == 0:

                    i_rule[3] = 1
                    d_rule[list(d_rule.keys())[3]] = 1

                else:
                    i_rule[3] = 0
                    d_rule[list(d_rule.keys())[3]] = 0

                last_step = step

            if keys[pygame.K_j] and step - last_step > delay:
                if i_rule[4] == 0:

                    i_rule[4] = 1
                    d_rule[list(d_rule.keys())[4]] = 1

                else:
                    i_rule[4] = 0
                    d_rule[list(d_rule.keys())[4]] = 0

                last_step = step

            if keys[pygame.K_k] and step - last_step > delay:
                if i_rule[5] == 0:

                    i_rule[5] = 1
                    d_rule[list(d_rule.keys())[5]] = 1

                else:
                    i_rule[5] = 0
                    d_rule[list(d_rule.keys())[5]] = 0

                last_step = step

            if keys[pygame.K_l] and step - last_step > delay:
                if i_rule[6] == 0:

                    i_rule[6] = 1
                    d_rule[list(d_rule.keys())[6]] = 1

                else:
                    i_rule[6] = 0
                    d_rule[list(d_rule.keys())[6]] = 0

                last_step = step

            if keys[pygame.K_SEMICOLON] and step - last_step > delay:
                if i_rule[7] == 0:

                    i_rule[7] = 1
                    d_rule[list(d_rule.keys())[7]] = 1

                else:
                    i_rule[7] = 0
                    d_rule[list(d_rule.keys())[7]] = 0
                last_step = step

        if base == 3:

            if held == 1:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_q:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 0
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_w:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            journal[rule] = page
                            page = []

                            place = 1
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_e:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 2
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_r:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 3
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_t:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 4
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_y:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 5
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_u:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 6
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_i:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 7
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_o:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 8
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_p:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 9
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_a:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 10
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_s:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 11
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_d:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 12
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_f:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 13
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_g:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 14
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_h:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 15
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_j:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 16
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_k:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 17
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_l:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 18
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_PERIOD:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 19
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_z:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 20
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_x:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 21
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_c:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 22
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_v:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 23
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_b:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 24
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_n:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 25
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_m:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            place = 26
                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

            else:

                if keys[pygame.K_q] and step - last_step > delay:

                    place = 0
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_w] and step - last_step > delay:

                    place = 1
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_e] and step - last_step > delay:

                    place = 2
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_r] and step - last_step > delay:

                    place = 3
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_t] and step - last_step > delay:

                    place = 4
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_y] and step - last_step > delay:

                    place = 5
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_u] and step - last_step > delay:

                    place = 6
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_i] and step - last_step > delay:

                    place = 7
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_o] and step - last_step > delay:

                    place = 8
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_p] and step - last_step > delay:

                    place = 9
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_a] and step - last_step > delay:

                    place = 10
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_s] and step - last_step > delay:

                    place = 11
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_d] and step - last_step > delay:

                    place = 12
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_f] and step - last_step > delay:

                    place = 13
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_g] and step - last_step > delay:

                    place = 14
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_h] and step - last_step > delay:

                    place = 15
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_j] and step - last_step > delay:

                    place = 16
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_k] and step - last_step > delay:

                    place = 17
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_l] and step - last_step > delay:

                    place = 18
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_SEMICOLON] and step - last_step > delay:

                    place = 19
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_z] and step - last_step > delay:

                    place = 20
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_x] and step - last_step > delay:

                    place = 21
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_c] and step - last_step > delay:

                    place = 22
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_v] and step - last_step > delay:

                    place = 23
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_b] and step - last_step > delay:

                    place = 24
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_n] and step - last_step > delay:

                    place = 25
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

                if keys[pygame.K_m] and step - last_step > delay:

                    place = 26
                    if i_rule[place] == 0:

                        i_rule[place] = 1
                        d_rule[list(d_rule.keys())[place]] = 1

                    elif i_rule[place] == 1:
                        i_rule[place] = 2
                        d_rule[list(d_rule.keys())[place]] = 2

                    else:
                        i_rule[place] = 0
                        d_rule[list(d_rule.keys())[place]] = 0
                    last_step = step

        if base == 4:

            if held == 1:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_q:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []


                            if 'q' not in press:
                                press['q'] = 1
                            else:
                                press['q'] += 1

                            place = 0 + (((press['q'] % 3) - 1) * 27) % (base ** view)


                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_w:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []


                            if 'w' not in press:
                                press['w'] = 1
                            else:
                                press['w'] += 1

                            place = 1 + (((press['w'] % 3) - 1) * 27) % (base ** view)


                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_e:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'e' not in press:
                                press['e'] = 1
                            else:
                                press['e'] += 1

                            place = 2 + (((press['e'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_r:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'r' not in press:
                                press['r'] = 1
                            else:
                                press['r'] += 1

                            place = 3 + (((press['r'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_t:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 't' not in press:
                                press['t'] = 1
                            else:
                                press['t'] += 1

                            place = 4 + (((press['t'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_y:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'y' not in press:
                                press['y'] = 1
                            else:
                                press['y'] += 1

                            place = 5 + (((press['y'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_u:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'u' not in press:
                                press['u'] = 1
                            else:
                                press['u'] += 1

                            place = 6 + (((press['u'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_i:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'i' not in press:
                                press['i'] = 1
                            else:
                                press['i'] += 1

                            place = 7 + (((press['i'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_o:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'o' not in press:
                                press['o'] = 1
                            else:
                                press['o'] += 1

                            place = 8 + (((press['o'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_p:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'p' not in press:
                                press['p'] = 1
                            else:
                                press['p'] += 1

                            place = 9 + (((press['p'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_a:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'a' not in press:
                                press['a'] = 1
                            else:
                                press['a'] += 1

                            place = 10 + (((press['a'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_s:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 's' not in press:
                                press['s'] = 1
                            else:
                                press['s'] += 1

                            place = 11 + (((press['s'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_d:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'd' not in press:
                                press['d'] = 1
                            else:
                                press['d'] += 1

                            place = 12 + (((press['d'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_f:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'f' not in press:
                                press['f'] = 1
                            else:
                                press['f'] += 1

                            place = 13 + (((press['f'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_g:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'g' not in press:
                                press['g'] = 1
                            else:
                                press['g'] += 1

                            place = 14 + (((press['g'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_h:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'h' not in press:
                                press['h'] = 1
                            else:
                                press['h'] += 1

                            place = 15 + (((press['h'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_j:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'j' not in press:
                                press['j'] = 1
                            else:
                                press['j'] += 1

                            place = 16 + (((press['j'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_k:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'k' not in press:
                                press['k'] = 1
                            else:
                                press['k'] += 1

                            place = 17 + (((press['k'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_l:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'l' not in press:
                                press['l'] = 1
                            else:
                                press['l'] += 1

                            place = 18 + (((press['l'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_z:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'z' not in press:
                                press['z'] = 1
                            else:
                                press['z'] += 1

                            place = 19 + (((press['z'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_x:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'x' not in press:
                                press['x'] = 1
                            else:
                                press['x'] += 1

                            place = 20 + (((press['x'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_c:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'c' not in press:
                                press['c'] = 1
                            else:
                                press['c'] += 1

                            place = 21 + (((press['c'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_v:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'v' not in press:
                                press['v'] = 1
                            else:
                                press['v'] += 1

                            place = 22 + (((press['v'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_b:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'b' not in press:
                                press['b'] = 1
                            else:
                                press['b'] += 1

                            place = 23 + (((press['b'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_n:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'n' not in press:
                                press['n'] = 1
                            else:
                                press['n'] += 1

                            place = 24 + (((press['n'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_m:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if 'm' not in press:
                                press['m'] = 1
                            else:
                                press['m'] += 1

                            place = 25 + (((press['m'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

                        if event.key == pygame.K_PERIOD:

                            if rule not in journal:
                                journal[rule] = []
                                journal[rule].append(page)
                            else:
                                journal[rule].append(page)
                            page = []

                            if '.' not in press:
                                press['.'] = 1
                            else:
                                press['.'] += 1

                            place = 26 + (((press['.'] % 3) - 1) * 27) % (base ** view)

                            if i_rule[place] == 0:

                                i_rule[place] = 1
                                d_rule[list(d_rule.keys())[place]] = 1

                            elif i_rule[place] == 1:
                                i_rule[place] = 2
                                d_rule[list(d_rule.keys())[place]] = 2

                            elif i_rule[place] == 2:
                                i_rule[place] = 3
                                d_rule[list(d_rule.keys())[place]] = 3

                            else:
                                i_rule[place] = 0
                                d_rule[list(d_rule.keys())[place]] = 0
                            last_step = step

        for r in range(cell_rows):
            for cell in cells[r][:]:
                cell.move(cell_vel)
                if cell.y + cell.get_height() > HEIGHT:
                    cells[r].remove(cell)

    filename = 'cell-journal'
    outfile = open(filename, 'wb')
    pickle.dump(journal, outfile)
    outfile.close

    if haptic == 0:
        redraw_window()

main()




















