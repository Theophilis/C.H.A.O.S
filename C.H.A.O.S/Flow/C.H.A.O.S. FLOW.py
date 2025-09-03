# C.H.A.O.S

import numpy as np
import pygame
import os
import pickle
import sys
import pygame.midi
import time
import matplotlib.pyplot as plt
from matplotlib import colors as c
from os import listdir

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

def base_xx(n, b):
    e = n // b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q) + ','
    else:
        return base_xx(e, b) + str(q) + ","

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

    return rules, int_rule[:base ** view]

def rule_gen_xx(rule, base=2):

    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_xx(int(rule), (base))

    int_rule = int_rule.split(',')[:-1]

    x = int_rule[::-1]

    while len(x) < base ** view:
        x += '0'

    bnr = x[::-1]
    int_rul = list(bnr)
    int_rule = []
    for i in int_rul:
        if i != ',':
            int_rule.append(int(i))

    for x in reversed(range(len(int_rule))):

        key = base_xx(x, base)
        key = list(key.split(',')[:-1])

        if len(key) < view:

            for y in range((view - len(key))):
                key.insert(0, '0')

        rules[tuple(key)] = int(int_rule[-x - 1])

    return rules, int_rule[:base ** view]

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

def viewer_1d(row, y, view, v_0, color_value):

    # print('view')
    # print(view)
    # print("v_0_v")
    # print(v_0)
    # print(len(v_0))

    if len(v_0) % 2 == 1:

        if y + len(v_0) > len(row) - 1:

            v_0.append('0')

        else:

            v_0.append(str(color_value[tuple(row[y + int(len(v_0) / 2) + 1])]))

    else:

        if y - len(v_0) < -1:

            v_0.insert(0, '0')

        else:

            v_0.insert(0, str(color_value[tuple(row[int(y - len(v_0) / 2)])]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer_1d(row, y, view, v_0, color_value)

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
WIDTH , HEIGHT = current_display.current_w - 50, current_display.current_h - 100
# WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
letter_values = {'q': 0, 'w': 1, 'e': 2, 'r': 3, 't': 4, 'y': 5, 'u': 6, 'i': 7, 'o': 8, 'p': 9, 'a': 10, 's': 11,
                 'd': 12, 'f': 13,
                 'g': 14, 'h': 15, 'j': 16, 'k': 17, 'l': 18, 'z': 19, 'x': 20, 'c': 21, 'v': 22, 'b': 23, 'n': 24,
                 'm': 25, ' ': 0}

pygame.display.set_caption("C.H.A.O.S")

click = False

mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)


def draw_text(text, font, color_dt, surface, x, y):
    textobj = font.render(text, 1, color_dt)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

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

def viewer(row, y, view, v_0):

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

        if y - len(v_0) < 0:

            v_0.insert(0, '0')

        else:

            v_0.insert(0, str(row[int(y - len(v_0) / 2)]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer(row, y, view, v_0)

        return v_0

def Color_cells(d_rule, cell_row_width, row_0):

    rc = []
    row_1 = [0 for x in range(cell_row_width)]

    for y in range(len(row_0)):

        # if direction != 0:
        #     y = len(row_0) - y - 1

        v_0 = []

        # print(" ")
        # print("y")
        # print(y)

        v_0 = tuple(viewer(row_0, y, view, v_0))

        # print("v_0")
        # print(v_0)
        #
        # print("rule")
        # print(d_rule[v_0])

        rc.append(list(d_rule.keys()).index(v_0))

        # print("color_cells")
        # print("y")
        # print(y)
        # print('len(row_1)')
        # print(len(row_1))
        # print("v_0")
        # print(v_0)

        row_1[y] = int(d_rule[v_0])

    return row_1, rc

def rule_gen_s(rule, base = 2, width = 0, string = 0):

    rules = dict()

    if string != 0:
        int_rule = [l for l in rule]


    else:

        if base == 2:

            int_rule = bin(rule).replace('0b', '')


        else:

            int_rule = base_x(rule, base)


        x = int_rule[::-1]

        if width == 0:
            while len(x) < base ** view:

                x += '0'

            bnr = x[::-1]
            int_rule = list(bnr)

        else:
            while len(x) < width:
                x += '0'

            bnr = x[::-1]
            int_rule = list(bnr)

    # print(" ")
    # print("int_rule")
    # [print(int_rule)]


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

        rules[tuple(key)] = int_rule[-x - 1]

    # print("")
    # print("rules")
    # print(rules)

    return rules, int_rule



def synthesize(j_name, color_list, bookmark_choices, reflect, center_seed, scales):

    infile = open("journals/" + j_name, "rb")
    journal = pickle.load(infile)
    infile.close

    path = 'synthesis'

    print("len of journals")
    print(len(list(journal.keys())))
    print("bookmarks")
    print(journal['bookmarks'])
    bookmarks = journal['bookmarks']
    base = journal['base']

    print("color_list")
    print(color_list[:base])
    cMap = c.ListedColormap(color_list[:base])

    color_list_label = []
    for color in color_list:

        color_list_label.append((int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))

    journal_key = list(journal.keys())[1:]

    # print("")
    # print('journal_key')
    # print(journal_key)

    if len(bookmark_choices) == 0:

        print('journal')
        print(journal)


        for x in range(len(bookmarks)-1):

            try:
                synthesis = []
                frame = []
                width = 0

                # print()
                # print("bookmarks")
                # print(bookmarks[x], bookmarks[x + 1])

                if bookmarks[x+1] - bookmarks[x] < 1:
                    continue
                journal_bookmark = journal_key[bookmarks[x]:bookmarks[x + 1]]
                print()
                print("journal_bookmarks")
                print(journal_bookmark)

                for rule in journal_bookmark:

                    print('rule')
                    print(rule)
                    print(journal[rule])
                    frame.append((rule[0], journal[rule]))
                    # print()
                    # print("journal[rule]")
                    # print(journal[rule])
                    #
                    # print("rule")
                    # print(rule)

                    # if type(journal[rule]) != int:
                    #     continue

                    # if journal[rule] > 6400:
                    #     continue


                    width += journal[rule]



                # print("frame")
                # print(frame)
                #
                # print('width')
                # print(width)



                print('width')
                print(width)
                width = int(width * scales[2]/scales[3])
                print('width_scale')
                print(width)



                row = [0 for x in range(width)]
                if center_seed[0] == 1:
                    for y in range(base):
                        row[int(len(row) / 2) + y - base] = y

                synthesis.append(row)

                for f in frame:

                    count = 0

                    d_rule, i_rule = rule_gen_s(f[0], base, string=1)

                    try:
                        while count < int(f[1] * (scales[0]/scales[1]) + 1):
                            synthesis.append(Color_cells(d_rule, width, synthesis[-1])[0])

                            count += 1

                    except:
                        continue

                print()
                print(x)
                print("len syn")
                print(len(synthesis))

                j_name += str(bookmarks[x])

                # print("")
                # print("synthesis")
                # print(synthesis)

                file = str(x) + '-' + str(base) + '-' + j_name + '_length' + str(scales[0]) + '-' + str(scales[0]) + '_width' + str(
                    scales[0]) + '-' + str(scales[0]) + '_Colors-' + str(color_list_label)
                path_name = os.path.join(path, file)



                ax = plt.gca()
                ax.set_aspect(1)

                plt.margins(0, None)

                plt.pcolormesh(synthesis, cmap=cMap)

                # hide x-axis
                ax.get_xaxis().set_visible(False)

                # hide y-axis
                ax.get_yaxis().set_visible(False)

                print("printing")

                # plt.show()

                try:
                    plt.savefig(path_name, dpi=width, bbox_inches='tight', pad_inches=0)
                    plt.close()

                except:
                    file = str(x) + '-' + str(base) + '-' + j_name + '_length' + str(scales[0]) + '-' + str(scales[0]) + '_width' + str(
                        scales[0]) + '-' + str(scales[0]) + '_Colors-' + str(color_list_label)
                    path_name = os.path.join(path, file)

                    path_name = path_name[:127]
                    plt.savefig(path_name, dpi=width, bbox_inches='tight', pad_inches=0)
                    plt.close()

            except:
                continue

    else:

        try:
            journal_bookmark = []
            synthesis = []
            frame = []
            width = 0

            for b in bookmark_choices:
                for o in range(bookmarks[b] - bookmarks[b - 1]):
                    journal_bookmark.append(journal_key[bookmarks[b-1] + o])

            # print("journal bookmark")
            # print(journal_bookmark)
            # print(len(journal_bookmark))

            for rule in journal_bookmark:
                frame.append((rule[0], journal[rule]))
                width += journal[rule]

            # print('width')
            # print(width)

            width = int(width * scales[2]/scales[3])


            row = [0 for x in range(width)]

            if center_seed[0] == 1:
                for z in range(center_seed[1]):
                    z += 1
                    for y in range(base):
                        row[int(len(row) / (1 + center_seed[1])) * z + y - base] = y

            synthesis.append(row)

            for f in frame:

                count = 0

                d_rule, i_rule = rule_gen_s(f[0], base, string=1)

                while count < int(f[1] * (scales[0]/scales[1]) + 1):
                    synthesis.append(Color_cells(d_rule, width, synthesis[-1])[0])

                    count += 1

            print()
            print("width")
            print(width)
            print("len syn")
            print(len(synthesis))

            if reflect == 1:

                for s in reversed(synthesis[:]):
                    # print("")
                    # print("s")
                    # print(s)
                    # print(type(s))

                    # s = list(reversed(s[:]))

                    # print(s)
                    # print(type(s))

                    synthesis.append(s)

            if reflect == 2:

                synthesis = list(reversed(synthesis))

                for s in reversed(synthesis[:]):
                    synthesis.append(s)

            j_name += '-bookmarks-'
            j_name += str(bookmark_choices)

            # print("")
            # print("synthesis")
            # print(synthesis)

            file = str(base) + '-' + j_name + '_length' + str(scales[0]) + '-' + str(scales[1]) + '_width' + str(
                scales[2]) + '-' + str(scales[3]) + '_Colors-' + str(color_list_label) + '-' + str(reflect) + '-' + str(center_seed)
            path_name = os.path.join(path, file)

            ax = plt.gca()
            ax.set_aspect(1)

            plt.margins(0, None)

            plt.pcolormesh(synthesis, cmap=cMap)

            # hide x-axis
            ax.get_xaxis().set_visible(False)

            # hide y-axis
            ax.get_yaxis().set_visible(False)

            print("printing")

            # plt.show()
            plt.savefig(path_name, dpi=width, bbox_inches='tight', pad_inches=0)
            plt.close()

        except:
            print('oops')

def Chaos_Window(base, analytics, device_id=-1, rule_0=0, gloves=0):

    print("base")
    print(base)
    print("device_id")
    print(device_id)
    p_m_i = 0
    ts_0 = time.time()

    #window
    if analytics == 1:

        CELL_WIDTH = HEIGHT

    else:

        CELL_WIDTH = WIDTH


    #colors
    color_0 = (0, 0, 0)
    color_1 = (32, 32, 32)
    color_2 = (255, 0, 255)
    color_3 = (0, 255, 255)
    color_4 = (255, 255, 0)
    color_5 = (255, 255, 255)
    color_6 = (255, 0, 0)
    color_7 = (0, 255, 0)
    color_8 = (0, 0, 255)

    #rainbow
    # color_0 = (0, 0, 0)
    # color_1 = (255, 0, 0)
    # color_2 = (255, 255, 0)
    # color_3 = (0, 255, 0)
    # color_4 = (0, 255, 255)
    # color_5 = (0, 0, 255)
    # color_6 = (255, 0, 255)
    # color_7 = (255, 255, 255)
    # color_8 = (128, 128, 128)


    if base < 5:

        value_color = {0:color_0, 1:color_2, 2:color_3, 3:color_4}
        color_value = {v:k for k, v in value_color.items()}

    elif base < 11:

        value_color = {0:color_0, 1:color_1, 2:color_2, 3:color_3, 4:color_4, 5:color_5,
                      6:color_6, 7:color_7, 8:color_8}
        color_value = {v:k for k, v in value_color.items()}

    else:
        value_color = {0:(0, 0, 0),
                       1:(31, 31, 31), 2:(255, 0, 255), 3:(0, 255, 255), 4:(255, 255, 0),
                       5:(63, 63, 192), 6:(127, 0, 127), 7:(0, 127, 127), 8:(127, 127, 0),
                       9:(255, 255, 255), 10:(255, 0, 0), 11:(0, 255, 0), 12:(0, 0, 255),
                       13:(223, 223, 223), 14:(127, 0, 0), 15:(0, 127, 0), 16:(0, 0, 127)}
        color_value = {v:k for k, v in value_color.items()}


    def redraw_window(input_box, v_input, dt, timer):

        #preparation


        #cell drawing
        WIN.blit(pygame.surfarray.make_surface(np.moveaxis(cells_a, 0, 1)), (0, 0))


        #ui drawing
        if ui_on == 1:

            [pygame.draw.rect(WIN, value_color[i_rule[rule_models.index(cell)]], cell) for cell in rule_models]



        step_label_b = main_font.render(f"5T3P: {step}", 1, (255, 255, 255))
        time_label = lable_font.render(str(int(timer/60)), 1, (255, 255, 255))
        step_length = main_font.render(f"5T3P: {step- step_0}", 1, (255, 255, 255))


        WIN.blit(step_length, (WIDTH - step_length.get_width() - 20, 20))


        #conosle inputs
        if input_box == 1:
            v_input_r = small_font.render(v_input, 1, (0, 0, 0))

            type_box = pygame.Rect(10, 10, v_input_r.get_width() + 2, v_input_r.get_height() + 2)

            pygame.draw.rect(WIN, (255, 255, 255), type_box)

            WIN.blit(v_input_r, (11, 11))

        if list_count != 0:
            draw_text(str(list_count), small_font, (255, 255, 255), WIN, 11, 33)

        #miliseconds per frame
        draw_text(str(dt), small_font, (255, 255, 255), WIN, WIDTH - 40, 80)

        pygame.display.update()

    def input(letter, base, page, input_box, v_input):

        if input_box == 1:
            v_input += letter

        place = (letter_values[letter] + (space * 26)) % bv

        # print('')
        # print(place)

        i_rule[place] = (i_rule[place] + 1) % base
        d_rule[list(d_rule.keys())[place]] = i_rule[place]

        return v_input

    #active variables
    run = 1
    pause = 0
    FPS = 120
    step = 0
    step_0 = 0
    space = 0
    clock = pygame.time.Clock()
    bv = base ** view
    bbv = base ** base ** view
    rule_window_scale = 4

    #record keeping
    journal = dict()
    page = []
    rule_point = list()
    bookmarks = [0]
    rule_count = 0
    rule = str()

    #ui
    ui_on = 1
    ui_scale = 20
    bar_height = 100
    bar_width = ui_scale + int(ui_scale / 2)

    rule_models = []
    ir_height = base * int(base/2)
    x_offset = CELL_WIDTH + 40

    #input augments
    midi_inputs = 0
    if gloves > 0:
        midi_inputs = 1
        device_id = 1


    number_of_sensors = 12
    g_letter = 2


    #chaos console
    input_box = 0
    list_count = 0
    v_input = ''
    write = 0
    j_name = ''

    #cell design
    cell_row_width = int(CELL_WIDTH)
    cell_rows = int(HEIGHT) + 1

    if base < 11:
        d_rule, i_rule = rule_gen(rule_0, base)

    else:
        d_rule, i_rule = rule_gen_xx(rule_0, base)


    print("")
    print('cells: width height')
    print((cell_row_width, cell_rows))

    cells_a = np.zeros((cell_rows, cell_row_width, 3), dtype='uint8')

    for x in range(base):
        cells_a[0, int(cell_row_width / 2) + x - int(base/2)] = value_color[x]


    for x in range(cell_rows - 1):

        cells_a = np.roll(cells_a, 1, 0)

        for y in range(cell_row_width):

            cells_a[0, y] = value_color[d_rule[tuple(viewer_1d(cells_a[1], y, view, [], color_value))]]


    if midi_inputs == 1:

        pygame.init()
        pygame.midi.init()
        pygame.fastevent.init()
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

        glove_values = [x for x in range(gloves * number_of_sensors)]


        print("")
        print("glove_values")
        print(glove_values)

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

    if ui_on == 1:

        rule_models = []
        ir_split = []

        [ir_split.append(i_rule[x * int(len(i_rule) / ir_height):(x + 1) * int(len(i_rule) / ir_height)]) for x in
         range(ir_height)]

        [[rule_models.append(
            pygame.Rect(1 * ui_scale * x + x_offset, 1 * ui_scale + 20 + ui_scale * y, ui_scale, ui_scale)) for x in
          range(len(ir_split[y]))] for y in range(ir_height)]


    #main loop
    while run == 1:

        # print("")
        # print("running")

        ts_1 = time.time()
        timer = ts_1 - ts_0
        WIN.fill((0, 0, 0))
        dt = clock.tick(FPS)
        redraw_window(input_box, v_input, dt, timer)


        if step - step_0 > 3000:
            print('rule_count')
            print(rule_count)
            journal[(rule, step)] = rule_count

            rule_point = i_rule[::]
            rule = str()
            for ir in i_rule:
                rule += str(ir)
            rule_count = 0

            rule_count += 1
            step += 1

            bookmarks.append(len(list(journal.keys())))
            print("")
            print("bookmarks")
            print(bookmarks)
            print("journal")
            print(journal)

            step_0 = step

        #mitosis
        if pause == 0:

            cells_a = np.roll(cells_a, 1, 0)

            for x in range(len(cells_a[0])):
                cells_a[0, x] = value_color[d_rule[tuple(viewer_1d(cells_a[1], x, view, [], color_value))]]

            #record keeping
            if i_rule != rule_point:

                # print()
                # print(rule)
                # print(rule_count)
                # print(step)
                journal[(rule,step)] = rule_count

                rule_point = i_rule[::]
                rule = str()
                for ir in i_rule:
                    rule += str(ir)
                rule_count = 0

            rule_count += 1
            step += 1


        #console rule inputs
        if list_count != 0:

            new_rule = rule_list[0] % bbv

            if base < 11:
                d_rule, i_rule = rule_gen(new_rule, base)

            else:
                d_rule, i_rule = rule_gen_xx(new_rule, base)

            rule_list = rule_list[1:]

            list_count -= 1


        #inputs
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2


            #keyboard
            elif event.type == pygame.KEYDOWN:

                if event.key == K_ESCAPE:


                    print('rule_count')
                    print(rule_count)
                    journal[(rule, step)] = rule_count

                    rule_point = i_rule[::]
                    rule = str()
                    for ir in i_rule:
                        rule += str(ir)
                    rule_count = 0

                    rule_count += 1
                    step += 1

                    bookmarks.append(len(list(journal.keys())))
                    print("")
                    print("bookmarks")
                    print(bookmarks)


                    run = 2

                elif event.key == pygame.K_q:
                    v_input = input('q', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_w:
                    v_input = input('w', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_e:
                    v_input = input('e', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_r:
                    v_input = input('r', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_t:
                    v_input = input('t', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_y:
                    v_input = input('y', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_u:
                    v_input = input('u', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_i:
                    v_input = input('i', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_o:
                    v_input = input('o', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_p:
                    v_input = input('p', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_a:
                    v_input = input('a', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_s:
                    v_input = input('s', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_d:
                    v_input = input('d', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_f:
                    v_input = input('f', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_g:
                    v_input = input('g', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_h:
                    v_input = input('h', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_j:
                    v_input = input('j', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_k:
                    v_input = input('k', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_l:
                    v_input = input('l', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_z:
                    v_input = input('z', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_x:
                    v_input = input('x', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_c:
                    v_input = input('c', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_v:
                    v_input = input('v', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_b:
                    v_input = input('b', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_n:
                    v_input = input('n', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_m:
                    v_input = input('m', base, page, input_box, v_input)
                    page = []

                elif event.key == pygame.K_SPACE:
                    v_input = input(' ', base, page, input_box, v_input)

                    space += 1

                elif event.key == pygame.K_0:

                    v = 0

                    if input_box == 1:
                        v_input += str(v)


                elif event.key == pygame.K_TAB:
                    d_rule, i_rule = rule_gen(rule_0, base)
                    #

                elif event.key == pygame.K_PERIOD:


                    bookmarks.append(len(list(journal.keys())))
                    print("")
                    print("bookmarks")
                    print(bookmarks)

                    step_0 = step



                elif event.key == pygame.K_1:

                    v = 1

                    if input_box == 1:
                        v_input += str(v)

                elif event.key == pygame.K_2:

                    v = 2

                    if input_box == 1:
                        v_input += str(v)

                elif event.key == pygame.K_3:

                    v = 3

                    if input_box == 1:
                        v_input += str(v)

                elif event.key == pygame.K_4:

                    v = 4

                    if input_box == 1:
                        v_input += str(v)

                elif event.key == pygame.K_5:

                    v = 5

                    if input_box == 1:
                        v_input += str(v)

                elif event.key == pygame.K_6:

                    v = 6

                    if input_box == 1:
                        v_input += str(v)

                elif event.key == pygame.K_7:

                    v = 7

                    if input_box == 1:
                        v_input += str(v)

                elif event.key == pygame.K_8:

                    v = 8

                    if input_box == 1:
                        v_input += str(v)

                elif event.key == pygame.K_9:

                    v = 9

                    if input_box == 1:
                        v_input += str(v)

                elif event.key == pygame.K_BACKSPACE:
                    v_input = v_input[0:-1]

                elif event.key == pygame.K_MINUS:
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


                                if input_list[0] == 'base':

                                    print("##########based##########")

                                    base = int(input_list[1])
                                    bv = base ** view

                                    step_size = int(base ** view / (base - 1))
                                    o_r = rule_gen(0, base)[1]
                                    for x in range(int((base ** view) / step_size) + 1):

                                        if x > 0:

                                            o_r[-((step_size * x + 1) % bv)] = x

                                        else:

                                            o_r[-((step_size * x + 1) % bv)] = 1
                                    o_r[-1] = 1
                                    origin_rule = decimal(o_r, base)
                                    ir_height = base

                                    # colors
                                    if base < 5:

                                        value_color = {0: (0, 0, 0), 1: (255, 0, 255), 2: (0, 255, 255),
                                                       3: (255, 255, 0), 4: (192, 192, 192), 5: (255, 0, 0),
                                                       6: (0, 255, 0), 7: (0, 0, 255)}
                                        color_value = {v: k for k, v in value_color.items()}

                                    else:

                                        value_color = {0: (0, 0, 0), 1: (32, 32, 32), 2: (255, 0, 255),
                                                       3: (0, 255, 255), 4: (255, 255, 0), 5: (192, 192, 192),
                                                       6: (255, 0, 0), 7: (0, 255, 0), 8: (0, 0, 255)}
                                        color_value = {v: k for k, v in value_color.items()}

                                    print("origin rule")
                                    print(o_r)
                                    print(origin_rule)

                                    d_rule, i_rule = rule_gen(origin_rule, base)

                                    print("d_rule, i_rule")
                                    print(d_rule)
                                    print(i_rule)

                                    if ui_on == 1:

                                        rule_models = []

                                        ir_split = []

                                        [ir_split.append(i_rule[x * int(len(i_rule) / ir_height):(x + 1) * int(
                                            len(i_rule) / ir_height)]) for x in
                                         range(ir_height)]

                                        [[rule_models.append(
                                            pygame.Rect(1 * ui_scale * x + x_offset,
                                                        1 * ui_scale + 20 + ui_scale * y, ui_scale, ui_scale)) for x
                                            in
                                            range(len(ir_split[y]))] for y in range(ir_height)]


                                    print("new_row")
                                    print(rule_gen_2(origin_rule, base, cell_row_width)[1])

                                    # mitosis

                                    cells_a = np.roll(cells_a, 1, 0)

                                    clunk = 0

                                    for y in rule_gen_2(origin_rule, base, cell_row_width)[1]:

                                            cells_a[0, clunk] = value_color[y]

                                            clunk += 1

                                elif input_list[0] == 'name':
                                    j_name = input_list[1]

                                    write = 1

                                elif input_list[0] == 't-clear':

                                    trigger_0 = 0
                                    trigger_1 = 0
                                    trigger_2 = 0
                                    trigger_3 = 0
                                    trigger_4 = 0
                                    trigger_5 = 0
                                    trigger_6 = 0
                                    trigger_7 = 0
                                    trigger_8 = 0


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

                    print('rule_count')
                    print(rule_count)
                    journal[(rule, step)] = rule_count

                    rule_point = i_rule[::]
                    rule = str()
                    for ir in i_rule:
                        rule += str(ir)
                    rule_count = 0

                    rule_count += 1
                    step += 1

                    bookmarks.append(len(list(journal.keys())))
                    print("")
                    print("bookmarks")
                    print(bookmarks)

                    step_0 = step

                if event.key == pygame.K_RETURN:

                    pause += 1
                    pause = pause % 2

                    print("")
                    print("pause")
                    print(pause)


            #midi
            elif event.type in [pygame.midi.MIDIIN]:

                # print(event)

                clean_e = str(event)[21:-3]
                # print(clean_e)
                list_e = clean_e.split(',')
                ev = []
                # print(list_e)

                for l in list_e:

                    ev.append(int(l.split(':')[1]))

                if ev[0] == 176:
                    # print('right')
                    # print(ev)
                    glove_values[ev[1]] = ev[2]

                elif ev[0] == 177:
                    # print('left')
                    # print(ev)
                    glove_values[ev[1] + number_of_sensors] = ev[2]

        # glove_application
        if gloves > 0:
            if g_letter == 1:
                g_sum = sum(glove_values)
                i_rule[g_sum % bv] += 1
                i_rule[g_sum % bv] = i_rule[g_sum % bv] % base
                d_rule[list(d_rule.keys())[g_sum % bv]] = i_rule[g_sum % bv]
            if g_letter == 2:
                for x in range(base):
                    if glove_values[(6+x)%number_of_sensors] > 32:
                        g_sum = sum(glove_values) + x * base
                        i_rule[g_sum % bv] = x
                        d_rule[list(d_rule.keys())[g_sum % bv]] = i_rule[g_sum % bv]

        #glove_application

        #midi clean up
        if device_id > 0:

            if midi_inputs == 1:

                if p_m_i.poll():

                    # print(' ')
                    # print('i')
                    # print(i)

                    midi_events = p_m_i.read(1024)
                    midi_evs = pygame.midi.midis2events(midi_events, p_m_i.device_id)

                    for m_e in midi_evs:
                        event_post(m_e)

    pygame.midi.quit()

    #journal write
    if write == 1:

        journal['bookmarks'] = bookmarks
        journal['base'] = base

        # print("")
        # print(bookmarks)
        # print(journal)

        if len(j_name) > 0:

            filename = 'journals/journal_' + j_name

        else:

            j_num = len(os.listdir('journals'))

            filename = 'journals/journal_' + str(j_num)

        outfile = open(filename, 'wb')
        pickle.dump(journal, outfile)
        outfile.close

        # print(len(journal))



def menu():

    click = False
    device_id = 0
    analytics = 0
    reflection = 0
    rule_0 = 0
    base = 0
    midi = 0
    gloves = 0

    #inputs
    input_text_c = ''
    input_text_v = ''
    input_text_rgb = ''
    input_text_bk = ''

    #journals
    j_choice = 0
    chosen_journal = ''
    bookmarks = []
    bookmarks_s = []

    #synthesize
    center_seed = [1, 1]
    scales = [1, 1, 1, 1]

    #colors
    black = (0, 0, 0)
    grey = (.5, .5, .5)
    white = (1, 1, 1)
    red = (1, 0, 0)
    green = (0, 1, 0)
    blue = (0, 0, 1)
    magenta = (1, 0, 1)
    cyan = (0, 1, 1)
    yellow = (1, 1, 0)

    c_choice = 0
    color_list = [black, magenta, cyan, yellow, grey, red, green, blue, white]
    # color_list = [black, red, yellow, green, cyan, blue, magenta, white, grey]

    pygame.init()
    pygame.fastevent.init()

    if midi > 0:
        pygame.init()
        pygame.midi.init()
        pygame.fastevent.init()
        event_post = pygame.fastevent.post

        # rtmidi init
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


    while True:

        #basics
        WIN.fill((0, 0, 0))
        draw_text('C311UL4R H4PT1C 4UT0M4T4 0P3R4T1NG 5Y5T3M', TITLE_FONT, (10, 100, 10), WIN, WIDTH / 2 - 655, 100)
        t_line = pygame.Rect(WIDTH / 2 - 633, 200, 1360, 2)
        pygame.draw.rect(WIN, (10, 100, 10), t_line)
        mx, my = pygame.mouse.get_pos()

        try:
            journals = os.listdir("journals")
        except:
            os.mkdir('journals')

        #inputs
        text_surface_c = main_font.render(input_text_c, True, (100, 10, 10))
        text_surface_v = main_font.render(input_text_v, True, (100, 10, 10))


        #####design#####
        x = 300
        y = 250
        design = pygame.Rect(x, y, 200, 70)
        design_i = pygame.Rect(x, y, 197, 65)
        pygame.draw.rect(WIN, (100, 10, 100), design)
        pygame.draw.rect(WIN, (0, 0, 0), design_i)
        if design.collidepoint((mx, my)):
            if click:
                draw_text('L04D1N6', TITLE_FONT, (255, 255, 255), WIN, WIDTH / 2 - 200, HEIGHT / 2 - 200)
                pygame.display.update()
                print("design")
                print(device_id)
                pygame.midi.quit()
                Chaos_Window(base, analytics, device_id, rule_0, gloves)
        draw_text('Design', lable_font, (100, 10, 100), WIN, x, y)


        #color choice
        x = 300
        y = 350
        color_rect = pygame.Rect(x, y, 200, 50)
        color_rect_i = pygame.Rect(x, y, 197, 43)
        pygame.draw.rect(WIN, (100, 10, 10), color_rect)
        pygame.draw.rect(WIN, (0, 0, 0), color_rect_i)
        draw_text('<mouse over red boxes to type;', small_font, (100, 10, 10), WIN, x + 210, y)
        draw_text('choose a single number between 2 and 9', small_font, (100, 10, 10), WIN, x + 220, y + 25)
        if color_rect.collidepoint((mx, my)):
            draw_text('Colors:', main_font, (100, 10, 10), WIN, x, y)
            WIN.blit(text_surface_c, (x + 100, y))

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
                    print('color')
                    print(input_text_c)

            if len(input_text_c) > 0:
                base = int(input_text_c)

        #initial rule
        y = 450
        rule_rect = pygame.Rect(x, y, 200, 50)
        rule_rect_i = pygame.Rect(x, y, 197, 43)
        pygame.draw.rect(WIN, (100, 10, 10), rule_rect)
        pygame.draw.rect(WIN, (0, 0, 0), rule_rect_i)
        draw_text('<choose any number', small_font, (100, 10, 10), WIN, x + 220, y)
        if rule_rect.collidepoint((mx, my)):
            draw_text('Rule:', main_font, (100, 10, 10), WIN, x, y)
            WIN.blit(text_surface_v, (x + 70, y))

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
                    print("rule")
                    print(input_text_v)

            if len(input_text_v) > 0:
                rule_0 = int(input_text_v)

        #analytics
        y = 550
        analytics_button = pygame.Rect(x, y, 200, 50)
        analytics_button_i = pygame.Rect(x, y, 197, 43)
        pygame.draw.rect(WIN, (0, 192, 192), analytics_button)
        pygame.draw.rect(WIN, (0, 0, 0), analytics_button_i)
        draw_text('<click blue boxes to toggle', small_font, (0, 192, 192), WIN, x + 210, y)
        draw_text('analytics: 0 off - 1 on', small_font, (0, 192, 192), WIN, x + 250, y + 25)
        if analytics_button.collidepoint((mx, my)):
            if click:
                print('analytics on')

                if analytics == 0:

                    analytics = 1

                else:

                    analytics = 0

            draw_text('analytics: ' + str(analytics), main_font, (0, 192, 192), WIN, x, y)

        #gloves
        x = 140
        y = 400
        glove_rect = pygame.Rect(x+25, y, 25, 50)
        glove_rect_i = pygame.Rect(x+50, y, 25, 50)
        pygame.draw.rect(WIN, (10, 100, 100), glove_rect)
        pygame.draw.rect(WIN, (100, 10, 100), glove_rect_i)
        draw_text('gloves', small_font, (10, 200, 200), WIN, x - 70, y)
        draw_text(str(gloves), main_font, (255, 255, 255), WIN, x+42, y)
        if glove_rect.collidepoint((mx, my)):
            if click:
                print('click')

                gloves += 1
        if glove_rect_i.collidepoint((mx, my)):
            if click:
                print('click')

                gloves -= 1
        if gloves > 2:
            gloves = 2
        if gloves < 0:
            gloves = 0

        #device id
        if gloves > 0:

            pygame.midi.init()

            x = 140
            y = 500
            dvid_rect = pygame.Rect(x+25, y, 25, 50)
            dvid_rect_i = pygame.Rect(x+50, y, 25, 50)
            pygame.draw.rect(WIN, (10, 100, 100), dvid_rect)
            pygame.draw.rect(WIN, (100, 10, 100), dvid_rect_i)
            draw_text('device_id', small_font, (10, 200, 200), WIN, x - 100, y)
            draw_text(str(device_id), main_font, (255, 255, 255), WIN, x+42, y)
            if dvid_rect.collidepoint((mx, my)):
                if click:
                    print('click')

                    device_id += 1
            if dvid_rect_i.collidepoint((mx, my)):
                if click:
                    print('click')

                    device_id -= 1
            if device_id < 0:
                device_id = 0

            for i in range(pygame.midi.get_count()):
                r = pygame.midi.get_device_info(i)
                (interf, name, input, output, opened) = r

                in_out = ""
                if input:
                    in_out = "(input)"
                if output:
                    in_out = "(output)"

                midi_lable_0 = "%2i:%s:, %s"% (i, name, in_out)
                midi_lable_1 = 3

                x = 150
                y = 620 + i * 60
                midi_button = pygame.Rect(x, y, 400, 50)
                midi_button_i = pygame.Rect(x, y, 395, 43)
                pygame.draw.rect(WIN, (192, 128, 0), midi_button)
                pygame.draw.rect(WIN, (0, 0, 0), midi_button_i)
                draw_text(str(midi_lable_0), small_font, (192, 128, 0), WIN, x, y)
                if analytics_button.collidepoint((mx, my)):
                    if click:
                        print('analytics on')

                        if analytics == 0:

                            analytics = 1

                        else:

                            analytics = 0



        #####print#####
        x = 1200
        y = 250
        print_r = pygame.Rect(x, y, 200, 70)
        print_i = pygame.Rect(x, y, 197, 65)
        pygame.draw.rect(WIN, (100, 10, 100), print_r)
        pygame.draw.rect(WIN, (0, 0, 0), print_i)
        if print_r.collidepoint((mx, my)):
            if click:
                print("print")
                draw_text('L04D1N6', TITLE_FONT, (255, 255, 255), WIN, WIDTH / 2 - 200, HEIGHT / 2 - 200)
                pygame.display.update()
                synthesize(chosen_journal, color_list, bookmarks, reflection, center_seed, scales)
                print("synthesized")
                print()
        draw_text('Print', lable_font, (100, 10, 100), WIN, x, y)

        #journals
        x = 1200
        y = 350
        journal_button = pygame.Rect(x, y, 200, 50)
        journal_button_i = pygame.Rect(x, y, 197, 43)
        pygame.draw.rect(WIN, (232, 96, 10), journal_button)
        pygame.draw.rect(WIN, (0, 0, 0), journal_button_i)
        draw_text('click for journals>', small_font, (232, 96, 10), WIN, x - 190, y + 5)
        draw_text(str(chosen_journal), main_font, (232, 96, 10), WIN, x, y)
        if journal_button.collidepoint((mx, my)):
            if click:
                print('choose a journal')

                if j_choice == 0:

                    j_choice = 1
                    c_choice = 0

                else:

                    j_choice = 0
        if j_choice == 1:
            for j in range(len(journals)):
                x = 1450
                y = 250 + (60*j)
                j_button = pygame.Rect(x, y, 200, 40)
                j_button_i = pygame.Rect(x, y, 197, 35)
                pygame.draw.rect(WIN, (232, 96, 10), j_button)
                pygame.draw.rect(WIN, (0, 0, 0), j_button_i)
                draw_text(str(journals[j]), small_font, (232, 96, 10), WIN, x, y)

                if j_button.collidepoint((mx, my)):
                    if click:
                        chosen_journal = str(journals[j])

        #colors
        x = 1200
        y = 450
        color_button = pygame.Rect(x, y, 200, 50)
        color_button_i = pygame.Rect(x, y, 197, 43)
        pygame.draw.rect(WIN, (10, 224, 96), color_button)
        pygame.draw.rect(WIN, (0, 0, 0), color_button_i)
        draw_text('click for colors>', small_font, (10, 224, 96), WIN, x - 190, y + 5)
        if color_button.collidepoint((mx, my)):
            if click:
                print('choose a color')

                if c_choice == 0:

                    c_choice = 1
                    j_choice = 0

                else:

                    c_choice = 0
        if c_choice == 1:

            draw_text(str(input_text_rgb), main_font, (10, 224, 96), WIN, x, y)

            for c in range(len(color_list)):
                x = 1450
                y = 250 + (60*c)
                box_color = []
                for co in color_list[c]:
                    box_color.append(co*255)

                c_button = pygame.Rect(x, y, 250, 40)
                c_button_i = pygame.Rect(x, y, 197, 35)
                pygame.draw.rect(WIN, box_color, c_button)
                pygame.draw.rect(WIN, (0, 0, 0), c_button_i)
                draw_text(str(color_list[c]), small_font, (10, 224, 96), WIN, x, y)


                if c_button_i.collidepoint((mx, my)):


                    for event in pygame.event.get():

                        if event.type == pygame.KEYDOWN:
                            if event.key == K_1:
                                input_text_rgb += '1'
                            if event.key == K_2:
                                input_text_rgb += '2'
                            if event.key == K_3:
                                input_text_rgb += '3'
                            if event.key == K_4:
                                input_text_rgb += '4'
                            if event.key == K_5:
                                input_text_rgb += '5'
                            if event.key == K_6:
                                input_text_rgb += '6'
                            if event.key == K_7:
                                input_text_rgb += '7'
                            if event.key == K_8:
                                input_text_rgb += '8'
                            if event.key == K_9:
                                input_text_rgb += '9'
                            if event.key == K_0:
                                input_text_rgb += '0'
                            if event.key == K_COMMA:
                                input_text_rgb += ','
                            if event.key == K_PERIOD:
                                input_text_rgb += '.'
                            if event.key == K_BACKSPACE:
                                input_text_rgb = input_text_rgb[:len(input_text_rgb) - 1]
                            print("rgb")
                            print(input_text_rgb)

                        if event.type == MOUSEBUTTONDOWN:
                            if event.button == 1:
                                click = True

                    if click == True:

                        try:
                            s_rgb = input_text_rgb.split(',')
                            n_rgb = []

                            print(s_rgb)
                            for s in s_rgb:
                                n_rgb.append(float(s))
                            print(n_rgb)
                            color_list[c] = tuple(n_rgb)

                        except:
                            continue


            draw_text('^(r, g, b) values from 0-1', small_font, (10, 224, 96), WIN, x + 27, y + 50)
            draw_text('mouse over to type', small_font, (10, 224, 96), WIN, x + 57, y + 80)
            draw_text('click to change', small_font, (10, 224, 96), WIN, x + 72, y + 110)

        #bookmarks
        x = 1200
        y = 550
        bookmark_rect = pygame.Rect(x, y, 200, 50)
        bookmark_rect_i = pygame.Rect(x, y, 197, 43)
        pygame.draw.rect(WIN, (100, 10, 10), bookmark_rect)
        pygame.draw.rect(WIN, (0, 0, 0), bookmark_rect_i)
        draw_text('mouse over for bookmarks>', small_font, (100, 10, 10), WIN, x - 300, y + 5)
        if bookmark_rect.collidepoint((mx, my)):
            draw_text(str(input_text_bk), main_font, (100, 10, 10), WIN, x, y)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        input_text_bk += '1'
                    if event.key == K_2:
                        input_text_bk += '2'
                    if event.key == K_3:
                        input_text_bk += '3'
                    if event.key == K_4:
                        input_text_bk += '4'
                    if event.key == K_5:
                        input_text_bk += '5'
                    if event.key == K_6:
                        input_text_bk += '6'
                    if event.key == K_7:
                        input_text_bk += '7'
                    if event.key == K_8:
                        input_text_bk += '8'
                    if event.key == K_9:
                        input_text_bk += '9'
                    if event.key == K_0:
                        input_text_bk += '0'
                    if event.key == K_COMMA:
                        input_text_bk += ','
                    if event.key == K_BACKSPACE:
                        input_text_bk = input_text_bk[:len(input_text_bk) - 1]
                    print("bookmark")
                    print(input_text_bk)
        else:
            if len(input_text_bk) > 0:
                bookmarks_s = input_text_bk.split(',')
                bookmarks = []
                for b in bookmarks_s:
                    bookmarks.append(int(b))
            else:
                bookmarks = []

        #reflect
        x = 1200
        y = 650
        reflect_button = pygame.Rect(x, y, 200, 50)
        reflect_button_i = pygame.Rect(x, y, 197, 43)
        pygame.draw.rect(WIN, (0, 192, 192), reflect_button)
        pygame.draw.rect(WIN, (0, 0, 0), reflect_button_i)
        draw_text('reflection: 0 off - 1 top - 2 bottom >', small_font, (0, 192, 192), WIN, x - 400, y)
        if reflect_button.collidepoint((mx, my)):
            if click:
                print('reflected')

                reflection += 1
                reflection = reflection %3

            draw_text('reflection: ' + str(reflection), main_font, (0, 192, 192), WIN, x, y)

        #scales
        x = 1200
        y = 750
        for s in range(2):
            for c in range(2):
                scale_rect = pygame.Rect(x + c*90 + 20, y + s*55 - 10, 50, 50)
                scale_rect_i = pygame.Rect(x + c*90 + 20, y + s*55 - 10, 48, 46)
                pygame.draw.rect(WIN, (100, 10, 10), scale_rect)
                pygame.draw.rect(WIN, (0, 0, 0), scale_rect_i)
                draw_text('length scale>', small_font, (100, 10, 10), WIN, x - 150, y + 20)
                draw_text('<width scale', small_font, (100, 10, 10), WIN, x + 190, y + 20)
                draw_text(str(scales[s + c * 2]), main_font, (100, 10, 10), WIN, x + c * 90 + 35, y + s * 55 - 10)
                if scale_rect.collidepoint((mx, my)):
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == K_1:
                                scales[s + c*2] = 1
                            if event.key == K_2:
                                scales[s + c*2] = 2
                            if event.key == K_3:
                                scales[s + c*2] = 3
                            if event.key == K_4:
                                scales[s + c*2] = 4
                            if event.key == K_5:
                                scales[s + c*2] = 5
                            if event.key == K_6:
                                scales[s + c*2] = 6
                            if event.key == K_7:
                                scales[s + c*2] = 7
                            if event.key == K_8:
                                scales[s + c*2] = 8
                            if event.key == K_9:
                                scales[s + c*2] = 9

                            if event.key == K_0:
                                scales[s + c*2] = 10
                            if event.key == K_q:
                                scales[s + c*2] = 11
                            if event.key == K_w:
                                scales[s + c*2] = 12
                            if event.key == K_e:
                                scales[s + c*2] = 13
                            if event.key == K_r:
                                scales[s + c*2] = 14
                            if event.key == K_t:
                                scales[s + c*2] = 15
                            if event.key == K_y:
                                scales[s + c*2] = 16
                            if event.key == K_u:
                                scales[s + c*2] = 17
                            if event.key == K_i:
                                scales[s + c*2] = 18

        #center seed
        x = 900
        y = 775
        cs_rect = pygame.Rect(x+25, y, 25, 50)
        cs_rect_i = pygame.Rect(x+50, y, 25, 50)
        pygame.draw.rect(WIN, (10, 100, 100), cs_rect)
        pygame.draw.rect(WIN, (100, 10, 100), cs_rect_i)
        draw_text('center seed', small_font, (10, 200, 200), WIN, x - 100, y)
        draw_text(str(center_seed[1]), main_font, (255, 255, 255), WIN, x+42, y)
        if cs_rect.collidepoint((mx, my)):
            if click:
                print('click')

                center_seed[1] += 1

        if cs_rect_i.collidepoint((mx, my)):
            if click:
                print('click')

                center_seed[1] -= 1



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



menu()


# Chaos_Window(3, 1, -1, 21621)





