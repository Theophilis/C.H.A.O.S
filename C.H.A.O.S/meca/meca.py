import pygame
import pygame.camera
import pygame.surfarray as surfarray
import pygame.font
import numpy as np
import pickle
import time
import os
from datetime import datetime
import pyautogui
import pygame.midi
import socket





# -----------------------------
# FLOW NETWORK CLIENT
# -----------------------------
FLOW_HOST = "127.0.0.1"   # same computer
FLOW_PORT = 50505

flow_client = None
flow_last_connect_try = 0


def connect_to_flow():
    global flow_client, flow_last_connect_try

    if flow_client is not None:
        return flow_client

    now = time.time()
    if now - flow_last_connect_try < 2.0:
        return None

    flow_last_connect_try = now

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((FLOW_HOST, FLOW_PORT))
        s.settimeout(None)

        flow_client = s
        print("Connected to Flow:", FLOW_HOST, FLOW_PORT)
        return flow_client

    except Exception as e:
        print("Flow not connected yet:", e)
        flow_client = None
        return None


def send_sign_to_flow(sign, score_0):
    global flow_client

    # make one readable network line
    msg = str(sign)
    score_0 = int(score_0)

    packet = msg + "|" + str(score_0) + "\n"

    s = connect_to_flow()
    if s is None:
        return

    try:
        s.sendall(packet.encode("utf-8"))
        print("SENT TO FLOW:", repr(packet))

    except Exception as e:
        print("Flow send failed:", e)

        try:
            s.close()
        except:
            pass

        flow_client = None





pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.02

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





signame = "Chaotomata"


signame = "Theophilis"

signame = 'Chal'






###theo screen###
screen_width, screen_height = 1280, 960


###chao screen###
screen_width, screen_height = 1922, 1082






screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('C.H.A.O.S')



text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)



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




###pygame cam###

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


arms = [0, 0]
code = ''
code_0 = ' '
code_00 = ' '
code_01 = ' '

score = 1
se = 0
score_h = 0
sign_bank = {}
bank_past = sign_bank
bank_chart = {}

phrase_past = phrase[::]
tts = [0, 0]
times = []
tts_0 = time.time()
tts_1 = time.time()
stenograph = []


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
rainbow_speed = 1
speed_limit = 99
edge_speed = 1
base = 2
base2 = base * base
base3 = base2 * base
base4 = base3 * base
view = 5
fade = 1



bv = base ** view
bvv = base ** view ** view
bbv = base**base**view
rv = 1431655766
rv_base = rv
rv_bank = {}


#####rulers######
rules, rule = rule_gen(rv, base)
rule = np.array(rule)
lookup = np.array(rule, dtype=np.uint8)

ruler = 4
shift = 0
flow_state = 12

print(rule)

l = 500
h = l
lh = l * h
pos_x = int(screen_width / 2) - int(l / 2)
pos_y = int(screen_height / 2) - int(h / 2)
pos_z = 0
mid_x = l // 2
mid_y = h // 2



####flow_state####

if dim == 1:
    flow = np.zeros(l, dtype=int)
    flow[int(l / 2)] = 1
    water = np.zeros((h, l), dtype=int)
    water[0] = flow

if dim == 2:

    if flow_state == 0:
        flow = np.zeros((h, l), dtype=int)
        flow[int(l / 2), int(h / 2)] = 1
        water = np.zeros((h, l), dtype=int)

        flow[0:mid_x, 0:mid_y] = 1
        flow[0:mid_x, mid_y:h] = 0
        flow[mid_x:l, 0:mid_y] = 1
        flow[mid_x:l, mid_y:h] = 0

        flow_base = flow.copy()

    elif flow_state == 1:

        flow = np.zeros((h, l), dtype=int)
        flow[int(l / 2), int(h / 2)] = 1
        water = np.zeros((h, l), dtype=int)

        def flow_radial(flow, base):
            h, l = flow.shape
            cx, cy = l // 2, h // 2
            ring_width = 6

            for y in range(h):
                for x in range(l):
                    d = int(((x - cx) ** 2 + (y - cy) ** 2) ** 0.5)
                    flow[y, x] = (d // ring_width) % base

            return flow

        flow_base = flow_radial(flow, base)

    elif flow_state == 2:
        def flow_yinyang(h, l, base=2):
            flow = np.zeros((h, l), dtype=np.uint8)

            cx = l // 2
            cy = h // 2
            R = min(cx, cy) * 0.9  # outer radius

            Y, X = np.ogrid[:h, :l]
            dx = X - cx
            dy = Y - cy
            dist = np.sqrt(dx * dx + dy * dy)

            # Inside the outer circle only
            inside = dist <= R

            # --- MAIN SWIRL PART ---
            # For Yin–Yang, top and bottom halves each contain one swirl.

            # Center of upper swirl
            uy = cy - R / 2
            # Center of lower swirl
            ly = cy + R / 2

            # distance to each swirl center
            dist_upper = np.sqrt(dx * dx + (dy - uy) ** 2)
            dist_lower = np.sqrt(dx * dx + (dy - ly) ** 2)

            # The rule:
            # - If pixel is closer to upper swirl center → color 1
            # - If closer to lower swirl center → color 0
            main = (dist_upper < dist_lower).astype(np.uint8)

            # --- INNER DOTS ---
            dot_r = R * 0.25

            # Upper small dot
            dot_up = dist_upper < dot_r
            # Lower small dot
            dot_down = dist_lower < dot_r

            # Apply final pattern
            flow[:] = 0
            flow[inside] = main[inside]

            # dots invert the region
            flow[dot_up] = 0  # dot inside yang (black dot)
            flow[dot_down] = 1  # dot inside yin (white dot)

            # mod for multibase automata
            if base > 2:
                flow = flow % base

            return flow

        flow = flow_yinyang(h, l, base)
        flow_base = flow.copy()

    elif flow_state == 3:
        def flow_quad_circles(h, l):
            """
            Creates a 4-quadrant flow state:
              TL: 0 with 1-circle
              TR: 1 with 0-circle
              BL: 1 with 0-circle
              BR: 0 with 1-circle
            All circles same radius, perfectly centered in each quadrant.
            """

            flow = np.zeros((h, l), dtype=np.uint8)

            # Quadrant size
            h2 = h // 2
            l2 = l // 2

            # Circle radius — use 1/3 of min quadrant dimension
            r = int(min(h2, l2) * 0.33)

            # Quadrant centers
            centers = [
                (h2 // 2, l2 // 2),  # TL
                (h2 // 2, l2 + l2 // 2),  # TR
                (h2 + h2 // 2, l2 // 2),  # BL
                (h2 + h2 // 2, l2 + l2 // 2)  # BR
            ]

            # Background values per quadrant
            backgrounds = [0, 1, 1, 0]

            # Circle values per quadrant
            circles = [1, 0, 0, 1]

            # Fill quadrants
            flow[:h2, :l2] = backgrounds[0]  # TL
            flow[:h2, l2:] = backgrounds[1]  # TR
            flow[h2:, :l2] = backgrounds[2]  # BL
            flow[h2:, l2:] = backgrounds[3]  # BR

            # Draw circles
            Y, X = np.ogrid[:h, :l]

            for (cy, cx), circle_val in zip(centers, circles):
                mask = (X - cx) ** 2 + (Y - cy) ** 2 <= r * r
                flow[mask] = circle_val

            return flow

        flow = flow_quad_circles(h, l)
        flow_base = flow.copy()

    elif flow_state == 4:

        def flow_quad_circle_stamp(h, l, base=2):
            """
            Creates a centered quad-inverted circle stamp pattern:
            - 4 quadrants: TL=0, TR=1, BL=1, BR=0
            - Inside circle: values are inverted
            - Output: h x l array of 0/1 (mod base)
            """

            flow = np.zeros((h, l), dtype=np.uint8)
            mid_y = h // 2
            mid_x = l // 2

            # quadrant base values
            # TL=0, TR=1, BL=1, BR=0
            flow[:mid_y, :mid_x] = 0  # TL
            flow[:mid_y, mid_x:] = 1  # TR
            flow[mid_y:, :mid_x] = 1  # BL
            flow[mid_y:, mid_x:] = 0  # BR

            # build circle mask
            Y, X = np.ogrid[:h, :l]
            dist = (X - mid_x) ** 2 + (Y - mid_y) ** 2

            # radius chosen to give equal 1s and 0s
            # area(circle) ~ half the square
            r = int(min(h, l) * (1 / (2 * np.pi)) ** 0.5)

            circle_mask = dist <= r * r

            # inside circle → invert
            flow[circle_mask] = (1 - flow[circle_mask]) % base

            return flow

        flow = flow_quad_circle_stamp(h, l)
        flow_base = flow.copy()

    elif flow_state == 5:


        def fibonacci_spiral_mask(h, w, turns=6.0, stripes=10, center=None):
            """
            Returns a boolean mask with EXACTLY ~50% True/False (as close as possible),
            with a golden (Fibonacci) spiral structure.
            """
            if center is None:
                cy, cx = h // 2, w // 2
            else:
                cy, cx = center

            Y, X = np.ogrid[:h, :w]
            dx = (X - cx).astype(np.float32)
            dy = (Y - cy).astype(np.float32)

            r = np.sqrt(dx * dx + dy * dy) + 1e-6
            theta = np.arctan2(dy, dx)  # [-pi, pi]

            phi = (1 + 5 ** 0.5) / 2.0
            b = (2.0 * np.log(phi)) / np.pi  # golden spiral growth rate

            # Spiral coordinate (constant along the spiral)
            F = np.log(r) - b * theta

            # Optional: add "rings/stripes" perpendicular to the spiral
            # This makes the spiral read more clearly than a single boundary.
            F_striped = np.sin(2 * np.pi * stripes * (F - F.min()) / (F.max() - F.min() + 1e-9))

            # Only keep a limited number of turns (window it) so it doesn't dominate edges
            # (Optional – comment out if you want full-screen)
            theta_span = turns * 2 * np.pi
            # unwrap theta-ish by using F as the window driver: keep central portion
            # Simple radial window:
            rmax = min(h, w) * 0.48
            window = r < rmax
            vals = F_striped[window]

            # Choose threshold so half of the *windowed* pixels are True
            t = np.median(vals)

            mask = np.zeros((h, w), dtype=bool)
            mask[window] = F_striped[window] > t

            # If you want 50/50 across the ENTIRE screen, not just window:
            # t = np.median(F_striped)
            # mask = F_striped > t

            return mask


        mask = fibonacci_spiral_mask(h, l, stripes=12, turns=6.0)
        flow = np.zeros((h, l), dtype=np.uint8)
        flow[mask] = 1
        flow_base = flow.copy()

    elif flow_state == 6:
        def _segment_norm_dist(X, Y, ax, ay, bx, by, thickness_px):
            """Normalized distance to segment A->B: dist/thickness."""
            abx = bx - ax
            aby = by - ay
            ab2 = abx * abx + aby * aby + 1e-12

            apx = X - ax
            apy = Y - ay

            t = (apx * abx + apy * aby) / ab2
            t = np.clip(t, 0.0, 1.0)

            cx = ax + t * abx
            cy = ay + t * aby

            dx = X - cx
            dy = Y - cy
            dist = np.sqrt(dx * dx + dy * dy)
            return dist / (thickness_px + 1e-9)


        def _hexagram_segments(cx, cy, R):
            """
            Return 6 segments (two equilateral triangles) for a Star of David centered at (cx,cy)
            with circumradius R (pixel units).
            """

            def verts(deg_list):
                ang = np.deg2rad(deg_list)
                vx = cx + R * np.cos(ang)
                vy = cy + R * np.sin(ang)
                return list(zip(vx, vy))

            up = verts([90, 210, 330])
            dn = verts([270, 30, 150])

            segs = [
                (up[0], up[1]), (up[1], up[2]), (up[2], up[0]),
                (dn[0], dn[1]), (dn[1], dn[2]), (dn[2], dn[0]),
            ]
            return segs


        def _fractal_centers(cx, cy, R, depth, scale=1 / 3, ring_factor=2 / 3):
            """
            Make a list of (center_x, center_y, radius) stars:
            - Start with one big star at center.
            - Each star spawns 6 children arranged on a hex ring (the "spaces") around it.
            - Child radius = parent_R * scale
            - Child ring distance = parent_R * ring_factor
            """
            stars = [(cx, cy, R)]
            if depth <= 0:
                return stars

            # recursive expansion (iterative stack)
            stack = [(cx, cy, R, 0)]
            while stack:
                x0, y0, r0, d = stack.pop()
                if d >= depth:
                    continue

                child_r = r0 * scale
                ring = r0 * ring_factor  # where the "spaces" live

                # 6 directions around the center (flat-top hex)
                angles = np.deg2rad([0, 60, 120, 180, 240, 300])
                for a in angles:
                    x1 = x0 + ring * np.cos(a)
                    y1 = y0 + ring * np.sin(a)
                    stars.append((x1, y1, child_r))
                    stack.append((x1, y1, child_r, d + 1))

            return stars


        def flow_fractal_star_50_50(
                h=500, l=500,
                depth=2,
                base_radius_px=210.0,
                thickness_px=1,
                scale=1 / 3,
                ring_factor=2 / 3,
        ):
            """
            Returns a (h,l) uint8 flow where:
            - background is 0 (black)
            - fractal star linework is 1 (white)
            - EXACTLY half the pixels are white (50/50), since h*l is even for 500x500.
            """
            total = h * l
            if total % 2 != 0:
                raise ValueError("Need even number of cells for exact 50/50.")

            # coordinate grids
            yy, xx = np.ogrid[:h, :l]
            X = xx.astype(np.float32)
            Y = yy.astype(np.float32)

            # center
            cx = (l - 1) / 2.0
            cy = (h - 1) / 2.0

            # build star list (fractal)
            stars = _fractal_centers(cx, cy, base_radius_px, depth, scale=scale, ring_factor=ring_factor)

            # distance field: for each pixel, how close to ANY line segment in the whole fractal?
            best = None
            for (sx, sy, sr) in stars:
                for (a, b) in _hexagram_segments(sx, sy, sr):
                    ax, ay = a
                    bx, by = b
                    nd = _segment_norm_dist(X, Y, ax, ay, bx, by, thickness_px)
                    best = nd if best is None else np.minimum(best, nd)

            # enforce EXACT 50/50: choose the closest half of pixels to the fractal lines as white
            N = total // 2
            flat = best.ravel()
            kth = np.partition(flat, N - 1)[N - 1]

            mask = best <= kth
            count = int(mask.sum())

            if count > N:
                # trim ties deterministically
                eq = (best == kth).ravel()
                eq_idx = np.flatnonzero(eq)
                extra = count - N
                mask_flat = mask.ravel()
                mask_flat[eq_idx[:extra]] = False
                mask = mask_flat.reshape(h, l)

            flow = np.zeros((h, l), dtype=np.uint8)
            flow[mask] = 1  # 0 background, 1 linework-ish pixels (closest half)
            return flow

        flow = flow_fractal_star_50_50(500, 500, depth=2, base_radius_px=210, thickness_px=1.2)
        flow_base = flow.copy()

    elif flow_state == 7:


        def _segment_norm_dist(X, Y, ax, ay, bx, by, thickness_px):
            """Normalized distance to segment A->B: dist/thickness."""
            abx = bx - ax
            aby = by - ay
            ab2 = abx * abx + aby * aby + 1e-12

            apx = X - ax
            apy = Y - ay

            t = (apx * abx + apy * aby) / ab2
            t = np.clip(t, 0.0, 1.0)

            cx = ax + t * abx
            cy = ay + t * aby

            dx = X - cx
            dy = Y - cy
            dist = np.sqrt(dx * dx + dy * dy)
            return dist / (thickness_px + 1e-9)


        def _hexagram_segments(cx, cy, R):
            """
            Return 6 segments (two equilateral triangles) for a Star of David centered at (cx,cy)
            with circumradius R (pixel units).
            """

            def verts(deg_list):
                ang = np.deg2rad(deg_list)
                vx = cx + R * np.cos(ang)
                vy = cy + R * np.sin(ang)
                return list(zip(vx, vy))

            up = verts([90, 210, 330])
            dn = verts([270, 30, 150])

            segs = [
                (up[0], up[1]), (up[1], up[2]), (up[2], up[0]),
                (dn[0], dn[1]), (dn[1], dn[2]), (dn[2], dn[0]),
            ]
            return segs


        def _nested_centers(cx, cy, R, depth,
                            inner_scale=0.50,
                            outer_scale=0.28,
                            outer_ring=0.50,
                            include_outer=True,
                            min_radius=6.0):
            """
            Nested star system:
              - each star spawns ONE inner star at same center (radius *= inner_scale)
              - optionally spawns SIX outer stars in the spaces (radius *= outer_scale)
                placed at distance R*outer_ring
            """
            stars = []
            stack = [(cx, cy, R, 0)]

            # angles for "spaces" between arms
            angles = np.deg2rad([0, 60, 120, 180, 240, 300])

            while stack:
                x0, y0, r0, d = stack.pop()
                if r0 < min_radius:
                    continue

                stars.append((x0, y0, r0))
                if d >= depth:
                    continue

                # inner child
                r_in = r0 * inner_scale
                stack.append((x0, y0, r_in, d + 1))

                # outer children (optional)
                if include_outer:
                    r_out = r0 * outer_scale
                    ring = r0 * outer_ring
                    for a in angles:
                        x1 = x0 + ring * np.cos(a)
                        y1 = y0 + ring * np.sin(a)
                        stack.append((x1, y1, r_out, d + 1))

            return stars

        def flow_nested_star_50_50(
                h=500, l=500,
                depth=2,
                base_radius_px=210.0,
                thickness_px=1,
                scale=1 / 3,
                ring_factor=2 / 3,
        ):
            """
            Returns a (h,l) uint8 flow where:
            - background is 0 (black)
            - fractal star linework is 1 (white)
            - EXACTLY half the pixels are white (50/50), since h*l is even for 500x500.
            """
            total = h * l
            if total % 2 != 0:
                raise ValueError("Need even number of cells for exact 50/50.")

            # coordinate grids
            yy, xx = np.ogrid[:h, :l]
            X = xx.astype(np.float32)
            Y = yy.astype(np.float32)

            # center
            cx = (l - 1) / 2.0
            cy = (h - 1) / 2.0

            # build star list (fractal)
            stars = _nested_centers(
                cx, cy, base_radius_px, depth,
                inner_scale=0.52,
                outer_scale=0.26,
                outer_ring=0.50,
                include_outer=True,  # set False for pure nested-in-center only
                min_radius=8.0
            )

            # distance field: for each pixel, how close to ANY line segment in the whole fractal?
            best = None
            for (sx, sy, sr) in stars:
                for (a, b) in _hexagram_segments(sx, sy, sr):
                    ax, ay = a
                    bx, by = b
                    nd = _segment_norm_dist(X, Y, ax, ay, bx, by, thickness_px)
                    best = nd if best is None else np.minimum(best, nd)

            # enforce EXACT 50/50: choose the closest half of pixels to the fractal lines as white
            N = total // 2
            flat = best.ravel()
            kth = np.partition(flat, N - 1)[N - 1]

            mask = best <= kth
            count = int(mask.sum())

            if count > N:
                # trim ties deterministically
                eq = (best == kth).ravel()
                eq_idx = np.flatnonzero(eq)
                extra = count - N
                mask_flat = mask.ravel()
                mask_flat[eq_idx[:extra]] = False
                mask = mask_flat.reshape(h, l)

            flow = np.zeros((h, l), dtype=np.uint8)
            flow[mask] = 1  # 0 background, 1 linework-ish pixels (closest half)
            return flow




        flow = flow_nested_star_50_50(500, 500, depth=2, base_radius_px=210, thickness_px=1.2)
        flow_base = flow.copy()

    elif flow_state == 8:
        def bezier_arc_points(A, B, bulge, n_samples=120):
            """
            A, B are (x,y) floats.
            bulge is in pixels: how far the arc bows outward at midpoint.
            Returns arrays px, py of sampled points along the arc.
            """
            ax, ay = A
            bx, by = B

            mx, my = (ax + bx) / 2.0, (ay + by) / 2.0
            vx, vy = (bx - ax), (by - ay)

            # perpendicular normal
            L = (vx * vx + vy * vy) ** 0.5 + 1e-9
            nx, ny = (-vy / L, vx / L)

            # control point
            cx, cy = (mx + bulge * nx, my + bulge * ny)

            t = np.linspace(0.0, 1.0, n_samples, dtype=np.float32)
            omt = 1.0 - t

            px = omt * omt * ax + 2 * omt * t * cx + t * t * bx
            py = omt * omt * ay + 2 * omt * t * cy + t * t * by
            return px, py


        def flow_star_radiating_arcs(
                h=500, l=500,
                base_radius_px=210.0,
                thickness_px=1.0,
                rainbow_speed=0,
                arcs_per_edge_base=2,  # minimum arcs per edge
                arc_step_px=10.0,  # spacing between arcs
                arc_phase_px=0.0,  # animate bulge phase if desired
                n_samples=110,
                keep_outside_black=True,
        ):
            """
            Makes a flow field where the prime Star-of-David edges radiate outward with curved arcs.
            Background = 0, arcs/lines = 1.

            - rainbow_speed controls how many arcs you get.
            - each edge gets multiple arcs with increasing bulge.
            """
            # grid
            yy, xx = np.ogrid[:h, :l]
            X = xx.astype(np.float32)
            Y = yy.astype(np.float32)

            cx = (l - 1) / 2.0
            cy = (h - 1) / 2.0
            R = float(base_radius_px)

            # Build prime star vertices (same as your _hexagram_segments)
            def verts(deg_list):
                ang = np.deg2rad(deg_list)
                vx = cx + R * np.cos(ang)
                vy = cy + R * np.sin(ang)
                return list(zip(vx, vy))

            up = verts([90, 210, 330])
            dn = verts([270, 30, 150])

            segs = [
                (up[0], up[1]), (up[1], up[2]), (up[2], up[0]),
                (dn[0], dn[1]), (dn[1], dn[2]), (dn[2], dn[0]),
            ]

            # How many arcs per edge this frame?
            # Example: ramps up with rainbow_speed, but caps to keep it fast.
            arcs_per_edge = arcs_per_edge_base + (rainbow_speed % 6)  # 2..7
            arcs_per_edge = int(np.clip(arcs_per_edge, 1, 10))

            # Distance field to arc points (we’ll take min)
            best = np.full((h, l), np.inf, dtype=np.float32)

            # bulge values: outward “ripples”
            # arc_phase_px can be tied to rainbow_speed if you want animation
            phase = float(arc_phase_px)

            for (A, B) in segs:
                # generate multiple arcs for this edge
                for k in range(1, arcs_per_edge + 1):
                    bulge = (k * arc_step_px) + phase

                    px, py = bezier_arc_points(A, B, bulge, n_samples=n_samples)

                    # Update distance field using sampled points
                    # Compute min over samples: min_s sqrt((X-px[s])^2 + (Y-py[s])^2)
                    # Do it incrementally to keep memory lower:
                    for s in range(len(px)):
                        dx = X - px[s]
                        dy = Y - py[s]
                        d = np.sqrt(dx * dx + dy * dy)
                        best = np.minimum(best, d)

            # Optional: keep everything outside the prime star’s outer circle black
            if keep_outside_black:
                inside = (X - cx) ** 2 + (Y - cy) ** 2 <= (R + 2) ** 2
            else:
                inside = np.ones((h, l), dtype=bool)

            # Thin line mask
            mask = (best <= float(thickness_px)) & inside

            flow = np.zeros((h, l), dtype=np.uint8)
            flow[mask] = 1
            return flow


        flow = flow_star_radiating_arcs(
            500, 500,
            base_radius_px=210,
            thickness_px=1.0,
            rainbow_speed=rainbow_speed,
            arcs_per_edge_base=2,
            arc_step_px=10.0,
            arc_phase_px=(rainbow_speed % 20) * 0.7,  # optional animation
            n_samples=90,
            keep_outside_black=True
        )
        flow_base = flow.copy()

    elif flow_state == 9:  # Star of Bethlehem — radiant guiding star
        def flow_star_of_bethlehem(h, l, base=2):
            flow = np.zeros((h, l), dtype=np.uint8)
            cx = l // 2
            cy = h // 2

            # Central bright star — small cross with halo
            star_r = int(min(h, l) * 0.06)  # small bright core
            halo_r = int(min(h, l) * 0.18)  # soft glow around it

            Y, X = np.ogrid[:h, :l]
            dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)

            # Core star (bright center)
            core = dist <= star_r
            flow[core] = 1

            # Halo (soft glow)
            halo = (dist > star_r) & (dist <= halo_r)
            flow[halo] = 1

            # 8 radiating beams — like the classic Christmas star
            angles = np.linspace(0, 360, 16, endpoint=False)  # 8 main beams
            beam_width = 8  # thickness in pixels
            beam_length = int(min(h, l) * 0.45)

            for angle in angles:
                rad = np.deg2rad(angle)
                dx = np.cos(rad)
                dy = np.sin(rad)

                # Parametric line from center
                t = np.linspace(0, beam_length, beam_length)
                bx = cx + t * dx
                by = cy + t * dy

                bx = bx.astype(int)
                by = by.astype(int)

                # Thicken the beam
                for offset in range(-beam_width // 2, beam_width // 2 + 1):
                    perp_dx = -dy * offset
                    perp_dy = dx * offset
                    px = np.clip(bx + perp_dx, 0, l - 1).astype(int)
                    py = np.clip(by + perp_dy, 0, h - 1).astype(int)
                    flow[py, px] = 1

            # Optional: subtle twinkle in the core
            # flow[core] = (flow[core] + 1) % base  # if you want pulsing values

            return flow % base


        flow = flow_star_of_bethlehem(h, l)
        flow_base = flow.copy()

    elif flow_state == 10:  # Star of Bethlehem - classic 8-point with long cardinal, short diagonal, radiating beams

        def flow_bethlehem_star(h, l):

            flow = np.zeros((h, l), dtype=np.uint8)

            cx = l // 2

            cy = h // 2

            Y, X = np.ogrid[:h, :l]

            # Long cardinal arms (N/S/E/W) - diamond shape

            long_len = int(min(h, l) * 0.48)

            long_w = int(min(h, l) * 0.12)

            flow[cy - long_len:cy + long_len, cx - long_w // 2:cx + long_w // 2] = 1  # vertical

            flow[cy - long_w // 2:cy + long_w // 2, cx - long_len:cx + long_len] = 1  # horizontal

            # Short diagonal arms

            short_len = int(min(h, l) * 0.28)

            short_w = int(min(h, l) * 0.08)

            diag_angles = [45, 135, 225, 315]

            for ang in diag_angles:

                rad = np.deg2rad(ang)

                dx = np.cos(rad)

                dy = np.sin(rad)

                for t in range(-short_len, short_len + 1):

                    px = int(cx + t * dx)

                    py = int(cy + t * dy)

                    if 0 <= px < l and 0 <= py < h:

                        for off in range(-short_w // 2, short_w // 2 + 1):

                            ppx = int(px - dy * off)

                            ppy = int(py + dx * off)

                            if 0 <= ppx < l and 0 <= ppy < h:
                                flow[ppy, ppx] = 1

            # Radiating lines from all 8 tips to center

            tips = [

                (cx, cy - long_len), (cx, cy + long_len),

                (cx - long_len, cy), (cx + long_len, cy)

            ]

            for a in diag_angles:
                rad = np.deg2rad(a)

                tips.append((int(cx + short_len * np.cos(rad)), int(cy + short_len * np.sin(rad))))

            for tx, ty in tips:

                steps = max(abs(tx - cx), abs(ty - cy)) or 1

                for i in range(steps + 1):

                    px = cx + int(i * (tx - cx) / steps)

                    py = cy + int(i * (ty - cy) / steps)

                    # Thick beams for visibility

                    for ox in range(-5, 6):

                        for oy in range(-5, 6):

                            if ox ** 2 + oy ** 2 <= 25:

                                ppx = px + ox

                                ppy = py + oy

                                if 0 <= ppx < l and 0 <= ppy < h:
                                    flow[ppy, ppx] = 1

            # Bright center with halo

            center_r = int(min(h, l) * 0.08)

            halo_r = int(min(h, l) * 0.15)

            dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)

            flow[dist <= center_r] = 1

            flow[(dist > center_r) & (dist <= halo_r)] = 1

            return flow


        flow = flow_bethlehem_star(h, l)

        flow_base = flow.copy()


    elif flow_state == 11:  # Rhombus - obtuse left/right, acute top/bottom
        def flow_rhombus_obtuse_lr_acute_tb(h, l):
            flow = np.zeros((h, l), dtype=np.uint8)
            cx = l // 2
            cy = h // 2

            # Wide horizontally (obtuse left/right), narrow vertically (acute top/bottom)
            horiz_half = int(l * 0.45)  # wide for obtuse sides
            vert_half = int(h * 0.25)  # narrow for acute top/bottom

            Y, X = np.ogrid[:h, :l]

            # Manhattan distance scaled — creates perfect rhombus
            mask = (np.abs(X - cx) / horiz_half) + (np.abs(Y - cy) / vert_half) <= 1

            flow[mask] = 1

            # Optional: bright center for glow
            center_r = int(min(h, l) * 0.05)
            dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
            flow[dist <= center_r] = 1

            return flow


        flow = flow_rhombus_obtuse_lr_acute_tb(h, l)
        flow_base = flow.copy()


    elif flow_state == 12:  # Bethlehem star — OUTLINE ONLY (no fill)
        def flow_bethlehem_outline(h, l, base=2):
            flow = np.zeros((h, l), dtype=np.uint8)

            cy = (h - 1) / 2.0
            cx = (l - 1) / 2.0

            Y, X = np.ogrid[:h, :l]
            Xf = X.astype(np.float32) - cx
            Yf = Y.astype(np.float32) - cy

            angles = np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315])

            Rmax = min(h, l) * 0.48
            long_len = Rmax * 1.00
            short_len = Rmax * 0.62

            # Sharp half-angles (+50% width already)
            half_angle_long = 0.39
            half_angle_short = 0.33

            edge_thickness = max(1.5, min(h, l) * 0.004)
            ray_thickness = max(2.0, min(h, l) * 0.006)

            mask = np.zeros((h, l), dtype=bool)

            for i, a in enumerate(angles):
                ca = np.cos(a)
                sa = np.sin(a)

                forward = ca * Xf + sa * Yf
                perp = -sa * Xf + ca * Yf

                if i % 2 == 0:
                    L = long_len
                    ha = half_angle_long
                else:
                    L = short_len
                    ha = half_angle_short

                slope = np.tan(ha)

                # -----------------------------
                # OUTWARD TRIANGLE (edges only)
                # |perp| = slope * (L - forward)
                # -----------------------------
                outer_edge = (
                        (forward >= 0) & (forward <= L) &
                        (np.abs(np.abs(perp) - slope * (L - forward)) <= edge_thickness)
                )
                mask |= outer_edge

                # -----------------------------
                # INVERTED TRIANGLE (edges only)
                # |perp| = slope * forward
                # -----------------------------
                inner_edge = (
                        (forward >= 0) & (forward <= L) &
                        (np.abs(np.abs(perp) - slope * forward) <= edge_thickness)
                )
                mask |= inner_edge

                # -----------------------------
                # TIP → CENTER RAY (diamond)
                # -----------------------------
                tx = L * ca
                ty = L * sa

                t = (Xf * tx + Yf * ty) / (tx * tx + ty * ty + 1e-9)
                t = np.clip(t, 0.0, 1.0)

                px = t * tx
                py = t * ty

                dx = Xf - px
                dy = Yf - py
                mask |= (np.abs(dx) + np.abs(dy)) <= ray_thickness

            # -----------------------------
            # CENTER DIAMOND (outline only)
            # -----------------------------
            center_r = min(h, l) * 0.05
            center_outline = np.abs((np.abs(Xf) + np.abs(Yf)) - center_r) <= edge_thickness
            mask |= center_outline

            flow[mask] = 1
            return flow % base


        flow = flow_bethlehem_outline(h, l, base=base)
        flow_base = flow.copy()









flow_0 = flow.copy()


rainbow_array = np.zeros((h, l), dtype=int)
rainbow_memory = np.zeros((h, l), dtype=int)
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
last_l = ''
last_r = ''
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


def water_update():
    global view, lookup, flow

    if view == 5:

        up = np.vstack((flow[1:, :], flow[0:1, :]))
        down = np.vstack((flow[-1:, :], flow[:-1, :]))
        left = np.hstack((flow[:, 1:], flow[:, 0:1]))
        right = np.hstack((flow[:, -1:], flow[:, :-1]))

        index = (
                flow +  # center
                left * base +
                right * base2 +
                up * base3 +
                down * base4
        ).astype(np.int32)



        water = lookup[index].astype(int)




        return water

    elif view == 9:
        flow32 = flow.astype(np.int32)

        L = np.roll(flow32, -1)
        R = np.roll(flow32, 1)
        U = np.roll(flow32, -l)
        D = np.roll(flow32, l)

        UL = np.roll(flow32, -l - 1)
        UR = np.roll(flow32, -l + 1)
        DL = np.roll(flow32, l - 1)
        DR = np.roll(flow32, l + 1)

        current = (
                UL * base ** 0 +
                U * base ** 1 +
                UR * base ** 2 +
                L * base ** 3 +
                flow32 * base ** 4 +
                R * base ** 5 +
                DL * base ** 6 +
                D * base ** 7 +
                DR * base ** 8
        )

        water = rule[-current]

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
    global stamp_x, stamp_y, code, rv, shift, rule, tts_1, shifts, hands_x, rule_base, lookup, flow_0


    if hand[0] == hand[1]:

        if hand[0] != code_0:

            letter = hand[0]
            code_0 = hand[0]
            code += hand[0]

            code_bin = base_x(digibet[code_0], 2)
            code_bin = fill_bin(code_bin)
            # print(goal_bin)

            stamp = 1

            if stamp == 1:
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


            #ruler
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

                rv = score
                rv = rv%bbv

                # rv = rv_base


                rules, rule_base = rule_gen(rv, base)
                rule_base = np.array(rule_base)
                rule = rule_base.copy()


                shift = digibet[code_0]
                shift = shift % len(rule)
                rule[shift] = str((int(rule[shift]) + 1) % base)
                shift_base = base_x(shift, base)
                shift_base = fill_bin(shift_base)
                shift_flip = shift_base[::-1]


                shifts[0] = [c for c in shift_flip]
                inv_base = shift_base.translate(str.maketrans('01', '10'))
                inv_flip = inv_base[::-1]

                shifts[1] = [c for c in inv_flip]
                inv_digits = [int(c) for c in inv_base]
                inv_index = digits_to_index(inv_digits, base)

                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)
                shifts[2] = shifts[0][::]
                shifts[3] = shifts[1][::]

                center = 0
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



            elif ruler == 7:

                rv = score
                rv = rv%bbv

                # rv = rv_base


                rules, rule_base = rule_gen(rv, base)
                rule_base = np.array(rule_base)
                rule = rule_base.copy()


                shift = digibet[code_0]
                shift = shift % len(rule)
                rule[shift] = str((int(rule[shift]) + 1) % base)
                shift_base = base_x(shift, base)
                shift_base = fill_bin(shift_base)
                shift_flip = shift_base[::-1]


                shifts[0] = [c for c in shift_flip]
                inv_base = shift_base.translate(str.maketrans('01', '10'))
                inv_flip = inv_base[::-1]

                shifts[1] = [c for c in inv_flip]
                inv_digits = [int(c) for c in inv_base]
                inv_index = digits_to_index(inv_digits, base)

                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)
                shifts[2] = shifts[0][::]
                shifts[3] = shifts[1][::]

                center = 0
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

                flip = shifts[2][::-1]
                inv_index = digits_to_index([int(c) for c in flip], base)
                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)


                flip = shifts[3][::-1]
                inv_index = digits_to_index([int(c) for c in flip], base)
                rule[inv_index] = str((int(rule[inv_index]) + 1) % base)


            lookup = np.array(rule, dtype=np.uint8)





        else:
            letter = code_0

    else:
        letter = code_0


    # print(letter)

    return letter, code_0


typed_total = 0
last_typed_total = 0
n_slots = 0
score_0 = 0




def submit(letter):

    # print(letter)

    global phrase, phrase_pos, message, tts, score, times, code, rv, code_0, last_typed, se, tts_0, flow, water, current_rung, typed_total, n_slots, score_0

    if letter == last_typed:
        letter = code_0
    elif letter == phrase[phrase_pos] or letter == phrase[phrase_pos:phrase_pos + 2]:

        typed_total += 1

        print("")
        print(typed_total)
        print(n_slots)

        message += phrase[phrase_pos]
        phrase_pos += 1

        if base == 2:
            flow = flow_base.copy()
            water = flow.copy()


        if len(letter) == 2:
            message += phrase[(phrase_pos + 1)%len(phrase)]
            phrase_pos += 1
            typed_total += 1

        if phrase_pos == 1:
            tts[0] = time.time()

        if phrase_pos == len(phrase):

            history.insert(0, (tts_0, current_rung))
            message += ' '

            score += 1
            score_0 = 1
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
                se += 1

            else:
                se = int(se / 2)

            code = ''

            sign_bank[phrase] = (score, rv, times)

            filename = os.path.join(SCRIPT_DIR, 'sign_bank', signame)
            outfile = open(filename, 'wb')
            pickle.dump(sign_bank, outfile)
            outfile.close()

            if ruler == 0:
                set_scale = 1
                for x in range(len(phrase)):
                    rv += digibet[phrase[x]] * int(se / set_scale)
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
                    flow = flow_base.copy()
                    water = flow.copy()


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





####hands####
hand_x = []
hands_1 = [0, 0]
hands_0 = [0, 0]
hands = [0, 0]
hand_x = [hands, hands_0, hands_1]

cell_map = [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1)]

rule_base = rule.copy()


###hand variables###
x_s = 36
y_s = 36
x_g = 28
y_g = 0
flex_c = 16
flex_m = 64
flex_p = 42

HAND_SIZE_SCALE = 1.0
HAND_SIZE_MIN = 0.55
HAND_SIZE_MAX = 1.00
HAND_SIZE_STEP = 0.05

BASE_X_S = 36
BASE_Y_S = 36
BASE_X_G = 28
BASE_Y_G = 0

def apply_hand_size_scale():
    global x_s, y_s, x_g, y_g

    s = float(np.clip(HAND_SIZE_SCALE, HAND_SIZE_MIN, HAND_SIZE_MAX))

    x_s = max(4, int(round(BASE_X_S * s)))
    y_s = max(4, int(round(BASE_Y_S * s)))
    x_g = max(0, int(round(BASE_X_G * s)))
    y_g = max(0, int(round(BASE_Y_G * s)))

apply_hand_size_scale()

flex_c = 16
flex_m = 64
flex_p = 42


ambient = 1
ambient_rgb_ref = None
ambient_delta = 0.0
# 0.0 = no correction, 1.0 = full correction.
# Start gentle.
AMBIENT_CORRECT_STRENGTH = 0.75



if ambient == 1:
    # -----------------------------
    # AMBIENT LIGHT COMPENSATION
    # -----------------------------

    # Pick empty background zones, away from your hand boxes.
    # array3d uses [x, y], so these are x1, y1, x2, y2.
    AMBIENT_SAMPLE_BOXES = [
        (20, 20, 180, 180),  # upper left background
        (screen_width - 180, 20, screen_width - 20, 180),  # upper right background
    ]


    def sample_ambient_rgb(frame):
        samples = []

        for x1, y1, x2, y2 in AMBIENT_SAMPLE_BOXES:
            crop = frame[x1:x2, y1:y2]

            if crop.size > 0:
                samples.append(crop.reshape(-1, 3).mean(axis=0))

        if len(samples) == 0:
            return frame.reshape(-1, 3).mean(axis=0)

        return np.mean(samples, axis=0)


    def calibrate_ambient(frame):
        global ambient_rgb_ref

        ambient_rgb_ref = sample_ambient_rgb(frame).astype(np.float32)
        print("AMBIENT CALIBRATED:", ambient_rgb_ref)


    def correct_ambient_light(frame):
        global ambient_rgb_ref, ambient_delta

        if ambient_rgb_ref is None:
            calibrate_ambient(frame)
            return frame

        now_rgb = sample_ambient_rgb(frame).astype(np.float32)

        # How much the room lighting changed from calibration.
        ambient_delta = float(np.mean(np.abs(now_rgb - ambient_rgb_ref)))

        # Per-channel gain correction.
        gain = ambient_rgb_ref / np.maximum(now_rgb, 1.0)

        # Prevent wild correction if a hand/object covers the sample box.
        gain = np.clip(gain, 0.65, 1.55)

        # Blend correction strength.
        blended_gain = 1.0 + AMBIENT_CORRECT_STRENGTH * (gain - 1.0)

        corrected = frame.astype(np.float32) * blended_gain
        corrected = np.clip(corrected, 0, 255).astype(np.uint8)

        return corrected


####right hand####
xr_pos = (x_s + x_g) * 3
yr_pos = 500
palm_xr = xr_pos + x_s * 6
palm_yr = yr_pos + y_s * 9


hand_r = [0, 0, 0, 0, 0, 0]
hand_r0 = [0, 0, 0, 0, 0, 0]
hand_r1 = [0, 0, 0, 0, 0, 0]


palm_r = [0, 0, 0, 0, 0, 0]

tips_r = [64, 16, 0, 24, 0]



#fingers x
right_x = {
    "size": x_s,
    "gap": x_g,
    "start": xr_pos,
    "palm": palm_xr,
    "step": x_s + x_g
}

#fingers y
right_y = {
    "size": y_s,
    "gap": y_g,
    "start": yr_pos,
    "palm": palm_yr,
    "step": y_s + y_g
}

#fingers
right_roi = [
    (
        right_x["start"] + right_x["step"] * (n + 1),
        right_y["start"] + tips_r[n],
        right_x["start"] + right_x["step"] * (n + 1) + right_x["size"],
        right_y["start"] + tips_r[n] + right_y["size"]
    )
    for n in range(5)
]

#thumb
right_roi[4] = (
    right_x["start"] + right_x["step"] * 5 + right_x["size"],
    right_y["start"] + tips_r[4] + right_y["size"] * 5,
    right_x["start"] + right_x["step"] * 5 + right_x["size"] * 2,
    right_y["start"] + tips_r[4] + right_y["size"] * 6
)

xr_pos = palm_xr - x_s * 1
yr_pos = palm_yr - x_s * 2

#palm
right_roi.append((xr_pos, yr_pos, xr_pos + x_s, yr_pos + y_s))


right_hand = [0, 0, 0]

roir_map = []
distr_map = []

hands_r = [hand_r, hand_r0, hand_r1, palm_r, tips_r, right_hand, roir_map, distr_map]

right_hands = []



###left hand###
xl_pos = screen_width - (x_s + x_g) * 10
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

left_hand = [0, 0, 0]


roil_map = []
distl_map = []

hands_l = [hand_l, hand_l0, hand_l1, palm_l, tips_l, left_hand, roil_map, distl_map]

left_hands = []

hand_numb = 1

if hand_numb > 1:

    for x in range(hand_numb):
        xr_pos = (x_s + x_g) * 3
        yr_pos = 500 - (y_s + y_g) * 10 * x
        palm_xr = xr_pos + x_s * 6
        palm_yr = yr_pos + y_s * 9

        hand_r = [0, 0, 0, 0, 0, 0]
        hand_r0 = [0, 0, 0, 0, 0, 0]
        hand_r1 = [0, 0, 0, 0, 0, 0]

        palm_r = [0, 0, 0, 0, 0, 0]

        tips_r = [64, 16, 0, 24, 0]

        # fingers x
        right_x = {
            "size": x_s,
            "gap": x_g,
            "start": xr_pos,
            "palm": palm_xr,
            "step": x_s + x_g
        }

        # fingers y
        right_y = {
            "size": y_s,
            "gap": y_g,
            "start": yr_pos,
            "palm": palm_yr,
            "step": y_s + y_g
        }

        # fingers
        right_roi = [
            (
                right_x["start"] + right_x["step"] * (n + 1),
                right_y["start"] + tips_r[n],
                right_x["start"] + right_x["step"] * (n + 1) + right_x["size"],
                right_y["start"] + tips_r[n] + right_y["size"]
            )
            for n in range(5)
        ]

        # thumb
        right_roi[4] = (
            right_x["start"] + right_x["step"] * 5 + right_x["size"],
            right_y["start"] + tips_r[4] + right_y["size"] * 5,
            right_x["start"] + right_x["step"] * 5 + right_x["size"] * 2,
            right_y["start"] + tips_r[4] + right_y["size"] * 6
        )

        xr_pos = palm_xr - x_s * 1
        yr_pos = palm_yr - x_s * 2

        # palm
        right_roi.append((xr_pos, yr_pos, xr_pos + x_s, yr_pos + y_s))

        right_hand = [0, 0, 0]

        roir_map = []
        distr_map = []
        palm_xy = (palm_xr, palm_yr)

        hands_r = [hand_r, hand_r0, hand_r1, palm_r, tips_r, right_hand, roir_map, distr_map, None, palm_xy]

        right_hand_x = [right_roi, hands_r]
        right_hands.append(right_hand_x)
        print("")
        print('right_hand_x')
        print(x)
        print(right_hand_x)

    for x in range(hand_numb):

        xl_pos = screen_width - (x_s + x_g) * 10
        yl_pos = 500 + (y_s + y_g) * 3 * x
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

        roil_map = []
        distl_map = []

        left_hand = [0, 0, 0]

        hands_l = [hand_l, hand_l0, hand_l1, palm_l, tips_l, left_hand, roil_map, distl_map]

        left_hand_x = [left_roi, hands_l]
        left_hands.append(left_hand_x)
        print("")
        print('left_hand_x')
        print(x)
        print(left_hand_x)


def right_hand_detect():
    global hand_r, hand_r0, hand_r1, right_hand, right_roi, hand_x, hands, hands_0, hands_1, roir_map, distr_map


    place = 0

    flex_c_live = flex_c + ambient_delta * 0.35
    flex_m_live = flex_m + (ambient_delta ** 2) * 0.05
    flex_p_live = flex_p + ambient_delta * 0.35




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

        distr_map.append(roi_dist)

        if ambient == 0:
            if roi_dist > flex_c:
                hand_r[place - 1] = 1
            else:
                hand_r[place - 1] = 0

            if roi_mean > flex_m:
                hand_r0[place - 1] = 1
            else:
                hand_r0[place - 1] = 0

            if roi_palm > flex_p:
                hand_r1[place - 1] = 1
            else:
                hand_r1[place - 1] = 0
        else:
            if roi_dist > flex_c_live:
                hand_r[place - 1] = 1
            else:
                hand_r[place - 1] = 0

            if roi_mean > flex_m_live:
                hand_r0[place - 1] = 1
            else:
                hand_r0[place - 1] = 0

            if roi_palm > flex_p_live:
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

    roir_map.clear()
    distr_map.clear()




def left_hand_detect():
    global hand_l, hand_l0, hand_l1, left_hand, left_roi, roil_map, distl_map, hands, hands_0, hands_1, hand_x, roil_map, distl_map

    place = 0

    flex_c_live = flex_c + ambient_delta * 0.35
    flex_m_live = flex_m + (ambient_delta ** 2) * 0.05
    flex_p_live = flex_p + ambient_delta * 0.35





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

        distl_map.append(roi_dist)


        if ambient == 0:
            if roi_dist > flex_c:
                hand_l[place - 1] = 1
            else:
                hand_l[place - 1] = 0

            if roi_mean > flex_m:
                hand_l0[place - 1] = 1
            else:
                hand_l0[place - 1] = 0

            if roi_palm > flex_p:
                hand_l1[place - 1] = 1
            else:
                hand_l1[place - 1] = 0
        else:
            if roi_dist > flex_c_live:
                hand_l[place - 1] = 1
            else:
                hand_l[place - 1] = 0

            if roi_mean > flex_m_live:
                hand_l0[place - 1] = 1
            else:
                hand_l0[place - 1] = 0

            if roi_palm > flex_p_live:
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



    left_hand[0] = hand_l[0] * 1 + hand_l[1] * 2 + hand_l[2] * 4 + hand_l[3] * 8 + hand_l[4] * 16
    left_hand[1] = hand_l0[0] * 1 + hand_l0[1] * 2 + hand_l0[2] * 4 + hand_l0[3] * 8 + hand_l0[4] * 16
    left_hand[2] = hand_l1[0] * 1 + hand_l1[1] * 2 + hand_l1[2] * 4 + hand_l1[3] * 8 + hand_l1[4] * 16

    hands[1] = digibetu[left_hand[0]]
    hands_0[1] = digibetu[left_hand[1]]
    hands_1[1] = digibetu[left_hand[2]]

    hand_x = [hand_l, hand_l0, hand_l1, hands, hands_0, hands_1, left_hand, right_hand]

    roil_map.clear()
    distl_map.clear()





def right_hand_detector():

    global right_hands


    for current_hand in right_hands:

        rois = current_hand[0]
        hands_r = current_hand[1]

        hand_r, hand_r0, hand_r1, palm_r, tips_r, right_hand, roir_map, distr_map, palm_prev, palm_xy = hands_r
        palm_xr, palm_yr = palm_xy

        place = 0
        for roi in rois:
            place += 1
            x1, y1, x2, y2 = roi

            roi_prev = array_past[x1:x2, y1:y2]
            roi_now = hand_array[x1:x2, y1:y2]
            roir_map.append((roi_prev, roi_now))

            if palm_prev is None:
                palm_prev = roi_now.copy()

            roi_dist = color_dist(roi_prev, roi_now)
            roi_mean = np.mean((roi_prev.astype(np.float32) - roi_now.astype(np.float32)) ** 2)
            roi_palm = int(color_dist(roi_now, palm_prev))

            palm_r[place - 1] = roi_palm
            distr_map.append(roi_dist)


            hand_r[place - 1]  = 1 if roi_dist > flex_c else 0
            hand_r0[place - 1] = 1 if roi_mean > flex_m else 0
            hand_r1[place - 1] = 1 if roi_palm > flex_p else 0


            x = place - 1
            value_rect = pygame.Rect(x1, y1, x_s, y_s)
            pygame.draw.rect(screen, value_color[0 + hand_r[x] * 9], value_rect)

            tip_rect = pygame.Rect(x1, y1, x_s / 2, y_s / 2)
            pygame.draw.rect(screen, value_color[0 + hand_r0[x] * 5], tip_rect)

            tip_rect = pygame.Rect(x1, y1, x_s / 3, y_s / 3)
            pygame.draw.rect(screen, value_color[0 + hand_r1[x] * 7], tip_rect)

            pygame.draw.line(screen, value_color[0 + int(goal_bin[x % len(goal_bin)]) * 9], (palm_xr, palm_yr),
                             (roi[0], roi[1]))

        palm_prev = roir_map[-1][1].copy()
        hands_r[8] = palm_prev

        right_hand[0] = hand_r[0] * 16 + hand_r[1] * 8 + hand_r[2] * 4 + hand_r[3] * 2 + hand_r[4] * 1
        right_hand[1] = hand_r0[0] * 16 + hand_r0[1] * 8 + hand_r0[2] * 4 + hand_r0[3] * 2 + hand_r0[4] * 1
        right_hand[2] = hand_r1[0] * 16 + hand_r1[1] * 8 + hand_r1[2] * 4 + hand_r1[3] * 2 + hand_r1[4] * 1

        roir_map.clear()
        distr_map.clear()

        current_hand[1] = [hand_r, hand_r0, hand_r1, palm_r, tips_r, right_hand, roir_map, distr_map, palm_prev, palm_xy]









count_scale = color_max*64
bong = 1

history = []


memory = np.zeros((h, l), dtype=np.float32)
learn_rate = 0.05
decay_rate = 0.98
memory_scale = 8.0


####star write####

GLYPH_MAP = {
    'a': draw_a, 'b': draw_b, 'c': draw_c, 'd': draw_d, 'e': draw_e,
    'f': draw_f, 'g': draw_g, 'h': draw_h, 'i': draw_i, 'j': draw_j,
    'k': draw_k, 'l': draw_l, 'm': draw_m, 'n': draw_n, 'o': draw_o,
    'p': draw_p, 'q': draw_q, 'r': draw_r, 's': draw_s, 't': draw_t,
    'u': draw_u, 'v': draw_v, 'w': draw_w, 'x': draw_x, 'y': draw_y, 'z': draw_z,
}



glyphs = 1
message_len = 150


if glyphs == 1:


    # --- use your existing GLYPH_MAP = {'a': draw_a, ...} ---

    def _poly_signed_area(pts):
        """Signed area (x,y). Negative => clockwise in screen coords (y down) depends on convention."""
        # We'll use standard shoelace; then we can test both and force a direction by checking the loop.
        x = np.array([p[0] for p in pts], dtype=np.float64)
        y = np.array([p[1] for p in pts], dtype=np.float64)
        return 0.5 * np.sum(x[:-1]*y[1:] - x[1:]*y[:-1])

    def star_loop_vertices(cx, cy, R):
        """
        6-vertex star loop (outline) as a closed polyline.
        IMPORTANT: y grows downward, so angle 270 is "up".
        """
        # These angles produce a nice hexagram loop. We'll reorder later anyway.
        ang = np.deg2rad([270, 330, 30, 90, 150, 210])  # starts near "top", goes around
        xs = cx + R * np.cos(ang)
        ys = cy + R * np.sin(ang)  # sin positive = down
        pts = list(zip(xs, ys))
        pts.append(pts[0])
        return pts

    def sample_polyline(points, step):
        out = []
        for i in range(len(points) - 1):
            x0, y0 = points[i]
            x1, y1 = points[i + 1]
            dx = x1 - x0
            dy = y1 - y0
            seg_len = float(np.hypot(dx, dy))
            if seg_len < 1e-9:
                continue
            n = max(1, int(seg_len // step))
            for k in range(n):
                t = (k * step) / seg_len
                out.append((x0 + t * dx, y0 + t * dy))
        return out




    def reorder_start_top_left_clockwise(loop_pts):
        """
        loop_pts: closed polyline [(x,y), ..., (x,y)=first]
        Returns closed polyline starting at the TOP-LEFT point and going clockwise.
        """
        pts = loop_pts[:-1]  # remove closure

        # start = smallest y, then smallest x  (top-left in screen coords)
        start_i = min(range(len(pts)), key=lambda i: (pts[i][1], pts[i][0]))

        pts = pts[start_i:] + pts[:start_i]
        pts_closed = pts + [pts[0]]

        # force clockwise: if area is positive, reverse order (keep same start)
        x = np.array([p[0] for p in pts_closed], dtype=np.float64)
        y = np.array([p[1] for p in pts_closed], dtype=np.float64)
        area = 0.5 * np.sum(x[:-1]*y[1:] - x[1:]*y[:-1])

        if area > 0:
            # reverse while preserving start point pts[0]
            pts_rev = [pts[0]] + list(reversed(pts[1:]))
            pts_closed = pts_rev + [pts_rev[0]]

        return pts_closed



    def canvas_write_star_path_aligned(
        message,
        size, l_size, x_space, y_space,
        offset_size, density,
        x_o, y_o,
        canvas,
        *,
        base_radius_px=210.0,   # MUST match your flow_state star radius
        center_xy=(250.0, 250.0),  # for 500x500
        loop=True,
    ):
        """
        Writes glyphs along the SAME Star of David geometry used in your flow_state.
        Starts at TOP-LEFT of the star path and moves CLOCKWISE.

        Keeps the SAME coordinate transforms as your canvas_write() so glyphs aren't inverted.
        """

        rainbow_reset = 0
        m_list = list(message.lower())

        # --- match your canvas_write() transform ---
        canvas = np.rot90(canvas)
        canvas = np.flipud(canvas)

        h, w = canvas.shape[:2]
        x_shift = 128
        y_shift = 16

        # Align to the flow-state star: same center & radius, but allow an (x_o,y_o) offset
        cx0, cy0 = center_xy
        cx = cx0 + x_o - x_shift
        cy = cy0 + y_o - y_shift
        R = float(base_radius_px)

        # Build loop and force start/top-left + clockwise
        loop_pts = star_loop_vertices(cx, cy, R)
        loop_pts = reorder_start_top_left_clockwise(loop_pts)
        loop_pts = [(y, x) for (x, y) in loop_pts]

        # Sample along the loop
        step = max(1.0, float(l_size + x_space))
        path_pts = sample_polyline(loop_pts, step=step)

        if not path_pts:
            canvas = np.flipud(canvas)
            canvas = np.rot90(canvas, 3)
            return canvas, rainbow_reset

        idx = 0
        for ch in m_list:
            if ch == ' ':
                idx += 1
                continue

            fn = GLYPH_MAP.get(ch)
            if fn is None:
                idx += 1
                continue

            if idx >= len(path_pts):
                if not loop:
                    break
                idx = 0
                rainbow_reset = 1

            px, py = path_pts[idx]
            idx += 1

            # center glyph at path point
            corner = (int(px - l_size / 2), int(py - l_size / 2))

            # stamp with your "density" offsets
            for off in (0, offset_size, density):
                fn(l_size, canvas, (corner[0] + off, corner[1]))
                fn(l_size, canvas, (corner[0] - off, corner[1]))
                fn(l_size, canvas, (corner[0], corner[1] + off))
                fn(l_size, canvas, (corner[0], corner[1] - off))

        # --- undo transform ---
        canvas = np.flipud(canvas)
        canvas = np.rot90(canvas, 3)

        return canvas, rainbow_reset






    def star_loop_vertices(cx, cy, R):
        # closed loop points (x,y); order doesn’t matter because we reorder start later
        ang = np.deg2rad([270, 330, 30, 90, 150, 210])
        xs = cx + R * np.cos(ang)
        ys = cy + R * np.sin(ang)
        pts = list(zip(xs, ys))
        pts.append(pts[0])
        return pts

    def sample_polyline(points, step):
        out = []
        for i in range(len(points) - 1):
            x0, y0 = points[i]
            x1, y1 = points[i + 1]
            dx = x1 - x0
            dy = y1 - y0
            seg_len = float(np.hypot(dx, dy))
            if seg_len < 1e-9:
                continue
            n = max(1, int(seg_len // step))
            for k in range(n):
                t = (k * step) / seg_len
                out.append((x0 + t * dx, y0 + t * dy))
        return out

    def reorder_start_top_left_clockwise(loop_pts):
        pts = loop_pts[:-1]

        # start at top-left (min y, then min x)
        start_i = min(range(len(pts)), key=lambda i: (pts[i][1], pts[i][0]))
        pts = pts[start_i:] + pts[:start_i]
        pts_closed = pts + [pts[0]]

        # force clockwise (area test)
        x = np.array([p[0] for p in pts_closed], dtype=np.float64)
        y = np.array([p[1] for p in pts_closed], dtype=np.float64)
        area = 0.5 * np.sum(x[:-1]*y[1:] - x[1:]*y[:-1])
        if area > 0:
            pts_rev = [pts[0]] + list(reversed(pts[1:]))
            pts_closed = pts_rev + [pts_rev[0]]

        return pts_closed



    def build_star_spiral_points(
        l_size, x_space,
        cx, cy,
        base_radius_px,
        in_step_px,
        min_radius_px,
    ):
        step = max(1.0, float(l_size + x_space))
        pts_all = []

        R = float(base_radius_px)
        while R >= float(min_radius_px):
            loop_pts = star_loop_vertices(cx, cy, R)          # (x,y) original
            loop_pts = [(y, x) for (x, y) in loop_pts]        # to transformed space
            loop_pts = reorder_start_top_left_clockwise(loop_pts)
            ring_pts = sample_polyline(loop_pts, step=step)
            if not ring_pts:
                break
            pts_all.extend(ring_pts)
            R -= float(in_step_px)

        return pts_all


    ###object of power###use with caution###
    def canvas_write_star_spiral_wholy(
        message,
        size, l_size, x_space, y_space,
        offset_size, density,
        x_o, y_o,
        canvas,
        *,
        base_radius_px=210.0,
        center_xy=(250.0, 250.0),
        x_shift=128,
        y_shift=16,
        in_step_px=18.0,
        min_radius_px=60.0,
        wrap_message=True,     # if False, will stop when message ends
    ):
        """
        Pure renderer:
        - builds the entire spiral path (all rings) each call
        - types along the entire spiral each call
        - does NOT assume any saved state in flow
        """
        m = message.lower()
        if len(m) == 0:
            return canvas, 0

        # match your canvas_write() transform
        canvas = np.rot90(canvas)
        canvas = np.flipud(canvas)

        cx0, cy0 = center_xy
        cx = cx0 + x_o - x_shift
        cy = cy0 + y_o - y_shift

        spiral_pts = build_star_spiral_points(
            l_size, x_space,
            cx, cy,
            base_radius_px,
            in_step_px,
            min_radius_px,
        )

        rainbow_reset = 0
        if not spiral_pts:
            canvas = np.flipud(canvas)
            canvas = np.rot90(canvas, 3)
            return canvas, rainbow_reset

        # draw exactly the spiral length (or until message ends if wrap_message=False)
        for i, (px, py) in enumerate(spiral_pts):
            if wrap_message:
                ch = m[i % len(m)]
            else:
                if i >= len(m):
                    break
                ch = m[i]

            if ch == ' ':
                continue

            fn = GLYPH_MAP.get(ch)
            if fn is None:
                continue

            corner = (int(px - l_size / 2), int(py - l_size / 2))

            for off in (0, offset_size, density):
                fn(l_size, canvas, (corner[0] + off, corner[1]))
                fn(l_size, canvas, (corner[0] - off, corner[1]))
                fn(l_size, canvas, (corner[0], corner[1] + off))
                fn(l_size, canvas, (corner[0], corner[1] - off))

        # undo transform
        canvas = np.flipud(canvas)
        canvas = np.rot90(canvas, 3)
        return canvas, rainbow_reset



    def canvas_write_star_spiral(
        message,
        size, l_size, x_space, y_space,
        offset_size, density,
        x_o, y_o,
        canvas=0,
        *,
        base_radius_px=210.0,
        in_step_px=18.0,
        min_radius_px=60.0,
        x_shift=128,     # you said these shifts look best
        y_shift=16,
        wrap_message=False,   # True => repeat message to fill whole spiral
        start_on_sample_top_left=True,  # keeps start stable
    ):
        """
        Like canvas_write(), but lays text along nested Star-of-David loops.
        - Outer loop first, then steps inward after each full loop.
        - Draws onto `canvas` (your flow array) in the same transformed coordinate system
          as canvas_write (rot90 + flipud), then un-transforms at end.
        - Does NOT keep state; it renders from `message` each call.
        """
        rainbow_reset = 0
        m = message.lower()
        if len(m) == 0:
            return canvas, rainbow_reset

        # --- match your canvas_write() coordinate transform ---
        canvas = np.rot90(canvas)
        canvas = np.flipud(canvas)

        h, w = canvas.shape[:2]

        # Your star is aligned relative to the canvas center, then offset by x_o/y_o and your shifts
        cx0 = (w - 1) / 2.0
        cy0 = (h - 1) / 2.0

        cx = cx0 + x_o - x_shift
        cy = cy0 + y_o - y_shift

        step = max(1.0, float(l_size + x_space))

        # --- build all spiral points (ring0 + ring1 + ...) ---
        spiral_pts = []
        R = float(base_radius_px)

        while R >= float(min_radius_px):
            loop_pts = star_loop_vertices(cx, cy, R)       # (x,y) in original space
            loop_pts = [(y, x) for (x, y) in loop_pts]     # map into transformed space (transpose)
            loop_pts = reorder_start_top_left_clockwise(loop_pts)

            ring_pts = sample_polyline(loop_pts, step=step)
            if not ring_pts:
                break

            # optional: start each ring at the most top-left sampled point (stabilizes visual start)
            if start_on_sample_top_left:
                si = min(range(len(ring_pts)), key=lambda i: (ring_pts[i][1], ring_pts[i][0]))
                ring_pts = ring_pts[si:] + ring_pts[:si]

            spiral_pts.extend(ring_pts)

            R -= float(in_step_px)



        spiral_pts = spiral_pts[::-1]

        if not spiral_pts:
            canvas = np.flipud(canvas)
            canvas = np.rot90(canvas, 3)
            return canvas, rainbow_reset

        # --- draw message along spiral points ---
        n_slots = len(spiral_pts)
        if wrap_message:
            n_draw = n_slots
        else:
            n_draw = min(len(m), n_slots)

        for i in range(n_draw):
            ch = m[i % len(m)] if wrap_message else m[i]
            if ch == ' ':
                continue

            fn = GLYPH_MAP.get(ch)
            if fn is None:
                continue

            px, py = spiral_pts[i]
            corner = (int(px - l_size / 2), int(py - l_size / 2))

            for off in (0, offset_size, density):
                fn(l_size, canvas, (corner[0] + off, corner[1]))
                fn(l_size, canvas, (corner[0] - off, corner[1]))
                fn(l_size, canvas, (corner[0], corner[1] + off))
                fn(l_size, canvas, (corner[0], corner[1] - off))

        # --- undo transform ---
        canvas = np.flipud(canvas)
        canvas = np.rot90(canvas, 3)

        print(len(message))
        print(message)

        if len(message) > 137:
            rainbow_reset = 1

        return canvas, rainbow_reset



    typed_total_0 = 0

    def canvas_write_star_spiral_shrink(
        message,
        size, l_size, x_space, y_space,
        offset_size, density,
        x_o, y_o,
        canvas=0,
        *,
        base_radius_px=210.0,
        in_step_px=18.0,
        min_radius_px=60.0,
        x_shift=128,
        y_shift=16,
        wrap_message=False,
        start_on_sample_top_left=True,

        # NEW: shrink behavior
        shrink_per_ring=0.7,   # 0.90–0.97 feels good
        min_l_size=12,          # don’t go smaller than this
    ):

        global typed_total, typed_total_0
        rainbow_reset = 0
        m = message.lower()
        if len(m) == 0:
            return canvas, rainbow_reset

        canvas = np.rot90(canvas)
        canvas = np.flipud(canvas)

        h, w = canvas.shape[:2]
        cx0 = (w - 1) / 2.0
        cy0 = (h - 1) / 2.0

        cx = cx0 + x_o - x_shift
        cy = cy0 + y_o - y_shift

        spiral_pts = []
        spiral_sizes = []  # store per-point l_size to use when drawing

        R = float(base_radius_px)
        ring_idx = 0

        while R >= float(min_radius_px):
            # compute ring-specific glyph size
            ring_l = int(round(l_size * (shrink_per_ring ** ring_idx)))
            ring_l = max(int(min_l_size), ring_l)

            # ring-specific spacing step (shrink with glyph)
            ring_step = max(1.0, float(ring_l + x_space))

            loop_pts = star_loop_vertices(cx, cy, R)       # (x,y)
            loop_pts = [(y, x) for (x, y) in loop_pts]     # transpose into transformed canvas space
            loop_pts = reorder_start_top_left_clockwise(loop_pts)

            ring_pts = sample_polyline(loop_pts, step=ring_step)
            if not ring_pts:
                break

            if start_on_sample_top_left:
                si = min(range(len(ring_pts)), key=lambda i: (ring_pts[i][1], ring_pts[i][0]))
                ring_pts = ring_pts[si:] + ring_pts[:si]

            spiral_pts.extend(ring_pts)
            spiral_sizes.extend([ring_l] * len(ring_pts))

            R -= float(in_step_px)
            ring_idx += 1

            # optional early stop if glyphs are tiny
            if ring_l <= min_l_size:
                # still allow a couple inner rings if you want; otherwise break
                pass

        if not spiral_pts:
            canvas = np.flipud(canvas)
            canvas = np.rot90(canvas, 3)
            return canvas, rainbow_reset

        n_slots = len(spiral_pts)

        message_len = len(spiral_pts)

        # trigger “page full” exactly like your other writer
        if typed_total%message_len == 0:
            print('loop')
            print(typed_total)
            if typed_total == typed_total_0:
                yeah = 1

            else:
                typed_total_0 = typed_total
                print(typed_total_0)
                if rainbow_reset == 0:
                    rainbow_reset = 1
                    print('reset')
                    print(rainbow_reset)

        if len(m) > n_slots:
            m = m[-n_slots:]

        n_draw = n_slots if wrap_message else min(len(m), n_slots)

        spiral_pts = spiral_pts[::-1]


        for i in range(n_draw):
            ch = m[i % len(m)] if wrap_message else m[i]
            if ch == ' ':
                continue

            fn = GLYPH_MAP.get(ch)
            if fn is None:
                continue

            px, py = spiral_pts[i]
            ring_l = spiral_sizes[i]

            # optional: shrink boldness with ring size
            ring_offset = 0 if ring_l < 18 else offset_size
            ring_density = 0 if ring_l < 18 else density

            corner = (int(px - ring_l / 2), int(py - ring_l / 2))

            for off in (0, ring_offset, ring_density):
                fn(ring_l, canvas, (corner[0] + off, corner[1]))
                fn(ring_l, canvas, (corner[0] - off, corner[1]))
                fn(ring_l, canvas, (corner[0], corner[1] + off))
                fn(ring_l, canvas, (corner[0], corner[1] - off))

        canvas = np.flipud(canvas)
        canvas = np.rot90(canvas, 3)

        return canvas, rainbow_reset








    def _sample_segment_with_step(A, B, step):
        """
        Sample points along segment A->B with spacing ~step.
        A,B are (x,y) floats.
        Returns list of (x,y) floats including A and B.
        """
        ax, ay = A
        bx, by = B
        dx = bx - ax
        dy = by - ay
        L = float(np.hypot(dx, dy))
        if L < 1e-9:
            return []

        # number of steps based on desired spacing
        n = max(1, int(L // step))
        pts = []
        for i in range(n + 1):
            t = (i * step) / L
            if t >= 1.0:
                pts.append((bx, by))
                break
            pts.append((ax + t * dx, ay + t * dy))
        return pts


    def _offsets_signed(spread, max_k):
        """
        Deterministic offset ordering:
          -far left ... -near left, 0, +near right ... +far right
        This tends to feel natural visually (and avoids "all right side first").
        """
        offs = []
        for k in range(max_k, 0, -1):
            offs.append(-k * spread)
        offs.append(0.0)
        for k in range(1, max_k + 1):
            offs.append(+k * spread)
        return offs


    def _lane_basis(theta):
        """
        Unit direction (ux,uy) and unit normal (nx,ny) for lane direction theta.
        """
        ux = float(np.cos(theta))
        uy = float(np.sin(theta))
        nx = -uy
        ny = ux
        return ux, uy, nx, ny



    def build_bethlehem_lane_slots_phased(
            *,
            cx, cy,
            long_len,
            short_len,
            l_size,
            x_space,
            n_layers=7,
            shrink_per_layer=0.86,
            lane_width_layers=3,
            lane_spread_px=10.0,
            diag_scale=1.0,

            # spacing safety
            spacing_scale=0.45,
            stamp_margin_px=3.0,
            offset_size=1,
            density=1,

            reverse_all=False
    ):
        TH_VERT = np.deg2rad(90)
        TH_HORZ = np.deg2rad(0)
        TH_D1 = np.deg2rad(45)  # TL->BR
        TH_D2 = np.deg2rad(-45)  # BL->TR

        lanes = [
            ("V", TH_VERT, long_len),
            ("H", TH_HORZ, long_len),
            ("D1", TH_D1, short_len * diag_scale),
            ("D2", TH_D2, short_len * diag_scale),
        ]

        def basis(theta):
            ux = float(np.cos(theta))
            uy = float(np.sin(theta))
            nx = -uy
            ny = ux
            return nx, ny

        def endpoints(name, L):
            if name == "V":
                return (cx, cy - L), (cx, cy + L)  # top->bottom
            if name == "H":
                return (cx - L, cy), (cx + L, cy)  # left->right
            if name == "D1":
                return (cx - L, cy - L), (cx + L, cy + L)  # TL->BR
            return (cx - L, cy + L), (cx + L, cy - L)  # BL->TR

        slots = []

        # phase bands: 0=centerline, 1=±1, 2=±2 ...
        for phase_k in range(0, lane_width_layers + 1):
            for name, th, L in lanes:
                nx, ny = basis(th)
                A0, B0 = endpoints(name, L)

                for layer in range(n_layers):
                    ring_l = int(round(l_size * (shrink_per_layer ** layer)))
                    if ring_l < 8:
                        break

                    # triangle narrowing inward
                    max_k_layer = max(0, lane_width_layers - (layer // 2))
                    if phase_k > max_k_layer:
                        continue

                    spread = float(lane_spread_px) * (shrink_per_layer ** layer)

                    # offsets for this phase
                    if phase_k == 0:
                        offsets = [0.0]
                    else:
                        offsets = [-phase_k * spread, +phase_k * spread]

                    stamp_footprint = 2.0 * max(offset_size, density)
                    step = (
                            float(ring_l) + float(x_space) +
                            float(ring_l) * float(spacing_scale) +
                            float(stamp_footprint) +
                            float(stamp_margin_px)
                    )
                    step = max(1.0, step)

                    for off in offsets:
                        A = (A0[0] + off * nx, A0[1] + off * ny)
                        B = (B0[0] + off * nx, B0[1] + off * ny)

                        pts = _sample_segment_with_step(A, B, step=step)
                        for (px, py) in pts:
                            slots.append((px, py, ring_l))

        if reverse_all:
            slots = slots[::-1]

        return slots



    def canvas_write_bethlehem_lanes(
            message,
            canvas,
            *,
            slots,  # [(x,y,ring_l), ...] original coords
            offset_size=1,
            density=1,
            wrap_message=False
    ):
        global typed_total, typed_total_0, rainbow_reset


        m = message.lower()
        if len(m) == 0 or not slots:
            return canvas, 0

        n_slots = len(slots)
        print(n_slots)


        # trigger “page full” exactly like your other writer
        if typed_total%n_slots == 0:
            print('loop')
            print(typed_total)
            if typed_total == typed_total_0:
                yeah = 1

            else:
                typed_total_0 = typed_total
                print(typed_total_0)
                if rainbow_reset == 0:
                    rainbow_reset = 1
                    print('reset')
                    print(rainbow_reset)

        if len(m) > n_slots:
            m = m[-n_slots:]



        # smooth rolling window
        if (not wrap_message) and (len(m) > n_slots):
            m = m[-n_slots:]

        canvas = np.rot90(canvas)
        canvas = np.flipud(canvas)

        # mapping for your rot90+flipud (square): (x,y)->(y,x)
        def to_transformed(x, y):
            return (y, x)

        n_draw = n_slots if wrap_message else min(len(m), n_slots)

        for i in range(n_draw):
            ch = m[i % len(m)] if wrap_message else m[i]
            if ch == ' ':
                continue

            fn = GLYPH_MAP.get(ch)
            if fn is None:
                continue

            x, y, ring_l = slots[i]
            tx, ty = to_transformed(x, y)

            corner = (int(tx - ring_l / 2), int(ty - ring_l / 2))

            # prevent overlap on small rings
            ring_offset = 0 if ring_l < 20 else offset_size
            ring_density = 0 if ring_l < 20 else density

            for off in (0, ring_offset, ring_density):
                fn(ring_l, canvas, (corner[0] + off, corner[1]))
                fn(ring_l, canvas, (corner[0] - off, corner[1]))
                fn(ring_l, canvas, (corner[0], corner[1] + off))
                fn(ring_l, canvas, (corner[0], corner[1] - off))

        canvas = np.flipud(canvas)
        canvas = np.rot90(canvas, 3)

        return canvas, n_slots



    def canvas_write_bethlehem_lanes(
            message,
            canvas,
            *,
            slots,  # [(x,y,ring_l), ...] original coords
            offset_size=1,
            density=1,
            wrap_message=False,
            clip_mode="skip",  # "skip" or "clamp"
    ):
        global typed_total, typed_total_0, rainbow_reset

        m = message.lower()
        if len(m) == 0 or not slots:
            return canvas, 0

        n_slots = len(slots)


        if n_slots <= 0:
            return canvas, 0

        # rolling window once
        if (not wrap_message) and (len(m) > n_slots):
            m = m[-n_slots:]

        # rotation clock: only once per new multiple, and not at 0
        if (typed_total > 0) and (typed_total % n_slots == 0) and (typed_total != typed_total_0):
            typed_total_0 = typed_total
            rainbow_reset = 1
            # print("reset", typed_total, "slots", n_slots)

        # draw transform (matches your system)
        canvas = np.rot90(canvas)
        canvas = np.flipud(canvas)

        H, W = canvas.shape[:2]

        # mapping for your rot90+flipud (square): (x,y)->(y,x)
        def to_transformed(x, y):
            return (y, x)

        def fits(cx0, cy0, size):
            pad = size
            return (
                    0 <= cx0 and
                    0 <= cy0 and
                    cx0 + pad < W and
                    cy0 + pad < H
            )

        n_draw = n_slots if wrap_message else min(len(m), n_slots)

        for i in range(n_draw):
            ch = m[i % len(m)] if wrap_message else m[i]
            if ch == ' ':
                continue

            fn = GLYPH_MAP.get(ch)
            if fn is None:
                continue

            x, y, ring_l = slots[i]
            tx, ty = to_transformed(x, y)

            base_corner = (int(tx - ring_l / 2), int(ty - ring_l / 2))

            # reduce stamp expansion for small glyphs
            ring_offset = 0 if ring_l < 20 else offset_size
            ring_density = 0 if ring_l < 20 else density

            for off in (0, ring_offset, ring_density):
                corners = (
                    (base_corner[0] + off, base_corner[1]),
                    (base_corner[0] - off, base_corner[1]),
                    (base_corner[0], base_corner[1] + off),
                    (base_corner[0], base_corner[1] - off),
                )

                for cx0, cy0 in corners:
                    if fits(cx0, cy0, ring_l):
                        fn(ring_l, canvas, (cx0, cy0))
                    else:
                        if clip_mode == "clamp":
                            # clamp so the entire glyph fits (prevents crash)
                            cx1 = min(max(cx0, 0), W - ring_l)
                            cy1 = min(max(cy0, 0), H - ring_l)
                            fn(ring_l, canvas, (cx1, cy1))
                        # clip_mode == "skip": do nothing (skip out-of-bounds stamp)

        # undo transform
        canvas = np.flipud(canvas)
        canvas = np.rot90(canvas, 3)

        return canvas, n_slots


    size = 64
    l_size = 32
    x_space = 8
    y_space = 16
    offset_size = 1
    density = 1
    x_o = 128
    y_o = 32 + water_line * (size + 16)



    bethlehem_slots = build_bethlehem_lane_slots_phased(
        cx=(l - 1) / 2.0,
        cy=(h - 1) / 2.0,
        long_len=min(h, l) * 0.48,
        short_len=min(h, l) * 0.30,
        l_size=l_size,
        x_space=x_space,
        n_layers=7,
        shrink_per_layer=0.86,
        lane_width_layers=3,
        lane_spread_px=10.0,
        diag_scale=1.0,
        spacing_scale=0.45,
        stamp_margin_px=3.0,
        offset_size=offset_size,
        density=density,
    )





last_letter_typed = ' '
current_voted_letter = ' '





### hand sensor####

hand_sensor = 1



if hand_sensor == 1:

    hand_box_pad = 48

    right_box = None
    right_open_hand_mask = None
    right_open_hand_frame = None

    edge_library = {}
    current_edge_label = "a"
    recognized_edge_label = " "
    recognized_edge_score = 999.0

    right_exclusion_edge_mask = None
    right_exclusion_threshold = 0.03

    right_change_speed = None
    right_cluster_count = 0

    right_shadow_mask = None

    tracked_squares = {
        "pinky": {"color": None, "point": None, "strength": 0.0, "misses": 0},
        "ring": {"color": None, "point": None, "strength": 0.0, "misses": 0},
        "middle": {"color": None, "point": None, "strength": 0.0, "misses": 0},
        "index": {"color": None, "point": None, "strength": 0.0, "misses": 0},
        "thumb": {"color": None, "point": None, "strength": 0.0, "misses": 0},
    }

    left_box = None
    left_open_hand_mask = None
    left_open_hand_frame = None

    left_exclusion_edge_mask = None
    left_exclusion_threshold = 0.03

    left_change_speed = None
    left_cluster_count = 0

    left_shadow_mask = None

    tracked_squares_left = {
        "pinky": {"color": None, "point": None, "strength": 0.0, "misses": 0},
        "ring": {"color": None, "point": None, "strength": 0.0, "misses": 0},
        "middle": {"color": None, "point": None, "strength": 0.0, "misses": 0},
        "index": {"color": None, "point": None, "strength": 0.0, "misses": 0},
        "thumb": {"color": None, "point": None, "strength": 0.0, "misses": 0},
    }




    def update_shadow_mask(current_mask, shadow_mask=None, rise=1.0, decay=0.92):
        """
        current_mask: (H,W) float/bool mask of current fast clusters
        shadow_mask: persistent fading memory in [0,1]

        rise:
            how strongly current pixels refresh the shadow
        decay:
            how long old pixels remain visible
        """
        if current_mask is None:
            return shadow_mask

        cur = current_mask.astype(np.float32)

        if shadow_mask is None or shadow_mask.shape != cur.shape:
            shadow_mask = np.zeros_like(cur, dtype=np.float32)

        shadow_mask = np.maximum(shadow_mask * decay, cur * rise)
        shadow_mask = np.clip(shadow_mask, 0.0, 1.0)

        return shadow_mask


    def draw_shadow_mask_on_field(screen, shadow_mask, box,
                                  live_mask=None,
                                  shadow_threshold=0.08,
                                  live_threshold=0.5):
        """
        Draw only the fading shadow.
        Live pixels are omitted here so they can be drawn separately if desired.
        """
        if shadow_mask is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        mh, mw = shadow_mask.shape

        if w <= 0 or h <= 0:
            return

        sx = w / float(mw)
        sy = h / float(mh)

        if live_mask is None or live_mask.shape != shadow_mask.shape:
            live_mask = np.zeros_like(shadow_mask, dtype=np.float32)

        ys, xs = np.where(shadow_mask >= shadow_threshold)
        for yy, xx in zip(ys, xs):
            if live_mask[yy, xx] >= live_threshold:
                continue

            v = float(shadow_mask[yy, xx])
            g = int(max(40, min(180, 180 * v)))   # soft grey shadow

            px = x1 + int(xx * sx)
            py = y1 + int(yy * sy)
            if 0 <= px < screen_width and 0 <= py < screen_height:
                screen.set_at((px, py), (g, g, g))

    def build_exclusionary_edge_mask(current_edge_mask, exclusion_edge_mask, keep_threshold=0.02):
        """
        Remove edges that were already present during calibration.
        Keeps only edges that are sufficiently stronger/different than exclusion edges.
        """
        if current_edge_mask is None:
            return None

        if exclusion_edge_mask is None:
            return (current_edge_mask >= keep_threshold).astype(np.float32)

        if current_edge_mask.shape != exclusion_edge_mask.shape:
            return (current_edge_mask >= keep_threshold).astype(np.float32)

        # subtract old/background edges
        diff = current_edge_mask - exclusion_edge_mask
        diff = np.clip(diff, 0.0, 1.0)

        return (diff >= keep_threshold).astype(np.float32)


    def threshold_edge_mask(edge_mask, threshold=0.03):
        if edge_mask is None:
            return None
        return (edge_mask >= threshold).astype(np.float32)


    def resize_binary_image(img, out_size=(64, 64)):
        if img is None:
            return None

        h, w = img.shape
        out_h, out_w = out_size

        ys = np.linspace(0, h - 1, out_h).astype(int)
        xs = np.linspace(0, w - 1, out_w).astype(int)

        return img[np.ix_(ys, xs)].astype(np.float32)


    def prepare_edge_template(field, edge_threshold=0.03, out_size=(64, 64)):
        edge_mask = build_hand_sensor(field)
        if edge_mask is None:
            return None

        binary = threshold_edge_mask(edge_mask, threshold=edge_threshold)
        templ = resize_binary_image(binary, out_size=out_size)
        return templ


    def edge_template_distance(a, b):
        if a is None or b is None:
            return 999.0
        if a.shape != b.shape:
            return 999.0

        # mean absolute difference
        return float(np.mean(np.abs(a - b)))


    def save_edge_template(template):
        global edge_library, phrase

        if template is None:
            print("no edge template to save")
            return

        if phrase == '':
            print("phrase is empty")
            return

        if phrase not in edge_library:
            edge_library[phrase] = []

        edge_library[phrase].append(template.copy())

        print("saved edge label:", phrase)
        print("templates for label:", len(edge_library[phrase]))
        print("template shape:", template.shape)


    def recognize_edge_template(template, library, threshold=0.18):
        if template is None:
            return " ", 999.0

        best_label = " "
        best_score = 999.0

        for label, templates in library.items():
            for templ in templates:
                score = edge_template_distance(template, templ)
                if score < best_score:
                    best_score = score
                    best_label = label

        if best_score > threshold:
            return " ", best_score

        return best_label, best_score



    def outline_hand_window(screen, rois, color, pad=40, width=3):
        xs = [r[0] for r in rois] + [r[2] for r in rois]
        ys = [r[1] for r in rois] + [r[3] for r in rois]

        x1 = max(0, min(xs) - pad)
        y1 = max(0, min(ys) - pad)
        x2 = min(screen_width, max(xs) + pad)
        y2 = min(screen_height, max(ys) + pad)

        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(x1, y1, x2 - x1, y2 - y1),
            width
        )

        return (x1, y1, x2, y2)


    def mean_color(region):
        if region is None or region.size == 0:
            return None
        return region.reshape(-1, 3).mean(axis=0)


    def sample_hand_color(frame_array, rois):
        px1, py1, px2, py2 = rois[-1]
        palm_region = frame_array[px1:px2, py1:py2]
        return mean_color(palm_region)


    def hand_color_mask(field, target_color, color_threshold=60, brightness_threshold=90):
        if field is None or field.size == 0 or target_color is None:
            return None

        field_f = field.astype(np.float32)
        target = np.array(target_color, dtype=np.float32)

        diff = field_f - target
        dist = np.sqrt(np.sum(diff * diff, axis=2))

        field_brightness = field_f.mean(axis=2)
        target_brightness = target.mean()
        brightness_diff = np.abs(field_brightness - target_brightness)

        mask = (dist <= color_threshold) | (
            (dist <= color_threshold * 1.5) & (brightness_diff <= brightness_threshold)
        )

        return mask.astype(np.float32)


    def largest_connected_blob(mask):
        if mask is None:
            return None

        mask = mask > 0.5
        h, w = mask.shape
        visited = np.zeros((h, w), dtype=bool)

        best_coords = []
        best_size = 0

        for y in range(h):
            for x in range(w):
                if not mask[y, x] or visited[y, x]:
                    continue

                stack = [(y, x)]
                visited[y, x] = True
                coords = []

                while stack:
                    cy, cx = stack.pop()
                    coords.append((cy, cx))

                    for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))

                if len(coords) > best_size:
                    best_size = len(coords)
                    best_coords = coords

        out = np.zeros((h, w), dtype=np.float32)
        for y, x in best_coords:
            out[y, x] = 1.0

        return out


    def capture_open_hand_mask(frame_array, rois, pad=60, color_threshold=60, brightness_threshold=90):
        xs = [r[0] for r in rois] + [r[2] for r in rois]
        ys = [r[1] for r in rois] + [r[3] for r in rois]

        x1 = max(0, min(xs) - pad)
        y1 = max(0, min(ys) - pad)
        x2 = min(screen_width, max(xs) + pad)
        y2 = min(screen_height, max(ys) + pad)

        field = frame_array[x1:x2, y1:y2].copy()
        target_color = sample_hand_color(frame_array, rois)

        raw_mask = hand_color_mask(
            field,
            target_color,
            color_threshold=color_threshold,
            brightness_threshold=brightness_threshold
        )
        if raw_mask is None:
            return None, (x1, y1, x2, y2)

        raw_mask = raw_mask.T
        blob = largest_connected_blob(raw_mask)

        return blob, (x1, y1, x2, y2)


    def capture_frame_from_fixed_box(frame_array, box):
        if box is None:
            return None

        x1, y1, x2, y2 = box
        return frame_array[x1:x2, y1:y2].copy()


    def draw_sensor_field(screen, sensor_rgb, pos):
        if sensor_rgb is None:
            return

        surf = pygame.surfarray.make_surface(np.transpose(sensor_rgb, (1, 0, 2)))
        screen.blit(surf, pos)


    x1, y1, x2, y2 = outline_hand_window(
        screen,
        right_roi,
        value_color[9],
        pad=hand_box_pad,
        width=3
    )




    def connected_components_with_stats(mask, field):
        """
        mask: (H,W) bool/float
        field: (W,H,3) raw crop
        returns list of dicts with:
          mask, size, bbox, mean_color
        """
        if mask is None:
            return []

        mask = mask > 0.5
        h, w = mask.shape
        visited = np.zeros((h, w), dtype=bool)

        # convert field to (H,W,3) to match mask coordinates
        img = np.transpose(field, (1, 0, 2)).astype(np.float32)

        comps = []

        for y in range(h):
            for x in range(w):
                if not mask[y, x] or visited[y, x]:
                    continue

                stack = [(y, x)]
                visited[y, x] = True
                coords = []

                while stack:
                    cy, cx = stack.pop()
                    coords.append((cy, cx))

                    for ny, nx in (
                        (cy - 1, cx), (cy + 1, cx),
                        (cy, cx - 1), (cy, cx + 1),
                        (cy - 1, cx - 1), (cy - 1, cx + 1),
                        (cy + 1, cx - 1), (cy + 1, cx + 1),
                    ):
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))

                comp_mask = np.zeros((h, w), dtype=np.float32)
                ys = []
                xs = []
                pixels = []

                for cy, cx in coords:
                    comp_mask[cy, cx] = 1.0
                    ys.append(cy)
                    xs.append(cx)
                    pixels.append(img[cy, cx])

                pixels = np.array(pixels, dtype=np.float32)
                mean_color = pixels.mean(axis=0) if len(pixels) > 0 else np.array([0, 0, 0], dtype=np.float32)

                comps.append({
                    "mask": comp_mask,
                    "size": len(coords),
                    "bbox": (min(xs), min(ys), max(xs) + 1, max(ys) + 1),
                    "mean_color": mean_color,
                })

        return comps


    def merge_largest_with_similar_neighbors(mask, field, color_threshold=50, gap_threshold=14, min_size_ratio=0.008):
        """
        Keep the largest blob, plus nearby blobs whose color is similar.
        mask: (H,W)
        field: (W,H,3)
        """
        comps = connected_components_with_stats(mask, field)
        if not comps:
            return None

        comps = sorted(comps, key=lambda c: c["size"], reverse=True)
        main = comps[0]

        main_size = main["size"]
        main_color = main["mean_color"]
        merged = main["mask"].copy()

        mx1, my1, mx2, my2 = main["bbox"]

        for comp in comps[1:]:
            if comp["size"] < max(4, int(main_size * min_size_ratio)):
                continue

            cx1, cy1, cx2, cy2 = comp["bbox"]

            dx = max(0, max(mx1 - cx2, cx1 - mx2))
            dy = max(0, max(my1 - cy2, cy1 - my2))
            gap = (dx * dx + dy * dy) ** 0.5

            color_dist = np.linalg.norm(comp["mean_color"] - main_color)

            if gap <= gap_threshold and color_dist <= color_threshold:
                merged = np.maximum(merged, comp["mask"])

        return merged.astype(np.float32)


    def build_hand_sensor(field):
        """
        field: raw hand crop in (W,H,3)

        returns:
            edge_mask: (H,W) float32 in [0,1]
        """
        if field is None or field.size == 0:
            return None

        img = np.transpose(field, (1, 0, 2)).astype(np.float32)  # (H,W,3)

        gray = (
            0.299 * img[:, :, 0] +
            0.587 * img[:, :, 1] +
            0.114 * img[:, :, 2]
        )

        gx = np.zeros_like(gray, dtype=np.float32)
        gy = np.zeros_like(gray, dtype=np.float32)

        gx[:, 1:] = np.abs(gray[:, 1:] - gray[:, :-1])
        gy[1:, :] = np.abs(gray[1:, :] - gray[:-1, :])

        edge = np.sqrt(gx * gx + gy * gy)

        emax = edge.max()
        if emax > 1e-6:
            edge_mask = edge / emax
        else:
            edge_mask = np.zeros_like(edge, dtype=np.float32)

        return edge_mask






    def overlay_edge_sensor_on_field(screen, sensor_rgb, box, alpha=0.65):
        """
        Draw edge sensor directly on top of the hand detector field.
        box = (x1, y1, x2, y2) in screen coordinates
        sensor_rgb should be (H,W,3)
        """
        if sensor_rgb is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1

        if w <= 0 or h <= 0:
            return

        surf = pygame.surfarray.make_surface(np.transpose(sensor_rgb, (1, 0, 2)))
        surf = pygame.transform.scale(surf, (w, h))
        surf.set_alpha(int(alpha * 255))
        screen.blit(surf, (x1, y1))


    def draw_edge_overlay_on_field(screen, edge_mask, box, threshold=0.22, edge_color=(140, 140, 140)):
        """
        Draw only the strong edges in grey over the live camera hand field.
        """
        if edge_mask is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1

        if w <= 0 or h <= 0:
            return

        edge_on = edge_mask >= threshold
        eh, ew = edge_on.shape

        # map edge mask coordinates to screen box coordinates
        sx = w / float(ew)
        sy = h / float(eh)

        for yy in range(eh):
            for xx in range(ew):
                if edge_on[yy, xx]:
                    px = x1 + int(xx * sx)
                    py = y1 + int(yy * sy)
                    if 0 <= px < screen_width and 0 <= py < screen_height:
                        screen.set_at((px, py), edge_color)


    def dilate_mask(mask, radius=2):
        if mask is None:
            return None

        out = mask.copy().astype(bool)

        for _ in range(radius):
            up = np.roll(out, -1, axis=0)
            down = np.roll(out, 1, axis=0)
            left = np.roll(out, -1, axis=1)
            right = np.roll(out, 1, axis=1)

            ul = np.roll(up, -1, axis=1)
            ur = np.roll(up, 1, axis=1)
            dl = np.roll(down, -1, axis=1)
            dr = np.roll(down, 1, axis=1)

            out = out | up | down | left | right | ul | ur | dl | dr

        return out.astype(np.float32)



    def build_calibrated_hand_region():
        global right_open_hand_mask

        if right_open_hand_mask is None:
            return None

        return dilate_mask(right_open_hand_mask, radius=4)




    def clean_edge_mask(edge_mask, hand_region, edge_threshold=0.02):
        """
        Keep only strong edges inside the calibrated hand region.
        """
        if edge_mask is None:
            return None

        edges_on = (edge_mask >= edge_threshold).astype(np.float32)

        if hand_region is None:
            return edges_on

        if hand_region.shape != edge_mask.shape:
            return edges_on

        cleaned = edges_on * (hand_region > 0.5)
        return cleaned.astype(np.float32)




    edge_library = {}
    current_edge_label = phrase


    def save_edge_mask(label, edge_mask):
        global edge_library

        if edge_mask is None:
            print("no edge mask to save")
            return

        if label not in edge_library:
            edge_library[label] = []

        edge_library[label].append(edge_mask.copy())

        print("saved edge label:", label)
        print("templates for label:", len(edge_library[label]))
        print("edge mask shape:", edge_mask.shape)


    def build_hand_isolation_mask(field, rois,
                                  color_threshold=70,
                                  brightness_threshold=110,
                                  gap_threshold=18,
                                  min_size_ratio=0.004,
                                  dilate_radius=4):
        """
        Build a forgiving hand-region mask in (H,W).
        Keeps likely hand area without throwing away finger detail too early.
        """
        if field is None or field.size == 0:
            return None

        target_color = sample_hand_color(hand_array, rois)

        raw_mask = hand_color_mask(
            field,
            target_color,
            color_threshold=color_threshold,
            brightness_threshold=brightness_threshold
        )
        if raw_mask is None:
            return None

        # (W,H) -> (H,W)
        mask = raw_mask.T

        # merge nearby similar components instead of strict single blob
        mask = merge_largest_with_similar_neighbors(
            mask,
            field,
            color_threshold=55,
            gap_threshold=gap_threshold,
            min_size_ratio=min_size_ratio
        )
        if mask is None:
            return None

        # expand slightly so thin finger edges are not clipped
        mask = dilate_mask(mask, radius=dilate_radius)

        return mask.astype(np.float32)











    def skin_closeness_map(field, target_color, brightness_threshold=110):
        """
        field: (W,H,3)
        target_color: sampled palm mean RGB
        returns closeness map in (H,W), values in [0,1]
        """
        if field is None or field.size == 0 or target_color is None:
            return None

        field_f = field.astype(np.float32)
        target = np.array(target_color, dtype=np.float32)

        diff = field_f - target
        dist = np.sqrt(np.sum(diff * diff, axis=2))

        field_brightness = field_f.mean(axis=2)
        target_brightness = target.mean()
        brightness_diff = np.abs(field_brightness - target_brightness)

        # convert to closeness instead of hard threshold
        color_score = 1.0 - np.clip(dist / 120.0, 0.0, 1.0)
        bright_score = 1.0 - np.clip(brightness_diff / float(brightness_threshold), 0.0, 1.0)

        closeness = color_score * 0.75 + bright_score * 0.25

        # transpose to (H,W) to match edge_mask
        return closeness.T.astype(np.float32)




    def heat_color(score):
        """
        score in [0,1]
        low -> blue
        mid -> green
        high -> yellow/red
        """
        s = float(np.clip(score, 0.0, 1.0))

        if s < 0.33:
            t = s / 0.33
            r = 0
            g = int(255 * t)
            b = int(255 * (1.0 - t))
        elif s < 0.66:
            t = (s - 0.33) / 0.33
            r = int(255 * t)
            g = 255
            b = 0
        else:
            t = (s - 0.66) / 0.34
            r = 255
            g = int(255 * (1.0 - t))
            b = 0

        return (r, g, b)


    def draw_edge_heat_overlay_on_field(screen, edge_mask, closeness_map, box, threshold=0.5):
        """
        Draw edge pixels colored by skin closeness heat.
        edge_mask, closeness_map are (H,W)
        """
        if edge_mask is None or closeness_map is None or box is None:
            return

        if edge_mask.shape != closeness_map.shape:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1

        if w <= 0 or h <= 0:
            return

        edge_on = edge_mask >= threshold
        eh, ew = edge_on.shape

        sx = w / float(ew)
        sy = h / float(eh)

        for yy in range(eh):
            for xx in range(ew):
                if edge_on[yy, xx]:
                    px = x1 + int(xx * sx)
                    py = y1 + int(yy * sy)
                    if 0 <= px < screen_width and 0 <= py < screen_height:
                        score = closeness_map[yy, xx]
                        screen.set_at((px, py), heat_color(score))



    def get_top_seed_points(mask, min_gap=6):
        """
        Starting points from the upper silhouette of the blob.
        """
        if mask is None:
            return []

        m = mask > 0.5
        h, w = m.shape

        seeds = []
        last_x = -999

        for x in range(w):
            ys = np.where(m[:, x])[0]
            if len(ys) == 0:
                continue

            y = int(ys.min())

            if x - last_x >= min_gap:
                seeds.append((x, y))
                last_x = x

        return seeds


    def trace_downward_path(mask, start, max_steps=90, lateral=2, angle_dot_min=-0.15):
        """
        Follow a finger-like route downward through the blob.
        angle_dot_min:
            higher = straighter
            lower = more bend allowed
        """
        if mask is None:
            return []

        m = mask > 0.5
        h, w = m.shape
        x, y = start

        if not (0 <= x < w and 0 <= y < h):
            return []
        if not m[y, x]:
            return []

        path = [(x, y)]
        prev_step = np.array([0.0, 1.0], dtype=np.float32)  # downward bias

        for _ in range(max_steps):
            candidates = []

            for dx in range(-lateral, lateral + 1):
                nx = x + dx
                ny = y + 1

                if 0 <= nx < w and 0 <= ny < h and m[ny, nx]:
                    step = np.array([nx - x, ny - y], dtype=np.float32)
                    nrm = np.linalg.norm(step)
                    if nrm <= 1e-6:
                        continue
                    step = step / nrm

                    dot = float(np.dot(prev_step, step))

                    # allow gentle or obtuse bends, reject strong reversals
                    if dot >= angle_dot_min:
                        # prefer straighter and more centered continuation
                        score = dot - 0.10 * abs(dx)
                        candidates.append((score, nx, ny, step))

            if not candidates:
                break

            candidates.sort(key=lambda t: t[0], reverse=True)
            _, x, y, step = candidates[0]

            if (x, y) in path:
                break

            path.append((x, y))
            prev_step = step

        return path


    def path_score(path):
        """
        Long, downward, not-too-wobbly paths score best.
        """
        if not path:
            return -999.0

        xs = np.array([p[0] for p in path], dtype=np.float32)
        ys = np.array([p[1] for p in path], dtype=np.float32)

        length = float(len(path))
        x_span = float(xs.max() - xs.min()) if len(xs) > 0 else 0.0
        y_span = float(ys.max() - ys.min()) if len(ys) > 0 else 0.0

        return length + 1.2 * y_span - 0.6 * x_span


    def paths_overlap_too_much(p1, p2, x_tol=8):
        if not p1 or not p2:
            return False

        c1 = np.mean([x for x, y in p1])
        c2 = np.mean([x for x, y in p2])

        return abs(c1 - c2) < x_tol


    def find_finger_paths(mask, max_fingers=5):
        if mask is None:
            return []

        seeds = get_top_seed_points(mask, min_gap=5)
        candidates = []

        for s in seeds:
            p = trace_downward_path(
                mask,
                s,
                max_steps=90,
                lateral=2,
                angle_dot_min=-0.15
            )

            if len(p) >= 10:
                candidates.append((path_score(p), p))

        candidates.sort(key=lambda t: t[0], reverse=True)

        chosen = []
        for score, p in candidates:
            keep = True
            for q in chosen:
                if paths_overlap_too_much(p, q, x_tol=8):
                    keep = False
                    break
            if keep:
                chosen.append(p)

            if len(chosen) >= max_fingers:
                break

        return chosen


    def draw_paths_on_field(screen, paths, box, mask_shape, color=(255, 0, 0), width=3):
        if not paths or box is None:
            return

        x1, y1, x2, y2 = box
        h, w = mask_shape

        sx = (x2 - x1) / float(w)
        sy = (y2 - y1) / float(h)

        for path in paths:
            if len(path) < 2:
                continue

            pts = []
            for px, py in path:
                sxp = x1 + int(px * sx)
                syp = y1 + int(py * sy)
                pts.append((sxp, syp))

            if len(pts) >= 2:
                pygame.draw.lines(screen, color, False, pts, width)

            # top endpoint
            pygame.draw.circle(screen, (255, 255, 255), pts[0], 4)



    def build_hyper_edge_mask(edge_mask, radius=6, min_balance=0.18, min_total=0.10):
        """
        Hyper edges:
        an edge pixel is kept if, in a meaningful neighborhood around it,
        one side has lots of edge activity and the other side has little.

        edge_mask: (H,W) float in [0,1]
        returns: (H,W) float mask in [0,1]
        """
        if edge_mask is None:
            return None

        e = edge_mask.astype(np.float32)
        h, w = e.shape
        out = np.zeros((h, w), dtype=np.float32)

        # gradients of the edge field give a local normal direction
        gx = np.zeros_like(e, dtype=np.float32)
        gy = np.zeros_like(e, dtype=np.float32)

        gx[:, 1:-1] = (e[:, 2:] - e[:, :-2]) * 0.5
        gy[1:-1, :] = (e[2:, :] - e[:-2, :]) * 0.5

        for y in range(radius, h - radius):
            for x in range(radius, w - radius):
                if e[y, x] <= 0.0:
                    continue

                nx = gx[y, x]
                ny = gy[y, x]
                nrm = float((nx * nx + ny * ny) ** 0.5)

                if nrm < 1e-6:
                    continue

                nx /= nrm
                ny /= nrm

                pos_sum = 0.0
                neg_sum = 0.0
                pos_n = 0
                neg_n = 0

                for r in range(1, radius + 1):
                    xp = int(round(x + nx * r))
                    yp = int(round(y + ny * r))
                    xm = int(round(x - nx * r))
                    ym = int(round(y - ny * r))

                    if 0 <= xp < w and 0 <= yp < h:
                        pos_sum += e[yp, xp]
                        pos_n += 1

                    if 0 <= xm < w and 0 <= ym < h:
                        neg_sum += e[ym, xm]
                        neg_n += 1

                if pos_n == 0 or neg_n == 0:
                    continue

                pos_mean = pos_sum / pos_n
                neg_mean = neg_sum / neg_n
                total = pos_mean + neg_mean
                balance = abs(pos_mean - neg_mean)

                if total >= min_total and balance >= min_balance:
                    out[y, x] = min(1.0, balance / max(total, 1e-6))

        return out


    def draw_hyper_edge_overlay_on_field(screen, hyper_edge_mask, box, threshold=0.25, color=(255, 255, 255)):
        if hyper_edge_mask is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        eh, ew = hyper_edge_mask.shape

        sx = w / float(ew)
        sy = h / float(eh)

        for yy in range(eh):
            for xx in range(ew):
                if hyper_edge_mask[yy, xx] >= threshold:
                    px = x1 + int(xx * sx)
                    py = y1 + int(yy * sy)
                    if 0 <= px < screen_width and 0 <= py < screen_height:
                        screen.set_at((px, py), color)



    def longest_connected_line(mask, threshold=0.25):
        """
        mask: (H,W) float
        returns a float mask with only the largest connected component kept
        """
        if mask is None:
            return None

        on = mask >= threshold
        h, w = on.shape
        visited = np.zeros((h, w), dtype=bool)

        best_coords = []
        best_size = 0

        for y in range(h):
            for x in range(w):
                if not on[y, x] or visited[y, x]:
                    continue

                stack = [(y, x)]
                visited[y, x] = True
                coords = []

                while stack:
                    cy, cx = stack.pop()
                    coords.append((cy, cx))

                    for ny, nx in (
                        (cy - 1, cx), (cy + 1, cx),
                        (cy, cx - 1), (cy, cx + 1),
                        (cy - 1, cx - 1), (cy - 1, cx + 1),
                        (cy + 1, cx - 1), (cy + 1, cx + 1),
                    ):
                        if 0 <= ny < h and 0 <= nx < w and on[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))

                if len(coords) > best_size:
                    best_size = len(coords)
                    best_coords = coords

        out = np.zeros((h, w), dtype=np.float32)
        for y, x in best_coords:
            out[y, x] = 1.0

        return out


    def draw_binary_mask_on_field(screen, mask, box, color=(255, 255, 255)):
        if mask is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1

        if w <= 0 or h <= 0:
            return

        mh, mw = mask.shape
        sx = w / float(mw)
        sy = h / float(mh)

        for yy in range(mh):
            for xx in range(mw):
                if mask[yy, xx] > 0.5:
                    px = x1 + int(xx * sx)
                    py = y1 + int(yy * sy)
                    if 0 <= px < screen_width and 0 <= py < screen_height:
                        screen.set_at((px, py), color)










    def draw_perimeter_on_field(screen, perimeter, box, color=(255, 255, 255)):
        if perimeter is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1

        if w <= 0 or h <= 0:
            return

        ph, pw = perimeter.shape
        sx = w / float(pw)
        sy = h / float(ph)

        for yy in range(ph):
            for xx in range(pw):
                if perimeter[yy, xx] > 0.5:
                    px = x1 + int(xx * sx)
                    py = y1 + int(yy * sy)
                    if 0 <= px < screen_width and 0 <= py < screen_height:
                        screen.set_at((px, py), color)




    def fast_hand_perimeter(edge_mask, hand_region, edge_threshold=0.023, close_radius=1):
        """
        One compact pass:
        1. threshold edges
        2. apply hand region
        3. small close
        4. extract perimeter

        returns:
            filled_mask, perimeter_mask
        """
        if edge_mask is None:
            return None, None

        m = edge_mask >= edge_threshold

        if hand_region is not None and hand_region.shape == edge_mask.shape:
            m &= (hand_region > 0.5)

        # small close = dilate then erode
        for _ in range(close_radius):
            up = np.roll(m, -1, axis=0)
            down = np.roll(m, 1, axis=0)
            left = np.roll(m, -1, axis=1)
            right = np.roll(m, 1, axis=1)
            ul = np.roll(up, -1, axis=1)
            ur = np.roll(up, 1, axis=1)
            dl = np.roll(down, -1, axis=1)
            dr = np.roll(down, 1, axis=1)
            m = m | up | down | left | right | ul | ur | dl | dr

        for _ in range(close_radius):
            up = np.roll(m, -1, axis=0)
            down = np.roll(m, 1, axis=0)
            left = np.roll(m, -1, axis=1)
            right = np.roll(m, 1, axis=1)
            ul = np.roll(up, -1, axis=1)
            ur = np.roll(up, 1, axis=1)
            dl = np.roll(down, -1, axis=1)
            dr = np.roll(down, 1, axis=1)
            m = m & up & down & left & right & ul & ur & dl & dr

        up = np.roll(m, -1, axis=0)
        down = np.roll(m, 1, axis=0)
        left = np.roll(m, -1, axis=1)
        right = np.roll(m, 1, axis=1)

        perimeter = m & ((~up) | (~down) | (~left) | (~right))

        return m.astype(np.float32), perimeter.astype(np.float32)




    def draw_binary_overlay_on_field(screen, mask, box, color=(255, 255, 255)):
        if mask is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        mh, mw = mask.shape

        if w <= 0 or h <= 0 or mw <= 0 or mh <= 0:
            return

        sx = w / float(mw)
        sy = h / float(mh)

        ys, xs = np.where(mask > 0.5)
        for yy, xx in zip(ys, xs):
            px = x1 + int(xx * sx)
            py = y1 + int(yy * sy)
            if 0 <= px < screen_width and 0 <= py < screen_height:
                screen.set_at((px, py), color)





    def build_change_speed_map(current_field, previous_field, prev_speed_map=None, alpha=0.35):
        """
        current_field, previous_field: (W,H,3)
        prev_speed_map: (H,W) float or None

        returns:
            speed_map: (H,W) float in [0,1]
        """
        if current_field is None or previous_field is None:
            return prev_speed_map

        if current_field.shape != previous_field.shape:
            return prev_speed_map

        cur = np.transpose(current_field, (1, 0, 2)).astype(np.float32)
        prev = np.transpose(previous_field, (1, 0, 2)).astype(np.float32)

        diff = np.abs(cur - prev)
        dist = np.sqrt(np.sum(diff * diff, axis=2))

        dmax = dist.max()
        if dmax > 1e-6:
            instant = dist / dmax
        else:
            instant = np.zeros_like(dist, dtype=np.float32)

        if prev_speed_map is None or prev_speed_map.shape != instant.shape:
            speed_map = instant
        else:
            speed_map = (1.0 - alpha) * prev_speed_map + alpha * instant

        return speed_map.astype(np.float32)


    def threshold_fast_pixels(speed_map, threshold=0.35):
        if speed_map is None:
            return None
        return (speed_map >= threshold).astype(np.float32)


    def count_clusters(mask, min_size=6):
        """
        mask: (H,W) float/bool
        returns:
            count, labeled_mask
        """
        if mask is None:
            return 0, None

        on = mask > 0.5
        h, w = on.shape
        visited = np.zeros((h, w), dtype=bool)
        out = np.zeros((h, w), dtype=np.float32)

        count = 0

        for y in range(h):
            for x in range(w):
                if not on[y, x] or visited[y, x]:
                    continue

                stack = [(y, x)]
                visited[y, x] = True
                coords = []

                while stack:
                    cy, cx = stack.pop()
                    coords.append((cy, cx))

                    for ny, nx in (
                        (cy - 1, cx), (cy + 1, cx),
                        (cy, cx - 1), (cy, cx + 1),
                        (cy - 1, cx - 1), (cy - 1, cx + 1),
                        (cy + 1, cx - 1), (cy + 1, cx + 1),
                    ):
                        if 0 <= ny < h and 0 <= nx < w and on[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))

                if len(coords) >= min_size:
                    count += 1
                    for cy, cx in coords:
                        out[cy, cx] = 1.0

        return count, out


    def draw_speed_heat_on_field(screen, speed_map, box, threshold=0.0):
        if speed_map is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        sh, sw = speed_map.shape

        if w <= 0 or h <= 0:
            return

        sx = w / float(sw)
        sy = h / float(sh)

        for yy in range(sh):
            for xx in range(sw):
                s = speed_map[yy, xx]
                if s < threshold:
                    continue
                px = x1 + int(xx * sx)
                py = y1 + int(yy * sy)
                if 0 <= px < screen_width and 0 <= py < screen_height:
                    screen.set_at((px, py), heat_color(s))


    def draw_cluster_mask_on_field(screen, mask, box, color=(255, 255, 255)):
        if mask is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        mh, mw = mask.shape

        if w <= 0 or h <= 0:
            return

        sx = w / float(mw)
        sy = h / float(mh)

        ys, xs = np.where(mask > 0.5)
        for yy, xx in zip(ys, xs):
            px = x1 + int(xx * sx)
            py = y1 + int(yy * sy)
            if 0 <= px < screen_width and 0 <= py < screen_height:
                screen.set_at((px, py), color)





    def xy_field_color(xx, yy, w, h):
        """
        Color by position in the local hand field.
        x -> red
        y -> green
        diagonal mix -> blue
        """
        if w <= 1:
            xr = 0.0
        else:
            xr = xx / float(w - 1)

        if h <= 1:
            yg = 0.0
        else:
            yg = yy / float(h - 1)

        r = int(255 * xr)
        g = int(255 * yg)
        b = int(255 * (0.5 * (1.0 - xr) + 0.5 * yg))

        return (r, g, b)


    def draw_binary_overlay_xycolor_on_field(screen, mask, box):
        if mask is None or box is None:
            return

        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        mh, mw = mask.shape

        if w <= 0 or h <= 0 or mw <= 0 or mh <= 0:
            return

        sx = w / float(mw)
        sy = h / float(mh)

        ys, xs = np.where(mask > 0.5)
        for yy, xx in zip(ys, xs):
            px = x1 + int(xx * sx)
            py = y1 + int(yy * sy)
            if 0 <= px < screen_width and 0 <= py < screen_height:
                screen.set_at((px, py), xy_field_color(xx, yy, mw, mh))




    def thin_cluster_mask(mask, step=2):
        """
        Reduce density by keeping only every Nth pixel in x and y.
        step=2 keeps about 1/4
        step=3 keeps about 1/9
        """
        if mask is None:
            return None

        out = np.zeros_like(mask, dtype=np.float32)
        out[::step, ::step] = mask[::step, ::step]
        return out




    def sample_perimeter_neighborhood_colors(field, perimeter_mask, radius=2):
        """
        field: (W,H,3)
        perimeter_mask: (H,W)

        returns list of RGB samples near perimeter pixels
        """
        if field is None or perimeter_mask is None:
            return []

        img = np.transpose(field, (1, 0, 2)).astype(np.float32)  # (H,W,3)
        h, w = perimeter_mask.shape

        ys, xs = np.where(perimeter_mask > 0.5)
        colors = []

        for yy, xx in zip(ys, xs):
            y1 = max(0, yy - radius)
            y2 = min(h, yy + radius + 1)
            x1 = max(0, xx - radius)
            x2 = min(w, xx + radius + 1)

            patch = img[y1:y2, x1:x2]
            if patch.size == 0:
                continue

            c = patch.reshape(-1, 3).mean(axis=0)
            colors.append(c)

        return colors


    def pick_most_distinct_colors(colors, k=5, min_dist=60.0):
        """
        Greedy distinct-color picker.
        """
        if not colors:
            return []

        arr = np.array(colors, dtype=np.float32)

        # start from mean-brightness spread
        brightness = arr.mean(axis=1)
        order = np.argsort(brightness)

        chosen = [arr[order[len(order) // 2]]]

        while len(chosen) < k:
            best_i = -1
            best_d = -1.0

            for i in range(len(arr)):
                c = arr[i]
                d = min(np.linalg.norm(c - cc) for cc in chosen)
                if d > best_d:
                    best_d = d
                    best_i = i

            if best_i < 0 or best_d < min_dist:
                break

            chosen.append(arr[best_i])

        return [np.clip(c, 0, 255).astype(np.uint8) for c in chosen]


    def color_presence_on_perimeter(field, perimeter_mask, target_color, color_tol=50.0, radius=2):
        """
        Count how much a target color appears near the perimeter.
        """
        if field is None or perimeter_mask is None:
            return 0.0

        img = np.transpose(field, (1, 0, 2)).astype(np.float32)
        h, w = perimeter_mask.shape

        ys, xs = np.where(perimeter_mask > 0.5)
        score = 0.0

        for yy, xx in zip(ys, xs):
            y1 = max(0, yy - radius)
            y2 = min(h, yy + radius + 1)
            x1 = max(0, xx - radius)
            x2 = min(w, xx + radius + 1)

            patch = img[y1:y2, x1:x2]
            if patch.size == 0:
                continue

            mean_c = patch.reshape(-1, 3).mean(axis=0)
            dist = np.linalg.norm(mean_c - target_color.astype(np.float32))

            if dist <= color_tol:
                score += 1.0

        return score


    def draw_distinct_color_squares(screen, colors, box, square_size=18, gap=4):
        """
        Draw little color squares above the hand box.
        """
        if not colors or box is None:
            return

        x1, y1, x2, y2 = box
        start_x = x1
        start_y = max(0, y1 - square_size - 6)

        for i, c in enumerate(colors):
            rx = start_x + i * (square_size + gap)
            ry = start_y
            rect = pygame.Rect(rx, ry, square_size, square_size)
            pygame.draw.rect(screen, tuple(int(v) for v in c), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)



    def perimeter_xy_colors(perimeter_mask):
        """
        Returns:
          colors: list of RGB colors from the perimeter grid coloring
          points: matching (x,y) positions in local field coords
        """
        if perimeter_mask is None:
            return [], []

        h, w = perimeter_mask.shape
        ys, xs = np.where(perimeter_mask > 0.5)

        colors = []
        points = []

        for yy, xx in zip(ys, xs):
            colors.append(np.array(xy_field_color(xx, yy, w, h), dtype=np.float32))
            points.append((xx, yy))

        return colors, points


    def pick_structured_perimeter_xy_colors(colors, points, mask_shape,
                                            edge_margin=12,
                                            top_margin=10,
                                            color_min_dist=35.0):
        """
        Pick 5 perimeter color points in this order:
          1 left-most
          3 top-most
          1 right-most

        Reject points too close to the outer field edges.
        """
        if not colors or not points:
            return [], []

        h, w = mask_shape

        # keep only safe interior points
        valid = []
        for c, (x, y) in zip(colors, points):
            if x < edge_margin or x > (w - 1 - edge_margin):
                continue
            if y < top_margin:
                continue
            valid.append((c, (x, y)))

        if not valid:
            return [], []

        chosen = []

        def far_enough(new_c):
            if not chosen:
                return True
            return min(np.linalg.norm(new_c - old_c) for old_c, _ in chosen) >= color_min_dist

        # 1) left-most
        left_candidates = sorted(valid, key=lambda t: (t[1][0], t[1][1]))
        for c, p in left_candidates:
            if far_enough(c):
                chosen.append((c, p))
                break

        # 2) three top-most, but not too close in x to already chosen
        top_candidates = sorted(valid, key=lambda t: (t[1][1], t[1][0]))
        for c, p in top_candidates:
            if len(chosen) >= 4:
                break

            if not far_enough(c):
                continue

            px = p[0]
            too_close_x = False
            for _, q in chosen:
                if abs(px - q[0]) < max(12, w // 10):
                    too_close_x = True
                    break

            if not too_close_x:
                chosen.append((c, p))

        # 3) right-most
        right_candidates = sorted(valid, key=lambda t: (-t[1][0], t[1][1]))
        for c, p in right_candidates:
            if len(chosen) >= 5:
                break
            if far_enough(c):
                px = p[0]
                too_close_x = False
                for _, q in chosen:
                    if abs(px - q[0]) < max(12, w // 10):
                        too_close_x = True
                        break
                if not too_close_x:
                    chosen.append((c, p))
                    break

        # fallback: fill any missing slots with best remaining top candidates
        if len(chosen) < 5:
            for c, p in top_candidates:
                if len(chosen) >= 5:
                    break
                if not far_enough(c):
                    continue
                px = p[0]
                too_close_x = False
                for _, q in chosen:
                    if abs(px - q[0]) < max(10, w // 12):
                        too_close_x = True
                        break
                if not too_close_x:
                    chosen.append((c, p))

        chosen_colors = [np.clip(c, 0, 255).astype(np.uint8) for c, _ in chosen]
        chosen_points = [p for _, p in chosen]

        return chosen_colors, chosen_points




    def draw_color_squares_at_points(screen, colors, points, box, mask_shape, square_size=14):
        """
        Draw little squares at the representative perimeter locations.
        """
        if not colors or not points or box is None:
            return

        x1, y1, x2, y2 = box
        h, w = mask_shape
        sx = (x2 - x1) / float(w)
        sy = (y2 - y1) / float(h)

        for c, (px, py) in zip(colors, points):
            sxp = x1 + int(px * sx)
            syp = y1 + int(py * sy)

            rect = pygame.Rect(
                sxp - square_size // 2,
                syp - square_size // 2,
                square_size,
                square_size
            )
            pygame.draw.rect(screen, tuple(int(v) for v in c), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)


    def init_finger_orbit_anchors(mask_shape, edge_margin=12, top_margin=10, bottom_margin=12):
        h, w = mask_shape

        # outer top vertices
        top_left = np.array([edge_margin, top_margin], dtype=np.float32)
        top_mid = np.array([w * 0.50, top_margin], dtype=np.float32)
        top_right = np.array([w - 1 - edge_margin, top_margin], dtype=np.float32)

        # center-ish reference points for inward pull
        center = np.array([w * 0.50, h * 0.36], dtype=np.float32)
        left_center = np.array([w * 0.30, h * 0.40], dtype=np.float32)
        right_center = np.array([w * 0.70, h * 0.40], dtype=np.float32)

        # 1/4 of the way from vertex toward interior reference
        ring_up = top_left + 0.25 * (left_center - top_left)
        index_up = top_right + 0.25 * (right_center - top_right)

        return {
            "pinky": {
                "up": (int(w * 0.18), int(h * 0.18)),
                "down": (int(w * 0.16), int(h * 0.52)),
            },
            "ring": {
                "up": (int(ring_up[0]), int(ring_up[1])),
                "down": (int(w * 0.30), int(h * 0.40)),
            },
            "middle": {
                "up": (int(top_mid[0]), int(h * 0.10)),
                "down": (int(w * 0.50), int(h * 0.36)),
            },
            "index": {
                "up": (int(index_up[0]), int(index_up[1])),
                "down": (int(w * 0.68), int(h * 0.40)),
            },
            "thumb": {
                "up": (int(w * 0.84), int(h * 0.50)),
                "down": (int(w * 0.78), int(h * 0.72)),
            },
        }


    def init_tracked_squares():
        return {
            "pinky": {"color": None, "point": None, "strength": 0.0, "misses": 0, "state": "down"},
            "ring": {"color": None, "point": None, "strength": 0.0, "misses": 0, "state": "down"},
            "middle": {"color": None, "point": None, "strength": 0.0, "misses": 0, "state": "down"},
            "index": {"color": None, "point": None, "strength": 0.0, "misses": 0, "state": "down"},
            "thumb": {"color": None, "point": None, "strength": 0.0, "misses": 0, "state": "down"},
        }


    def point_distance(p1, p2):
        if p1 is None or p2 is None:
            return 9999.0
        dx = float(p1[0] - p2[0])
        dy = float(p1[1] - p2[1])
        return float((dx * dx + dy * dy) ** 0.5)


    def color_distance(c1, c2):
        if c1 is None or c2 is None:
            return 9999.0
        c1 = np.array(c1, dtype=np.float32)
        c2 = np.array(c2, dtype=np.float32)
        return float(np.linalg.norm(c1 - c2))


    def finger_candidate_score(candidate_color, candidate_point, mem, anchors):
        up_d = point_distance(candidate_point, anchors["up"])
        down_d = point_distance(candidate_point, anchors["down"])

        if mem["point"] is None:
            mem_d = min(up_d, down_d)
        else:
            mem_d = point_distance(candidate_point, mem["point"])

        if mem["color"] is None:
            col_d = 0.0
        else:
            col_d = color_distance(candidate_color, mem["color"])

        # Let both orbit endpoints participate
        orbit_d = min(up_d, down_d)

        return 1.1 * orbit_d + 0.9 * mem_d + 1.0 * col_d, up_d, down_d


    def finger_order_ok(name, candidate_point, chosen_points):
        x = candidate_point[0]

        if name == "pinky":
            return True
        if name == "ring":
            return chosen_points["pinky"] is None or x > chosen_points["pinky"][0]
        if name == "middle":
            return chosen_points["ring"] is None or x > chosen_points["ring"][0]
        if name == "index":
            return chosen_points["middle"] is None or x > chosen_points["middle"][0]
        if name == "thumb":
            return chosen_points["index"] is None or x > chosen_points["index"][0]

        return True


    def hand_present(mask, min_pixels=1200):
        """
        True only when enough hand-region pixels are present.
        """
        if mask is None:
            return False
        return int(np.sum(mask > 0.5)) >= min_pixels


    def extract_clusters(mask, min_size=6):
        """
        Returns a list of clusters:
          {
            "coords": [(y,x), ...],
            "size": int,
            "mask": (H,W) float32,
            "centroid": (x,y)
          }
        """
        if mask is None:
            return []

        on = mask > 0.5
        h, w = on.shape
        visited = np.zeros((h, w), dtype=bool)

        clusters = []

        for y in range(h):
            for x in range(w):
                if not on[y, x] or visited[y, x]:
                    continue

                stack = [(y, x)]
                visited[y, x] = True
                coords = []

                while stack:
                    cy, cx = stack.pop()
                    coords.append((cy, cx))

                    for ny, nx in (
                            (cy - 1, cx), (cy + 1, cx),
                            (cy, cx - 1), (cy, cx + 1),
                            (cy - 1, cx - 1), (cy - 1, cx + 1),
                            (cy + 1, cx - 1), (cy + 1, cx + 1),
                    ):
                        if 0 <= ny < h and 0 <= nx < w and on[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))

                if len(coords) < min_size:
                    continue

                out = np.zeros((h, w), dtype=np.float32)
                xs = []
                ys = []

                for cy, cx in coords:
                    out[cy, cx] = 1.0
                    xs.append(cx)
                    ys.append(cy)

                centroid = (float(np.mean(xs)), float(np.mean(ys)))

                clusters.append({
                    "coords": coords,
                    "size": len(coords),
                    "mask": out,
                    "centroid": centroid,
                })

        return clusters


    def score_shadow_clusters_with_proximity(clusters, prev_shadow_mask=None, reference_point=None,
                                             proximity_scale=40.0):
        """
        Score clusters by:
          - size
          - recency (overlap with previous shadow)
          - proximity to a reference point

        Higher score is better.
        """
        if not clusters:
            return []

        max_size = max(c["size"] for c in clusters)

        scored = []
        for c in clusters:
            size_norm = c["size"] / float(max_size)

            if prev_shadow_mask is None or prev_shadow_mask.shape != c["mask"].shape:
                recency = 0.0
            else:
                overlap = np.sum((c["mask"] > 0.5) & (prev_shadow_mask > 0.08))
                recency = overlap / float(max(1, c["size"]))

            if reference_point is None:
                proximity = 0.0
            else:
                d = point_distance(c["centroid"], reference_point)
                proximity = max(0.0, 1.0 - d / float(proximity_scale))

            score = (
                    1.2 * size_norm +
                    1.8 * recency +
                    1.6 * proximity
            )

            cc = dict(c)
            cc["score"] = float(score)
            cc["size_norm"] = float(size_norm)
            cc["recency"] = float(recency)
            cc["proximity"] = float(proximity)
            scored.append(cc)

        scored.sort(key=lambda c: c["score"], reverse=True)
        return scored


    def top_shadow_cluster_mask(scored_clusters, keep_n=1):
        if not scored_clusters:
            return None

        h, w = scored_clusters[0]["mask"].shape
        out = np.zeros((h, w), dtype=np.float32)

        for c in scored_clusters[:keep_n]:
            out = np.maximum(out, c["mask"])

        return out


    def best_cluster_for_point(clusters, prev_shadow_mask, reference_point, proximity_scale=40.0):
        scored = score_shadow_clusters_with_proximity(
            clusters,
            prev_shadow_mask=prev_shadow_mask,
            reference_point=reference_point,
            proximity_scale=proximity_scale
        )
        if not scored:
            return None
        return scored[0]


    def mask_perimeter(mask):
        """
        Return the outer perimeter of a binary mask.
        mask is (H,W) float or bool.
        """
        if mask is None:
            return None

        m = mask > 0.5

        up = np.zeros_like(m, dtype=bool)
        down = np.zeros_like(m, dtype=bool)
        left = np.zeros_like(m, dtype=bool)
        right = np.zeros_like(m, dtype=bool)

        up[1:, :] = m[:-1, :]
        down[:-1, :] = m[1:, :]
        left[:, 1:] = m[:, :-1]
        right[:, :-1] = m[:, 1:]

        perimeter = m & (~up | ~down | ~left | ~right)
        return perimeter.astype(np.float32)




### cave_table ###

note = ' '
# chord build-out
chord_intervals = [0, 4, 7, 12]

# amplitudes per voice
voice_amps = [0.22, 0.12, 0.16, 0.10]

# pan positions: 1=center, 4=outer sides
voice_pans = [0.50, 0.35, 0.65, 0.85]

# optional mirrored outer version if you want both left/right sides explicitly
voice_pans_left  = [0.50, 0.35, 0.22, 0.15]
voice_pans_right = [0.50, 0.65, 0.78, 0.85]

# smoothing
water_smooth_passes = 12
rainbow_smooth_passes = 10
audio_smooth_passes = 2

# envelopes
attack_ms = 12
release_ms = 120

# echo / reverb
fx_on = 1
echo_mix = 0.16
echo_feedback = 0.28
echo_delay_ms = 140

reverb_mix = 0.18
reverb_decay = 0.42
reverb_delays_ms = [31, 47, 73, 109]






hello_please_thank_you = 1

if hello_please_thank_you == 1:




    def build_swell_envelope(n, peak_pos=0.38, swell_curve=1.8, tail_curve=1.4):
        """
        Slow bloom up to peak, then long curved release.
        Returns float32 envelope in [0,1].
        """
        if n <= 1:
            return np.ones(max(1, n), dtype=np.float32)

        peak_idx = int(np.clip(peak_pos, 0.05, 0.95) * n)
        peak_idx = max(1, min(n - 1, peak_idx))

        env = np.zeros(n, dtype=np.float32)

        # swell up
        up = np.linspace(0.0, 1.0, peak_idx, endpoint=False, dtype=np.float32)
        env[:peak_idx] = up ** swell_curve

        # tail down
        down_len = n - peak_idx
        down = np.linspace(1.0, 0.0, down_len, endpoint=True, dtype=np.float32)
        env[peak_idx:] = down ** tail_curve

        return env


    def lerp(a, b, t):
        return a + (b - a) * t


    def stepped_smooth_from_env(env, smooth_start, smooth_end, steps=4):
        """
        Build a per-sample smoothness control from the envelope.
        High env -> smoother front, low env -> rougher tail.
        """
        # invert so tail gets less smooth
        inv = 1.0 - env
        raw = lerp(float(smooth_start), float(smooth_end), inv)
        return np.clip(np.round(raw), min(smooth_start, smooth_end), max(smooth_start, smooth_end)).astype(np.int32)


    def build_segmented_wavetable_audio(freq, table_builder, field, n, sample_rate,
                                        smooth_start, smooth_end,
                                        segment_len=2048):
        """
        Rebuild wavetable in segments so smoothness can change over the note.
        """
        mono = np.zeros(n, dtype=np.float32)
        phase0 = 0.0
        i = 0

        while i < n:
            j = min(n, i + segment_len)
            tpos = i / float(max(1, n - 1))
            smooth_passes = int(round(lerp(smooth_start, smooth_end, tpos)))

            table = table_builder(field, smooth_passes=smooth_passes)
            seg_n = j - i

            phase = (phase0 + (np.arange(seg_n, dtype=np.float32) * freq / sample_rate)) % 1.0
            idx = (phase * len(table)).astype(np.int32) % len(table)
            mono[i:j] = table[idx]

            phase0 = float((phase[-1] + freq / sample_rate) % 1.0)
            i = j

        return mono


    def apply_dynamic_fx_chain(stereo_i16, env, sample_rate=44100):
        """
        More wetness as the note decays.
        """
        if stereo_i16 is None:
            return None

        x = stereo_i16.astype(np.float32)

        echo_wet = apply_echo_stereo(
            stereo_i16,
            sample_rate=sample_rate,
            delay_ms=echo_delay_ms,
            mix=1.0,
            feedback=echo_feedback
        ).astype(np.float32)

        reverb_wet = apply_reverb_stereo(
            stereo_i16,
            sample_rate=sample_rate,
            mix=1.0,
            decay=reverb_decay,
            delays_ms=reverb_delays_ms
        ).astype(np.float32)

        # tail gets wetter
        inv = 1.0 - env
        echo_mix_curve = lerp(echo_mix_start, echo_mix_end, inv).reshape(-1, 1)
        reverb_mix_curve = lerp(reverb_mix_start, reverb_mix_end, inv).reshape(-1, 1)

        y = x * (1.0 - echo_mix_curve) + echo_wet * echo_mix_curve
        y = y * (1.0 - reverb_mix_curve) + reverb_wet * reverb_mix_curve

        y = np.clip(y, -32767, 32767).astype(np.int16)
        return y



    def smooth_audio_mono(mono, passes=2):
        x = mono.astype(np.float32).copy()
        for _ in range(max(0, passes)):
            x = (np.roll(x, 1) + 2.0 * x + np.roll(x, -1)) / 4.0
        return x


    def apply_echo_stereo(stereo_i16, sample_rate=44100, delay_ms=140, mix=0.16, feedback=0.28):
        if stereo_i16 is None:
            return None

        x = stereo_i16.astype(np.float32).copy()
        y = x.copy()

        delay = max(1, int(sample_rate * delay_ms / 1000.0))
        if delay >= len(x):
            return stereo_i16

        echo = np.zeros_like(x, dtype=np.float32)
        echo[delay:] = x[:-delay] * feedback

        y = x * (1.0 - mix) + echo * mix
        y = np.clip(y, -32767, 32767).astype(np.int16)
        return y


    def apply_reverb_stereo(stereo_i16, sample_rate=44100, mix=0.18, decay=0.42, delays_ms=(31, 47, 73, 109)):
        if stereo_i16 is None:
            return None

        x = stereo_i16.astype(np.float32).copy()
        wet = np.zeros_like(x, dtype=np.float32)

        for i, d_ms in enumerate(delays_ms):
            delay_samples = max(1, int(sample_rate * d_ms / 1000.0))
            if delay_samples >= len(x):
                continue
            gain = decay ** (i + 1)
            wet[delay_samples:] += x[:-delay_samples] * gain

        y = x * (1.0 - mix) + wet * mix
        y = np.clip(y, -32767, 32767).astype(np.int16)
        return y


    def apply_fx_chain(stereo_i16, sample_rate=44100):
        if stereo_i16 is None:
            return None

        y = stereo_i16

        if fx_on == 1:
            y = apply_echo_stereo(
                y,
                sample_rate=sample_rate,
                delay_ms=echo_delay_ms,
                mix=echo_mix,
                feedback=echo_feedback
            )

            y = apply_reverb_stereo(
                y,
                sample_rate=sample_rate,
                mix=reverb_mix,
                decay=reverb_decay,
                delays_ms=reverb_delays_ms
            )

        return y







    def build_ca_wavetable(water_field, base=2, table_size=2048, smooth_passes=8):
        arr = np.asarray(water_field, dtype=np.float32)
        flat = arr.flatten()

        if flat.size == 0:
            return np.zeros(table_size, dtype=np.float32)

        # normalize CA states into [-1, 1]
        if base <= 1:
            wave = np.zeros_like(flat, dtype=np.float32)
        else:
            wave = (flat / float(base - 1)) * 2.0 - 1.0

        # remove DC
        wave = wave - np.mean(wave)

        peak = np.max(np.abs(wave))
        if peak < 1e-6:
            wave = np.zeros_like(wave, dtype=np.float32)
            wave[0] = 1.0
        else:
            wave = wave / peak

        # smooth raw source circularly
        for _ in range(max(0, smooth_passes // 2)):
            wave = (np.roll(wave, 1) + 2.0 * wave + np.roll(wave, -1)) / 4.0

        # resample to fixed table
        src_x = np.linspace(0.0, 1.0, num=wave.size, endpoint=False)
        dst_x = np.linspace(0.0, 1.0, num=table_size, endpoint=False)
        table = np.interp(dst_x, src_x, wave).astype(np.float32)

        # smooth again after resampling
        for _ in range(max(0, smooth_passes)):
            table = (np.roll(table, 1) + 2.0 * table + np.roll(table, -1)) / 4.0

        # remove DC again
        table = table - np.mean(table)

        peak = np.max(np.abs(table))
        if peak > 1e-6:
            table = table / peak

        return table


    def ca_tone_from_note(sign, water_field, digibet, *,
                          base=2,
                          sample_rate=44100,
                          duration=0.35,
                          amp=0.25,
                          midi_base_hz=55.0,
                          note_offset=12):
        """
        sign -> digibet value controls pitch
        CA field controls waveform shape
        """
        if sign not in digibet:
            return None

        sign_value = digibet[sign] -1

        if sign_value == -1:
            return None

        # pitch from digibet value
        semitone = note_offset + sign_value
        freq = midi_base_hz * (2.0 ** (semitone / 12.0))

        table = build_ca_wavetable(water_field, base=base, table_size=2048)
        n = int(sample_rate * duration)

        # phase accumulation through the wavetable
        phase = (np.arange(n, dtype=np.float32) * freq / sample_rate) % 1.0
        idx = (phase * len(table)).astype(np.int32) % len(table)
        mono = table[idx]

        # short envelope to avoid clicks
        attack = max(1, int(0.01 * sample_rate))
        release = max(1, int(0.05 * sample_rate))
        env = np.ones(n, dtype=np.float32)
        env[:attack] = np.linspace(0.0, 1.0, attack, endpoint=False)
        env[-release:] = np.linspace(1.0, 0.0, release, endpoint=True)

        mono = mono * env * amp

        # int16 stereo for pygame
        mono_i16 = np.clip(mono * 32767.0, -32767, 32767).astype(np.int16)
        stereo = np.repeat(mono_i16.reshape(-1, 1), 2, axis=1)

        return pygame.sndarray.make_sound(stereo)



    def build_rainbow_wavetable(rainbow_field, color_max=2048, table_size=2048, smooth_passes=6):
        arr = np.asarray(rainbow_field, dtype=np.float32)
        flat = arr.flatten()

        if flat.size == 0:
            return np.zeros(table_size, dtype=np.float32)

        # normalize rainbow values into [-1, 1]
        wave = (flat / float(color_max - 1)) * 2.0 - 1.0

        # remove DC
        wave = wave - np.mean(wave)

        peak = np.max(np.abs(wave))
        if peak < 1e-6:
            wave = np.zeros_like(wave, dtype=np.float32)
            wave[0] = 1.0
        else:
            wave = wave / peak

        # smooth raw source
        for _ in range(max(0, smooth_passes // 2)):
            wave = (np.roll(wave, 1) + 2.0 * wave + np.roll(wave, -1)) / 4.0

        # resample to fixed table
        src_x = np.linspace(0.0, 1.0, num=wave.size, endpoint=False)
        dst_x = np.linspace(0.0, 1.0, num=table_size, endpoint=False)
        table = np.interp(dst_x, src_x, wave).astype(np.float32)

        # smooth again
        for _ in range(max(0, smooth_passes)):
            table = (np.roll(table, 1) + 2.0 * table + np.roll(table, -1)) / 4.0

        table = table - np.mean(table)
        peak = np.max(np.abs(table))
        if peak > 1e-6:
            table = table / peak

        return table




    def rainbow_tone_from_note(sign, rainbow_field, digibet, *,
                               color_max=2048,
                               sample_rate=44100,
                               duration=0.35,
                               amp=0.18,
                               midi_base_hz=55.0,
                               note_offset=24,
                               octave_shift=0,
                               harmony_offset=0,
                               pitch_detune=0.0,
                               pan=0.8):
        if sign not in digibet:
            return None

        sign_value = digibet[sign] - 1
        if sign_value == -1:
            return None

        semitone = note_offset + sign_value + (octave_shift * 12) + harmony_offset
        freq = midi_base_hz * (2.0 ** (semitone / 12.0))

        # optional slight detune for side shimmer
        freq *= (2.0 ** (pitch_detune / 12.0))

        table = build_rainbow_wavetable(rainbow_field, color_max=color_max, table_size=2048)
        n = int(sample_rate * duration)

        phase = (np.arange(n, dtype=np.float32) * freq / sample_rate) % 1.0
        idx = (phase * len(table)).astype(np.int32) % len(table)
        mono = table[idx]

        # envelope
        attack = max(1, int(0.01 * sample_rate))
        release = max(1, int(0.08 * sample_rate))
        env = np.ones(n, dtype=np.float32)
        env[:attack] = np.linspace(0.0, 1.0, attack, endpoint=False)
        env[-release:] = np.linspace(1.0, 0.0, release, endpoint=True)

        mono = mono * env * amp

        # pan outward
        pan = float(np.clip(pan, 0.0, 1.0))
        left_gain = np.sqrt(1.0 - pan)
        right_gain = np.sqrt(pan)

        left = np.clip(mono * left_gain * 32767.0, -32767, 32767).astype(np.int16)
        right = np.clip(mono * right_gain * 32767.0, -32767, 32767).astype(np.int16)

        stereo = np.column_stack((left, right))
        return pygame.sndarray.make_sound(stereo)


    base_hz = 55.0
    note_offset = 0


    def ca_tone_from_note(sign, water_field, digibet, *,
                          base=2,
                          sample_rate=44100,
                          duration=0.35,
                          amp=0.25,
                          midi_base_hz=55.0,
                          note_offset=0,
                          octave_shift=0,
                          harmony_offset=0,
                          pan=0.5):
        if sign not in digibet:
            return None

        sign_value = digibet[sign] - 1
        if sign_value == -1:
            return None

        semitone = note_offset + sign_value + (octave_shift * 12) + harmony_offset
        freq = midi_base_hz * (2.0 ** (semitone / 12.0))

        table = build_ca_wavetable(water_field, base=base, table_size=2048)
        n = int(sample_rate * duration)

        phase = (np.arange(n, dtype=np.float32) * freq / sample_rate) % 1.0
        idx = (phase * len(table)).astype(np.int32) % len(table)
        mono = table[idx]

        attack = max(1, int(0.01 * sample_rate))
        release = max(1, int(0.05 * sample_rate))
        env = np.ones(n, dtype=np.float32)
        env[:attack] = np.linspace(0.0, 1.0, attack, endpoint=False)
        env[-release:] = np.linspace(1.0, 0.0, release, endpoint=True)

        mono = mono * env * amp

        pan = float(np.clip(pan, 0.0, 1.0))
        left_gain = np.sqrt(1.0 - pan)
        right_gain = np.sqrt(pan)

        left = np.clip(mono * left_gain * 32767.0, -32767, 32767).astype(np.int16)
        right = np.clip(mono * right_gain * 32767.0, -32767, 32767).astype(np.int16)

        stereo = np.column_stack((left, right))
        return pygame.sndarray.make_sound(stereo)





    def play_water_rainbow_chord(sign, water_field, rainbow_field):
        if sign not in digibet or digibet[sign] == 0:
            return

        voices = [
            ("water",   0, 0.14, 0.47, -0.01),
            ("water",   0, 0.14, 0.53,  0.01),

            ("rainbow", 4, 0.08, 0.35, -0.03),
            ("rainbow", 4, 0.08, 0.65,  0.03),

            ("water",   7, 0.10, 0.22, -0.01),
            ("water",   7, 0.10, 0.78,  0.01),

            ("rainbow", 12, 0.06, 0.15, -0.04),
            ("rainbow", 12, 0.06, 0.85,  0.04),
        ]

        for source, interval, amp, pan, detune in voices:
            if source == "water":
                snd = ca_tone_from_note(
                    sign,
                    water_field,
                    digibet,
                    base=base,
                    sample_rate=sample_rate,
                    duration=0.35,
                    amp=amp,
                    midi_base_hz=base_hz,
                    note_offset=base_note_offset,
                    octave_shift=octave_shift,
                    harmony_offset=interval,
                    pan=pan
                )
            else:
                snd = rainbow_tone_from_note(
                    sign,
                    rainbow_field,
                    digibet,
                    color_max=color_max,
                    sample_rate=sample_rate,
                    duration=0.35,
                    amp=amp,
                    midi_base_hz=base_hz,
                    note_offset=base_note_offset,
                    octave_shift=octave_shift,
                    harmony_offset=interval,
                    pitch_detune=detune,
                    pan=pan
                )

            if snd is not None:
                snd.play()





    def build_ca_wavetable(water_field, base=2, table_size=2048, smooth_passes=None):
        if smooth_passes is None:
            smooth_passes = water_smooth_passes

        arr = np.asarray(water_field, dtype=np.float32)
        flat = arr.flatten()

        if flat.size == 0:
            return np.zeros(table_size, dtype=np.float32)

        if base <= 1:
            wave = np.zeros_like(flat, dtype=np.float32)
        else:
            wave = (flat / float(base - 1)) * 2.0 - 1.0

        wave = wave - np.mean(wave)

        peak = np.max(np.abs(wave))
        if peak < 1e-6:
            wave = np.zeros_like(wave, dtype=np.float32)
            wave[0] = 1.0
        else:
            wave = wave / peak

        for _ in range(max(0, smooth_passes // 2)):
            wave = (np.roll(wave, 1) + 2.0 * wave + np.roll(wave, -1)) / 4.0

        src_x = np.linspace(0.0, 1.0, num=wave.size, endpoint=False)
        dst_x = np.linspace(0.0, 1.0, num=table_size, endpoint=False)
        table = np.interp(dst_x, src_x, wave).astype(np.float32)

        for _ in range(max(0, smooth_passes)):
            table = (np.roll(table, 1) + 2.0 * table + np.roll(table, -1)) / 4.0

        # soften the wrap point a little
        seam = min(48, len(table) // 8)
        if seam > 1:
            start = table[:seam].copy()
            end = table[-seam:].copy()
            blend = np.linspace(0.0, 1.0, seam, endpoint=False)
            mixed = end * (1.0 - blend) + start * blend
            table[:seam] = mixed
            table[-seam:] = mixed

        table = table - np.mean(table)
        peak = np.max(np.abs(table))
        if peak > 1e-6:
            table = table / peak

        return table




    def build_rainbow_wavetable(rainbow_field, color_max=2048, table_size=2048, smooth_passes=None):
        if smooth_passes is None:
            smooth_passes = rainbow_smooth_passes

        arr = np.asarray(rainbow_field, dtype=np.float32)
        flat = arr.flatten()

        if flat.size == 0:
            return np.zeros(table_size, dtype=np.float32)

        wave = (flat / float(color_max - 1)) * 2.0 - 1.0
        wave = wave - np.mean(wave)

        peak = np.max(np.abs(wave))
        if peak < 1e-6:
            wave = np.zeros_like(wave, dtype=np.float32)
            wave[0] = 1.0
        else:
            wave = wave / peak

        for _ in range(max(0, smooth_passes // 2)):
            wave = (np.roll(wave, 1) + 2.0 * wave + np.roll(wave, -1)) / 4.0

        src_x = np.linspace(0.0, 1.0, num=wave.size, endpoint=False)
        dst_x = np.linspace(0.0, 1.0, num=table_size, endpoint=False)
        table = np.interp(dst_x, src_x, wave).astype(np.float32)

        for _ in range(max(0, smooth_passes)):
            table = (np.roll(table, 1) + 2.0 * table + np.roll(table, -1)) / 4.0

        seam = min(48, len(table) // 8)
        if seam > 1:
            start = table[:seam].copy()
            end = table[-seam:].copy()
            blend = np.linspace(0.0, 1.0, seam, endpoint=False)
            mixed = end * (1.0 - blend) + start * blend
            table[:seam] = mixed
            table[-seam:] = mixed

        table = table - np.mean(table)
        peak = np.max(np.abs(table))
        if peak > 1e-6:
            table = table / peak

        return table








    def ca_tone_from_note_4(sign, water_field, digibet, *,
                          base=2,
                          sample_rate=44100,
                          duration=0.35,
                          amp=0.25,
                          midi_base_hz=55.0,
                          note_offset=0,
                          octave_shift=0,
                          harmony_offset=0,
                          pitch_detune=0.0,
                          pan=0.5):
        if sign not in digibet:
            return None

        sign_value = digibet[sign] - 1
        if sign_value == -1:
            return None

        semitone = note_offset + sign_value + (octave_shift * 12) + harmony_offset
        freq = midi_base_hz * (2.0 ** (semitone / 12.0))
        freq *= (2.0 ** (pitch_detune / 12.0))

        table = build_ca_wavetable(water_field, base=base, table_size=2048)
        n = int(sample_rate * duration)

        phase = (np.arange(n, dtype=np.float32) * freq / sample_rate) % 1.0
        idx = (phase * len(table)).astype(np.int32) % len(table)
        mono = table[idx]

        mono = smooth_audio_mono(mono, passes=audio_smooth_passes)

        attack = max(1, int((attack_ms / 1000.0) * sample_rate))
        release = max(1, int((release_ms / 1000.0) * sample_rate))
        env = np.ones(n, dtype=np.float32)
        env[:attack] = np.linspace(0.0, 1.0, attack, endpoint=False)
        env[-release:] = np.linspace(1.0, 0.0, release, endpoint=True)

        mono = mono * env * amp

        pan = float(np.clip(pan, 0.0, 1.0))
        left_gain = np.sqrt(1.0 - pan)
        right_gain = np.sqrt(pan)

        left = np.clip(mono * left_gain * 32767.0, -32767, 32767).astype(np.int16)
        right = np.clip(mono * right_gain * 32767.0, -32767, 32767).astype(np.int16)

        stereo = np.column_stack((left, right))
        stereo = apply_fx_chain(stereo, sample_rate=sample_rate)

        return pygame.sndarray.make_sound(stereo)




    def rainbow_tone_from_note_4(sign, rainbow_field, digibet, *,
                               color_max=2048,
                               sample_rate=44100,
                               duration=0.35,
                               amp=0.18,
                               midi_base_hz=55.0,
                               note_offset=0,
                               octave_shift=0,
                               harmony_offset=0,
                               pitch_detune=0.0,
                               pan=0.8):
        if sign not in digibet:
            return None

        sign_value = digibet[sign] - 1
        if sign_value == -1:
            return None

        semitone = note_offset + sign_value + (octave_shift * 12) + harmony_offset
        freq = midi_base_hz * (2.0 ** (semitone / 12.0))
        freq *= (2.0 ** (pitch_detune / 12.0))

        table = build_rainbow_wavetable(rainbow_field, color_max=color_max, table_size=2048)
        n = int(sample_rate * duration)

        phase = (np.arange(n, dtype=np.float32) * freq / sample_rate) % 1.0
        idx = (phase * len(table)).astype(np.int32) % len(table)
        mono = table[idx]

        mono = smooth_audio_mono(mono, passes=audio_smooth_passes)

        attack = max(1, int((attack_ms / 1000.0) * sample_rate))
        release = max(1, int((release_ms / 1000.0) * sample_rate))
        env = np.ones(n, dtype=np.float32)
        env[:attack] = np.linspace(0.0, 1.0, attack, endpoint=False)
        env[-release:] = np.linspace(1.0, 0.0, release, endpoint=True)

        mono = mono * env * amp

        pan = float(np.clip(pan, 0.0, 1.0))
        left_gain = np.sqrt(1.0 - pan)
        right_gain = np.sqrt(pan)

        left = np.clip(mono * left_gain * 32767.0, -32767, 32767).astype(np.int16)
        right = np.clip(mono * right_gain * 32767.0, -32767, 32767).astype(np.int16)

        stereo = np.column_stack((left, right))
        stereo = apply_fx_chain(stereo, sample_rate=sample_rate)

        return pygame.sndarray.make_sound(stereo)









    # note shape
    note_duration = .7

    # swell envelope
    swell_peak_pos = .01     # where the note reaches max body, 0..1
    swell_curve = 1        # larger = more dramatic swell
    tail_curve = 1          # release shape

    # dynamic smoothness
    water_smooth_start = 10
    water_smooth_end = 1

    rainbow_smooth_start = 14
    rainbow_smooth_end = 1

    # dynamic fx
    echo_mix_start = 0.16
    echo_mix_end = 0.32

    reverb_mix_start = 0.16
    reverb_mix_end = 0.32




    def ca_tone_from_note(sign, water_field, digibet, *,
                          base=2,
                          sample_rate=44100,
                          duration=0.85,
                          amp=0.25,
                          midi_base_hz=55.0,
                          note_offset=0,
                          octave_shift=0,
                          harmony_offset=0,
                          pitch_detune=0.0,
                          pan=0.5):
        if sign not in digibet:
            return None

        sign_value = digibet[sign] - 1
        if sign_value == -1:
            return None

        semitone = note_offset + sign_value + (octave_shift * 12) + harmony_offset
        freq = midi_base_hz * (2.0 ** (semitone / 12.0))
        freq *= (2.0 ** (pitch_detune / 12.0))

        n = int(sample_rate * duration)

        mono = build_segmented_wavetable_audio(
            freq,
            lambda field, smooth_passes: build_ca_wavetable(
                field, base=base, table_size=2048, smooth_passes=smooth_passes
            ),
            water_field,
            n,
            sample_rate,
            smooth_start=water_smooth_start,
            smooth_end=water_smooth_end,
            segment_len=2048
        )

        mono = smooth_audio_mono(mono, passes=max(0, audio_smooth_passes - 1))

        env = build_swell_envelope(
            n,
            peak_pos=swell_peak_pos,
            swell_curve=swell_curve,
            tail_curve=tail_curve
        )

        mono = mono * env * amp

        pan = float(np.clip(pan, 0.0, 1.0))
        left_gain = np.sqrt(1.0 - pan)
        right_gain = np.sqrt(pan)

        left = np.clip(mono * left_gain * 32767.0, -32767, 32767).astype(np.int16)
        right = np.clip(mono * right_gain * 32767.0, -32767, 32767).astype(np.int16)

        stereo = np.column_stack((left, right))

        if fx_on == 1:
            stereo = apply_dynamic_fx_chain(stereo, env, sample_rate=sample_rate)

        return pygame.sndarray.make_sound(stereo)





    def rainbow_tone_from_note(sign, rainbow_field, digibet, *,
                               color_max=2048,
                               sample_rate=44100,
                               duration=0.85,
                               amp=0.18,
                               midi_base_hz=55.0,
                               note_offset=0,
                               octave_shift=0,
                               harmony_offset=0,
                               pitch_detune=0.0,
                               pan=0.8):
        if sign not in digibet:
            return None

        sign_value = digibet[sign] - 1
        if sign_value == -1:
            return None

        semitone = note_offset + sign_value + (octave_shift * 12) + harmony_offset
        freq = midi_base_hz * (2.0 ** (semitone / 12.0))
        freq *= (2.0 ** (pitch_detune / 12.0))

        n = int(sample_rate * duration)

        mono = build_segmented_wavetable_audio(
            freq,
            lambda field, smooth_passes: build_rainbow_wavetable(
                field, color_max=color_max, table_size=2048, smooth_passes=smooth_passes
            ),
            rainbow_field,
            n,
            sample_rate,
            smooth_start=rainbow_smooth_start,
            smooth_end=rainbow_smooth_end,
            segment_len=2048
        )

        mono = smooth_audio_mono(mono, passes=max(0, audio_smooth_passes - 1))

        env = build_swell_envelope(
            n,
            peak_pos=swell_peak_pos,
            swell_curve=swell_curve,
            tail_curve=tail_curve
        )

        mono = mono * env * amp

        pan = float(np.clip(pan, 0.0, 1.0))
        left_gain = np.sqrt(1.0 - pan)
        right_gain = np.sqrt(pan)

        left = np.clip(mono * left_gain * 32767.0, -32767, 32767).astype(np.int16)
        right = np.clip(mono * right_gain * 32767.0, -32767, 32767).astype(np.int16)

        stereo = np.column_stack((left, right))

        if fx_on == 1:
            stereo = apply_dynamic_fx_chain(stereo, env, sample_rate=sample_rate)

        return pygame.sndarray.make_sound(stereo)








digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, 'an': 14, 'er': 15,
           'ou': 16, 'in': 17, 'th': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}
digibetu = {v: k for k, v in digibet.items()}








last_score = 0
#to send





# -----------------------------
# WOW HELD KEY OUTPUT
# -----------------------------

# Try DirectInput-style output first for games.
# Install with: pip install pydirectinput
try:
    import pydirectinput as keyout
    keyout.PAUSE = 0.0
    print("Using pydirectinput for WoW keys")
except ImportError:
    import pyautogui as keyout
    keyout.PAUSE = 0.0
    print("Using pyautogui for WoW keys")

# Map your detected signs to WoW movement keys.
# Change these however you want.
WOW_HOLD_KEYS = {
    "e": ["e"],       # forward
    "w": ["w"],       # strafe left default
    "r": ["r"],       # strafe right default
}

held_keys = set()
last_wow_sign = None


def press_key_down(key):
    global held_keys

    if key not in held_keys:
        try:
            keyout.keyDown(key)
            held_keys.add(key)
            print("KEY DOWN:", key)
        except Exception as e:
            print("keyDown error:", key, e)


def release_key_up(key):
    global held_keys

    if key in held_keys:
        try:
            keyout.keyUp(key)
            held_keys.remove(key)
            print("KEY UP:", key)
        except Exception as e:
            print("keyUp error:", key, e)


def release_all_wow_keys():
    for key in list(held_keys):
        release_key_up(key)


def send_sign_to_keyboard(sign):
    """
    WoW movement mode:
    - movement signs hold keys down
    - changing signs releases old keys
    - neutral/unknown signs release movement
    """
    global last_wow_sign

    if sign == "":
        sign = " "

    # Only update if sign changed.
    if sign == last_wow_sign:
        return

    last_wow_sign = sign

    desired_keys = set(WOW_HOLD_KEYS.get(sign, []))

    # Release keys we no longer want held.
    for key in list(held_keys):
        if key not in desired_keys:
            release_key_up(key)

    # Press new keys.
    for key in desired_keys:
        press_key_down(key)








# -----------------------------
# SIMPLE WOW HOLD OUTPUT
# uses pyautogui because it at least got W recognized once
# -----------------------------

WOW_HOLD_SIGNS = {"e", "w", "r", "z", "x"}

held_keys = set()


def hold_key_down(key):
    if key not in held_keys:
        try:
            pyautogui.keyDown(key)
            held_keys.add(key)
            print("KEY DOWN:", key)
        except Exception as e:
            print("keyDown error:", key, e)


def hold_key_up(key):
    if key in held_keys:
        try:
            pyautogui.keyUp(key)
            held_keys.remove(key)
            print("KEY UP:", key)
        except Exception as e:
            print("keyUp error:", key, e)


def release_all_held_keys():
    for key in list(held_keys):
        hold_key_up(key)


def send_sign_to_keyboard(sign):
    """
    Movement mode:
    - if sign is a hold sign, hold that key down
    - if sign changes, release the old held key
    - if sign becomes neutral/blank, release everything
    """
    if sign == "":
        sign = " "

    # Hold movement keys
    if sign in WOW_HOLD_SIGNS:

        # release other held keys first
        for key in list(held_keys):
            if key != sign:
                hold_key_up(key)

        hold_key_down(sign)
        return

    # Neutral or non-hold sign releases movement
    release_all_held_keys()








held = ''



detect_change = 4

if detect_change == 4:

    state = 1  # finger is on / near / tracked by this button
    state = 0  # finger is gone / button returned to baseline

    DC4_FINGER_NAMES = ["pinky", "ring", "middle", "index", "thumb"]

    DC4_RIGHT_FINGER_NAMES = ["pinky", "ring", "middle", "index", "thumb"]
    DC4_LEFT_FINGER_NAMES = ["pinky", "ring", "middle", "index", "thumb"]

    dc4_buttons = {
        "right": [],
        "left": [],
    }

    DC4_CHANGE_THRESHOLD = 22.0
    DC4_COLOR_MATCH_THRESHOLD = 55.0
    DC4_SEARCH_RADIUS = 80
    DC4_LOCK_FRAMES = 2
    DC4_RELEASE_FRAMES = 5
    DC4_COLOR_LEARN_RATE = 0.08
    DC4_POINT_SMOOTH = 0.35

    DC4_CHANGE_THRESHOLD = 22.0

    # stricter matching
    DC4_COLOR_MATCH_THRESHOLD = 32.0  # was 55. Lower = stricter finger color match
    DC4_BASELINE_REJECT_THRESHOLD = 28.0  # must be this different from empty button/background
    DC4_BRIGHTNESS_MATCH_THRESHOLD = 28.0  # keeps wall highlights from matching skin color
    DC4_RELEASE_CHANGE_THRESHOLD = 10.0  # if button returns near baseline, release
    DC4_MIN_MATCH_PIXELS = 10
    DC4_MAX_POINT_JUMP = 38

    DC4_SEARCH_RADIUS = 45  # was 80. Smaller = less wall grabbing
    DC4_LOCK_FRAMES = 2
    DC4_RELEASE_FRAMES = 3
    DC4_COLOR_LEARN_RATE = 0.03  # was 0.08. Slower = less drift into wall/background
    DC4_POINT_SMOOTH = 0.35

    # visuals
    DC4_COLOR_ON = (255, 0, 0)
    DC4_COLOR_OFF = (255, 255, 255)

    DC4_COLOR_LINE_ACTIVE = (0, 0, 255)
    DC4_COLOR_DOT_ACTIVE = (0, 0, 255)

    DC4_COLOR_LINE_PASSIVE = (0, 0, 128)
    DC4_COLOR_DOT_PASSIVE = (0, 0, 128)

    DC4_COLOR_LANE_CENTER = (80, 80, 180)
    DC4_COLOR_LANE_RAIL = (45, 45, 100)

    DC4_COLOR_TEXT = (255, 255, 255)


    DC4_BUTTON_THICKNESS = 4

    DC4_LINE_THICKNESS_ACTIVE = 4
    DC4_LINE_THICKNESS_PASSIVE = 2

    DC4_DOT_RADIUS_ACTIVE = 4
    DC4_DOT_RADIUS_PASSIVE = 2

    DC4_RESET_LINE_ON_PRESS = 1
    DC4_RELEARN_COLOR_ON_PRESS = 1


    DC4_USE_LANES = 1
    DC4_DRAW_LANES = 1

    DC4_LANE_FORWARD = 128
    DC4_LANE_BACK = 28
    DC4_LANE_WIDTH = 20
    DC4_THUMB_LANE_WIDTH = 28

    DC4_TRACK_MISS_LIMIT = 12

    DC4_COLOR_LANE = (255, 255, 255)
    DC4_LANE_THICKNESS = 1




    def roi_center(roi):
        x1, y1, x2, y2 = roi
        return ((x1 + x2) // 2, (y1 + y2) // 2)


    def mean_rgb(region):
        if region is None or region.size == 0:
            return None
        return region.reshape(-1, 3).mean(axis=0).astype(np.float32)


    def rgb_dist(a, b):
        if a is None or b is None:
            return 9999.0
        return float(np.linalg.norm(np.array(a, dtype=np.float32) - np.array(b, dtype=np.float32)))




    def dc4_norm_vec(v):
        vx, vy = v
        mag = float((vx * vx + vy * vy) ** 0.5)

        if mag <= 1e-6:
            return (0.0, -1.0)

        return (vx / mag, vy / mag)


    def dc4_angle_to_vec(degrees):
        """
        Pygame angle system:
        0   = right
        45  = down-right
        90  = straight down
        135 = down-left
        180 = left
        -90 = up
        """
        rad = np.deg2rad(degrees)
        return dc4_norm_vec((np.cos(rad), np.sin(rad)))


    # Manually tune these.
    # Bigger angle turns lane left.
    # Smaller angle turns lane right.
    DC4_LANE_ANGLES = {
        "right": {
            "pinky": 96,
            "ring": 93,
            "middle": 90,
            "index": 87,
            "thumb": 135,
        },

        # LEFT HAND:
        # pinky is on the left, thumb is on the right.
        "left": {
            "pinky": 84,
            "ring": 87,
            "middle": 90,
            "index": 93,
            "thumb": 135,
        },
    }


    def dc4_lane_vector(hand_name, finger_name):
        angle = DC4_LANE_ANGLES.get(hand_name, {}).get(finger_name, 90)
        return dc4_angle_to_vec(angle)


    def dc4_points_in_lane(
            global_xs,
            global_ys,
            lane_anchor,
            lane_dir,
            lane_width,
            lane_forward,
            lane_back
    ):
        """
        global_xs/global_ys are arrays of candidate pixel positions.
        Keeps only candidates inside a capsule-like finger lane.
        """

        ax, ay = lane_anchor
        vx, vy = dc4_norm_vec(lane_dir)

        dx = global_xs.astype(np.float32) - float(ax)
        dy = global_ys.astype(np.float32) - float(ay)

        # distance along the lane direction
        forward = dx * vx + dy * vy

        # side distance from the lane centerline
        perp = np.abs(dx * (-vy) + dy * vx)

        inside = (
                (forward >= -float(lane_back)) &
                (forward <= float(lane_forward)) &
                (perp <= float(lane_width))
        )

        return inside


    def activate_dc4_button(b, current_color):
        """
        Rising-edge button activation:
        this is where the line resets and color can be relearned.
        """

        b["state"] = 1
        b["tracking"] = 1
        b["misses"] = 0
        b["track_misses"] = 0
        b["candidate_frames"] = 0
        b["press_count"] = b.get("press_count", 0) + 1

        if current_color is not None:
            if DC4_RELEARN_COLOR_ON_PRESS == 1 or b["finger_color"] is None:
                b["finger_color"] = current_color.copy()

        if DC4_RESET_LINE_ON_PRESS == 1:
            b["finger_point"] = b["anchor"]



    def make_dc4_buttons():
        global dc4_buttons

        dc4_buttons = {
            "right": [],
            "left": [],
        }

        # right_roi and left_roi already include 5 finger boxes + 1 palm box.
        # We only want the first 5 finger boxes.
        for hand_name, rois, names in (
                ("right", right_roi[:5], DC4_RIGHT_FINGER_NAMES),
                ("left", left_roi[:5], DC4_LEFT_FINGER_NAMES),
        ):
            for name, roi in zip(names, rois):
                dc4_buttons[hand_name].append({
                    "hand": hand_name,
                    "name": name,
                    "roi": roi,
                    "anchor": roi_center(roi),

                    "baseline_color": None,
                    "finger_color": None,
                    "finger_point": None,

                    "state": 0,
                    "tracking": 0,
                    "candidate_frames": 0,
                    "misses": 0,
                    "track_misses": 0,
                    "press_count": 0,

                    "lane_dir": dc4_lane_vector(hand_name, name),
                    "lane_width": DC4_THUMB_LANE_WIDTH if name == "thumb" else DC4_LANE_WIDTH,
                })

        print("DC4 buttons made")
        print("right:", [b["name"] for b in dc4_buttons["right"]])
        print("left:", [b["name"] for b in dc4_buttons["left"]])



    def calibrate_dc4_buttons(frame):
        for hand_name in ("right", "left"):
            for b in dc4_buttons[hand_name]:
                x1, y1, x2, y2 = b["roi"]
                crop = frame[x1:x2, y1:y2]

                b["baseline_color"] = mean_rgb(crop)
                b["finger_color"] = None
                b["finger_point"] = b["anchor"]
                b["state"] = 0
                b["candidate_frames"] = 0
                b["misses"] = 0

                b["tracking"] = 0
                b["track_misses"] = 0
                b["press_count"] = 0
                b["lane_dir"] = dc4_lane_vector(hand_name, b["name"])
                b["lane_width"] = DC4_THUMB_LANE_WIDTH if b["name"] == "thumb" else DC4_LANE_WIDTH


        print("DC4 finger buttons calibrated")


    def find_finger_color_point(
            frame,
            target_color,
            start_point,
            baseline_color=None,
            search_radius=45,
            color_threshold=32,
            baseline_reject_threshold=28,
            brightness_threshold=28,
            min_pixels=10,
            max_point_jump=38,
            lane_anchor=None,
            lane_dir=None,
            lane_width=34,
            lane_forward=220,
            lane_back=28
    ):
        if target_color is None or start_point is None:
            return None, 0.0

        sx, sy = start_point

        x1 = max(0, int(sx - search_radius))
        x2 = min(screen_width, int(sx + search_radius))
        y1 = max(0, int(sy - search_radius))
        y2 = min(screen_height, int(sy + search_radius))

        field = frame[x1:x2, y1:y2]
        if field.size == 0:
            return None, 0.0

        field_f = field.astype(np.float32)
        target = np.array(target_color, dtype=np.float32)

        diff = field_f - target
        finger_dist = np.sqrt(np.sum(diff * diff, axis=2))

        field_brightness = field_f.mean(axis=2)
        target_brightness = target.mean()
        brightness_diff = np.abs(field_brightness - target_brightness)

        mask = (
                (finger_dist <= color_threshold) &
                (brightness_diff <= brightness_threshold)
        )

        if baseline_color is not None:
            baseline = np.array(baseline_color, dtype=np.float32)
            base_diff = field_f - baseline
            baseline_dist = np.sqrt(np.sum(base_diff * base_diff, axis=2))
            mask = mask & (baseline_dist >= baseline_reject_threshold)

        if np.sum(mask) < min_pixels:
            return None, 0.0

        xs, ys = np.where(mask)

        global_xs = x1 + xs
        global_ys = y1 + ys

        # normal nearby-point guard
        jump_dist = np.sqrt((global_xs - sx) ** 2 + (global_ys - sy) ** 2)
        near = jump_dist <= max_point_jump

        if np.sum(near) < min_pixels:
            return None, 0.0

        xs = xs[near]
        ys = ys[near]
        global_xs = global_xs[near]
        global_ys = global_ys[near]

        # lane guard
        if DC4_USE_LANES == 1 and lane_anchor is not None and lane_dir is not None:
            lane_ok = dc4_points_in_lane(
                global_xs,
                global_ys,
                lane_anchor,
                lane_dir,
                lane_width,
                lane_forward,
                lane_back
            )

            if np.sum(lane_ok) < min_pixels:
                return None, 0.0

            xs = xs[lane_ok]
            ys = ys[lane_ok]

        match_dist = finger_dist[xs, ys]

        order = np.argsort(match_dist)
        keep_n = max(min_pixels, int(len(order) * 0.35))
        keep = order[:keep_n]

        px = int(x1 + np.mean(xs[keep]))
        py = int(y1 + np.mean(ys[keep]))

        confidence = float(np.clip(1.0 - np.mean(match_dist[keep]) / color_threshold, 0.0, 1.0))

        return (px, py), confidence


    def update_dc4_button(frame, b):
        x1, y1, x2, y2 = b["roi"]
        crop = frame[x1:x2, y1:y2]
        current_color = mean_rgb(crop)

        if current_color is None:
            return 0.0, 0.0

        if b["baseline_color"] is None:
            b["finger_point"] = b["anchor"]
            b["state"] = 0
            b["tracking"] = 0
            b["candidate_frames"] = 0
            b["misses"] = 0
            b["track_misses"] = 0
            return 0.0, 0.0

        change = rgb_dist(current_color, b["baseline_color"])
        was_pressed = b["state"] == 1

        # -------------------------------------------------
        # FIRST CONTACT:
        # No finger color has been learned yet.
        # -------------------------------------------------
        if b["finger_color"] is None:
            if change > DC4_CHANGE_THRESHOLD:
                b["candidate_frames"] += 1

                if b["candidate_frames"] >= DC4_LOCK_FRAMES:
                    activate_dc4_button(b, current_color)
            else:
                b["candidate_frames"] = 0
                b["state"] = 0

            return change, 0.0

        # -------------------------------------------------
        # BUTTON STATE:
        # Button can release, but tracking can continue.
        # Re-pressing the button resets/relearns the line.
        # -------------------------------------------------
        if change < DC4_RELEASE_CHANGE_THRESHOLD:
            b["misses"] += 1

            if b["misses"] >= DC4_RELEASE_FRAMES:
                b["state"] = 0
                b["candidate_frames"] = 0

        elif change > DC4_CHANGE_THRESHOLD:
            # Rising edge: released -> pressed.
            # This resets the line and relearns the current finger color.
            if not was_pressed:
                activate_dc4_button(b, current_color)
            else:
                b["state"] = 1
                b["misses"] = 0

        # -------------------------------------------------
        # TRACKING STATE:
        # If this button has ever activated, keep tracking
        # inside its own lane until tracking misses too long.
        # -------------------------------------------------
        if b.get("tracking", 0) != 1:
            return change, 0.0

        search_start = b["finger_point"] if b["finger_point"] is not None else b["anchor"]

        point, confidence = find_finger_color_point(
            frame,
            b["finger_color"],
            search_start,
            baseline_color=b["baseline_color"],
            search_radius=DC4_SEARCH_RADIUS,
            color_threshold=DC4_COLOR_MATCH_THRESHOLD,
            baseline_reject_threshold=DC4_BASELINE_REJECT_THRESHOLD,
            brightness_threshold=DC4_BRIGHTNESS_MATCH_THRESHOLD,
            min_pixels=DC4_MIN_MATCH_PIXELS,
            max_point_jump=DC4_MAX_POINT_JUMP,

            # lane limits
            lane_anchor=b["anchor"],
            lane_dir=b.get("lane_dir", (0.0, -1.0)),
            lane_width=b.get("lane_width", DC4_LANE_WIDTH),
            lane_forward=DC4_LANE_FORWARD,
            lane_back=DC4_LANE_BACK
        )

        if point is not None:
            old_x, old_y = b["finger_point"]
            new_x, new_y = point

            smooth = DC4_POINT_SMOOTH
            b["finger_point"] = (
                int(old_x * (1.0 - smooth) + new_x * smooth),
                int(old_y * (1.0 - smooth) + new_y * smooth),
            )

            b["track_misses"] = 0

            # Only adapt finger color while actively pressed.
            if b["state"] == 1 and change > DC4_CHANGE_THRESHOLD:
                b["finger_color"] = (
                        b["finger_color"] * (1.0 - DC4_COLOR_LEARN_RATE)
                        + current_color * DC4_COLOR_LEARN_RATE
                )

        else:
            b["track_misses"] = b.get("track_misses", 0) + 1

            if b["track_misses"] >= DC4_TRACK_MISS_LIMIT:
                b["tracking"] = 0
                b["finger_point"] = b["anchor"]

        return change, confidence



    def draw_dc4_lane(b):
        if DC4_DRAW_LANES != 1:
            return

        ax, ay = b["anchor"]
        vx, vy = dc4_norm_vec(b.get("lane_dir", (0.0, -1.0)))
        width = b.get("lane_width", DC4_LANE_WIDTH)

        bx = ax - vx * DC4_LANE_BACK
        by = ay - vy * DC4_LANE_BACK

        ex = ax + vx * DC4_LANE_FORWARD
        ey = ay + vy * DC4_LANE_FORWARD

        nx = -vy
        ny = vx

        # lane center
        pygame.draw.line(
            screen,
            DC4_COLOR_LANE_CENTER,
            (int(bx), int(by)),
            (int(ex), int(ey)),
            DC4_LANE_THICKNESS
        )

        # lane rails
        for off in (-width, width):
            pygame.draw.line(
                screen,
                DC4_COLOR_LANE_RAIL,
                (int(bx + nx * off), int(by + ny * off)),
                (int(ex + nx * off), int(ey + ny * off)),
                DC4_LANE_THICKNESS
            )


    def draw_dc4_button(b, change=0.0, confidence=0.0):
        x1, y1, x2, y2 = b["roi"]
        ax, ay = b["anchor"]


        draw_dc4_lane(b)


        if b["state"] == 1:
            color = DC4_COLOR_ON
        else:
            color = DC4_COLOR_OFF

        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(x1, y1, x2 - x1, y2 - y1),
            DC4_BUTTON_THICKNESS
        )

        if b["finger_point"] is not None:
            fx, fy = b["finger_point"]

            if b["state"] == 1:
                line_color = DC4_COLOR_LINE_ACTIVE
                dot_color = DC4_COLOR_DOT_ACTIVE
                line_thickness = DC4_LINE_THICKNESS_ACTIVE
                dot_radius = DC4_DOT_RADIUS_ACTIVE

            else:
                line_color = DC4_COLOR_LINE_PASSIVE
                dot_color = DC4_COLOR_DOT_PASSIVE
                line_thickness = DC4_LINE_THICKNESS_PASSIVE
                dot_radius = DC4_DOT_RADIUS_PASSIVE

            pygame.draw.line(
                screen,
                line_color,
                (ax, ay),
                (fx, fy),
                line_thickness
            )

            pygame.draw.circle(
                screen,
                dot_color,
                (fx, fy),
                dot_radius
            )


        label = text_font.render(
            f'{b["name"]}:{b["state"]} c:{round(change, 1)} f:{round(confidence, 2)}',
            True,
            DC4_COLOR_TEXT
        )
        screen.blit(label, (x1, y1 - 18))


    def dc4_finger_buttons_detect():
        for hand_name in ("right", "left"):
            for b in dc4_buttons[hand_name]:
                change, confidence = update_dc4_button(hand_array, b)
                draw_dc4_button(b, change, confidence)

make_dc4_buttons()






running = True
while running:



    screen.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()

    image = camera.get_image()

    if ambient == 0:
        image_array = pygame.surfarray.array3d(image)
        hand_array = pygame.surfarray.array3d(image)
    else:
        image_array = pygame.surfarray.array3d(image)

        # Raw camera frame for display / reference
        hand_array_raw = pygame.surfarray.array3d(image)

        # Lighting-corrected frame for finger detection
        hand_array = correct_ambient_light(hand_array_raw)


    type = 6
    ####water type####

    if type == 1:
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


    if type == 2:
        size = 64
        l_size = 32
        x_space = 8
        y_space = 16
        offset_size = 1
        density = 1
        x_o = 128
        y_o = 32 + water_line* (size+16)


        if len(message) > 0:
            canvas, rainbow_reset = canvas_write_star_path_aligned(
                message,
                size, l_size, x_space, y_space,
                offset_size, density,
                x_o, y_o,
                flow,
                base_radius_px=210.0,  # match your flow_state star radius
                center_xy=(250.0, 250.0),  # for 500x500
                loop=True
            )


    if type == 3:
        size = 64
        l_size = 32
        x_space = 8
        y_space = 16
        offset_size = 1
        density = 1
        x_o = 128
        y_o = 32 + water_line* (size+16)


        if len(message) > 0:



            canvas, rainbow_reset = canvas_write_star_spiral_wholy(
                message, size, l_size, x_space, y_space, offset_size, density, x_o, y_o, flow,
                in_step_px=18.0, min_radius_px=60.0, wrap_message=True
            )


    if type == 4:
        size = 64
        l_size = 32
        x_space = 8
        y_space = 16
        offset_size = 1
        density = 1
        x_o = 128
        y_o = 32 + water_line * (size+16)


        if len(message) > 0:


            canvas, rainbow_reset = canvas_write_star_spiral(
                message,
                size, l_size, x_space, y_space, offset_size, density,
                x_o, y_o,
                flow,
                base_radius_px=210.0,
                in_step_px=l_size,
                min_radius_px=60.0,
                x_shift=128,
                y_shift=16,
                wrap_message=False,  # set True if you want to fill whole spiral every call
            )


    if type == 5:
        size = 64
        l_size = 32
        x_space = 8
        y_space = 16
        offset_size = 1
        density = 1
        x_o = 128
        y_o = 32 + water_line * (size+16)


        if len(message) > 0:


            canvas, rainbow_reset = canvas_write_star_spiral_shrink(
                message,
                size, l_size, x_space, y_space, offset_size, density,
                x_o, y_o,
                flow,
                base_radius_px=210.0,
                in_step_px=l_size,
                min_radius_px=60.0,
                x_shift=128,
                y_shift=16,
                wrap_message=False,  # set True if you want to fill whole spiral every call
            )


    if type == 6:
        size = 64
        l_size = 32
        x_space = 8
        y_space = 16
        offset_size = 1
        density = 1
        x_o = 128
        y_o = 32 + water_line * (size+16)


        if len(message) > 0:


            flow, n_slots = canvas_write_bethlehem_lanes(
                message,
                flow,
                slots=bethlehem_slots,
                offset_size=offset_size,
                density=density,
                wrap_message=False
            )





    if rainbow_reset == 1:
        rainbow_array = np.zeros((h, l), dtype=int)
        rainbow_speed += 1
        se += 1



        rainbow_reset = 0

        if type < 5:
            messages.append(message[::])
            message = ''


        if ruler > 3:


            flow = flow_base.copy()
            water = flow.copy()

        if flow_state == 8:
            flow = flow_star_radiating_arcs(
                500, 500,
                base_radius_px=210,
                thickness_px=1.0,
                rainbow_speed=rainbow_speed,
                arcs_per_edge_base=2,
                arc_step_px=10.0,
                arc_phase_px=(rainbow_speed % 20) * 0.7,  # optional animation
                n_samples=90,
                keep_outside_black=True
            )
            flow_base = flow.copy()


    ###messages###
    messages[0] = message




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

            water = water_update()
            water = water.astype(np.int32)

            flow = water



        # rainbow = 2
        region = image_array[pos_x:pos_x + l, pos_y:pos_y + h]

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
                up_mask = (flow == 1)
                down_mask = (flow == 0)


                rainbow_strength = np.array([-1, 1], dtype=np.int8)

            elif base == 3:
                up_mask = (flow == 1)
                down_mask = (flow == 2)



                rainbow_strength = np.array([0, 1, -1], dtype=np.int8)

            elif base == 4:

                up_mask = (flow == 0) | (flow == 2)
                down_mask = (flow == 1) | (flow == 3)


                rainbow_strength = np.array([+1, -1, +2, -2], dtype=np.int8)





            region = image_array[pos_x:pos_x+l, pos_y:pos_y+h]
            region_original = region.copy()


            delta = rainbow_strength[flow] * rainbow_speed * se
            delta_base = rainbow_strength[flow_base] * rainbow_speed * se

            delta += delta_base

            rainbow_array = (rainbow_array + delta) % color_max

            rainbow_flow = full_colors[rainbow_array]



            ###edge###
            edge = 1
            edge_depth = 16

            if edge == 1:

                gray = region.mean(axis=2).astype(np.float32)
                gx = np.abs(np.diff(gray, axis=1))
                gy = np.abs(np.diff(gray, axis=0))

                gx = np.pad(gx, ((0, 0), (0, 1)), mode='constant')
                gy = np.pad(gy, ((0, 1), (0, 0)), mode='constant')

                edges = (np.sqrt(gx ** 2 + gy ** 2))
                edges = (edges / np.max(edges + 1e-6) * 255).astype(np.uint8)

                edge_mask = edges > edge_depth

                # Add CA turbulence at edge boundaries
                flow[edge_mask] = (flow[edge_mask] + 1) % base



            fade_max = 8

            fade = score % fade_max
            fade = 1

            # print(fade)


            if fade == 0:
                region[:, :] = rainbow_flow

            elif fade == 1:
                mask = flow != 0
                region[mask] = rainbow_flow[mask]

            elif fade == 2:

                region[:] = ((region.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)


            elif fade == 3:

                mixed = ((region.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)
                mask = (flow != 0)
                mixed[mask] = rainbow_flow[mask]
                region = mixed


            elif fade == 4:

                region = ((region.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)
                region[flow != 0] = rainbow_flow[flow != 0]
                region[edge_mask] = region_original[edge_mask]


            elif fade == 5:

                alpha = 1.0 if base == 2 else round(1 / base, 3)
                flow_alpha = (flow[..., np.newaxis].astype(np.float32))

                region = (
                        region.astype(np.float32) * (1 - alpha * flow_alpha) +
                        rainbow_flow.astype(np.float32) * (alpha * flow_alpha)
                ).astype(np.uint8)

                # Edge highlight momentum
                speed_boost = len(message)
                region[edge_mask] = region_original[edge_mask]
                rainbow_array[edge_mask] += speed_boost + set
                rainbow_array %= color_max

            elif fade == 6:

                image_flow = color_array[flow]
                half_mix = ((image_flow.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)

                alpha = 1.0 if base == 2 else round(1 / base, 3)
                flow_alpha = flow[..., np.newaxis].astype(np.float32)

                region = (
                        region.astype(np.float32) * (1 - alpha * flow_alpha) +
                        half_mix.astype(np.float32) * (alpha * flow_alpha)
                ).astype(np.uint8)

                speed_boost = len(message)
                region[edge_mask] = region_original[edge_mask]
                rainbow_array[edge_mask] += speed_boost + set
                rainbow_array %= color_max


            elif fade == 7:

                # Very complex mode from your original system, preserved fully
                sum_up = np.sum(up_mask)
                sum_down = np.sum(down_mask)

                base_region = region.astype(np.float32)
                rainbow_region = rainbow_flow.astype(np.float32)

                up_mask = (flow == 1)
                down_mask = (flow == 0)

                result = base_region.copy()

                alpha_fade = 0.5
                alpha_full = 1.0

                if sum_up > sum_down:
                    result[up_mask] = base_region[up_mask] * (1 - alpha_fade) + rainbow_region[up_mask] * alpha_fade
                    result[down_mask] = base_region[down_mask] * (1 - alpha_full) + rainbow_region[down_mask] * alpha_full
                else:
                    result[down_mask] = base_region[down_mask] * (1 - alpha_fade) + rainbow_region[down_mask] * alpha_fade
                    result[up_mask] = base_region[up_mask] * (1 - alpha_full) + rainbow_region[up_mask] * alpha_full

                region = result.astype(np.uint8)
                region[edge_mask] = region_original[edge_mask]
                rainbow_array[edge_mask] += len(message) + set
                rainbow_array %= color_max


        if rainbow == 2:


            if base == 2:

                up_mask = (flow == 1)
                down_mask = (flow == 0)

                rainbow_strength = np.array([-1, 1], dtype=np.int8)

            elif base == 3:
                up_mask = (flow == 1)
                down_mask = (flow == 2)



                rainbow_strength = np.array([0, 1, -1], dtype=np.int8)

            elif base == 4:

                up_mask = (flow == 0) | (flow == 2)
                down_mask = (flow == 1) | (flow == 3)


                rainbow_strength = np.array([+1, -1, +2, -2], dtype=np.int8)



            impulse = np.where(flow==1, +learn_rate, -learn_rate)
            memory = memory * decay_rate + impulse
            memory = np.clip(memory, -1.0, 1.0)


            delta = rainbow_strength[flow] * (rainbow_speed + memory*memory_scale) * set



            region = image_array[pos_x:pos_x+l, pos_y:pos_y+h]
            region_original = region.copy()




            rainbow_array = (rainbow_array + delta.astype(int)) % color_max

            rainbow_flow = full_colors[rainbow_array]



            ###edge###
            edge = 1
            edge_depth = 16

            if edge == 1:

                gray = region.mean(axis=2).astype(np.float32)
                gx = np.abs(np.diff(gray, axis=1))
                gy = np.abs(np.diff(gray, axis=0))

                gx = np.pad(gx, ((0, 0), (0, 1)), mode='constant')
                gy = np.pad(gy, ((0, 1), (0, 0)), mode='constant')

                edges = (np.sqrt(gx ** 2 + gy ** 2))
                edges = (edges / np.max(edges + 1e-6) * 255).astype(np.uint8)

                edge_mask = edges > edge_depth

                # Add CA turbulence at edge boundaries
                flow[edge_mask] = (flow[edge_mask] + 1) % base



            fade_max = 8

            fade = score % fade_max
            fade = 0

            # print(fade)


            if fade == 0:
                region[:, :] = rainbow_flow

            elif fade == 1:
                mask = flow != 0
                region[mask] = rainbow_flow[mask]

            elif fade == 2:

                region[:] = ((region.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)


            elif fade == 3:

                mixed = ((region.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)
                mask = (flow != 0)
                mixed[mask] = rainbow_flow[mask]
                region = mixed


            elif fade == 4:

                region = ((region.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)
                region[flow != 0] = rainbow_flow[flow != 0]
                region[edge_mask] = region_original[edge_mask]


            elif fade == 5:

                alpha = 1.0 if base == 2 else round(1 / base, 3)
                flow_alpha = (flow[..., np.newaxis].astype(np.float32))

                region = (
                        region.astype(np.float32) * (1 - alpha * flow_alpha) +
                        rainbow_flow.astype(np.float32) * (alpha * flow_alpha)
                ).astype(np.uint8)

                # Edge highlight momentum
                speed_boost = len(message)
                region[edge_mask] = region_original[edge_mask]
                rainbow_array[edge_mask] += speed_boost + set
                rainbow_array %= color_max

            elif fade == 6:

                image_flow = color_array[flow]
                half_mix = ((image_flow.astype(np.float32) + rainbow_flow.astype(np.float32)) / 2).astype(np.uint8)

                alpha = 1.0 if base == 2 else round(1 / base, 3)
                flow_alpha = flow[..., np.newaxis].astype(np.float32)

                region = (
                        region.astype(np.float32) * (1 - alpha * flow_alpha) +
                        half_mix.astype(np.float32) * (alpha * flow_alpha)
                ).astype(np.uint8)

                speed_boost = len(message)
                region[edge_mask] = region_original[edge_mask]
                rainbow_array[edge_mask] += speed_boost + set
                rainbow_array %= color_max


            elif fade == 7:

                # Very complex mode from your original system, preserved fully
                sum_up = np.sum(up_mask)
                sum_down = np.sum(down_mask)

                base_region = region.astype(np.float32)
                rainbow_region = rainbow_flow.astype(np.float32)

                up_mask = (flow == 1)
                down_mask = (flow == 0)

                result = base_region.copy()

                alpha_fade = 0.5
                alpha_full = 1.0

                if sum_up > sum_down:
                    result[up_mask] = base_region[up_mask] * (1 - alpha_fade) + rainbow_region[up_mask] * alpha_fade
                    result[down_mask] = base_region[down_mask] * (1 - alpha_full) + rainbow_region[down_mask] * alpha_full
                else:
                    result[down_mask] = base_region[down_mask] * (1 - alpha_fade) + rainbow_region[down_mask] * alpha_fade
                    result[up_mask] = base_region[up_mask] * (1 - alpha_full) + rainbow_region[up_mask] * alpha_full

                region = result.astype(np.uint8)
                region[edge_mask] = region_original[edge_mask]
                rainbow_array[edge_mask] += len(message) + set
                rainbow_array %= color_max




        image_array[pos_x:pos_x + l, pos_y:pos_y + h] = region





    image = pygame.surfarray.make_surface(image_array)
    screen.blit(image, (0, 0))



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

    elif detect_change == 2:






        ####right hand####

        right_hand_detector()





        ####left hand####
        left_hand_detect()


    elif detect_change == 3:

        right_dc3 = 1
        left_dc3 = 1

        lr_edge_threshold = 0.032


        if right_dc3 == 1:

            x1, y1, x2, y2 = outline_hand_window(
                screen,
                right_roi,
                value_color[9],
                pad=hand_box_pad,
                width=3
            )

            ###right hand###
            if right_box is not None:
                bx1, by1, bx2, by2 = right_box
            else:
                bx1, by1, bx2, by2 = x1, y1, x2, y2

            right_field = hand_array[bx1:bx2, by1:by2].copy()

            if array_past is not None:
                previous_right_field = array_past[bx1:bx2, by1:by2].copy()
            else:
                previous_right_field = None

            right_change_speed = build_change_speed_map(
                right_field,
                previous_right_field,
                prev_speed_map=right_change_speed,
                alpha=0.35
            )

            edge_mask = build_hand_sensor(right_field)

            hand_region = build_hand_isolation_mask(
                right_field,
                right_roi,
                color_threshold=50,
                brightness_threshold=50,
                gap_threshold=18,
                min_size_ratio=0.004,
                dilate_radius=4
            )

            hand_is_present = hand_present(hand_region, min_pixels=1200)

            if right_change_speed is not None and hand_region is not None and right_change_speed.shape == hand_region.shape:
                right_change_speed = right_change_speed * (hand_region > 0.5)



            cleaned_edge_mask, hand_perimeter = fast_hand_perimeter(
                edge_mask,
                hand_region,
                edge_threshold=lr_edge_threshold,
                close_radius=1
            )

            skin_perimeter = mask_perimeter(hand_region)

            if skin_perimeter is not None:
                hand_perimeter = np.maximum(hand_perimeter, skin_perimeter).astype(np.float32)


            xy_colors, xy_points = perimeter_xy_colors(hand_perimeter)

            distinct_xy_colors, distinct_xy_points = pick_structured_perimeter_xy_colors(
                xy_colors,
                xy_points,
                hand_perimeter.shape,
                edge_margin=12,
                top_margin=10,
                color_min_dist=42.0
            )


            draw_color_squares_at_points(
                screen,
                distinct_xy_colors,
                distinct_xy_points,
                (bx1, by1, bx2, by2),
                hand_perimeter.shape,
                square_size=14
            )

            fast_pixels = threshold_fast_pixels(right_change_speed, threshold=0.42)

            clusters = extract_clusters(fast_pixels, min_size=7)

            # use a proximity reference if you have one
            # for now, simplest is the middle of the chosen squares if they exist
            if distinct_xy_points:
                ref_x = float(np.mean([p[0] for p in distinct_xy_points]))
                ref_y = float(np.mean([p[1] for p in distinct_xy_points]))
                reference_point = (ref_x, ref_y)
            else:
                reference_point = None

            scored_clusters = score_shadow_clusters_with_proximity(
                clusters,
                prev_shadow_mask=right_shadow_mask,
                reference_point=reference_point,
                proximity_scale=40.0
            )

            right_cluster_count = len(scored_clusters)

            priority_cluster_mask = top_shadow_cluster_mask(scored_clusters, keep_n=1)

            thin_clusters = thin_cluster_mask(priority_cluster_mask,
                                              step=2) if priority_cluster_mask is not None else None




            edge_shadow_source = (
                hand_perimeter * thin_clusters
                if thin_clusters is not None
                else np.zeros_like(hand_perimeter, dtype=np.float32)
            )



            right_shadow_mask = update_shadow_mask(
                edge_shadow_source,
                shadow_mask=right_shadow_mask,
                rise=1.0,
                decay=0.82
            )

            draw_shadow_mask_on_field(
                screen,
                right_shadow_mask,
                (bx1, by1, bx2, by2),
                live_mask=hand_perimeter,
                shadow_threshold=0.08,
                live_threshold=0.5
            )

            draw_binary_overlay_xycolor_on_field(
                screen,
                hand_perimeter,
                (bx1, by1, bx2, by2)
            )





            current_template = prepare_edge_template(
                right_field,
                edge_threshold=0.04,
                out_size=(64, 64)
            )

            recognized_edge_label, recognized_edge_score = recognize_edge_template(
                current_template,
                edge_library,
                threshold=0.18
            )

            label = text_font.render(
                f"edge label: {phrase}   match: {recognized_edge_label}   score: {round(recognized_edge_score, 4)}",
                True,
                value_color[9]
            )
            screen.blit(label, (x1, max(0, y1 - 20)))

            cluster_label = text_font.render(
                f"clusters: {right_cluster_count}",
                True,
                value_color[9]
            )
            screen.blit(cluster_label, (x1, max(0, y1 - 40)))


        if left_dc3 == 1:

            ### left hand ###

            lx1, ly1, lx2, ly2 = outline_hand_window(
                screen,
                left_roi,
                value_color[9],
                pad=hand_box_pad,
                width=3
            )

            if left_box is not None:
                lbx1, lby1, lbx2, lby2 = left_box
            else:
                lbx1, lby1, lbx2, lby2 = lx1, ly1, lx2, ly2

            left_field = hand_array[lbx1:lbx2, lby1:lby2].copy()

            if array_past is not None:
                previous_left_field = array_past[lbx1:lbx2, lby1:lby2].copy()
            else:
                previous_left_field = None

            left_change_speed = build_change_speed_map(
                left_field,
                previous_left_field,
                prev_speed_map=left_change_speed,
                alpha=0.35
            )

            left_edge_mask = build_hand_sensor(left_field)

            left_hand_region = build_hand_isolation_mask(
                left_field,
                left_roi,
                color_threshold=19,
                brightness_threshold=80,
                gap_threshold=18,
                min_size_ratio=0.004,
                dilate_radius=4
            )

            left_hand_is_present = hand_present(left_hand_region, min_pixels=1200)

            if left_change_speed is not None and left_hand_region is not None and left_change_speed.shape == left_hand_region.shape:
                left_change_speed = left_change_speed * (left_hand_region > 0.5)

            left_cleaned_edge_mask, left_hand_perimeter = fast_hand_perimeter(
                left_edge_mask,
                left_hand_region,
                edge_threshold=lr_edge_threshold,
                close_radius=1
            )

            left_skin_perimeter = mask_perimeter(left_hand_region)

            if left_skin_perimeter is not None:
                left_hand_perimeter = np.maximum(left_hand_perimeter, left_skin_perimeter).astype(np.float32)

            left_xy_colors, left_xy_points = perimeter_xy_colors(left_hand_perimeter)

            left_distinct_xy_colors, left_distinct_xy_points = pick_structured_perimeter_xy_colors(
                left_xy_colors,
                left_xy_points,
                left_hand_perimeter.shape,
                edge_margin=12,
                top_margin=10,
                color_min_dist=42.0
            )

            draw_color_squares_at_points(
                screen,
                left_distinct_xy_colors,
                left_distinct_xy_points,
                (lbx1, lby1, lbx2, lby2),
                left_hand_perimeter.shape,
                square_size=14
            )

            left_fast_pixels = threshold_fast_pixels(left_change_speed, threshold=0.42)

            left_cluster_count, left_fast_clusters = count_clusters(
                left_fast_pixels,
                min_size=7
            )

            left_thin_clusters = thin_cluster_mask(left_fast_clusters, step=2)

            left_edge_shadow_source = left_hand_perimeter * left_thin_clusters

            left_shadow_mask = update_shadow_mask(
                left_edge_shadow_source,
                shadow_mask=left_shadow_mask,
                rise=1.0,
                decay=0.82
            )

            draw_shadow_mask_on_field(
                screen,
                left_shadow_mask,
                (lbx1, lby1, lbx2, lby2),
                live_mask=left_hand_perimeter,
                shadow_threshold=0.08,
                live_threshold=0.5
            )

            draw_binary_overlay_xycolor_on_field(
                screen,
                left_hand_perimeter,
                (lbx1, lby1, lbx2, lby2)
            )




















        if rethresh == 1:
            rethresh = 0

            if right_box is not None:
                current_field = capture_frame_from_fixed_box(hand_array, right_box)
            else:
                bx1, by1, bx2, by2 = outline_hand_window(screen, right_roi, value_color[9], pad=hand_box_pad, width=3)
                current_field = hand_array[bx1:bx2, by1:by2].copy()

            current_template = prepare_edge_template(
                current_field,
                edge_threshold=0.03,
                out_size=(64, 64)
            )

            save_edge_template(current_template)

    elif detect_change == 4:

        dc4_finger_buttons_detect()






    ###stats###
    times_limit = 20
    for x in range(len(times)):
        if x > times_limit:
            break
        lesson_t = text_font.render(str(times[x]), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 128, screen_height / 16 + lesson_t.get_height()*x))

    times_limit = 20
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


    def time_ladder(times):
        """
        Group times into rounded tenth-second buckets:
        0.4s, 0.5s, 0.6s, 0.7s, etc.
        Returns a dictionary like {0.4: 3, 0.5: 7, 0.6: 2}
        """
        ladders = {}

        for t in times:
            if t <= 0:
                continue  # ignore invalid

            key = round(t, 1)  # e.g. 0.412 → 0.4
            ladders[key] = ladders.get(key, 0) + 1

        return ladders


    ladders = time_ladder(times)
    ladder_most = sorted(ladders.items(), key=lambda x: x[1], reverse=True)


    ladder_list = list(ladders.items())


    for x in range(len(ladder_list)):

        if x > 20:
            break


        lesson_t = text_font.render(str(ladder_list[x]), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 16, screen_height / 16 + lesson_t.get_height()*x))

        lesson_t = text_font.render(str(ladder_most[x]), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 8, screen_height / 16 + lesson_t.get_height()*x))



    if tts_0 < 10 and round(tts_0, 1) in ladders:

        current_rung = ladders[round(tts_0, 1)]

        lesson_t = small_font.render(str(current_rung), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 4, screen_height / 16 - 32))
    else:
        current_rung = 1



    ###history
    for x in range(len(history)):

        if x > 20:
            break

        lesson_t = text_font.render(str(history[x]), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 8 + screen_width/16, screen_height / 16 + lesson_t.get_height()*x))




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


    letters_on = 1

    if letters_on == 1:
        letters = []


        letter, code_0 = handle(hands, code_0)
        letter_0, code_00 = handle(hands_0, code_00)
        letter_1, code_01 = handle(hands_1, code_01)

        typing_mode = 0

        typed = 0
        bong = 0
        score_0 = 0

        ###typing###
        if typing_mode == 0 or typing_mode == 2:

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
                    bong = 1
                    submit(letter)
                    last_typed = letter

                    if typing_mode == 2:

                        send_sign_to_keyboard(letter)
                        send_sign_to_flow(letter, score_0)



                elif letter_0 != last_typed:
                    bong = 1
                    submit(letter_0)
                    last_typed = letter_0

                    if typing_mode == 2:
                        send_sign_to_keyboard(letter)
                        send_sign_to_flow(letter, score_0)


                elif letter_1 != last_typed:
                    bong = 1
                    submit(letter_1)
                    last_typed = letter_1

                    if typing_mode == 2:
                        send_sign_to_keyboard(letter)
                        send_sign_to_flow(letter, score_0)




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


        if typing_mode == 1 or typing_mode == 2:

            def send_sign_to_keyboard(sign):

                try:
                    pyautogui.write(sign)
                    print("SENT TO KEYBOARD:", sign)
                except Exception as e:
                    print("pyautogui error:", e)

            ####thank you####


            if letter == letter_0:
                if letter_0 == letter_1:
                    if letter != last_letter_typed:
                        last_letter_typed = letter


                        if letter == '':
                            letter = ' '

                        send_sign_to_keyboard(letter)

                        send_sign_to_flow(letter, score_0)


        if typing_mode == 3:

            def send_sign_to_keyboard(sign):

                global held

                holds = ['e', 'w', 'r', 'z', 'x', 'l', 'o', 'v', 'p', 'a', 'r', 'd', 'b', 'i', 'q', 'f', 'm', 'h']

                if sign not in holds:
                    try:
                        pyautogui.write(sign)
                        print("write:", sign)
                    except Exception as e:
                        print("pyautogui error:", e)

                else:
                    try:
                        press_key_down(sign)
                        print("Press:", sign)
                        held = sign
                    except Exception as e:
                        print("pyautogui error:", e)


            match = ''


            if letter == letter_0:
                match = letter
            elif letter_0 == letter_1:
                match = letter_0
            elif letter_1 == letter:
                match = letter_1




            if match != last_typed:
                hold_key_up(held)


                print('')
                print('match')
                print(match)


                bong_on = 1
                code = ' '
                send_sign_to_keyboard(match)
                last_typed = match


        if typing_mode == 4:

            def send_sign_to_keyboard(sign):

                global held

                holds = ['e', 'w', 'r', 'z', 'x', 'l', 'o', 'v', 'p', 'a', 'r', 'd', 'b', 'i', 'q', 'f', 'm', 'h', 's', 't', 'u', 'g']

                if sign not in holds:
                    try:
                        pyautogui.write(sign)
                        print("write:", sign)
                    except Exception as e:
                        print("pyautogui error:", e)

                else:
                    try:
                        press_key_down(sign)
                        print("Press:", sign)
                        held = sign
                    except Exception as e:
                        print("pyautogui error:", e)


            match_l = ''
            match_r = ''


            if hands[0] == hands_0[0]:
                match_r = hands[0]
            elif hands_0[0] == hands_1[0]:
                match_r = hands_0[0]
            elif hands_1[0] == hands[0]:
                match_r = hands_1[0]


            if hands[1] == hands_0[1]:
                match_l = hands[1]
            elif hands_0[1] == hands_1[1]:
                match_l = hands_0[1]
            elif hands_1[1] == hands[1]:
                match_l = hands_1[1]


            if match_r != last_r:

                print()
                print('match_r')
                print(match_r)

                hold_key_up(last_r)
                bong_on = 1
                code = ''
                send_sign_to_keyboard(match_r)
                last_r = match_r

            if match_l != last_l:

                print()
                print('match_l')
                print(match_l)

                hold_key_up(last_l)
                bong_on = 1
                code = ''
                send_sign_to_keyboard(match_l)
                last_l = match_l



















    ### rule display #####

    if base == 2:

        if view == 5:
            rule_l = 32
            rule_h = rule_l
            cells = len(rule)
            rows = 4
            bins = 8

            # print(rule)



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

                            rule_str = "".join(rule)
                            rv = int(rule_str, base)
                            rv = rv % bbv

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




    # ###code display####
    #
    # for x in range(int(len(code)/64)+1):
    #     lesson_t = main_font.render(str(code), True, value_color[9])
    #     screen.blit(lesson_t, (screen_width / 2 - int(lesson_t.get_width()/2), screen_height / 8 - 128 + x*lesson_t.get_height()))
    #ambient display
    if ambient == 1:
        ambient_label = text_font.render(
            f"ambient Δ: {round(ambient_delta, 2)}",
            True,
            value_color[9]
        )
        screen.blit(ambient_label, (screen_width / 64, screen_height / 32))

    lesson_t = main_font.render('rv: ' + str(rv), True, value_color[9])
    screen.blit(lesson_t, (screen_width - screen_width/3, screen_height / 32 - 32))


    lesson_t = lable_font.render('score' + str(score), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 2 - lesson_t.get_width()/2, screen_height / 4 - 64))

    lesson_t = main_font.render('set' + str(set), True, value_color[9])
    screen.blit(lesson_t, (screen_width - 224, screen_height / 32 - 32))

    lesson_t = main_font.render('speed' + str(rainbow_speed), True, value_color[9])
    screen.blit(lesson_t, (screen_width - 128, screen_height / 32 - 32 ))

    lesson_t = small_font.render('tts: ' + str(round(tts_0, 3)), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 64, screen_height / 32 - 32))

    lesson_t = main_font.render(str((up_count, down_count)), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 4, screen_height / 32 - 32))


    ###synth###
    beat = 1
    volume = 0.0
    bong = 4
    ######bong#####
    if bong_on == 1:
        if bong == 1:
            bong = 0
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



        elif bong == 2:
            bong_on = 0
            # print('gong', note)

            if dim == 1:
                water0 = np.rot90(water[::], 2)
            elif dim == 2:
                water0 = water
            else:
                water0 = flow

            if note in digibet:
                flow_sound = ca_tone_from_note(
                    note,
                    water0,
                    digibet,
                    base=base,
                    sample_rate=sample_rate,
                    duration=0.35,
                    amp=volume,
                    midi_base_hz=55.0,
                    note_offset=0
                )

                if flow_sound is not None:
                    flow_sound.play()




        elif bong == 3:
            bong_on = 0
            # print('gong', note)

            if dim == 1:
                water0 = np.rot90(water[::], 2)
            elif dim == 2:
                water0 = water
            else:
                water0 = flow

            rainbow0 = rainbow_array.copy()

            if note in digibet:
                # main centered water voice
                flow_sound = ca_tone_from_note(
                    note,
                    water0,
                    digibet,
                    base=base,
                    sample_rate=sample_rate,
                    duration=0.35,
                    amp=0.22,
                    midi_base_hz=55.0,
                    note_offset=0,
                    octave_shift=0,
                    pan=0.5
                )

                # left rainbow side voice
                rainbow_left = rainbow_tone_from_note(
                    note,
                    rainbow0,
                    digibet,
                    color_max=color_max,
                    sample_rate=sample_rate,
                    duration=0.35,
                    amp=0.10,
                    midi_base_hz=55.0,
                    note_offset=0,
                    octave_shift=0,
                    pitch_detune=-0.01,
                    pan=0.3
                )

                # right rainbow side voice
                rainbow_right = rainbow_tone_from_note(
                    note,
                    rainbow0,
                    digibet,
                    color_max=color_max,
                    sample_rate=sample_rate,
                    duration=0.35,
                    amp=0.10,
                    midi_base_hz=55.0,
                    note_offset=0,
                    octave_shift=0,
                    pitch_detune=0.01,
                    pan=0.7
                )

                if flow_sound is not None:
                    flow_sound.play()

                if rainbow_left is not None:
                    rainbow_left.play()

                if rainbow_right is not None:
                    rainbow_right.play()



        elif bong == 4:
            bong_on = 0
            # print('gong', note)

            if dim == 1:
                water0 = np.rot90(water[::], 2)
            elif dim == 2:
                water0 = water
            else:
                water0 = flow

            rainbow0 = rainbow_array.copy()

            if note in digibet:
                flow_sound = ca_tone_from_note(
                    note,
                    water0,
                    digibet,
                    base=base,
                    sample_rate=sample_rate,
                    duration=0.40,
                    amp=0.22,
                    midi_base_hz=55.0,
                    note_offset=0,
                    octave_shift=0,
                    pitch_detune=0.0,
                    pan=0.5
                )

                rainbow_left = rainbow_tone_from_note(
                    note,
                    rainbow0,
                    digibet,
                    color_max=color_max,
                    sample_rate=sample_rate,
                    duration=0.40,
                    amp=0.10,
                    midi_base_hz=55.0,
                    note_offset=0,
                    octave_shift=0,
                    pitch_detune=-0.008,
                    pan=0.34
                )

                rainbow_right = rainbow_tone_from_note(
                    note,
                    rainbow0,
                    digibet,
                    color_max=color_max,
                    sample_rate=sample_rate,
                    duration=0.40,
                    amp=0.10,
                    midi_base_hz=55.0,
                    note_offset=0,
                    octave_shift=0,
                    pitch_detune=0.008,
                    pan=0.66
                )

                if flow_sound is not None:
                    flow_sound.play()
                if rainbow_left is not None:
                    rainbow_left.play()
                if rainbow_right is not None:
                    rainbow_right.play()





        elif bong == 5:
            bong_on = 0
            # print('gong', note)

            if dim == 1:
                water0 = np.rot90(water[::], 2)
            elif dim == 2:
                water0 = water
            else:
                water0 = flow

            rainbow0 = rainbow_array.copy()

            if note in digibet:
                flow_sound = ca_tone_from_note(
                    note,
                    water0,
                    digibet,
                    base=base,
                    sample_rate=sample_rate,
                    duration=note_duration,
                    amp=0.24,
                    midi_base_hz=55.0,
                    note_offset=0,
                    octave_shift=0,
                    pitch_detune=0.0,
                    pan=0.5
                )

                rainbow_left = rainbow_tone_from_note(
                    note,
                    rainbow0,
                    digibet,
                    color_max=color_max,
                    sample_rate=sample_rate,
                    duration=note_duration,
                    amp=0.11,
                    midi_base_hz=55.0,
                    note_offset=0,
                    octave_shift=0,
                    pitch_detune=-0.008,
                    pan=0.32
                )

                rainbow_right = rainbow_tone_from_note(
                    note,
                    rainbow0,
                    digibet,
                    color_max=color_max,
                    sample_rate=sample_rate,
                    duration=note_duration,
                    amp=0.11,
                    midi_base_hz=55.0,
                    note_offset=0,
                    octave_shift=0,
                    pitch_detune=0.008,
                    pan=0.68
                )

                if flow_sound is not None:
                    flow_sound.play()
                if rainbow_left is not None:
                    rainbow_left.play()
                if rainbow_right is not None:
                    rainbow_right.play()








    ###shifts###

    for i in range(5):


        cell_map = [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1)]

        xs = 16
        ys = 16
        x = screen_width / 2 + int(cell_map[i][0]*xs) + xs*4
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
            rainbow = rainbow%3



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

                if ambient == 0:
                    rethresh = 1
                    array_past = hand_array.copy()
                else:
                    rethresh = 1
                    array_past = hand_array.copy()
                    palm_prev = [None, None]
                    print("detector baseline reset")


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

                if ambient == 0:
                    array_past = hand_array.copy()
                else:
                    array_past = hand_array.copy()
                    palm_prev = [None, None]
                    print("finger box baseline reset")






            elif event.key == pygame.K_F3:

                right_open_hand_mask, right_box = capture_open_hand_mask(

                    hand_array,

                    right_roi,

                    pad=hand_box_pad,

                    color_threshold=60,

                    brightness_threshold=90

                )

                right_open_hand_frame = capture_frame_from_fixed_box(hand_array, right_box)

                if right_open_hand_frame is not None:
                    right_exclusion_edge_mask = build_hand_sensor(right_open_hand_frame)

                if right_open_hand_mask is not None and right_open_hand_frame is not None:

                    print("exclusion calibration saved")

                    print("box:", right_box)

                    print("mask shape:", right_open_hand_mask.shape)

                    print("frame shape:", right_open_hand_frame.shape)

                    if right_exclusion_edge_mask is not None:
                        print("exclusion edge shape:", right_exclusion_edge_mask.shape)

                else:

                    print("exclusion calibration failed")


            elif event.key == pygame.K_F4:
                if ambient == 1:
                    calibrate_ambient(hand_array_raw)
                    array_past = correct_ambient_light(hand_array_raw).copy()
                    palm_prev = [None, None]
                    print("ambient + detector baseline reset")
                else:
                    array_past = hand_array.copy()
                    palm_prev = [None, None]
                    print("detector baseline reset")


            elif event.key == pygame.K_F8:
                calibrate_dc4_buttons(hand_array)



            # elif event.key == pygame.K_LEFT:
            #     current -= 1
            #
            # elif event.key == pygame.K_RIGHT:
            #     current += 1
            #
            elif event.key == pygame.K_UP:

                rainbow_speed += 1

                if rainbow_speed > speed_limit:
                    rainbow_speed = speed_limit

            elif event.key == pygame.K_DOWN:

                rainbow_speed -= 1
                if rainbow_speed < -int(speed_limit)/2:
                    rainbow_speed = -int(speed_limit)/2

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


