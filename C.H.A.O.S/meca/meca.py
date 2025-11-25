import pygame
import pygame.camera
import pygame.surfarray as surfarray
import pygame.font
import numpy as np
import pickle
import time
import os
from datetime import datetime

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))





def draw_a(size, canvas, corner):
    apex = (corner[1], corner[0] + int(size / 2))

    canvas[apex] = 1

    a_legs = dict()

    for x in range(2):
        a_legs[x] = []

    for x in range(size - 1):

        if x % 2 == 0:

            a_legs[0].append((apex[0] + 1 + x, apex[1] - 1 - int(x / 2)))
            a_legs[1].append((apex[0] + 1 + x, apex[1] + 1 + int(x / 2)))

        else:

            a_legs[0].append((apex[0] + 1 + x, apex[1] - 1 - int(x / 2)))
            a_legs[1].append((apex[0] + 1 + x, apex[1] + 1 + int(x / 2)))

    for x in range(2):
        for a in a_legs[x]:
            canvas[a] = 1

    canvas[a_legs[0][int(len(a_legs[0]) / 2)][0],
    a_legs[0][int(len(a_legs[0]) / 2)][1]:a_legs[1][int(len(a_legs[1]) / 2)][1]] = 1


def draw_b(size, canvas, corner):
    canvas[corner[1]:corner[1] + size, corner[0]] = 1

    canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
    canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 4)] = 1

    for x in range(int(size / 4) + 1):
        canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
        canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1

        canvas[corner[1] + x + int(size / 2), corner[0] + int(size / 4) + int(x / 2)] = 1
        canvas[corner[1] + int(size) - x - 1, corner[0] + int(size / 4) + int(x / 2)] = 1


def draw_c(size, canvas, corner):
    for x in range(int(size / 3) + 1):
        canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1

        canvas[corner[1] + int(size / 3) + x, corner[0]] = 1

    for x in range(int(size / 3) + 2):
        canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1


def draw_d(size, canvas, corner):
    canvas[corner[1]:corner[1] + size, corner[0]] = 1

    d_coord_0 = (corner[1], corner[0] + int(size / 3))
    d_coord_1 = (corner[1] + size - 1, corner[0] + int(size / 3))

    canvas[d_coord_0] = 1
    canvas[d_coord_1] = 1

    canvas[corner[1], corner[0]:corner[0] + int(size / 3)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 3)] = 1

    d_legs = dict()

    for x in range(2):
        d_legs[x] = []

    for x in range(int(size / 3)):

        if x == 0:
            d_legs[0].append(d_coord_0)
            d_legs[1].append(d_coord_1)

        d_legs[0].append((d_coord_0[0] + 1 + x, d_coord_0[1] + 1 + x))
        d_legs[1].append((d_coord_1[0] - 1 - x, d_coord_1[1] + 1 + x))

    # print(d_legs[0])
    # print(d_legs[1])

    for k in d_legs[0]:
        canvas[k] = 1

    for k in d_legs[1]:
        canvas[k] = 1

    canvas[d_legs[0][-1][0]:d_legs[1][-1][0], d_legs[0][-1][1]] = 1


def draw_e(size, canvas, corner):
    canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    canvas[corner[1], corner[0]:corner[0] + int(size / 3)] = 1
    canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 3)] = 1


def draw_f(size, canvas, corner):
    canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    canvas[corner[1], corner[0]:corner[0] + int(size / 3)] = 1
    canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1


def draw_g(size, canvas, corner):
    canvas[corner[1] + int(size / 3 * 2), corner[0] + int(size / 3):corner[0] + int(size / 3 * 2)] = 1

    for x in range(int(size / 3) + 1):
        canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1

        canvas[corner[1] + int(size / 3) + x, corner[0]] = 1

    for x in range(int(size / 3) + 2):
        canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1


def draw_h(size, canvas, corner):
    canvas[corner[1]:corner[1] + size, corner[0]] = 1
    canvas[corner[1]:corner[1] + size, corner[0] + int(size / 2)] = 1
    canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 2)] = 1


def draw_i(size, canvas, corner):
    canvas[corner[1], corner[0] + int(size / 4):corner[0] + size - int(size / 4)] = 1
    canvas[corner[1] + size - 1, corner[0] + int(size / 4):corner[0] + size - int(size / 4)] = 1
    canvas[corner[1]:corner[1] + size - 1, corner[0] + int(size / 2)] = 1


def draw_j(size, canvas, corner):
    for x in range(int(size / 3) + 1):
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1

    for x in range(int(size / 3 * 2)):
        canvas[corner[1] + x, corner[0] + int(size / 3 * 2)] = 1

    for x in range(int(size / 3) + 2):
        canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1


def draw_k(size, canvas, corner):
    canvas[corner[1]:corner[1] + size, corner[0]] = 1

    k_coord_0 = (corner[1] + int(size / 2), corner[0] + 1)

    canvas[k_coord_0] = 1

    k_legs = dict()

    for x in range(2):
        k_legs[x] = []

    for x in range(int(size / 2)):

        if x == 0:
            k_legs[0].append(k_coord_0)
            k_legs[1].append(k_coord_0)

        k_legs[0].append((k_coord_0[0] + 1 + x, k_coord_0[1] + 1 + x))
        k_legs[1].append((k_coord_0[0] - 1 - x, k_coord_0[1] + 1 + x))

    # print(k_legs[0])
    # print(k_legs[1])

    for k in k_legs[0]:
        canvas[k] = 1

    for k in k_legs[1]:
        canvas[k] = 1


def draw_l(size, canvas, corner):
    canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 2)] = 1


def draw_m(size, canvas, corner):
    canvas[corner[1]:corner[1] + size, corner[0]] = 1
    canvas[corner[1]:corner[1] + size, corner[0] + size - 1] = 1

    apex = (corner[1] + size - 1, corner[0] + int(size / 2))

    canvas[apex] = 1

    m_legs = dict()

    for x in range(2):
        m_legs[x] = []

    for x in range(size - 2):

        if x % 2 == 0:

            m_legs[0].append((apex[0] - 1 - x, apex[1] - 1 - int(x / 2)))
            m_legs[1].append((apex[0] - 1 - x, apex[1] + 1 + int(x / 2)))

        else:

            m_legs[0].append((apex[0] - 1 - x, apex[1] - 1 - int(x / 2)))
            m_legs[1].append((apex[0] - 1 - x, apex[1] + 1 + int(x / 2)))

    for x in range(2):
        for m in m_legs[x]:
            canvas[m] = 1


def draw_n(size, canvas, corner):
    canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    canvas[corner[1]:corner[1] + size - 1, corner[0] + int(size / 2)] = 1

    for x in range(size - 1):
        canvas[corner[1] + x, corner[0] + int(x / 2)] = 1


def draw_o(size, canvas, corner):
    for x in range(int(size / 3) + 1):
        canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + int(size / 3) - x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1

        canvas[corner[1] + int(size / 3) + x, corner[0]] = 1
        canvas[corner[1] + int(size / 3) + x, corner[0] + int(size / 3 * 2)] = 1

    for x in range(int(size / 3) + 2):
        canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1


def draw_p(size, canvas, corner):
    canvas[corner[1]:corner[1] + size, corner[0]] = 1

    canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
    canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1

    for x in range(int(size / 4) + 1):
        canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
        canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1


def draw_q(size, canvas, corner):
    for x in range(int(size / 3) + 1):
        canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + int(size / 3) - x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2) + int(size / 3) + int(size / 3 / 2)] = 1

        canvas[corner[1] + int(size / 3) + x, corner[0]] = 1
        canvas[corner[1] + int(size / 3) + x, corner[0] + int(size / 3 * 2)] = 1

    for x in range(int(size / 3) + 2):
        canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1


def draw_r(size, canvas, corner):
    canvas[corner[1]:corner[1] + size, corner[0]] = 1

    r_coord_0 = (corner[1] + int(size / 2), corner[0] + 1)
    r_coord_1 = (corner[1], corner[0] + 1)
    r_coord_2 = (corner[1] + int(size / 2), corner[0] + 1 + int(size / 5))
    r_coord_3 = (corner[1], corner[0] + 1 + int(size / 5))

    # print(r_coord_1)
    # print(r_coord_2)

    canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
    canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1

    r_legs = dict()

    for x in range(3):
        r_legs[x] = []

    for x in range(int(size / 2) + 1):
        canvas[corner[1] + int(size / 2) + x, corner[0] + int(size / 5) + int(x / 2)] = 1

    for x in range(int(size / 4) + 1):
        canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
        canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1


def draw_s(size, canvas, corner):
    canvas[corner[1] + int(size / 6):corner[1] + int(size / 6) * 2, corner[0]] = 1
    canvas[corner[1] + int(size / 6) * 4:corner[1] + int(size / 6) * 5, corner[0] + int(size / 2)] = 1
    canvas[corner[1], corner[0] + int(size / 6):corner[0] + int(size / 2)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 2) - int(size / 6)] = 1

    for x in range(int(size / 2)):
        canvas[corner[1] + int(size / 6) * 2 + int(5 * x / 6) - 1, corner[0] + x] = 1

    for x in range(int(size / 6)):
        canvas[corner[1] + int(size / 6) - x, corner[0] + x] = 1
        canvas[corner[1] + int(size / 6) * 5 + x, corner[0] + int(size / 2) - x - 1] = 1


def draw_t(size, canvas, corner):
    canvas[corner[1]:corner[1] + size, corner[0] + int(size / 2)] = 1
    canvas[corner[1], corner[0] + int(size / 5):corner[0] + size - int(size / 5)] = 1


def draw_u(size, canvas, corner):
    for x in range(int(size / 3) + 1):
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1

    for x in range(int(size / 3 * 2)):
        canvas[corner[1] + x, corner[0]] = 1
        canvas[corner[1] + x, corner[0] + int(size / 3 * 2)] = 1

    for x in range(int(size / 3) + 2):
        canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1


def draw_v(size, canvas, corner):
    for x in range(size - 1):
        canvas[corner[1] + x, corner[0] + int(x / 3)] = 1
        canvas[corner[1] + x, corner[0] + int(size / 3 * 2) - int(x / 3) - 1] = 1


def draw_w(size, canvas, corner):
    for x in range(size):
        canvas[corner[1] + x, corner[0] + int(x / 4)] = 1
        canvas[corner[1] + x, corner[0] + int(size / 2) - int(x / 4)] = 1
        canvas[corner[1] + x, corner[0] + int(x / 4) + int(size / 2)] = 1
        canvas[corner[1] + x, corner[0] + int(size) - int(x / 4) - 1] = 1


def draw_x(size, canvas, corner):
    for x in range(size - 1):
        canvas[corner[1] + x, corner[0] + int(x / 2)] = 1
        canvas[corner[1] + x, corner[0] + int(size / 2) - int(x / 2) - 1] = 1


def draw_y(size, canvas, corner):
    canvas[corner[1] + int(size / 2):corner[1] + int(size), corner[0] + int(size / 2)] = 1

    for x in range(int(size / 2)):
        canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
        canvas[corner[1] + x, corner[0] + int(size / 4 * 3) - int(x / 2)] = 1


def draw_z(size, canvas, corner):
    canvas[corner[1], corner[0]:corner[0] + int(size / 3 * 2)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 3 * 2)] = 1

    for x in range(size):
        canvas[corner[1] + x, corner[0] + int(size / 3 * 2) - int(2 * x / 3)] = 1







pygame.init()
pygame.camera.init()



###theo screen###
screen_width, screen_height = 1280, 960

###chao screen###
screen_width, screen_height = 1800, 960


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('C.H.A.O.S')







text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)


def detect_change_in_roi_mse(img1, img2, roi_coords, threshold=1):
    y1, x1, y2, x2 = roi_coords
    roi1 = img1[y1:y2, x1:x2].astype(np.float32)
    roi2 = img2[y1:y2, x1:x2].astype(np.float32)

    mse = np.mean((roi1 - roi2) ** 2)

    # print("")
    # print(mse)
    # print(mse)

    return mse, mse > threshold, roi1, roi2


def base_x(n, b):
    result = ""
    while n != 0:
        e = n // b
        q = n % b
        if e == 0:
            result += str(q)
        else:
            result = str(q) + result
        n = e
    return result if result else '0'


def rule_gen(rule, base=2, width=0, string=0):
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


#######flow######
# print("")
# print("water")
# print(water)
# print(flow)



cam_list = pygame.camera.list_cameras()
if not cam_list:
    print("no cameras found")
    pygame.quit()
    exit()

print("camlist")
print(cam_list)

camera = pygame.camera.Camera(cam_list[0], (screen_width, screen_height))

camera.start()

image = camera.get_image()
value_color = {0: (0, 0, 0), 1: (255, 0, 255), 2: (0, 255, 255), 3: (255, 255, 0), 4: (128, 128, 128), 5: (255, 0, 0),
               6: (0, 255, 0), 7: (0, 0, 255), 8: (255, 255, 255), 9: (255, 255, 255)}
color_array = np.array(list(value_color.values()), dtype=int)

array_past = pygame.surfarray.array3d(image)
target= np.array(array_past[0][0])

points = 16
threshold = 64
thresholds = [threshold for x in range(points)]
rethresh = 0




# bets
bet_detect = 1
ui = 0
digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, 'an': 14, 'er': 15,
           'ou': 16, 'in': 17, 'th': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}
digibetu = {v: k for k, v in digibet.items()}
phrase = ''
phrase_pos = 0
goal_bin = '000000'
gb_len = 6

hand_x = []
hands_1 = [0, 0]
hands_0 = [0, 0]
hands = [0, 0]
hand_x = [hands, hands_0, hands_1]
arms = [0, 0]
code = ''
code_0 = ' '
code_00 = ' '
code_01 = ' '

score = 1
set = 0
score_h = 0
sign_bank = {}
phrase_past = phrase[::]
tts = [0, 0]
times = []
tts_0 = time.time()
tts_1 = time.time()
stenograph = []

signame = "Chaotomata"

try:
    filename = os.path.join(SCRIPT_DIR, 'sign_bank', signame)
    infile = open(filename, "rb")
    sign_bank = pickle.load(infile)
    infile.close()

    print("loading" + signame)


except:
    print('new user')
    sign_bank = {}




print(len(stenograph))
if len(stenograph) > 1000:
    os.makedirs(os.path.join(SCRIPT_DIR, 'stenograph'), exist_ok=True)
    filename = os.path.join(SCRIPT_DIR, 'stenograph', signame + str(time.time()))
    outfile = open(filename, 'wb')
    pickle.dump(stenograph, outfile)
    outfile.close()

    stenograph = []

os.makedirs(os.path.join(SCRIPT_DIR, 'sign_bank'), exist_ok=True)
filename = os.path.join(SCRIPT_DIR, 'sign_bank', signame + 'backup' + str(time.time()))
outfile = open(filename, 'wb')
pickle.dump(sign_bank, outfile)
outfile.close()




ram = {}

mse_mem = {0:[threshold], 1:[threshold], 2:[threshold], 3:[threshold], 4:[threshold],
           5:[threshold], 6:[threshold], 7:[threshold], 8:[threshold], 9:[threshold]}

#####flow#####
pos_x = screen_width / 2
pos_y = screen_height / 2
dim = 2


rainbow = 1
rainbow_speed = 2
edge_speed = 1
base = 2
base2 = base * base
base3 = base2 * base
base4 = base3 * base
view = 5
fade = 1

gpu = 0


bv = base ** view
bvv = base ** view ** view
bbv = base**base**view
rv = 0
rv_bank = {}

#####rulers######
rules, rule = rule_gen(rv, base)
rule = np.array(rule)
ruler = 4
shift = 0

print(rule)

l = 500
h = l
lh = l * h
pos_x = int(screen_width / 2) - int(l / 2)
pos_y = int(screen_height / 2) - int(h / 2)
pos_z = 0
mid_x = l // 2
mid_y = h // 2

if dim == 1:
    flow = np.zeros(l, dtype=int)
    flow[int(l / 2)] = 1
    water = np.zeros((h, l), dtype=int)
    water[0] = flow

if dim == 2:
    flow = np.zeros((h, l), dtype=int)
    flow[int(l / 2), int(h / 2)] = 1
    water = np.zeros((h, l), dtype=int)

    flow[0:mid_x, 0:mid_y] = 1
    flow[0:mid_x, mid_y:h] = 0
    flow[mid_x:l, 0:mid_y] = 1
    flow[mid_x:l, mid_y:h] = 0



if dim == 3:
    flow = np.zeros((h, l), dtype=int)
    flow[int(l / 2), int(h / 2)] = 1
    water = np.zeros((h, l), dtype=int)


rainbow_array = np.zeros((h, l), dtype=int)
dirivative_array = np.zeros((h, l), dtype=int)
uw = 256**3 - 1  # = 16,777,216





try:
    filename = os.path.join(SCRIPT_DIR, 'color_bank', 'fullcolors')
    infile = open(filename, "rb")
    full_colors = pickle.load(infile)
    infile.close()

    print("loading" + signame)


except:
    full_colors = np.zeros((uw, 3), dtype=np.uint8)

    for x in range(uw):
        full_colors[x, 2] = (x // 65536) % 256  # Red channel
        full_colors[x, 1] = (x // 256) % 256    # Green channel
        full_colors[x, 0] = x % 256

        # print(full_colors[x])

    os.makedirs(os.path.join(SCRIPT_DIR, 'color_bank'), exist_ok=True)
    filename = os.path.join(SCRIPT_DIR, 'color_bank', 'fullcolors')
    outfile = open(filename, 'wb')
    pickle.dump(full_colors, outfile)
    outfile.close()



color_max = 256*8

full_colors = np.zeros((color_max, 3), dtype=int)

for x in range(color_max):


    rgb = [0, 0, 0]


    if x // 256 == 0:
        rgb = [x, 0, 0]
    elif x // 256 == 1:
        rgb = [255, x%256, 0]
    elif x // 256 == 2:
        rgb = [255-x%256, 255, 0]
    elif x // 256 == 3:
        rgb = [0, 255, x%256]
    elif x // 256 == 4:
        rgb = [0, 255-x%256, 255]
    elif x // 256 == 5:
        rgb = [x%256, 0, 255]
    elif x // 256 == 6:
        rgb = [255, x%256, 255]
    elif x // 256 == 7:
        rgb = [255-x%256, 255-x%256, 255-x%256]



    full_colors[x, 0] = rgb[0]
    full_colors[x, 1] = rgb[1]
    full_colors[x, 2] = rgb[2]

    print(full_colors[x])

os.makedirs(os.path.join(SCRIPT_DIR, 'color_bank'), exist_ok=True)
filename = os.path.join(SCRIPT_DIR, 'color_bank', 'fullcolors')
outfile = open(filename, 'wb')
pickle.dump(full_colors, outfile)
outfile.close()




print(full_colors[:10])

###clock###
time_d = time.time()
time_b = time.time()
print(time_d)
print(time_b)




##sythn##
sample_rate = 44100
duration = 1
frequency = 440 * (2 ** 1 / 12) ** digibet[code_0]
max_amplitude = 2 ** 15 - 1
previous_note = []


t = np.linspace(0, duration, int(sample_rate * duration), False)
mono_wave = max_amplitude * np.sin(frequency * t * 2 * np.pi)
mono_samples = mono_wave.astype(np.int16)

pygame.mixer.pre_init(sample_rate, -16, channels=1)

stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
stereo_sound = pygame.sndarray.make_sound(stereo_samples)


start = 55
key_sin = []
key_square = []
key_saw = []
key_triangle = []

key_track = {}
track_shift = 0

waffle_house = [2, 2, 1, 2, 2, 2, 1]
pentatonic = [0, 2, 2, 3, 2, 3, 2, 2]
major = [0, 7, 5, 4, 3, 5, 7, 5]

scale = pentatonic
octave = 12

for x in range(128):

    ###sin###
    frequency = start * 2**(x/12)
    # print(frequency)

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sin_wave = max_amplitude * np.sin(frequency * t * 2 * np.pi)
    mono_samples = sin_wave.astype(np.int16)

    pygame.mixer.pre_init(sample_rate, -16, channels=1)

    stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
    stereo_sound = pygame.sndarray.make_sound(stereo_samples)
    key_sin.append(stereo_sound)


    ###square###
    frequency = start * 2**(x/12)
    # print(frequency)

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    square_wave = max_amplitude * np.sign(np.sin(frequency * t * 2 * np.pi))
    mono_samples = square_wave.astype(np.int16)

    pygame.mixer.pre_init(sample_rate, -16, channels=1)

    stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
    stereo_sound = pygame.sndarray.make_sound(stereo_samples)

    key_square.append(stereo_sound)

    ###saw###
    frequency = start * 2**(x/12)
    # print(frequency)

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    saw_wave = max_amplitude * (t * frequency % 1 * 2 - 1)
    mono_samples = saw_wave.astype(np.int16)

    pygame.mixer.pre_init(sample_rate, -16, channels=1)

    stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
    stereo_sound = pygame.sndarray.make_sound(stereo_samples)
    key_saw.append(stereo_sound)

    ###triangle###
    frequency = start * 2**(x/12)
    # print(frequency)

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    triangle_wave = max_amplitude * (2 * np.abs(saw_wave / max_amplitude) - 1)
    mono_samples = triangle_wave.astype(np.int16)

    pygame.mixer.pre_init(sample_rate, -16, channels=1)

    stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
    stereo_sound = pygame.sndarray.make_sound(stereo_samples)

    key_triangle.append(stereo_sound)




#drums

def generate_kick(duration_s, sample_rate=44100, max_amplitude=32767):

    t = np.linspace(0, duration_s, int(sample_rate*duration_s), endpoint=False)

    decaying_freq = 200 * np.exp(-t * 20) + 50

    phase = np.cumsum(decaying_freq/sample_rate) * 2 * np.pi
    kick_wave = max_amplitude * np.sin(phase)

    envelope = np.exp(-t * 8)
    kick_wave *= envelope

    return kick_wave.astype(np.int16)

def generate_snare(duration_s, sample_rate = 44100, max_amplitude = 32767):

    t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)

    body_freq = 200
    body_envelope = np.exp(-t * 20)
    body_wave = np.sin(2*np.pi*body_freq*t) * body_envelope

    noise = np.random.uniform(-1, 1, len(t))

    noise_envelope = np.exp(-t * 50)
    noise_wave = noise * noise_envelope

    snare_wave = (0.5 * body_wave + 0.5 * noise_wave)

    final_envelope = np.exp(-t * 10)

    snare_wave *= final_envelope

    snare_wave *= max_amplitude

    return snare_wave.astype(np.int16)

def generate_hihat(duration_s, sample_rate=44100, max_amplitude=32767):

    t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)

    white_noise = np.random.uniform(-1, 1, len(t))

    envelope = np.exp(-t * 40)

    hihat_wave = white_noise * envelope
    hihat_wave *= max_amplitude

    return hihat_wave.astype(np.int16)




tempo = 0

kick_sample = generate_kick(0.3)
snare_sample = generate_snare(0.25)
hihat_sample = generate_hihat(0.1)


kick_stereo = np.repeat(kick_sample.reshape(-1, 1), 2, axis=1)
snare_stereo = np.repeat(snare_sample.reshape(-1, 1), 2, axis=1)
hihat_stereo = np.repeat(hihat_sample.reshape(-1, 1), 2, axis=1)


kick_sound = pygame.sndarray.make_sound(kick_stereo)
snare_sound = pygame.sndarray.make_sound(snare_stereo)
hihat_sound = pygame.sndarray.make_sound(hihat_stereo)


detect_change = 1
bong_on = 0





#####water typing#####
reg_x = 0
reg_y = 0

stamp_s = 16
stamp_x = 32 + int(reg_x * stamp_s * 1.2)
stamp_y = 32 + int(reg_y * stamp_s * 2)



####rainbow runner####

runner = 1
up_count = 0
down_count = 0


messages = ['']
message = ''
messages[0] = message


water_line = 0
rainbow_reset = 0

init = datetime.now()

init = init.strftime("%Y-%m-%d_%H-%M-%S")



###letters###
letter = ' '
letter_0 = ' '
letter_1 = ' '
last_typed = letter
shifts = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

palm_prev = [None, None]


def canvas_write(message, size, l_size, x_space, y_space, offset_size, density, x_o, y_o, canvas=0):
    #
    # def draw_a(size, canvas, corner):
    #
    #     apex = (corner[1], corner[0] + int(size / 2))
    #
    #     canvas[apex] = 1
    #
    #     a_legs = dict()
    #
    #     for x in range(2):
    #         a_legs[x] = []
    #
    #     for x in range(size - 1):
    #
    #         if x % 2 == 0:
    #
    #             a_legs[0].append((apex[0] + 1 + x, apex[1] - 1 - int(x / 2)))
    #             a_legs[1].append((apex[0] + 1 + x, apex[1] + 1 + int(x / 2)))
    #
    #         else:
    #
    #             a_legs[0].append((apex[0] + 1 + x, apex[1] - 1 - int(x / 2)))
    #             a_legs[1].append((apex[0] + 1 + x, apex[1] + 1 + int(x / 2)))
    #
    #     for x in range(2):
    #         for a in a_legs[x]:
    #             canvas[a] = 1
    #
    #     canvas[a_legs[0][int(len(a_legs[0]) / 2)][0],
    #     a_legs[0][int(len(a_legs[0]) / 2)][1]:a_legs[1][int(len(a_legs[1]) / 2)][1]] = 1
    #
    # def draw_b(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size, corner[0]] = 1
    #
    #     canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
    #     canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1
    #     canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 4)] = 1
    #
    #     for x in range(int(size / 4) + 1):
    #         canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1
    #
    #         canvas[corner[1] + x + int(size / 2), corner[0] + int(size / 4) + int(x / 2)] = 1
    #         canvas[corner[1] + int(size) - x - 1, corner[0] + int(size / 4) + int(x / 2)] = 1
    #
    # def draw_c(size, canvas, corner):
    #
    #     for x in range(int(size / 3) + 1):
    #         canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
    #
    #         canvas[corner[1] + int(size / 3) + x, corner[0]] = 1
    #
    #     for x in range(int(size / 3) + 2):
    #         canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
    #         canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1
    #
    # def draw_d(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size, corner[0]] = 1
    #
    #     d_coord_0 = (corner[1], corner[0] + int(size / 3))
    #     d_coord_1 = (corner[1] + size - 1, corner[0] + int(size / 3))
    #
    #     canvas[d_coord_0] = 1
    #     canvas[d_coord_1] = 1
    #
    #     canvas[corner[1], corner[0]:corner[0] + int(size / 3)] = 1
    #     canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 3)] = 1
    #
    #     d_legs = dict()
    #
    #     for x in range(2):
    #         d_legs[x] = []
    #
    #     for x in range(int(size / 3)):
    #
    #         if x == 0:
    #             d_legs[0].append(d_coord_0)
    #             d_legs[1].append(d_coord_1)
    #
    #         d_legs[0].append((d_coord_0[0] + 1 + x, d_coord_0[1] + 1 + x))
    #         d_legs[1].append((d_coord_1[0] - 1 - x, d_coord_1[1] + 1 + x))
    #
    #     # print(d_legs[0])
    #     # print(d_legs[1])
    #
    #     for k in d_legs[0]:
    #         canvas[k] = 1
    #
    #     for k in d_legs[1]:
    #         canvas[k] = 1
    #
    #     canvas[d_legs[0][-1][0]:d_legs[1][-1][0], d_legs[0][-1][1]] = 1
    #
    # def draw_e(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    #     canvas[corner[1], corner[0]:corner[0] + int(size / 3)] = 1
    #     canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1
    #     canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 3)] = 1
    #
    # def draw_f(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    #     canvas[corner[1], corner[0]:corner[0] + int(size / 3)] = 1
    #     canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1
    #
    # def draw_g(size, canvas, corner):
    #
    #     canvas[corner[1] + int(size / 3 * 2), corner[0] + int(size / 3):corner[0] + int(size / 3 * 2)] = 1
    #
    #     for x in range(int(size / 3) + 1):
    #         canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
    #
    #         canvas[corner[1] + int(size / 3) + x, corner[0]] = 1
    #
    #     for x in range(int(size / 3) + 2):
    #         canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
    #         canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1
    #
    # def draw_h(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size, corner[0]] = 1
    #     canvas[corner[1]:corner[1] + size, corner[0] + int(size / 2)] = 1
    #     canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 2)] = 1
    #
    # def draw_i(size, canvas, corner):
    #
    #     canvas[corner[1], corner[0] + int(size / 4):corner[0] + size - int(size / 4)] = 1
    #     canvas[corner[1] + size - 1, corner[0] + int(size / 4):corner[0] + size - int(size / 4)] = 1
    #     canvas[corner[1]:corner[1] + size - 1, corner[0] + int(size / 2)] = 1
    #
    # def draw_j(size, canvas, corner):
    #
    #     for x in range(int(size / 3) + 1):
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
    #
    #     for x in range(int(size / 3 * 2)):
    #         canvas[corner[1] + x, corner[0] + int(size / 3 * 2)] = 1
    #
    #     for x in range(int(size / 3) + 2):
    #         canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1
    #
    # def draw_k(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size, corner[0]] = 1
    #
    #     k_coord_0 = (corner[1] + int(size / 2), corner[0] + 1)
    #
    #     canvas[k_coord_0] = 1
    #
    #     k_legs = dict()
    #
    #     for x in range(2):
    #         k_legs[x] = []
    #
    #     for x in range(int(size / 2)):
    #
    #         if x == 0:
    #             k_legs[0].append(k_coord_0)
    #             k_legs[1].append(k_coord_0)
    #
    #         k_legs[0].append((k_coord_0[0] + 1 + x, k_coord_0[1] + 1 + x))
    #         k_legs[1].append((k_coord_0[0] - 1 - x, k_coord_0[1] + 1 + x))
    #
    #     # print(k_legs[0])
    #     # print(k_legs[1])
    #
    #     for k in k_legs[0]:
    #         canvas[k] = 1
    #
    #     for k in k_legs[1]:
    #         canvas[k] = 1
    #
    # def draw_l(size, canvas, corner):
    #     canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    #     canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 2)] = 1
    #
    # def draw_m(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size, corner[0]] = 1
    #     canvas[corner[1]:corner[1] + size, corner[0] + size - 1] = 1
    #
    #     apex = (corner[1] + size - 1, corner[0] + int(size / 2))
    #
    #     canvas[apex] = 1
    #
    #     m_legs = dict()
    #
    #     for x in range(2):
    #         m_legs[x] = []
    #
    #     for x in range(size - 2):
    #
    #         if x % 2 == 0:
    #
    #             m_legs[0].append((apex[0] - 1 - x, apex[1] - 1 - int(x / 2)))
    #             m_legs[1].append((apex[0] - 1 - x, apex[1] + 1 + int(x / 2)))
    #
    #         else:
    #
    #             m_legs[0].append((apex[0] - 1 - x, apex[1] - 1 - int(x / 2)))
    #             m_legs[1].append((apex[0] - 1 - x, apex[1] + 1 + int(x / 2)))
    #
    #     for x in range(2):
    #         for m in m_legs[x]:
    #             canvas[m] = 1
    #
    # def draw_n(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    #     canvas[corner[1]:corner[1] + size - 1, corner[0] + int(size / 2)] = 1
    #
    #     for x in range(size - 1):
    #         canvas[corner[1] + x, corner[0] + int(x / 2)] = 1
    #
    # def draw_o(size, canvas, corner):
    #
    #     for x in range(int(size / 3) + 1):
    #         canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 3) - x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
    #
    #         canvas[corner[1] + int(size / 3) + x, corner[0]] = 1
    #         canvas[corner[1] + int(size / 3) + x, corner[0] + int(size / 3 * 2)] = 1
    #
    #     for x in range(int(size / 3) + 2):
    #         canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
    #         canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1
    #
    # def draw_p(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size, corner[0]] = 1
    #
    #     canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
    #     canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1
    #
    #     for x in range(int(size / 4) + 1):
    #         canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1
    #
    # def draw_q(size, canvas, corner):
    #
    #     for x in range(int(size / 3) + 1):
    #         canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 3) - x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2) + int(size / 3) + int(size / 3 / 2)] = 1
    #
    #         canvas[corner[1] + int(size / 3) + x, corner[0]] = 1
    #         canvas[corner[1] + int(size / 3) + x, corner[0] + int(size / 3 * 2)] = 1
    #
    #     for x in range(int(size / 3) + 2):
    #         canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
    #         canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1
    #
    # def draw_r(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size, corner[0]] = 1
    #
    #     r_coord_0 = (corner[1] + int(size / 2), corner[0] + 1)
    #     r_coord_1 = (corner[1], corner[0] + 1)
    #     r_coord_2 = (corner[1] + int(size / 2), corner[0] + 1 + int(size / 5))
    #     r_coord_3 = (corner[1], corner[0] + 1 + int(size / 5))
    #
    #     # print(r_coord_1)
    #     # print(r_coord_2)
    #
    #     canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
    #     canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1
    #
    #     r_legs = dict()
    #
    #     for x in range(3):
    #         r_legs[x] = []
    #
    #     for x in range(int(size / 2) + 1):
    #         canvas[corner[1] + int(size / 2) + x, corner[0] + int(size / 5) + int(x / 2)] = 1
    #
    #     for x in range(int(size / 4) + 1):
    #         canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1
    #
    # def draw_s(size, canvas, corner):
    #
    #     canvas[corner[1] + int(size / 6):corner[1] + int(size / 6) * 2, corner[0]] = 1
    #     canvas[corner[1] + int(size / 6) * 4:corner[1] + int(size / 6) * 5, corner[0] + int(size / 2)] = 1
    #     canvas[corner[1], corner[0] + int(size / 6):corner[0] + int(size / 2)] = 1
    #     canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 2) - int(size / 6)] = 1
    #
    #     for x in range(int(size / 2)):
    #         canvas[corner[1] + int(size / 6) * 2 + int(5 * x / 6) - 1, corner[0] + x] = 1
    #
    #     for x in range(int(size / 6)):
    #         canvas[corner[1] + int(size / 6) - x, corner[0] + x] = 1
    #         canvas[corner[1] + int(size / 6) * 5 + x, corner[0] + int(size / 2) - x - 1] = 1
    #
    # def draw_t(size, canvas, corner):
    #
    #     canvas[corner[1]:corner[1] + size, corner[0] + int(size / 2)] = 1
    #     canvas[corner[1], corner[0] + int(size / 5):corner[0] + size - int(size / 5)] = 1
    #
    # def draw_u(size, canvas, corner):
    #
    #     for x in range(int(size / 3) + 1):
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
    #
    #     for x in range(int(size / 3 * 2)):
    #         canvas[corner[1] + x, corner[0]] = 1
    #         canvas[corner[1] + x, corner[0] + int(size / 3 * 2)] = 1
    #
    #     for x in range(int(size / 3) + 2):
    #         canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1
    #
    # def draw_v(size, canvas, corner):
    #
    #     for x in range(size - 1):
    #         canvas[corner[1] + x, corner[0] + int(x / 3)] = 1
    #         canvas[corner[1] + x, corner[0] + int(size / 3 * 2) - int(x / 3) - 1] = 1
    #
    # def draw_w(size, canvas, corner):
    #
    #     for x in range(size):
    #         canvas[corner[1] + x, corner[0] + int(x / 4)] = 1
    #         canvas[corner[1] + x, corner[0] + int(size / 2) - int(x / 4)] = 1
    #         canvas[corner[1] + x, corner[0] + int(x / 4) + int(size / 2)] = 1
    #         canvas[corner[1] + x, corner[0] + int(size) - int(x / 4) - 1] = 1
    #
    # def draw_x(size, canvas, corner):
    #
    #     for x in range(size - 1):
    #         canvas[corner[1] + x, corner[0] + int(x / 2)] = 1
    #         canvas[corner[1] + x, corner[0] + int(size / 2) - int(x / 2) - 1] = 1
    #
    # def draw_y(size, canvas, corner):
    #
    #     canvas[corner[1] + int(size / 2):corner[1] + int(size), corner[0] + int(size / 2)] = 1
    #
    #     for x in range(int(size / 2)):
    #         canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
    #         canvas[corner[1] + x, corner[0] + int(size / 4 * 3) - int(x / 2)] = 1
    #
    # def draw_z(size, canvas, corner):
    #     canvas[corner[1], corner[0]:corner[0] + int(size / 3 * 2)] = 1
    #     canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 3 * 2)] = 1
    #
    #     for x in range(size):
    #         canvas[corner[1] + x, corner[0] + int(size / 3 * 2) - int(2 * x / 3)] = 1

    rainbow_reset = 0

    m_list = list(message)

    # print("")
    # print("m_list")
    # print(m_list)

    line = 0

    canvas = np.rot90(canvas)
    canvas = np.flipud(canvas)

    l_place = 0

    for c in m_list:

        if x_o + l_size + (l_size + x_space) * l_place > l - x_o:
            l_place = 0
            line += 1

        if y_o + l_size + l_size * line + y_space * line > h - y_o:
            l_place = 0
            line = 0
            x_o += 1

            rainbow_reset = 1

        # for c in m:

        if c == 'a':

            for offset in (0, offset_size, density):
                draw_a(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_a(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_a(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_a(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'b':

            for offset in (0, offset_size, density):
                draw_b(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_b(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_b(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_b(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'c':

            for offset in (0, offset_size, density):
                draw_c(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_c(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_c(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_c(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'd':

            for offset in (0, offset_size, density):
                draw_d(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_d(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_d(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_d(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'e':

            for offset in (0, offset_size, density):
                draw_e(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_e(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_e(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_e(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'f':

            for offset in (0, offset_size, density):
                draw_f(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_f(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_f(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_f(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'g':

            for offset in (0, offset_size, density):
                draw_g(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_g(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_g(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_g(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'h':

            for offset in (0, offset_size, density):
                draw_h(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_h(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_h(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_h(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'i':

            for offset in (0, offset_size, density):
                draw_i(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_i(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_i(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_i(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'j':

            for offset in (0, offset_size, density):
                draw_j(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_j(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_j(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_j(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'k':

            for offset in (0, offset_size, density):
                draw_k(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_k(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_k(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_k(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'l':

            for offset in (0, offset_size, density):
                draw_l(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_l(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_l(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_l(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'm':

            for offset in (0, offset_size, density):
                draw_m(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_m(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_m(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_m(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'n':

            for offset in (0, offset_size, density):
                draw_n(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_n(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_n(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_n(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'o':

            for offset in (0, offset_size, density):
                draw_o(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_o(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_o(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_o(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'p':

            for offset in (0, offset_size, density):
                draw_p(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_p(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_p(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_p(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'q':

            for offset in (0, offset_size, density):
                draw_q(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_q(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_q(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_q(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'r':

            for offset in (0, offset_size, density):
                draw_r(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_r(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_r(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_r(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 's':

            for offset in (0, offset_size, density):
                draw_s(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_s(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_s(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_s(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 't':

            for offset in (0, offset_size, density):
                draw_t(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_t(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_t(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_t(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'u':

            for offset in (0, offset_size, density):
                draw_u(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_u(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_u(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_u(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'v':

            for offset in (0, offset_size, density):
                draw_v(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_v(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_v(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_v(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'w':

            for offset in (0, offset_size, density):
                draw_w(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_w(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_w(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_w(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'x':

            for offset in (0, offset_size, density):
                draw_x(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_x(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_x(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_x(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'y':

            for offset in (0, offset_size, density):
                draw_y(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_y(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_y(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_y(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == 'z':

            for offset in (0, offset_size, density):
                draw_z(l_size, canvas,
                       (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_z(l_size, canvas,
                       (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                draw_z(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                draw_z(l_size, canvas,
                       (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

        if c == ' ':
            l_place += 1

        l_place += 1

    canvas = np.flipud(canvas)
    canvas = np.rot90(canvas, 3)

    return canvas, rainbow_reset


def water_update(flow):
    global view, cell_map, rule

    if view == 5:

        up = np.vstack((flow[1:, :], flow[0:1, :]))
        down = np.vstack((flow[-1:, :], flow[:-1, :]))
        left = np.hstack((flow[:, 1:], flow[:, 0:1]))
        right = np.hstack((flow[:, -1:], flow[:, :-1]))

        index = (
                flow +  # center
                left * base +  # up
                right * base2 +  # down
                up * base3 +  # left
                down * base4  # right
        ).astype(np.int32)

        lookup = np.array(rule, dtype=np.uint8)

        water = lookup[index]




        water = water.astype(int)

        return water

    elif view == 9:
        L = np.roll(flow, -1)
        R = np.roll(flow, 1)
        U = np.roll(flow, -l)
        D = np.roll(flow, l)

        UL = np.roll(flow, -l - 1)
        UR = np.roll(flow, -l + 1)
        DL = np.roll(flow, l - 1)
        DR = np.roll(flow, l + 1)

        current = (
                UL * base ** 0 +
                U * base ** 1 +
                UR * base ** 2 +
                L * base ** 3 +
                flow * base ** 4 +
                R * base ** 5 +
                DL * base ** 6 +
                D * base ** 7 +
                DR * base ** 8
        )
        # print()
        # print(current)
        water = rule[-current.astype(int)]


        water = water.astype(int)

        return water

def color_dist(a, b):

        ca = np.mean(a.reshape(-1, 3), axis=0)
        cb = np.mean(b.reshape(-1, 3), axis=0)


        return np.linalg.norm(ca - cb)


def fill_bin(bin):
    if len(bin) < 5:
        zeros = ''
        for x in range(5 - len(bin)):
            zeros += '0'
        bin = zeros + bin

    return bin


def digits_to_index(digits, base):
    idx = 0
    for d in digits:
        idx = idx * base + d
    return idx

def handle(hand, code_0):
    global stamp_x, stamp_y, code, rv, shift, rule, tts_1, shifts, hands_x, rule_base


    if hand[0] == hand[1]:

        if hand[0] != code_0:

            letter = hand[0]
            code_0 = hand[0]
            code += hand[0]

            code_bin = base_x(digibet[code_0], 2)
            code_bin = fill_bin(code_bin)
            # print(goal_bin)

            for x in range(5):

                stamp_y0 = stamp_y + int(stamp_s * 1.2) * x

                if code_bin[x] == '1':
                    flow[stamp_x:stamp_x + stamp_s, stamp_y0:stamp_y0 + stamp_s + (stamp_s + 2) * x] = (flow[
                                                                                                        stamp_x:stamp_x + stamp_s,
                                                                                                        stamp_y0:stamp_y0 + stamp_s + (
                                                                                                                    stamp_s + 2) * x] + 1) % base

            stamp_x += int(stamp_s * 1.3)

            if stamp_x > 400:
                stamp_x = 32
                stamp_y += stamp_s * 6

            if stamp_y > 400:
                stamp_y = 32

            stenograph.append((code_0, round(time.time() - tts_1, 3), datetime.now()))
            # sign_bank['steno'] = []
            tts_1 = time.time()

            if ruler == 0:
                rv += digibet[code_0]
                rv = rv % bbv
                rules, rule = rule_gen(rv, base)
                rule = np.array(rule)


            elif ruler == 1:

                shift += digibet[code_0]

                shift = shift % len(rule)

                rule[shift] = str((int(rule[shift]) + 1) % base)

                rule_str = "".join(rule)
                rv = int(rule_str, base)
                rv = rv % bbv


            elif ruler == 2:


                shift += digibet[code_0]

                shift = shift % len(rule)

                rule[shift] = str((int(rule[shift]) + 1) % base)

                mirror = (int(len(rule)/2) + shift)%len(rule)
                rule[mirror] = str((int(rule[mirror]) + 1) % base)


            elif ruler == 3:



                shift += digibet[code_0]

                shift = shift % len(rule)

                # print()
                # print('shift')
                # print(shift)

                rule[shift] = str((int(rule[shift]) + 1) % base)

                shift_base = base_x(shift, base)

                shift_base = fill_bin(shift_base)

                shift_flip = shift_base[::-1]



                # print('base')
                # print(shift_base)
                # print(shift_flip)

                shifts[0] = [c for c in shift_flip]

                if len(code_bin) < view:
                    zeros = ''
                    for x in range(5 - len(code_bin)):
                        zeros += '0'
                    shift_base = zeros + shift_base

                inv_base = shift_base.translate(str.maketrans('01', '10'))

                inv_flip = inv_base[::-1]

                shifts[1] = [c for c in inv_flip]

                # print(inv_flip)
                #
                # print(inv_base)


                inv_digits = [int(c) for c in inv_base]



                inv_index = digits_to_index(inv_digits, base)


                # print('inv')
                # print(inv_index)
                #
                # print("")
                # print("shifts")
                # print(shifts)


                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)



                shifts[2] = shifts[0][::]
                shifts[3] = shifts[1][::]

                # print(int(view/2))

                center = 0

                # print('center')
                # print(center)
                #
                # print(shifts)

                for x in range(2):

                    if shifts[2+x][center] == '0':

                        shifts[2+x][center] = '1'

                    elif shifts[2+x][center] == '1':

                        if base == 2:
                            shifts[2+x][center] = '0'
                        else:
                            shifts[2 + x][center] = '2'

                    elif shifts[2+x][center] == '2':

                        shifts[2 + x][center] = '0'


                # print(shifts)

                flip = shifts[2][::-1]
                inv_index = digits_to_index([int(c) for c in flip], base)
                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)


                flip = shifts[3][::-1]
                inv_index = digits_to_index([int(c) for c in flip], base)
                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)


            elif ruler == 4:

                # print('')
                # print(rv)
                rv += 1
                rv = rv%bbv
                # print(rv)
                # print('rv')

                rules, rule_base = rule_gen(rv, base)
                rule_base = np.array(rule_base)
                # print(rule_base)

                rule = rule_base.copy()

                # print(rule)



                shift = digibet[code_0]

                shift = shift % len(rule)

                # print()
                # print('shift')
                # print(shift)

                rule[shift] = str((int(rule[shift]) + 1) % base)

                shift_base = base_x(shift, base)

                shift_base = fill_bin(shift_base)

                shift_flip = shift_base[::-1]



                # print('base')
                # print(shift_base)
                # print(shift_flip)

                shifts[0] = [c for c in shift_flip]


                inv_base = shift_base.translate(str.maketrans('01', '10'))

                inv_flip = inv_base[::-1]

                shifts[1] = [c for c in inv_flip]

                # print(inv_flip)
                #
                # print(inv_base)


                inv_digits = [int(c) for c in inv_base]



                inv_index = digits_to_index(inv_digits, base)


                # print('inv')
                # print(inv_index)
                #
                # print("")
                # print("shifts")
                # print(shifts)


                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)



                shifts[2] = shifts[0][::]
                shifts[3] = shifts[1][::]

                # print(int(view/2))

                center = 0

                # print('center')
                # print(center)
                #
                # print(shifts)

                for x in range(2):

                    if shifts[2+x][center] == '0':

                        shifts[2+x][center] = '1'

                    elif shifts[2+x][center] == '1':

                        if base == 2:
                            shifts[2+x][center] = '0'
                        else:
                            shifts[2 + x][center] = '2'

                    elif shifts[2+x][center] == '2':

                        shifts[2 + x][center] = '0'


                # print(shifts)

                flip = shifts[2][::-1]
                inv_index = digits_to_index([int(c) for c in flip], base)
                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)


                flip = shifts[3][::-1]
                inv_index = digits_to_index([int(c) for c in flip], base)
                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)


            elif ruler == 5:

                rule = rule_base.copy()



                shift = digibet[code_0]

                shift = shift % len(rule)

                print()
                print('shift')
                print(shift)

                rule[shift] = str((int(rule[shift]) + 1) % base)

                shift_base = base_x(shift, base)

                shift_base = fill_bin(shift_base)

                shift_flip = shift_base[::-1]



                print('base')
                print(shift_base)
                print(shift_flip)

                shifts[0] = [c for c in shift_flip]


                inv_base = shift_base.translate(str.maketrans('01', '10'))

                inv_flip = inv_base[::-1]

                shifts[1] = [c for c in inv_flip]

                print(inv_flip)

                print(inv_base)


                inv_digits = [int(c) for c in inv_base]



                inv_index = digits_to_index(inv_digits, base)


                print('inv')
                print(inv_index)

                print("")
                print("shifts")
                print(shifts)


                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)



                shifts[2] = shifts[0][::]
                shifts[3] = shifts[1][::]

                # print(int(view/2))

                center = 0

                # print('center')
                # print(center)
                #
                # print(shifts)

                for x in range(2):

                    if shifts[2+x][center] == '0':

                        shifts[2+x][center] = '1'

                    elif shifts[2+x][center] == '1':

                        if base == 2:
                            shifts[2+x][center] = '0'
                        else:
                            shifts[2 + x][center] = '2'

                    elif shifts[2+x][center] == '2':

                        shifts[2 + x][center] = '0'


                # print(shifts)


            elif ruler == 6:

                rule = rule_base.copy()



                shift = digibet[code_0]

                shift = shift % len(rule)

                print()
                print('shift')
                print(shift)

                rule[shift] = str((int(rule[shift]) + 1) % base)

                shift_base = base_x(shift, base)

                shift_base = fill_bin(shift_base)

                shift_flip = shift_base[::-1]



                print('base')
                print(shift_base)
                print(shift_flip)

                shifts[0] = [c for c in shift_flip]


                # inv_base = shift_base.translate(str.maketrans('01', '10'))
                #
                # inv_flip = inv_base[::-1]
                #
                # shifts[1] = [c for c in inv_flip]
                #
                # print(inv_flip)
                #
                # print(inv_base)
                #
                #
                # inv_digits = [int(c) for c in inv_base]
                #
                #
                #
                # inv_index = digits_to_index(inv_digits, base)
                #
                #
                # print('inv')
                # print(inv_index)
                #
                # print("")
                # print("shifts")
                # print(shifts)
                #
                #
                # rule[inv_index] = str((int(rule[inv_index]) + 1) % base)
                #
                #
                #
                # shifts[2] = shifts[0][::]
                # shifts[3] = shifts[1][::]
                #
                # # print(int(view/2))
                #
                # center = 0
                #
                # # print('center')
                # # print(center)
                # #
                # # print(shifts)
                #
                # for x in range(2):
                #
                #     if shifts[2+x][center] == '0':
                #
                #         shifts[2+x][center] = '1'
                #
                #     elif shifts[2+x][center] == '1':
                #
                #         if base == 2:
                #             shifts[2+x][center] = '0'
                #         else:
                #             shifts[2 + x][center] = '2'
                #
                #     elif shifts[2+x][center] == '2':
                #
                #         shifts[2 + x][center] = '0'
                #
                #
                # # print(shifts)












        else:
            letter = code_0

    else:
        letter = code_0


    # print(letter)

    return letter, code_0

def submit(letter):

    # print(letter)

    global phrase, phrase_pos, message, tts, score, times, code, rv, code_0, last_typed, set, tts_0, flow, water

    if letter == last_typed:
        letter = code_0
    elif letter == phrase[phrase_pos] or letter == phrase[phrase_pos:phrase_pos + 2]:
        message += phrase[phrase_pos]
        phrase_pos += 1

        if base == 2:
            flow = np.zeros((h, l), dtype=int)
            flow[int(l / 2), int(h / 2)] = 1
            water = np.zeros((h, l), dtype=int)

            flow[0:mid_x, 0:mid_y] = 1
            flow[0:mid_x, mid_y:h] = 0
            flow[mid_x:l, mid_y:h] = 1
            flow[mid_x:l, 0:mid_y] = 0

        if len(letter) == 2:
            message += phrase[(phrase_pos + 1)%len(phrase)]
            phrase_pos += 1

        if phrase_pos == 1:
            tts[0] = time.time()

        if phrase_pos == len(phrase):

            message += ' '

            score += 1
            phrase_pos = 0
            tts[1] = time.time()

            tts_0 = round(tts[1] - tts[0], 3)
            tts[0] = time.time()

            times_0 = []
            t_max = 99999999999999999999999999999999999999
            for t in times:
                if t < t_max and t > 0:
                    times_0.append(round(t, 3))
            times = times_0

            # print()
            # print(tts)
            # print(tts_0)

            times.append(tts_0)
            times = sorted(times)

            # print()
            # print("times")
            # print(times)

            if phrase == code[len(code) - len(phrase):len(code)]:
                set += 1

            else:
                set = int(set / 2)

            code = ''

            sign_bank[phrase] = (score, rv, times)

            filename = os.path.join(SCRIPT_DIR, 'sign_bank', signame)
            outfile = open(filename, 'wb')
            pickle.dump(sign_bank, outfile)
            outfile.close()

            if ruler == 0:
                set_scale = 1
                for x in range(len(phrase)):
                    rv += digibet[phrase[x]] * int(set / set_scale)
                rv = rv % bbv

                # print("")
                # print(rv)
                # print(rule)
                rules, rule = rule_gen(rv, base)
                # print(rule)

                rule = np.array(rule)

            if dim == 1:
                flow = np.zeros(l, dtype=int)
                flow[int(l / 2)] = 1
                water = np.zeros((h, l), dtype=int)
                water[0] = flow

            if dim == 2:
                if ruler < 4:
                    flow = np.zeros((h, l), dtype=int)
                    flow[int(l / 2), int(h / 2)] = 1
                    water = np.zeros((h, l), dtype=int)


            if dim == 3:
                flow = np.zeros((h, l), dtype=int)
                flow[int(l / 2), int(h / 2)] = 1
                water = np.zeros((h, l), dtype=int)

def base_x(n, b):
    if n == 0:
        return "0"
    digits = ""
    while n > 0:
        digits = str(n % b) + digits
        n //= b
    return digits


####right hand####


x_s = 36
y_s = 36
x_g = 28
y_g = 0
x_pos = (x_s + x_g) * 2
y_pos = 500
palm_x = x_pos + x_s * 6
palm_y = y_pos + y_s * 9

hand = [0, 0, 0, 0, 0, 0]
hand_0 = [0, 0, 0, 0, 0, 0]
hand_1 = [0, 0, 0, 0, 0, 0]

palm = [0, 0, 0, 0, 0, 0]

tips = [64, 16, 0, 24, 0]

right_x = {
    "size": x_s,
    "gap": x_g,
    "start": x_pos,
    "palm": palm_x,
    "step": x_s + x_g
}

right_y = {
    "size": y_s,
    "gap": y_g,
    "start": y_pos,
    "palm": palm_y,
    "step": y_s + y_g
}

right_roi = [
    (
        right_x["start"] + right_x["step"] * (n + 1),
        right_y["start"] + tips[n],
        right_x["start"] + right_x["step"] * (n + 1) + right_x["size"],
        right_y["start"] + tips[n] + right_y["size"]
    )
    for n in range(5)
]

right_roi[4] = (
    right_x["start"] + right_x["step"] * 5 + right_x["size"],
    right_y["start"] + tips[4] + right_y["size"] * 5,
    right_x["start"] + right_x["step"] * 5 + right_x["size"] * 2,
    right_y["start"] + tips[4] + right_y["size"] * 6
)

x_pos = palm_x - x_s * 1
y_pos = palm_y - x_s * 2

right_roi.append((x_pos, y_pos, x_pos + x_s, y_pos + y_s))

roi_map = []
dist_map = []
place = 0

flex_c = 16
flex_m = 64
flex_p = 128



cell_map = [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1)]

rule_base = rule.copy()

###hand variables###

x_s = 36
y_s = 36
x_g = 28
y_g = 0
flex_c = 16
flex_m = 64
flex_p = 128

hands_1 = [0, 0]
hands_0 = [0, 0]
hands = [0, 0]
hand_x = [hands, hands_0, hands_1]


####right hand####
xr_pos = 0
yr_pos = 500
palm_xr = xr_pos + x_s * 6
palm_yr = yr_pos + y_s * 9


hand_r = [0, 0, 0, 0, 0, 0]
hand_r0 = [0, 0, 0, 0, 0, 0]
hand_r1 = [0, 0, 0, 0, 0, 0]

palm_r = [0, 0, 0, 0, 0, 0]

tips_r = [64, 16, 0, 24, 0]

right_x = {
    "size": x_s,
    "gap": x_g,
    "start": xr_pos,
    "palm": palm_xr,
    "step": x_s + x_g
}

right_y = {
    "size": y_s,
    "gap": y_g,
    "start": yr_pos,
    "palm": palm_yr,
    "step": y_s + y_g
}

right_roi = [
    (
        right_x["start"] + right_x["step"] * (n + 1),
        right_y["start"] + tips_r[n],
        right_x["start"] + right_x["step"] * (n + 1) + right_x["size"],
        right_y["start"] + tips_r[n] + right_y["size"]
    )
    for n in range(5)
]

right_roi[4] = (
    right_x["start"] + right_x["step"] * 5 + right_x["size"],
    right_y["start"] + tips_r[4] + right_y["size"] * 5,
    right_x["start"] + right_x["step"] * 5 + right_x["size"] * 2,
    right_y["start"] + tips_r[4] + right_y["size"] * 6
)

xr_pos = palm_xr - x_s * 1
yr_pos = palm_yr - x_s * 2

right_roi.append((xr_pos, yr_pos, xr_pos + x_s, yr_pos + y_s))


right_hand = [0, 0, 0]


def right_hand_detect():
    global hand_r, hand_r0, hand_r1, right_hand, right_roi, hand_x, hands, hands_0, hands_1

    roir_map = []
    distr_map = []


    place = 0


    for roi in right_roi:
        place += 1
        # print(place)

        x1, y1, x2, y2 = roi
        roi_prev = array_past[x1:x2, y1:y2]
        roi_now = hand_array[x1:x2, y1:y2]
        roir_map.append((roi_prev, roi_now))

        if palm_prev[0] is None:
            palm_prev[0] = roi_now.copy()

        roi_dist = color_dist(roi_prev, roi_now)
        roi_mean = np.mean((roi_prev.astype(np.float32) - roi_now.astype(np.float32)) ** 2)
        roi_palm = int(color_dist(roi_now, palm_prev[0]))

        palm_r[place - 1] = roi_palm

        # print(roi_dist)

        dist_map.append(roi_dist)
        if roi_dist > flex_c:
            hand_r[place - 1] = 1
        else:
            hand_r[place - 1] = 0

        if roi_mean > flex_m:
            hand_r0[place - 1] = 1
        else:
            hand_r0[place - 1] = 0

        if roi_mean > flex_p:
            hand_r1[place - 1] = 1
        else:
            hand_r1[place - 1] = 0

        x = place - 1
        value_rect = pygame.Rect(x1, y1, x_s, y_s)
        pygame.draw.rect(screen, value_color[0 + hand_r[x] * 9], value_rect)

        tip_rect = pygame.Rect(x1, y1, x_s / 2, y_s / 2)
        pygame.draw.rect(screen, value_color[0 + hand_r0[x] * 5], tip_rect)

        tip_rect = pygame.Rect(x1, y1, x_s / 3, y_s / 3)
        pygame.draw.rect(screen, value_color[0 + hand_r1[x] * 7], tip_rect)

        pygame.draw.line(screen, value_color[0 + int(goal_bin[x % len(goal_bin)]) * 9], (palm_xr, palm_yr),
                         (roi[0], roi[1]))

    palm_prev[0] = roir_map[-1][1].copy()

    right_hand[0] = hand_r[0] * 16 + hand_r[1] * 8 + hand_r[2] * 4 + hand_r[3] * 2 + hand_r[4] * 1
    right_hand[1] = hand_r0[0] * 16 + hand_r0[1] * 8 + hand_r0[2] * 4 + hand_r0[3] * 2 + hand_r0[4] * 1
    right_hand[2] = hand_r1[0] * 16 + hand_r1[1] * 8 + hand_r1[2] * 4 + hand_r1[3] * 2 + hand_r1[4] * 1

    hands[0] = digibetu[right_hand[0]]
    hands_0[0] = digibetu[right_hand[1]]
    hands_1[0] = digibetu[right_hand[2]]






###left hand###


xl_pos = screen_width - (x_s + x_g) * 7
yl_pos = 500
palm_xl = xl_pos + x_s * 6
palm_yl = yl_pos + y_s * 9

hand_l = [0, 0, 0, 0, 0, 0]
hand_l0 = [0, 0, 0, 0, 0, 0]
hand_l1 = [0, 0, 0, 0, 0, 0]

palm_l = [0, 0, 0, 0, 0, 0]
tips_l = [0, 24, 0, 16, 64]

left_roi = [(xl_pos + (x_s + x_g) * (n + 1), yl_pos + tips_l[n],
             xl_pos + (x_s + x_g) * (n + 1) + x_s, yl_pos + tips_l[n] + y_s) for n in range(5)]
left_roi[0] = (xl_pos + x_s, yl_pos + tips_l[4] + y_s * 4, xl_pos + x_s * 2, yl_pos + tips_l[4] + y_s * 5)

xl_pos = palm_xl - x_s * 1
yl_pos = palm_yl - x_s * 2

left_roi.append((xl_pos, yl_pos, xl_pos + x_s, yl_pos + y_s))




def left_hand_detect():
    global hand_l, hand_l0, hand_l1, left_hand, left_roi, roil_map, distl_map, hands, hands_0, hands_1, hand_x

    roil_map = []
    distl_map = []

    place = 0



    for roi in left_roi:
        place += 1
        # print(place)

        x1, y1, x2, y2 = roi
        roi_prev = array_past[x1:x2, y1:y2]
        roi_now = hand_array[x1:x2, y1:y2]
        roil_map.append((roi_prev, roi_now))

        if palm_prev[1] is None:
            palm_prev[1] = roi_now.copy()

        roi_dist = color_dist(roi_prev, roi_now)
        roi_mean = np.mean((roi_prev.astype(np.float32) - roi_now.astype(np.float32)) ** 2)
        roi_palm = int(color_dist(roi_now, palm_prev[1]))

        palm_l[place - 1] = roi_palm

        # print(roi_dist)

        dist_map.append(roi_dist)
        if roi_dist > flex_c:
            hand_l[place - 1] = 1
        else:
            hand_l[place - 1] = 0

        if roi_mean > flex_m:
            hand_l0[place - 1] = 1
        else:
            hand_l0[place - 1] = 0

        if roi_mean > flex_p:
            hand_l1[place - 1] = 1
        else:
            hand_l1[place - 1] = 0

        x = place - 1
        value_rect = pygame.Rect(x1, y1, x_s, y_s)
        pygame.draw.rect(screen, value_color[0 + hand_l[x] * 9], value_rect)

        tip_rect = pygame.Rect(x1, y1, x_s / 2, y_s / 2)
        pygame.draw.rect(screen, value_color[0 + hand_l0[x] * 5], tip_rect)

        tip_rect = pygame.Rect(x1, y1, x_s / 3, y_s / 3)
        pygame.draw.rect(screen, value_color[0 + hand_l1[x] * 7], tip_rect)

        pygame.draw.line(screen, value_color[0 + int(goal_bin[x % len(goal_bin)]) * 9], (palm_xl, palm_yl),
                         (roi[0], roi[1]))

    # print(left_roi)
    # print(dist_map)
    # print("")
    # print("hand")
    # print(hand)
    # print(hand_0)

    palm_prev[1] = roil_map[-1][1].copy()

    # print('palm l')
    # print(palm)
    # print(hand_1)

    left_hand = [0, 0, 0]

    left_hand[0] = hand_l[0] * 1 + hand_l[1] * 2 + hand_l[2] * 4 + hand_l[3] * 8 + hand_l[4] * 16
    left_hand[1] = hand_l0[0] * 1 + hand_l0[1] * 2 + hand_l0[2] * 4 + hand_l0[3] * 8 + hand_l0[4] * 16
    left_hand[2] = hand_l1[0] * 1 + hand_l1[1] * 2 + hand_l1[2] * 4 + hand_l1[3] * 8 + hand_l1[4] * 16

    hands[1] = digibetu[left_hand[0]]
    hands_0[1] = digibetu[left_hand[1]]
    hands_1[1] = digibetu[left_hand[2]]

    hand_x = [hand_l, hand_l0, hand_l1, hands, hands_0, hands_1, left_hand, right_hand]


running = True
while running:



    screen.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()

    image = camera.get_image()
    image_array = pygame.surfarray.array3d(image)
    hand_array = pygame.surfarray.array3d(image)



    ###water canvas

    ####water type####


    size = 64
    l_size = 32
    x_space = 8
    y_space = 16
    offset_size = 1
    density = 1
    x_o = 128
    y_o = 32 + water_line* (size+16)


    if len(message) > 0:
        canvas , rainbow_reset = canvas_write(message, size, l_size, x_space, y_space, offset_size, density, x_o, y_o, flow)

        # print()
        # print("canvas")
        # print(canvas)


    if rainbow_reset == 1:
        rainbow_array = np.zeros((h, l), dtype=int)
        rainbow_speed += 1
        set += 1



        rainbow_reset = 0

        messages.append(message[::])
        message = []


        if ruler > 3:
            flow = np.zeros((h, l), dtype=int)
            flow[int(l / 2), int(h / 2)] = 1
            water = np.zeros((h, l), dtype=int)


    ###messages###
    messages[0] = message

    os.makedirs(os.path.join(SCRIPT_DIR, 'messages'), exist_ok=True)
    filename = os.path.join(SCRIPT_DIR, 'messages', signame + str(init))
    outfile = open(filename, 'wb')
    pickle.dump(messages, outfile)
    outfile.close()


    pause = 0

    ###flow###
    if dim == 1:

        currents = []
        for x in range(view):

            x = x + 1

            if x == 0:
                currents.append(flow)
            else:
                if x % 2 == 0:
                    shift = -int(x / 2)
                else:
                    shift = int(x / 2)
                flow_r = np.roll(flow, shift)
                currents.append(flow_r)

            # print(currents[x-1])
        current = currents[1] * 1 + currents[0] * base + currents[2] * base**2
        # print(current)
        row = rule[-current.astype(int)]
        # print(row)

        water = np.roll(water, l)
        water[0] = row
        flow = water[0]

        # print(code_flow)

        code_flow = digibet[code_0]

        flow_pos = code_flow*int(l/32)

        flow[flow_pos:flow_pos + int(l/32)] = 1 + score % (base-1)

        image_flow = color_array[water]

        image_array[pos_x:pos_x+l, pos_y:pos_y+h] = np.rot90(image_flow, 4)

    elif dim == 2:


        # l = 592
        # h = l
        # lh = l * h
        # pos_x = int(screen_width / 2) - int(l / 2)
        # pos_y = int(screen_height / 3) - int(h / 2)
        # pos_z = 0

        # flow = np.zeros((h, l), dtype=int)
        # flow[int(l / 2), int(h / 2)] = 1
        # water = np.zeros((h, l), dtype=int)

        for x in range(len(phrase)):

            if phrase[x] in digibet:
                idx = digibet[phrase[x]]

                fx = idx * (l // 32)
                fy = idx * (h // 32)

                # Upper-right seed
                flow[fy, fx] = (flow[fy, fx] + 1) % base

                # Upper-left symmetric seed
                flow[fy, -fx] = (flow[fy, -fx] + 1) % base

        currents = []

        # if view == 5:
        #     flow_1 = np.roll(flow, -1)
        #     flow_2 = np.roll(flow, 1)
        #     flow_3 = np.roll(flow, -l)
        #     flow_4 = np.roll(flow, l)
        #
        #
        #     currents = [flow, flow_1, flow_2, flow_3, flow_4]
        #
        #     current = currents[3] * 1 + currents[1] * base + currents[0] * base ** 2 + currents[2] * base ** 3 + currents[4] * base ** 4
        #     # print()
        #     # print(current)
        #     water = rule[-current.astype(int)]
        #
        #     if sim == 1:
        #         water = rule[-(current.astype(int)%int(len(rule)/base))]
        #
        #     water = water.astype(int)

        if pause == 0:
            water = water_update(flow)



            flow = water
        # sign_value = digibet[code_0]
        # flow[int(l / 2), int(h / 2) +sign_value] = 1



        if rainbow == 0:


            if fade == 0:
                image_flow = color_array[flow]
                image_array[pos_x:pos_x + l, pos_y:pos_y + h] = image_flow

            elif fade == 1:
                mask = flow != 0

                region = image_array[pos_x:pos_x + l, pos_y:pos_y + h]


                region[mask] = color_array[flow[mask]]

                image_array[pos_x:pos_x + l, pos_y:pos_y + h] = region


        if rainbow == 1:



            if base == 2:
                up_mask = water == 1
                down_mask = water == 0

            elif base == 3:

                up_mask = water == 1
                down_mask = water == 2

            elif base == 4:

                up_mask = water == 0
                down_mask = water == 1
                up_mask_0 = water == 2
                down_mask_0 = water == 3

                rainbow_array[up_mask_0] += rainbow_speed * set
                rainbow_array[down_mask_0] -= rainbow_speed * set
                rainbow_array[rainbow_array < 0] = color_max - 1
                rainbow_array[rainbow_array > color_max - 1] = 0

            count_scale = color_max*64

            up_count += int(np.sum(up_mask)/count_scale)
            down_count += int(np.sum(down_mask)/count_scale)

            rainbow_array[up_mask] += rainbow_speed + set
            rainbow_array[down_mask] -= rainbow_speed + set
            rainbow_array[rainbow_array < 0] = color_max-1
            rainbow_array[rainbow_array > color_max-1] = 0



            rainbow_flow = np.zeros((l, h, 3), dtype=np.uint8)

            rainbow_flow = full_colors[rainbow_array]




            region = image_array[pos_x:pos_x+l, pos_y:pos_y+h]
            region_0 = region

            fade = 7

            if fade == 1:
                mask = flow != 0
                region[mask] = rainbow_flow[mask]
            elif fade == 0:
                region = rainbow_flow

            elif fade == 2:
                blended = ((region.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)
                region = blended

            elif fade == 3:

                blended = ((region.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)
                region = blended

                mask = flow != 0
                region[mask] = rainbow_flow[mask]

            ###edge###
            edge = 1
            edge_depth = 32

            if edge == 1:
                gray = region.mean(axis=2)

                gx = np.abs(np.diff(gray, axis=1))
                gy = np.abs(np.diff(gray, axis=0))

                gx = np.pad(gx, ((0, 0), (0, 1)), mode='constant')
                gy = np.pad(gy, ((0, 1), (0, 0)), mode='constant')

                edges = np.sqrt(gx ** 2 + gy ** 2)
                edges = (edges / edges.max() * 255).astype(np.uint8)

                edge_mask = edges > edge_depth

                flow[edge_mask] = (flow[edge_mask] + 1) % base

            if fade == 4:

                blended = ((region.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)
                region = blended

                mask = flow != 0
                region[mask] = rainbow_flow[mask]

                if edge == 1:
                    region[edge_mask] = region_0[edge_mask]

            elif fade == 5:

                alpha = round(1/base, 3)
                if base == 2:
                    alpha = 1
                flow_alpha = np.clip(water, 0, base)
                flow_alpha = flow_alpha[..., np.newaxis]
                blended = (
                        region.astype(np.float32) * (1 - alpha * flow_alpha) +
                        rainbow_flow.astype(np.float32) * (alpha * flow_alpha)
                ).astype(np.uint8)

                region = blended

                if edge == 1:
                    edge_speed = len(message)
                    region[edge_mask] = region_0[edge_mask]

                    rainbow_array[edge_mask] += edge_speed + set
                    rainbow_array[rainbow_array < 0] = color_max - 1
                    rainbow_array[rainbow_array > color_max - 1] = 0


            elif fade == 6:


                image_flow = color_array[flow]

                rainbow_flow = ((image_flow.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)


                alpha = round(1/base, 3)
                flow_alpha = np.clip(water, 0, base)
                flow_alpha = flow_alpha[..., np.newaxis]
                blended = (
                        region.astype(np.float32) * (1 - alpha * flow_alpha) +
                        rainbow_flow.astype(np.float32) * (alpha * flow_alpha)
                ).astype(np.uint8)

                region = blended

                if edge == 1:
                    edge_speed = len(message)
                    region[edge_mask] = region_0[edge_mask]

                    rainbow_array[edge_mask] += edge_speed + set
                    rainbow_array[rainbow_array < 0] = color_max - 1
                    rainbow_array[rainbow_array > color_max - 1] = 0


            elif fade == 7:
                sum_up = np.sum(flow == 1)
                sum_down = np.sum(flow == 0)

                # print()
                # print('sums')
                # print(sum_up)
                print(sum_down)



                image_flow = color_array[flow]

                alpha = round(1, 3)

                mask_1 = up_mask
                mask_0 = down_mask


                base_region = region.astype(np.float32)
                rainbow_region = rainbow_flow.astype(np.float32)


                result = base_region.copy()


                alpha_fade = 0.50
                alpha_full = 1.00


                if sum_up > sum_down:

                    # 1 is more common → fade 1s, full for 0s
                    result[mask_1] = (
                            base_region[mask_1] * (1 - alpha_fade) +
                            rainbow_region[mask_1] * alpha_fade
                    )
                    result[mask_0] = (
                            base_region[mask_0] * (1 - alpha_full) +
                            rainbow_region[mask_0] * alpha_full
                    )

                else:
                    # 0 is more common → fade 0s, full for 1s
                    result[mask_0] = (
                            base_region[mask_0] * (1 - alpha_fade) +
                            rainbow_region[mask_0] * alpha_fade
                    )
                    result[mask_1] = (
                            base_region[mask_1] * (1 - alpha_full) +
                            rainbow_region[mask_1] * alpha_full
                    )

                region = result.astype(np.uint8)

                if edge == 1:

                    # edge_speed = len(message)
                    # region[edge_mask] = region_0[edge_mask]
                    #
                    # rainbow_array[edge_mask] += edge_speed + set
                    # rainbow_array[rainbow_array < 0] = color_max - 1
                    # rainbow_array[rainbow_array > color_max - 1] = 0

                    region[edge_mask] = region_0[edge_mask]
                    rainbow_array[edge_mask] += len(message) + set
                    rainbow_array %= color_max





        image_array[pos_x:pos_x + l, pos_y:pos_y + h] = region





    image = pygame.surfarray.make_surface(image_array)
    screen.blit(image, (0, 0))





    ######runner######

    if runner == 1:

        lesson_t = main_font.render(str((up_count, down_count)), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 16, screen_height / 16))


    #####hands######
    detect_change = 1


    if detect_change == 1:






        ####right hand####

        right_hand_detect()


        ####left hand####
        left_hand_detect()


        #
        # x_s = 36
        # y_s = 36
        # x_g = 28
        # y_g = 0
        #
        # x_pos = screen_width - (x_s+x_g)*7
        # y_pos = 500
        # palm_x = x_pos + x_s*6
        # palm_y = y_pos + y_s*9
        #
        # hand = [0, 0, 0, 0, 0, 0]
        # hand_0 = [0, 0, 0, 0, 0, 0]
        # hand_1 = [0, 0, 0, 0, 0, 0]
        #
        # palm = [0, 0, 0, 0, 0, 0]
        # tips = [0, 24, 0, 16, 64]
        #
        #
        # left_roi = [(x_pos + (x_s + x_g) * (n + 1), y_pos + tips[n],
        #               x_pos + (x_s + x_g) * (n + 1) + x_s, y_pos + tips[n] + y_s) for n in range(5)]
        # left_roi[0] = (x_pos + x_s, y_pos + tips[4] + y_s*4, x_pos + x_s*2, y_pos + tips[4] + y_s*5)
        #
        #
        # x_pos = palm_x - x_s*1
        # y_pos = palm_y - x_s*2
        #
        # left_roi.append((x_pos, y_pos, x_pos + x_s, y_pos + y_s))
        #
        # roi_map = []
        # dist_map = []
        # place = 0
        #
        # # flex_c = 16
        # # flex_m = 24
        # # flex_p = 32
        #
        #
        #
        # for roi in left_roi:
        #     place += 1
        #     # print(place)
        #
        #
        #     x1, y1, x2, y2 = roi
        #     roi_prev = array_past[x1:x2, y1:y2]
        #     roi_now = hand_array[x1:x2, y1:y2]
        #     roi_map.append((roi_prev, roi_now))
        #
        #
        #     if palm_prev[1] is None:
        #         palm_prev[1] = roi_now.copy()
        #
        #
        #
        #     roi_dist = color_dist(roi_prev, roi_now)
        #     roi_mean = np.mean((roi_prev.astype(np.float32) - roi_now.astype(np.float32)) ** 2)
        #     roi_palm = int(color_dist(roi_now, palm_prev[1]))
        #
        #     palm[place-1] = roi_palm
        #
        #     # print(roi_dist)
        #
        #     dist_map.append(roi_dist)
        #     if roi_dist > flex_c:
        #         hand[place-1] = 1
        #     else:
        #         hand[place-1] = 0
        #
        #
        #     if roi_mean > flex_m:
        #         hand_0[place-1] = 1
        #     else:
        #         hand_0[place-1] = 0
        #
        #
        #     if roi_mean > flex_p:
        #         hand_1[place-1] = 1
        #     else:
        #         hand_1[place-1] = 0
        #
        #     x = place-1
        #     value_rect = pygame.Rect(x1, y1, x_s, y_s)
        #     pygame.draw.rect(screen, value_color[0 + hand[x]*9], value_rect)
        #
        #     tip_rect = pygame.Rect(x1, y1, x_s/2, y_s/2)
        #     pygame.draw.rect(screen, value_color[0 + hand_0[x]*5], tip_rect)
        #
        #     tip_rect = pygame.Rect(x1, y1, x_s/3, y_s/3)
        #     pygame.draw.rect(screen, value_color[0 + hand_1[x]*7], tip_rect)
        #
        #     pygame.draw.line(screen, value_color[0 + int(goal_bin[x%len(goal_bin)]) * 9], (palm_x, palm_y), (roi[0], roi[1]))
        #
        # # print(left_roi)
        # # print(dist_map)
        # # print("")
        # # print("hand")
        # # print(hand)
        # # print(hand_0)
        #
        # palm_prev[1] = roi_map[-1][1].copy()
        #
        # # print('palm l')
        # # print(palm)
        # # print(hand_1)
        #
        # left_hand = [0, 0, 0]
        #
        # left_hand[0] = hand[0] * 1 + hand[1]*2 + hand[2]*4 + hand[3]*8 + hand[4]*16
        # left_hand[1] = hand_0[0] * 1 + hand_0[1] * 2 + hand_0[2] * 4 + hand_0[3] * 8 + hand_0[4] * 16
        # left_hand[2] = hand_1[0] * 1 + hand_1[1] * 2 + hand_1[2] * 4 + hand_1[3] * 8 + hand_1[4] * 16
        #
        #
        #
        # hands[1] = digibetu[left_hand[0]]
        # hands_0[1] = digibetu[left_hand[1]]
        # hands_1[1] = digibetu[left_hand[2]]
        #
        # hand_x = [hand, hand_0, hand_1, hands, hands_0, hands_1, left_hand, right_hand]
        #
        # # print()
        # # print('hands')
        # # print(left_hand)
        # # print(right_hand)
        # # print(hands)
        # # print(hands_0)



    ###stats###
    times_limit = 10
    for x in range(len(times)):
        if x > times_limit:
            break
        lesson_t = small_font.render(str(times[x]), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 8, screen_height / 8 + lesson_t.get_height()*x))

    times_limit = 10
    sign_items = list(sign_bank.items())[::]

    for s in sign_items:
        if s[0] == 'steno':
            sign_items.pop(sign_items.index(s))

    sign_items = sorted(sign_items, key=lambda x: x[1][0], reverse=True)
    for x in range(len(sign_items)):
        if x > times_limit:
            break
        lesson_t = text_font.render(str((sign_items[x][1][0], sign_items[x][0])), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 2 + screen_width/2.5, screen_height / 16 + lesson_t.get_height()*x))



    ######phrase walk#######
    walk = 0

    for x in range(len(phrase)):
        color = value_color[9]
        if x == phrase_pos:
            color = value_color[5]


        row_limit = 24
        y = int(x/row_limit)

        if x%row_limit == 0:
            walk = 0

        lesson_t = lable_font.render(str(phrase[x]), True, color)
        screen.blit(lesson_t, (screen_width / 2 + walk - screen_width/4.3, screen_height / 2 + lesson_t.get_height()*y+ 128))
        walk += lesson_t.get_width()



    letters = []


    letter, code_0 = handle(hands, code_0)
    letter_0, code_00 = handle(hands_0, code_00)
    letter_1, code_01 = handle(hands_1, code_01)



    ###typing###
    if phrase != '':

        goal_bin = base_x(digibet[phrase[phrase_pos]], 2)
        if len(goal_bin) < gb_len:
            zeros = ''
            for x in range(5-len(goal_bin)):
                zeros += '0'
            goal_bin = zeros + goal_bin
        # print(goal_bin)

        if phrase != phrase_past:

            rainbow_array = np.zeros((h, l), dtype=int)


            tts[0] = time.time()
            score = 1

            if phrase not in sign_bank:
                sign_bank[phrase] = (score, rv, [])

                score, rv, times = sign_bank[phrase]
            else:

                try:
                    score, rv , times = sign_bank[phrase]
                except:

                    try:
                        score, rv = sign_bank[phrase]
                        times = []

                    except:

                        score = sign_bank[phrase]
                        rv = rv
                        times = []




            # print(phrase, sign_bank[phrase])

            phrase_past = phrase[::]

            filename = os.path.join(SCRIPT_DIR, 'sign_bank', signame)
            outfile = open(filename, 'wb')
            pickle.dump(sign_bank, outfile)
            outfile.close()


        if letter != last_typed:
            submit(letter)
            last_typed = letter

        elif letter_0 != last_typed:
            submit(letter_0)
            last_typed = letter_0

        elif letter_1 != last_typed:
            submit(letter_1)
            last_typed = letter_1


        # elif letter == phrase[phrase_pos] or letter == phrase[phrase_pos:phrase_pos+2]:
        #
        #     message += phrase[phrase_pos]
        #
        #     if len(letter) == 2:
        #         message += phrase[phrase_pos + 1]
        #         phrase_pos += 1
        #
        #     phrase_pos += 1
        #
        #     if phrase_pos == 1:
        #         tts[0] = time.time()
        #
        #     if phrase_pos == len(phrase):
        #
        #
        #         message += ' '
        #
        #         score += 1
        #         phrase_pos = 0
        #         tts[1] = time.time()
        #
        #
        #         tts_0 = round(tts[1] - tts[0], 3)
        #         tts[0] = time.time()
        #
        #         times_0 = []
        #         t_max = 99999999999999999999999999999999999999
        #         for t in times:
        #             if t < t_max and t > 0:
        #                 times_0.append(round(t, 3))
        #         times = times_0
        #
        #         # print()
        #         # print(tts)
        #         # print(tts_0)
        #
        #         times.append(tts_0)
        #         times = sorted(times)
        #
        #         # print()
        #         # print("times")
        #         # print(times)
        #
        #
        #
        #         if phrase == code[len(code)-len(phrase):len(code)]:
        #             set += 1
        #
        #         else:
        #             set = int(set/2)
        #
        #
        #         code = ''
        #
        #         sign_bank[phrase] = (score, rv, times)
        #
        #
        #         filename = 'sign_bank/' + signame
        #         outfile = open(filename, 'wb')
        #         pickle.dump(sign_bank, outfile)
        #         outfile.close
        #
        #
        #
        #
        #
        #
        #         if ruler == 0:
        #             set_scale = 1
        #             for x in range(len(phrase)):
        #                 rv += digibet[phrase[x]]*int(set/set_scale)
        #             rv = rv % bbv
        #
        #             # print("")
        #             # print(rv)
        #             # print(rule)
        #             rules, rule = rule_gen(rv, base)
        #             # print(rule)
        #
        #             rule = np.array(rule)
        #
        #         if dim == 1:
        #             flow = np.zeros(l, dtype=int)
        #             flow[int(l / 2)] = 1
        #             water = np.zeros((h, l), dtype=int)
        #             water[0] = flow
        #
        #         if dim == 2:
        #             flow = np.zeros((h, l), dtype=int)
        #             flow[int(l / 2), int(h / 2)] = 1
        #             water = np.zeros((h, l), dtype=int)
        #
        # elif letter_0 == phrase[phrase_pos] or letter_0 == phrase[phrase_pos:phrase_pos+2]:
        #
        #     message += phrase[phrase_pos]
        #
        #     if len(letter_0) == 2:
        #         message += phrase[phrase_pos + 1]
        #         phrase_pos += 1
        #
        #     phrase_pos += 1
        #
        #     if phrase_pos == 1:
        #         tts[0] = time.time()
        #
        #     if phrase_pos == len(phrase):
        #
        #
        #         message += ' '
        #
        #         score += 1
        #         phrase_pos = 0
        #         tts[1] = time.time()
        #
        #
        #         tts_0 = round(tts[1] - tts[0], 3)
        #         tts[0] = time.time()
        #
        #         times_0 = []
        #         t_max = 99999999999999999999999999999999999999
        #         for t in times:
        #             if t < t_max and t > 0:
        #                 times_0.append(round(t, 3))
        #         times = times_0
        #
        #         # print()
        #         # print(tts)
        #         # print(tts_0)
        #
        #         times.append(tts_0)
        #         times = sorted(times)
        #
        #         # print()
        #         # print("times")
        #         # print(times)
        #
        #
        #
        #         if phrase == code[len(code)-len(phrase):len(code)]:
        #             set += 1
        #
        #         else:
        #             set = int(set/2)
        #
        #
        #         code = ''
        #
        #         sign_bank[phrase] = (score, rv, times)
        #
        #
        #         filename = 'sign_bank/' + signame
        #         outfile = open(filename, 'wb')
        #         pickle.dump(sign_bank, outfile)
        #         outfile.close
        #
        #
        #
        #
        #
        #
        #         if ruler == 0:
        #             set_scale = 1
        #             for x in range(len(phrase)):
        #                 rv += digibet[phrase[x]]*int(set/set_scale)
        #             rv = rv % bbv
        #
        #             # print("")
        #             # print(rv)
        #             # print(rule)
        #             rules, rule = rule_gen(rv, base)
        #             # print(rule)
        #
        #             rule = np.array(rule)
        #
        #         if dim == 1:
        #             flow = np.zeros(l, dtype=int)
        #             flow[int(l / 2)] = 1
        #             water = np.zeros((h, l), dtype=int)
        #             water[0] = flow
        #
        #         if dim == 2:
        #             flow = np.zeros((h, l), dtype=int)
        #             flow[int(l / 2), int(h / 2)] = 1
        #             water = np.zeros((h, l), dtype=int)



    ### rule display #####

    if base == 2:

        if view == 5:
            rule_l = 32
            rule_h = rule_l
            cells = len(rule)
            rows = 4
            bins = 8

            print(rule)



            for r in range(len(rule)):



                rule_x = screen_width / 3 + rule_l * (r % bins)
                rule_y =  (screen_height / 16 + rule_h * (int(r / bins)))

                # Convert rule index r into 5-bit state pattern
                x_bin = base_x(r, base)  # raw binary string like "101"
                x_bin = x_bin.zfill(5)  # → always 5 bits: "00101"

                # Rule output value (0 or 1)
                rule_value = int(rule[r])  # convert '0'/'1' → 0/1


                # Draw the 5-cell neighborhood pattern
                cell_map = [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1)]  # center, L, R, up, down

                xs = rule_l / 4
                ys = rule_h / 4
                # print()
                # print(r)
                # print(x_bin)
                # print(rule_value)

                for i in range(5):
                    cx = rule_x + cell_map[-i - 1][0] * xs
                    cy = rule_y + cell_map[-i - 1][1] * ys

                    rect = pygame.Rect(cx, cy, xs, ys)



                    # Color = VALUE OF RULE OUTPUT
                    pygame.draw.rect(screen, value_color[int(x_bin[i])*1 + rule_value*7], rect)

                    if rect.collidepoint((mx, my)):
                        print('collide')
                        if click:
                            print('click')
                            r_plus = (int(rule[r]) + 1)%base
                            rule[r] = str(r_plus)
                            rule_base = rule.copy()

                            click = False





        if view == 9:
            rule_l = 9
            rule_h = 9

            # print(rule)

            rows = 7

            for x in range(len(rule)):
                rule_x = screen_width / 2 + (x % int(len(rule) / rows)) * rule_l - int(len(rule) / (2 * rows)) * rule_l
                rule_y = screen_height - screen_height / 16 - screen_height / 16 + rule_h * int(
                    x / int(len(rule) / rows))

                t_line = pygame.Rect(rule_x, rule_y, rule_l, rule_h)
                pygame.draw.rect(screen, value_color[(int(rule[x]))], t_line)

    elif base == 3:
        rule_l = 9
        rule_h = 9

        # print(rule)

        rows = 7

        for x in range(len(rule)):
            rule_x = screen_width / 2 + (x % int(len(rule) / rows)) * rule_l - int(len(rule) / (2*rows)) * rule_l
            rule_y = screen_height - screen_height/16 - screen_height / 16 + rule_h * int(x / int(len(rule) / rows))

            t_line = pygame.Rect(rule_x, rule_y, rule_l, rule_h)
            pygame.draw.rect(screen, value_color[(int(rule[x]))], t_line)

    elif base == 4:
        rule_l = 4
        rule_h = 4

        # print(rule)

        rows = 20

        for x in range(len(rule)):
            rule_x = screen_width / 2 + (x % int(len(rule) / rows)) * rule_l - int(len(rule) / (2*rows)) * rule_l
            rule_y = screen_height - screen_height/16 - screen_height / 16 + rule_h * int(x / int(len(rule) / rows))

            t_line = pygame.Rect(rule_x, rule_y, rule_l, rule_h)
            pygame.draw.rect(screen, value_color[(int(rule[x]))], t_line)




    ###code display####

    for x in range(int(len(code)/64)+1):
        lesson_t = main_font.render(str(code), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 2 - int(lesson_t.get_width()/2), screen_height / 8 - 128 + x*lesson_t.get_height()))

    lesson_t = lable_font.render('score' + str(score), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 4 - 192, screen_height / 32 - 32))

    lesson_t = main_font.render('set' + str(set), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 4 - 256, screen_height / 32 - 32))

    lesson_t = main_font.render('speed' + str(rainbow_speed), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 4, screen_height / 32 - 32))

    lesson_t = main_font.render('tts: ' + str(tts_0), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 64, screen_height / 2 - 32))



    ###synth###
    beat = 1
    volume = 0.3
    ######bong#####
    if bong_on == 1:
        if time.time() - time_b > beat:
            print('gong')

            # if dim == 2:
            #
            #     code_flow = digibet[code_0]
            #     flow_pos = code_flow * int(l / 32) + int(l / 128)
            #     flow[1:l, flow_pos:flow_pos + int(l / 64)] += 1
            #     flow[flow_pos:flow_pos + int(l / 64), 1:h] += 1
            #     flow[1:l, flow_pos:flow_pos + int(l / 64)] = flow[1:l, flow_pos:flow_pos + int(l / 64)] % base
            #     flow[flow_pos:flow_pos + int(l / 64), 1:h] = flow[flow_pos:flow_pos + int(l / 64), 1:h] % base

            if dim == 1:
                water0 = np.rot90(water[::], 2)
            elif dim == 2:
                water0 = water

            if dim > 0:

                flatten = water0.flatten()
                scaled = (flatten * 2 - 1) * max_amplitude
                sample = scaled.astype(np.int16)
                stereo = sample.reshape(-1, 1)
                stack = np.column_stack((stereo, stereo))
                flow_sound = pygame.sndarray.make_sound(stack)

                flow_sound.play()



            # print()
            # print('bong')
            #



            # note_value = digibet[code_0]
            #
            #
            # # print(note_value)
            #
            # octave = 24

            # note_shape = int(note_value/8)
            # note_scale = sum(waffle_house[:note_value%8])
            #
            # note_scale = sum(scale[:note_value%8])
            # note_scale += track_shift
            # note_scale = note_scale + octave % len(key_sin)

            # print(note_shape)
            # print(note_scale)

            # note_shape = 0
            # note_scale = note_value + octave
            #
            # if note_shape == 0:
            #
            #     key_sin[note_scale].set_volume(volume)
            #     key_sin[note_scale].play()
            #
            # elif note_shape == 1:
            #
            #     key_square[note_scale].set_volume(volume-.25)
            #     key_square[note_scale].play()
            #
            # elif note_shape == 2:
            #
            #     key_saw[note_scale].set_volume(volume-.25)
            #     key_saw[note_scale].play()
            #
            # elif note_shape == 3:
            #
            #     key_triangle[note_scale].set_volume(volume)
            #     key_triangle[note_scale].play()
            #


            time_b = time.time()





    ###shifts###

    for i in range(5):


        cell_map = [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1)]

        xs = 16
        ys = 16
        x = screen_width / 2 + int(cell_map[i][0]*xs) + xs*1
        y = screen_height / 7 + int(cell_map[i][1]*ys)


        if base == 2:
            design = pygame.Rect(x, y, xs, ys)
            pygame.draw.rect(screen, value_color[int(shifts[0][i])*9], design)

            design = pygame.Rect(x + xs*4, y, xs, ys)
            pygame.draw.rect(screen, value_color[int(shifts[1][i])*9], design)

            design = pygame.Rect(x + xs*8, y, xs, ys)
            pygame.draw.rect(screen, value_color[int(shifts[2][i])*9], design)

            design = pygame.Rect(x + xs*12, y, xs, ys)
            pygame.draw.rect(screen, value_color[int(shifts[3][i])*9], design)

        elif base == 3:
            design = pygame.Rect(x, y, xs, ys)
            pygame.draw.rect(screen, value_color[int(shifts[0][i])], design)

            design = pygame.Rect(x + xs * 4, y, xs, ys)
            pygame.draw.rect(screen, value_color[int(shifts[1][i])], design)

            design = pygame.Rect(x + xs * 8, y, xs, ys)
            pygame.draw.rect(screen, value_color[int(shifts[2][i])], design)

            design = pygame.Rect(x + xs * 12, y, xs, ys)
            pygame.draw.rect(screen, value_color[int(shifts[3][i])], design)



    ###buttons###


    #####dim#####
    x = screen_width/8
    y = screen_height - screen_height/8

    xs = 30
    ys = 30

    design = pygame.Rect(x, y, xs, ys)
    design_i = pygame.Rect(x, y, int(xs/2), int(ys/2))
    pygame.draw.rect(screen, (100, 10, 100), design)
    pygame.draw.rect(screen, (0, 0, 0), design_i)

    if design.collidepoint((mx, my)):
        print('collide')
        if click:
            print('click')
            dim += 2
            dim = dim%4

            click = False



    #####bong#####
    x = screen_width - screen_width/8
    y = screen_height - screen_height/8

    xs = 30
    ys = 30

    design = pygame.Rect(x, y, xs, ys)
    design_i = pygame.Rect(x, y, int(xs/2), int(ys/2))
    pygame.draw.rect(screen, (100, 10, 100), design)
    pygame.draw.rect(screen, (0, 0, 0), design_i)

    if design.collidepoint((mx, my)):

        if click:
            print('bong')
            bong_on += 1
            bong_on = bong_on%2

            print("bong_on")
            print(bong_on)


            click = False



    #####bong#####
    x = screen_width - screen_width/8
    y = screen_height - screen_height/8

    xs = 30
    ys = 30

    design = pygame.Rect(x, y, xs, ys)
    design_i = pygame.Rect(x, y, int(xs/2), int(ys/2))
    pygame.draw.rect(screen, (100, 10, 100), design)
    pygame.draw.rect(screen, (0, 0, 0), design_i)

    if design.collidepoint((mx, my)):

        if click:
            print('bong')
            bong_on += 1
            bong_on = bong_on%2

            print("bong_on")
            print(bong_on)


            click = False


    #####rainbow#####
    x = screen_width - screen_width/2
    y = screen_height - screen_height/32

    xs = 30
    ys = 30

    design = pygame.Rect(x, y, xs, ys)
    design_i = pygame.Rect(x, y, int(xs/2), int(ys/2))
    pygame.draw.rect(screen, (100, 10, 100), design)
    pygame.draw.rect(screen, (0, 0, 0), design_i)

    if design.collidepoint((mx, my)):

        if click:
            print('rainbow')
            rainbow += 1
            rainbow = rainbow%2



            click = False



    click = False
    ####events####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            filename = os.path.join(SCRIPT_DIR, 'sign_bank', signame)
            outfile = open(filename, 'wb')
            pickle.dump(sign_bank, outfile)
            outfile.close()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                print('click')
                click = True
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_ESCAPE:
        #         pygame.quit()
        #
        #     elif event.key == pygame.K_RETURN:
        #
        #         threshold = mse
        #         array_past = image_array
        #
        #         print(threshold)
        #         print('past')

        # keyboard
        elif event.type == pygame.KEYDOWN:

            def type(phrase, letter):
                print("letter")

                phrase += letter

                return phrase


            if event.key == pygame.K_ESCAPE:
                filename = os.path.join(SCRIPT_DIR, 'sign_bank', signame)
                outfile = open(filename, 'wb')
                pickle.dump(sign_bank, outfile)
                outfile.close()
                pygame.quit()

            elif event.key == pygame.K_RETURN:


                rethresh = 1
                array_past = hand_array

                # print()
                # print(current)
                # print(lessons[current])
                # print(phrase)
                #
                # print(len(lessons[current]))
                # print(len(phrase))
                #
                # records['current'] = current
                #
                # focus = 0
                #
                # if phrase == lessons[current]:
                #     valid = 3
                #     power[0] += 1
                # else:
                #     valid = 1
                #     power[0] = 0
                #
                # clock[1] = clock[0]
                # clock[0] = time.time()
                #
                # # records
                # if valid == 3:
                #
                #     if record == 1:
                #
                #         if time_0 < records[current]:
                #             records[current] = time_0
                #             valid = 4
                #
                #         filename = 'records/' + record_name
                #         outfile = open(filename, 'wb')
                #         pickle.dump(records, outfile)
                #         outfile.close
                #
                #     current += 1
                #
                # phrase_1 = phrase[::]
                # phrase = ''
                # settings = 0
                # men = 0


            elif event.key == pygame.K_F1:

                print("wu")
                phrase = ''


            elif event.key == pygame.K_F2:
                array_past = image_array

            # elif event.key == pygame.K_LEFT:
            #     current -= 1
            #
            # elif event.key == pygame.K_RIGHT:
            #     current += 1
            #
            elif event.key == pygame.K_UP:

                for x in range(len(thresholds)):
                    thresholds[x] += 1

            elif event.key == pygame.K_DOWN:

                for x in range(len(thresholds)):
                    thresholds[x] = thresholds[x] - 1

            # upper
            elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'A'

            elif event.key == pygame.K_b and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'B'

            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'C'

            elif event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'D'

            elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'E'

            elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'F'

            elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'G'

            elif event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'H'

            elif event.key == pygame.K_i and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'I'

            elif event.key == pygame.K_j and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'J'

            elif event.key == pygame.K_k and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'K'

            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'L'

            elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'M'

            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'N'

            elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'O'

            elif event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'P'

            elif event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'Q'

            elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'R'

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'S'

            elif event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'T'

            elif event.key == pygame.K_u and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'U'

            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'V'

            elif event.key == pygame.K_w and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'W'

            elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'X'

            elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'Y'

            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += 'Z'

            elif event.key == pygame.K_9 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += '('

            elif event.key == pygame.K_0 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += ')'

            elif event.key == pygame.K_1 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += '!'

            # number
            elif event.key == pygame.K_0:
                phrase += '0'
            elif event.key == pygame.K_1:
                phrase += '1'
            elif event.key == pygame.K_2:
                phrase += '2'
            elif event.key == pygame.K_3:
                phrase += '3'
            elif event.key == pygame.K_4:
                phrase += '4'
            elif event.key == pygame.K_5:
                phrase += '5'
            elif event.key == pygame.K_6:
                phrase += '6'
            elif event.key == pygame.K_7:
                phrase += '7'
            elif event.key == pygame.K_8:
                phrase += '8'
            elif event.key == pygame.K_9:
                phrase += '9'



            # lower
            elif event.key == pygame.K_a:
                phrase += 'a'

            elif event.key == pygame.K_b:
                phrase += 'b'

            elif event.key == pygame.K_c:
                phrase += 'c'

            elif event.key == pygame.K_d:
                phrase += 'd'

            elif event.key == pygame.K_e:
                phrase += 'e'

            elif event.key == pygame.K_f:
                phrase += 'f'

            elif event.key == pygame.K_g:
                phrase += 'g'

            elif event.key == pygame.K_h:
                phrase += 'h'

            elif event.key == pygame.K_i:
                phrase += 'i'

            elif event.key == pygame.K_j:
                phrase += 'j'

            elif event.key == pygame.K_k:
                phrase += 'k'

            elif event.key == pygame.K_l:
                phrase += 'l'

            elif event.key == pygame.K_m:
                phrase += 'm'

            elif event.key == pygame.K_n:
                phrase += 'n'

            elif event.key == pygame.K_o:
                phrase += 'o'

            elif event.key == pygame.K_p:
                phrase += 'p'

            elif event.key == pygame.K_q:
                phrase += 'q'

            elif event.key == pygame.K_r:
                phrase += 'r'

            elif event.key == pygame.K_s:
                phrase += 's'

            elif event.key == pygame.K_t:
                phrase += 't'

            elif event.key == pygame.K_u:
                phrase += 'u'

            elif event.key == pygame.K_v:
                phrase += 'v'

            elif event.key == pygame.K_w:
                phrase += 'w'

            elif event.key == pygame.K_x:
                phrase += 'x'

            elif event.key == pygame.K_y:
                phrase += 'y'

            elif event.key == pygame.K_z:
                phrase += 'z'

            elif event.key == pygame.K_SPACE:
                phrase += ' '

            elif event.key == pygame.K_PERIOD:
                phrase += '.'

            elif event.key == pygame.K_COMMA:
                phrase += ','

            elif event.key == pygame.K_SLASH and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += '?'

            elif event.key == pygame.K_EXCLAIM:
                phrase += '!'

            elif event.key == pygame.K_SEMICOLON and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += ':'

            elif event.key == pygame.K_SEMICOLON:
                phrase += ';'

            elif event.key == pygame.K_QUOTE and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                phrase += '"'

            elif event.key == pygame.K_QUOTE:
                phrase += "'"

            elif event.key == pygame.K_MINUS:
                phrase += "-"

            elif event.key == pygame.K_LEFTBRACKET:
                phrase += '['

            elif event.key == pygame.K_RIGHTBRACKET:
                phrase += ']'





            elif event.key == pygame.K_BACKSPACE:
                phrase = phrase[:-1]
                phrase_pos -= 1
                if phrase_pos < 0:
                    phrase_pos = 0

    #####################
    pygame.display.flip()
    pygame.display.flip()

camera.stop()
pygame.quit()


