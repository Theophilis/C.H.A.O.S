import socket
import pickle
from struct import unpack
import pygame
import math
import time

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '192.168.1.3', 21621
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

#####game#####

pygame.init()
pygame.display.init()
current_display = pygame.display.Info()
WIDTH, HEIGHT = current_display.current_w - 50, current_display.current_h - 100
# WIDTH, HEIGHT = 400, 400
width_2 = int(WIDTH / 2)
width_3 = int(WIDTH / 3)
width_4 = int(WIDTH / 4)
width_8 = int(WIDTH / 8)
width_16 = int(WIDTH / 16)
width_32 = int(WIDTH / 32)
width_64 = int(WIDTH / 64)
width_128 = int(WIDTH / 128)
width_256 = int(WIDTH / 256)
width_512 = int(WIDTH / 512)

height_2 = int(HEIGHT / 2)
height_4 = int(HEIGHT / 4)
height_8 = int(HEIGHT / 8)
height_16 = int(HEIGHT / 16)
height_32 = int(HEIGHT / 32)
height_64 = int(HEIGHT / 64)
height_128 = int(HEIGHT / 128)
height_256 = int(HEIGHT / 256)
height_512 = int(HEIGHT / 512)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)


click = False

value_color = {0: (0, 0, 0), 1: (255, 0, 0), 2: (255, 255, 0), 3: (0, 255, 0), 4: (0, 255, 255), 5: (0, 0, 255),
               6: (255, 0, 255), 7: (255, 255, 255), 8: (127, 127, 127), 9: (127, 0, 0), 10:(127, 127, 0),
               11: (0, 127, 0), 12: (0, 127, 127), 13: (0, 0, 127), 14: (127, 0, 127)}



run = 1
#number_of_sensors
nos = 8

clock = pygame.time.Clock()

glove_name = 'arm'
glove_values = [[0, [0, 0, 0, 0, 0, 0]] for x in range(nos)]
sensor_order = ['arm', 'wrist', 'hand', 'thumb', 'index', 'middle', 'ring', 'pinky']

#orients
orients = ['FB', 'LR', 'UD']
#chaotomata
if glove_name == 'chaotomata':
    orientation = {'FB':{0:1, 1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0},
                   'LR':{0:0, 1:0, 2:0, 3:1, 4:1, 5:1, 6:1, 7:1},
                   'UD':{0:2, 1:2, 2:2, 3:3, 4:3, 5:2, 6:2, 7:2}}
#gos
if glove_name == 'gos':
    orientation = {'FB':{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0},
                   'LR':{0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1},
                   'UD':{0:2, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2}}
#arm
if glove_name == 'arm':
    orientation = {'FB':{0:1, 1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0},
                   'LR':{0:0, 1:0, 2:0, 3:1, 4:1, 5:1, 6:1, 7:1},
                   'UD':{0:2, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2}}

calibrations = {'FB': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'LR': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'UD': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]}
midpoints = {'FB': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'LR': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'UD': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]}

#calibrations
try:
    filename = 'calibrations/' + glove_name
    infile = open(filename, "rb")
    revelations = pickle.load(infile)
    infile.close

except:

    revelations = {'FB':[[0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
                    'LR':[[0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
                    'UD':[[0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]}

compass = [[0, 0, 0, 0, 0, 0] for x in range(nos)]
g_time = [[time.time(), 0] for x in range(nos)]
acc_switch = [1 for x in range(nos)]

gyros = [1 for x in range(nos)]
accs = [1 for x in range(nos)]
gyro_switch = [1 for x in range(nos)]
gyro_polarity = [1 for x in range(nos)]
gyro_cap = [1 for x in range(nos)]
spin_min = [8 for x in range(nos)]

graph = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}


total_gs = {'FB':0, 'LR':0, 'UD':0}

# bets
digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, 'an': 14, 'er': 15,
           'ou': 16, 'in': 17, 'th': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}
digibetu = {v: k for k, v in digibet.items()}

filename = 'bets/armbet_2'
infile = open(filename, "rb")
armbet = pickle.load(infile)
infile.close

print()
for d in digibet:
    print(armbet[d])

#ui
compui = 0
calui = 1
gyrui = 1
switchui = 1

digisign = 0
digisign_s = ''
armsign = 0
armsign_s = ''
betcalibration = 0
recordcali = 0

calibet = {}
mhl = {}
cali_limit = 255

mean = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
high = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
low = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

while run == 1:

    clock.tick()
    WIN.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()

    # Wait for message
    message, address = sock.recvfrom(4096)

    Ax, Ay, Az, Gx, Gy, Gz, channel = unpack('7f', message)
    channel = int(channel)

    glove_values[channel] = [sensor_order[channel], [Ax, Ay, Az, Gx, Gy, Gz]]
    g_time[channel][1] = g_time[channel][0]
    g_time[channel][0] = time.time()

    gyros[channel] = [int(Gx) , int(Gy), int(Gz)]
    accs[channel] = [Ax, Ay, Az]


    #compass
    try:
        compass[channel][0] = round(Ax, 3)
        compass[channel][3] = round(Gx, 3)
    except:
        continue

    try:
        compass[channel][1] = round(Ay, 3)
        compass[channel][4] = round(Gy, 3)
    except:
        continue

    try:
        compass[channel][2] = round(Az, 3)
        compass[channel][5] = round(Gz, 3)
    except:
        continue



    max_graph = 64
    graph[channel].insert(0, [compass[channel][0], compass[channel][1], compass[channel][2], compass[channel][3], compass[channel][4], compass[channel][5]])
    if len(graph[channel]) > max_graph:
        graph[channel] = graph[channel][:-1]

    x0 = width_32
    y0 = height_16
    button_size = height_64



    if betcalibration == 1:

        if (armsign, digisign) not in calibet:
            calibet[(armsign, digisign)] = []
            mhl[(armsign, digisign)] = []

        if recordcali == 1:

            calichunk = []
            for x in range(8):
                for y in range(3):
                    calichunk.append(round(compass[x][y],1))
            calibet[(armsign, digisign)].append(calichunk)
            if len(calibet[(armsign, digisign)]) > cali_limit:
                calibet[(armsign, digisign)] = calibet[(armsign, digisign)][1:]

            #mhl
            mean = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            high = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            low = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

            if len(calibet[(armsign, digisign)]) > 0:
                digicali_t = text_font.render(str(calibet[(armsign, digisign)][-1]), True, (255, 255, 255))
                WIN.blit(digicali_t, (width_32, height_4 + height_16))

            for x in range(len(calibet[(armsign, digisign)])):
                current_set = calibet[(armsign, digisign)][x]
                for y in range(len(current_set)):
                    mean[y] += current_set[y]

                    if current_set[y] > high[y]:
                        high[y] = current_set[y]

                    if current_set[y] < low[y]:
                        low[y] = current_set[y]

            if len(calibet[(armsign, digisign)]) > 0:
                for y in range(24):
                    mean[y] = round(mean[y]/len(calibet[(armsign, digisign)]),1)

        armcali_t = main_font.render(str(len(calibet[(armsign, digisign)])), True, (255, 255, 255))
        WIN.blit(armcali_t, (width_8 + width_8, height_16))

        armcali_t = main_font.render(str(armbet[digibetu[digisign]][armsign]), True, (255, 255, 255))
        WIN.blit(armcali_t, (width_8 + width_16, height_8))

        digicali_t = main_font.render(str(digibetu[digisign]), True, (255, 255, 255))
        WIN.blit(digicali_t, (width_8 + width_8, height_8))

        digicali_t = text_font.render(str(mean), True, (255, 255, 255))
        WIN.blit(digicali_t, (width_32, height_4 + height_16 * 2))

        digicali_t = text_font.render(str(high), True, (255, 255, 255))
        WIN.blit(digicali_t, (width_32, height_4 + height_16 * 3))

        digicali_t = text_font.render(str(low), True, (255, 255, 255))
        WIN.blit(digicali_t, (width_32, height_4 + height_16 * 4))







    button_size = 64

    #squares
    for x in range(nos):
        y0 = height_32 + height_8*x
        for y in range(6):
            x0 = width_8 + width_16*y
            # value_t = small_font.render(str(compass[x][y]), True, (255, 255, 255))
            # WIN.blit(value_t, (x0, y0))

            if y < 3:
                button_size = abs(compass[x][y]) * 64
            else:
                button_size = abs(compass[x][y]) *2

            if compass[x][y] > 0:
                color = 7
            else:
                color = 1


            ui_b = pygame.Rect(x0 + width_2, y0, button_size, button_size)
            pygame.draw.rect(WIN, value_color[color], ui_b)

    # buttons
        #betcalibration
    x = width_16
    y = height_32
    betcalibration_b = pygame.Rect(x, y, 64, 64)
    pygame.draw.rect(WIN, value_color[8], betcalibration_b)
    betcalibration_t = main_font.render(str(recordcali), True, (255, 255, 255))
    WIN.blit(betcalibration_t, (x + 24 + width_16, y + 8))
    if betcalibration_b.collidepoint((mx, my)):
        betcalibration_t = main_font.render(str(betcalibration), True, (255, 255, 255))
        WIN.blit(betcalibration_t, (x + 24, y + 8))
        if click:
            betcalibration += 1
            betcalibration = betcalibration % 2
            click = False

    #digisign
    x = width_16
    y = height_8
    digisign_b = pygame.Rect(x, y, 64, 64)
    pygame.draw.rect(WIN, value_color[1], digisign_b)
    digisign_t = main_font.render(str(digisign), True, (255, 255, 255))
    WIN.blit(digisign_t, (x + 24 + 64, y + 8))
    if digisign_b.collidepoint((mx, my)):
        digisign_t = main_font.render(str(digisign_s), True, (255, 255, 255))
        WIN.blit(digisign_t, (x + 24, y + 8))
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    digisign = int(digisign_s)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    run = 2

                elif event.key == pygame.K_1:
                    digisign_s += '1'
                elif event.key == pygame.K_2:
                    digisign_s += '2'
                elif event.key == pygame.K_3:
                    digisign_s += '3'
                elif event.key == pygame.K_4:
                    digisign_s += '4'
                elif event.key == pygame.K_5:
                    digisign_s += '5'
                elif event.key == pygame.K_6:
                    digisign_s += '6'
                elif event.key == pygame.K_7:
                    digisign_s += '7'
                elif event.key == pygame.K_8:
                    digisign_s += '8'
                elif event.key == pygame.K_9:
                    digisign_s += '9'
                elif event.key == pygame.K_0:
                    digisign_s += '0'

                elif event.key == pygame.K_BACKSPACE:
                    digisign_s = ''

    #armsign
    x = width_16
    y = height_8 + height_8 - height_32
    armsign_b = pygame.Rect(x, y, 64, 64)
    pygame.draw.rect(WIN, value_color[5], armsign_b)
    armsign_t = main_font.render(str(armsign), True, (255, 255, 255))
    WIN.blit(armsign_t, (x + 24 + 64, y + 8))
    if armsign_b.collidepoint((mx, my)):
        armsign_t = main_font.render(str(armsign_s), True, (255, 255, 255))
        WIN.blit(armsign_t, (x + 24, y + 8))
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    armsign = int(armsign_s)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    run = 2

                elif event.key == pygame.K_1:
                    armsign_s += '1'
                elif event.key == pygame.K_2:
                    armsign_s += '2'
                elif event.key == pygame.K_3:
                    armsign_s += '3'
                elif event.key == pygame.K_4:
                    armsign_s += '4'
                elif event.key == pygame.K_5:
                    armsign_s += '5'
                elif event.key == pygame.K_6:
                    armsign_s += '6'
                elif event.key == pygame.K_7:
                    armsign_s += '7'
                elif event.key == pygame.K_8:
                    armsign_s += '8'
                elif event.key == pygame.K_9:
                    armsign_s += '9'
                elif event.key == pygame.K_0:
                    armsign_s += '0'

                elif event.key == pygame.K_BACKSPACE:
                    armsign_s = ''



    # inputs
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = 2

        click = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                run = 2

            elif event.key == pygame.K_SPACE:
                recordcali += 1
                recordcali = recordcali%2

            elif event.key == pygame.K_UP:
                digisign += 1
                digisign = digisign%32

            elif event.key == pygame.K_DOWN:
                digisign -= 1
                if digisign < 0:
                    digisign  = 0

            elif event.key == pygame.K_RIGHT:
                armsign += 1
                armsign = armsign%31

            elif event.key == pygame.K_LEFT:
                armsign -= 1
                if armsign < 0:
                    armsign = 0

        # keyboard

        # elif event.type == pygame.KEYDOWN:
        #
        #     def type(phrase, letter):
        #         print("letter")
        #
        #         phrase += letter
        #
        #         return phrase
        #
        #
        #     if event.key == pygame.K_ESCAPE:
        #         run = 2
        #
        #     elif event.key == pygame.K_RETURN:
        #
        #         print()
        #         print(lessons[current])
        #         print(phrase)
        #
        #         print(len(lessons[current]))
        #         print(len(phrase))
        #
        #         records['current'] = current
        #
        #         focus = 0
        #
        #         if phrase == lessons[current]:
        #             valid = 3
        #             power[0] += 1
        #         else:
        #             valid = 1
        #             power[0] = 0
        #
        #         clock[1] = clock[0]
        #         clock[0] = time.time()
        #
        #         # records
        #         if valid == 3:
        #
        #             if record == 1:
        #
        #                 if time_0 < records[current]:
        #                     records[current] = time_0
        #                     valid = 4
        #
        #                 filename = 'records/' + record_name
        #                 outfile = open(filename, 'wb')
        #                 pickle.dump(records, outfile)
        #                 outfile.close
        #
        #             current += 1
        #
        #         phrase_1 = phrase[::]
        #         phrase = ''
        #         settings = 0
        #         men = 0
        #
        #
        #     elif event.key == pygame.K_F1:
        #
        #         loop_8(wu, 1, 0, 10)
        #         wu += 1
        #         print("wu")
        #         print(wu)
        #
        #
        #     elif event.key == pygame.K_LEFT:
        #         current -= 1
        #
        #     elif event.key == pygame.K_RIGHT:
        #         current += 1
        #
        #     elif event.key == pygame.K_UP:
        #         ripple_show += 1
        #         ripple_show = ripple_show % 2
        #         power[0] += 1
        #
        #     elif event.key == pygame.K_DOWN:
        #         print('wall')
        #         print(wall)
        #         wall += 1
        #         wall = wall % 2
        #
        #         hail_mary += 1
        #         hail_mary = hail_mary % 2
        #
        #         if valid == 3:
        #
        #             left = 0
        #             right = 0
        #             look_behind = text.index(phrase_c)
        #             look_ahead = text.index(phrase_c)
        #             index_0 = text.index(phrase_c)
        #             while left == 0 or right == 0:
        #
        #                 if text[look_behind] == walls[wall]:
        #                     left = look_behind
        #                 else:
        #                     look_behind = look_behind - 1
        #
        #                 if text[look_ahead] == walls[wall]:
        #                     right = look_ahead
        #                 else:
        #                     look_ahead = look_ahead + 1
        #
        #             if left < 0:
        #                 left = 0
        #
        #             ripple = text[left:right]
        #
        #         power[0] -= 1
        #
        #     # upper
        #     elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'A'
        #
        #     elif event.key == pygame.K_b and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'B'
        #
        #     elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'C'
        #
        #     elif event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'D'
        #
        #     elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'E'
        #
        #     elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'F'
        #
        #     elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'G'
        #
        #     elif event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'H'
        #
        #     elif event.key == pygame.K_i and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'I'
        #
        #     elif event.key == pygame.K_j and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'J'
        #
        #     elif event.key == pygame.K_k and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'K'
        #
        #     elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'L'
        #
        #     elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'M'
        #
        #     elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'N'
        #
        #     elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'O'
        #
        #     elif event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'P'
        #
        #     elif event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'Q'
        #
        #     elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'R'
        #
        #     elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'S'
        #
        #     elif event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'T'
        #
        #     elif event.key == pygame.K_u and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'U'
        #
        #     elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'V'
        #
        #     elif event.key == pygame.K_w and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'W'
        #
        #     elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'X'
        #
        #     elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'Y'
        #
        #     elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += 'Z'
        #
        #     elif event.key == pygame.K_9 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += '('
        #
        #     elif event.key == pygame.K_0 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += ')'
        #
        #     elif event.key == pygame.K_1 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += '!'
        #
        #     # number
        #     elif event.key == pygame.K_0:
        #         phrase += '0'
        #     elif event.key == pygame.K_1:
        #         phrase += '1'
        #     elif event.key == pygame.K_2:
        #         phrase += '2'
        #     elif event.key == pygame.K_3:
        #         phrase += '3'
        #     elif event.key == pygame.K_4:
        #         phrase += '4'
        #     elif event.key == pygame.K_5:
        #         phrase += '5'
        #     elif event.key == pygame.K_6:
        #         phrase += '6'
        #     elif event.key == pygame.K_7:
        #         phrase += '7'
        #     elif event.key == pygame.K_8:
        #         phrase += '8'
        #     elif event.key == pygame.K_9:
        #         phrase += '9'
        #
        #
        #
        #     # lower
        #     elif event.key == pygame.K_a:
        #         phrase += 'a'
        #
        #     elif event.key == pygame.K_b:
        #         phrase += 'b'
        #
        #     elif event.key == pygame.K_c:
        #         phrase += 'c'
        #
        #     elif event.key == pygame.K_d:
        #         phrase += 'd'
        #
        #     elif event.key == pygame.K_e:
        #         phrase += 'e'
        #
        #     elif event.key == pygame.K_f:
        #         phrase += 'f'
        #
        #     elif event.key == pygame.K_g:
        #         phrase += 'g'
        #
        #     elif event.key == pygame.K_h:
        #         phrase += 'h'
        #
        #     elif event.key == pygame.K_i:
        #         phrase += 'i'
        #
        #     elif event.key == pygame.K_j:
        #         phrase += 'j'
        #
        #     elif event.key == pygame.K_k:
        #         phrase += 'k'
        #
        #     elif event.key == pygame.K_l:
        #         phrase += 'l'
        #
        #     elif event.key == pygame.K_m:
        #         phrase += 'm'
        #
        #     elif event.key == pygame.K_n:
        #         phrase += 'n'
        #
        #     elif event.key == pygame.K_o:
        #         phrase += 'o'
        #
        #     elif event.key == pygame.K_p:
        #         phrase += 'p'
        #
        #     elif event.key == pygame.K_q:
        #         phrase += 'q'
        #
        #     elif event.key == pygame.K_r:
        #         phrase += 'r'
        #
        #     elif event.key == pygame.K_s:
        #         phrase += 's'
        #
        #     elif event.key == pygame.K_t:
        #         phrase += 't'
        #
        #     elif event.key == pygame.K_u:
        #         phrase += 'u'
        #
        #     elif event.key == pygame.K_v:
        #         phrase += 'v'
        #
        #     elif event.key == pygame.K_w:
        #         phrase += 'w'
        #
        #     elif event.key == pygame.K_x:
        #         phrase += 'x'
        #
        #     elif event.key == pygame.K_y:
        #         phrase += 'y'
        #
        #     elif event.key == pygame.K_z:
        #         phrase += 'z'
        #
        #     elif event.key == pygame.K_SPACE:
        #         phrase += ' '
        #
        #     elif event.key == pygame.K_PERIOD:
        #         phrase += '.'
        #
        #     elif event.key == pygame.K_COMMA:
        #         phrase += ','
        #
        #     elif event.key == pygame.K_SLASH and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += '?'
        #
        #     elif event.key == pygame.K_EXCLAIM:
        #         phrase += '!'
        #
        #     elif event.key == pygame.K_SEMICOLON and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += ':'
        #
        #     elif event.key == pygame.K_SEMICOLON:
        #         phrase += ';'
        #
        #     elif event.key == pygame.K_QUOTE and pygame.key.get_mods() & pygame.KMOD_SHIFT:
        #         phrase += '"'
        #
        #     elif event.key == pygame.K_QUOTE:
        #         phrase += "'"
        #
        #     elif event.key == pygame.K_MINUS:
        #         phrase += "-"
        #
        #     elif event.key == pygame.K_LEFTBRACKET:
        #         phrase += '['
        #
        #     elif event.key == pygame.K_RIGHTBRACKET:
        #         phrase += ']'
        #
        #
        #
        #
        #
        #     elif event.key == pygame.K_BACKSPACE:
        #         phrase = phrase[:-1]

        # # midi
        # elif event.type in [pygame.midi.MIDIIN]:
        #
        #     # print(event)
        #
        #     clean_e = str(event)[21:-3]
        #     # print(clean_e)
        #     list_e = clean_e.split(',')
        #     ev = []
        #     # print(list_e)
        #
        #     for l in list_e:
        #         ev.append(int(l.split(':')[1]))
        #
        #     if ev[0] == 176:
        #         # print('right')
        #         # print(ev)
        #         glove_values[ev[1]] = ev[2]
        #
        #     if ev[0] == 177:
        #         # print('left')
        #         # print(ev)
        #         glove_values[ev[1] + glove_sensors] = ev[2]

    pygame.display.update()


