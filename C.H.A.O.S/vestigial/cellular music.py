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
import rtmidi2 as rtmidi
import pygame.midi


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

BLACK_PIXEL_1 = pygame.image.load(os.path.join('../assets', 'black-2.png')).convert()
WHITE_PIXEL_1 = pygame.image.load(os.path.join('../assets', 'grey-2.png')).convert()
M_GREEN_PIXEL_1 = pygame.image.load(os.path.join('../assets', 'cyan-2.png')).convert()
BLUE_PIXEL_1 = pygame.image.load(os.path.join('../assets', 'cyan-2.png')).convert_alpha()
PURPLE_PIXEL_1 = pygame.image.load(os.path.join('../assets', 'magenta-2.png')).convert_alpha()
RED_PIXEL_1 = pygame.image.load(os.path.join('../assets', "magenta-2.png"))
ORANGE_PIXEL_1 = pygame.image.load(os.path.join('../assets', 'orange-2.png'))
YELLOW_PIXEL_1 = pygame.image.load(os.path.join('../assets', 'yellow-2.png'))

BLACK_PIXEL_0 = pygame.image.load(os.path.join('../assets', 'black-2.png')).convert()
WHITE_PIXEL_0 = pygame.image.load(os.path.join('../assets', 'grey-2.png')).convert()
M_GREEN_PIXEL_0 = pygame.image.load(os.path.join('../assets', 'moss-2.png')).convert()
BLUE_PIXEL_0 = pygame.image.load(os.path.join('../assets', 'cyan-2.png')).convert_alpha()
PURPLE_PIXEL_0 = pygame.image.load(os.path.join('../assets', 'magenta-2.png')).convert_alpha()
RED_PIXEL_0 = pygame.image.load(os.path.join('../assets', "magenta-2.png"))
ORANGE_PIXEL_0 = pygame.image.load(os.path.join('../assets', 'orange-2.png'))
YELLOW_PIXEL_0 = pygame.image.load(os.path.join('../assets', 'yellow-2.png'))

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
                "black_0" : (BLACK_PIXEL_0),
                'white_0' : (WHITE_PIXEL_0),
                'red_0' : (RED_PIXEL_0),
                'orange_0' : (ORANGE_PIXEL_0),
                'yellow_0' : (YELLOW_PIXEL_0),
                'green_0' : (M_GREEN_PIXEL_0),
                'blue_0' : (BLUE_PIXEL_0),
                'purple_0' : (PURPLE_PIXEL_0),

                "black_1": (BLACK_PIXEL_1),
                'white_1': (WHITE_PIXEL_1),
                'red_1': (RED_PIXEL_1),
                'orange_1': (ORANGE_PIXEL_1),
                'yellow_1': (YELLOW_PIXEL_1),
                'green_1': (M_GREEN_PIXEL_1),
                'blue_1': (BLUE_PIXEL_1),
                'purple_1': (PURPLE_PIXEL_1)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, vel):
        self.y += vel

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

def main(device_id=None):

    run = True
    FPS = 30
    rule = 232731
    step = 0
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("arial", 32)
    journal = dict()
    page = []

    print("")
    print("journal type")
    print(type(journal))


    r_c = 0
    base = 3
    haptic = 0
    held = 1
    midi = 1

    cells = []
    cell_row_width = int(WIDTH/BLUE_PIXEL_0.get_width())
    cell_rows = int(HEIGHT/BLUE_PIXEL_0.get_height())
    cell_vel = 10

    d_rule, i_rule = rule_gen(rule, base)

    pygame.init()
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    #rtmidi init
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_port_name(5)
    print(" ")
    print("available_ports")
    print(available_ports)
    if available_ports:
        midiout.open_port(5)
    else:
        midiout.open_virtual_port('My virtual output')

    pygame.midi.init()
    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id :%s:" % input_id)
    midin = pygame.midi.Input(input_id)

    #rule print
    print(" ")
    print("d_rule")
    print(d_rule)
    print("i_rule")
    print(i_rule)

    def redraw_window():

        for r in range(cell_rows):
            for cell in cells[r]:
                cell.draw(WIN)

        rule_label = main_font.render(f"RUL3: {i_rule}", 1, (255, 255, 255))
        step_label = main_font.render(f"5T3P: {step}", 1, (255, 255, 255))

        WIN.blit(rule_label, (10, 10))
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
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'black_1')
                    cells[r].append(cell)
                if row[0, i] == 1:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'purple_1')
                    cells[r].append(cell)
                if row[0, i] == 2:
                    cell = Cell(1 * BLUE_PIXEL_0.get_width() * i, 0, 'green_1')
                    cells[r].append(cell)

    last_step = 0

    #row prep
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

        clock.tick(FPS)

        #midi event recognition
        events = event_get()
        for e in events:
            if e.type in [pygame.QUIT]:
                run = False
            if e.type in [pygame.KEYDOWN]:
                run = False
            if e.type in [pygame.midi.MIDIIN]:

                print(e)
                clean_e = str(e)[21:-3]
                list_e = clean_e.split(',')
                ev = []
                count = 0

                for l in list_e:
                    ev.append(int(l.split(':')[1]))

                print("ev")
                print(ev)
                if ev[0] == 144:
                    midiout.send_noteon(ev[0], ev[1], ev[2])

                    for rl in range(1, 28):



                        if ev[1] % 27 == rl:

                            print("pre rules")
                            print(i_rule[rl])
                            print(d_rule[list(d_rule.keys())[rl]])
                            print("rl")
                            print(rl)

                            if i_rule[rl] == 0:
                                print("rl 0")
                                i_rule[rl] = 1
                                d_rule[list(d_rule.keys())[rl]] = 1

                            elif i_rule[rl] == 1:
                                print("rl 1")
                                i_rule[rl] = 2
                                d_rule[list(d_rule.keys())[rl]] = 2

                            elif i_rule[rl] == 2:
                                print("rl 2")
                                i_rule[rl] = 0
                                d_rule[list(d_rule.keys())[rl]] = 0

                            print("post rules")
                            print(i_rule[rl])
                            print(d_rule[list(d_rule.keys())[rl]])
                    # if ev[1] % 8 == 1:
                    #     place = 1
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 2:
                    #     place = 2
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 3:
                    #     place = 3
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 4:
                    #     place = 4
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 5:
                    #     place = 5
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 6:
                    #     place = 6
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 7:
                    #     place = 7
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 0:
                    #     place = 0
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 1:
                    #     place = 1
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 2:
                    #     place = 2
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 3:
                    #     place = 3
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 4:
                    #     place = 4
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 5:
                    #     place = 5
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 6:
                    #     place = 6
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 7:
                    #     place = 7
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 0:
                    #     place = 0
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 1:
                    #     place = 1
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 2:
                    #     place = 2
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 3:
                    #     place = 3
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 4:
                    #     place = 4
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 5:
                    #     place = 5
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 6:
                    #     place = 6
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 7:
                    #     place = 7
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 0:
                    #     place = 0
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 1:
                    #     place = 1
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 2:
                    #     place = 2
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 3:
                    #     place = 3
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 4:
                    #     place = 4
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 5:
                    #     place = 5
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 6:
                    #     place = 6
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0
                    #
                    # if ev[1] % 8 == 7:
                    #     place = 7
                    #     if i_rule[place] == 0:
                    #
                    #         i_rule[place] = 1
                    #         d_rule[list(d_rule.keys())[place]] = 1
                    #
                    #     else:
                    #         i_rule[place] = 0
                    #         d_rule[list(d_rule.keys())[place]] = 0


                elif ev[0] == 128:
                    midiout.send_noteoff(ev[0], ev[1])


        if midin.poll():
            midi_events = midin.read(10)
            midi_evs = pygame.midi.midis2events(midi_events, midin.device_id)

            for m_e in midi_evs:
                event_post(m_e)

        for r in range(cell_rows):

            if len(cells[r]) == 0:

                color, rc, row = Color(color, d_rule, cell_row_width, base, row)

                # row_l = np.ndarray.tolist(row)
                # line = (row_l, rc)
                #
                # if line in page:
                #
                #     # print("duplicate")
                #
                #     rand = random.randrange(0, 7)
                #
                #     # print(rand)
                #     # print(i_rule)
                #     # print(d_rule)
                #
                #     if rule not in journal:
                #         journal[rule] = []
                #         journal[rule].append(page)
                #     else:
                #         journal[rule].append(page)
                #     page = []
                #
                #     if i_rule[rand] == 0:
                #
                #         i_rule[rand] = 1
                #         d_rule[list(d_rule.keys())[rand]] = 1
                #
                #     elif i_rule[rand] == 1:
                #         i_rule[rand] = 2
                #         d_rule[list(d_rule.keys())[rand]] = 2
                #
                #     else:
                #         i_rule[rand] = 0
                #         d_rule[list(d_rule.keys())[rand]] = 0
                #
                #     # print("change")
                #     # print(i_rule)
                #     # print(d_rule)
                #
                # else:
                #     page.append((row_l, rc))
                #
                # step += 1

                for i in range(cell_row_width):

                    mitosis(i, r, color, rc, row)

        redraw_window()

        # for event in pygame.event.get():


        #keyboard inputs

        delay = 1
        keys = pygame.key.get_pressed()

        if midi == 0:

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

            #####base 3#####
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

                            if event.key == pygame.K_SEMICOLON:

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


        for r in range(cell_rows):
            for cell in cells[r][:]:
                cell.move(cell_vel)
                if cell.y + cell.get_height() > HEIGHT:
                    cells[r].remove(cell)

    del midin

    filename = 'cell-journal'
    outfile = open(filename, 'wb')
    pickle.dump(journal, outfile)
    outfile.close

    if haptic == 0:
        redraw_window()

main()



# for r in record:
#     print(record.index(r))
#     print(r)



















