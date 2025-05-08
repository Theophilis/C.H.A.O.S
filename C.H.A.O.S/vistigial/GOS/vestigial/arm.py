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



#digibet
digibet_0 = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, ',': 14, '!': 15,
           '?': 16, '.': 17, '"': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}

digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, 'an': 14, 'er': 15,
           'ou': 16, 'in': 17, 'th': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}

digibetu = {v: k for k, v in digibet.items()}

#armbet
filename = '../bets/armbet_2'
infile = open(filename, "rb")
armbet = pickle.load(infile)
infile.close

print()
for d in digibet:
    print(armbet[d])


click = False

value_color = {0: (0, 0, 0), 1: (255, 0, 0), 2: (255, 255, 0), 3: (0, 255, 0), 4: (0, 255, 255), 5: (0, 0, 255),
               6: (255, 0, 255), 7: (255, 255, 255), 8: (127, 127, 127)}

run = 1
#number_of_sensors
nos = 8

clock = pygame.time.Clock()

glove_name = 'arm'
glove_values = [[0, [0, 0, 0, 0, 0, 0]] for x in range(nos)]
sensor_order = ['arm', 'wrist', 'hand', 'thumb', 'index', 'middle', 'ring', 'pinky']

sensor_order = ['arm', 'wrist', 'hand', 'pinky', 'ring', 'middle', 'index', 'thumb']

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
                   'UD':{0:1, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2}}

#alm
if glove_name == 'alm':
    orientation = {'FB':{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0},
                   'LR':{0:1, 1:2, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1},
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

#analytics
analytics = 1

compass = [[0, 0, 0, 0, 0, 0] for x in range(nos)]
g_time = [[time.time(), 0] for x in range(nos)]
gyros = [1 for x in range(nos)]


cali_range = [16, 32, 32, 48, 48, 48, 48, 48]
calibrations = [240, 180, 180, 180, 180, 180, 180, 180]
switches = [1 for x in range(nos + 1)]

#typewriter
typwrite = 1
letter_value = 0
arm_value = 0
av0 = ''
av1 = ''
phrase = ':'

pause = 0
timer = time.time()
cadence = 3

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

    gyros[channel] = int(Gx)

    #compass
    try:
        compass[channel][0] = 180 + int(math.degrees(math.atan2(Ay, Az)))
        compass[channel][3] += Gx * (g_time[channel][0] - g_time[channel][1])
    except:
        continue

    try:
        compass[channel][1] = 180 + int(math.degrees(math.atan2(Ax, Az)))
        compass[channel][4] += Gy * (g_time[channel][0] - g_time[channel][1])
    except:
        continue

    try:
        compass[channel][2] = 180 + int(math.degrees(math.atan2(Ax, Ay)))
        compass[channel][5] += Gz * (g_time[channel][0] - g_time[channel][1])
    except:
        continue


    #switch
    av = compass[0][orientation['FB'][0]]
    wv = compass[1][orientation['FB'][1]]
    hv = compass[2][orientation['FB'][2]]

    #fingers
    for x in range(5):
        fv = compass[x + 3][orientation['FB'][x + 3]]

        gap = abs(hv-fv)

        if gap < cali_range[x+3] or gap > 360-cali_range[x+3]:
            switches[x+3] = 1
        else:
            switches[x+3] = 0

    #hand
    gap = abs(wv-hv)
    if gap < cali_range[2] or gap > 360-cali_range[2]:
        switches[2] = 0
        #
    else:
        switches[2] = 1
        #

    #wrist
    if abs(wv-calibrations[1]) < cali_range[1] or abs(wv-calibrations[1]) > 360-cali_range[1]:
        switches[1] = 0
        #
    else:
        switches[1] = 1
        #

    #arm
    if abs(av-calibrations[0]) < cali_range[0]:
        switches[0] = 0
        #
    else:
        switches[0] = 1
        #

    #up/down
    if glove_values[1][1][2] < 0:
        switches[8] = 0
        calibrations[1] = 0
    else:
        switches[8] = 1
        calibrations[1] = 180

    letter_value = switches[7] + switches[6]*2 + switches[5]*4 + switches[4]*8 + switches[3]*16
    # letter_value = switches[3] + switches[4]*2 + switches[5]*4 + switches[6]*8 + switches[7]*16
    arm_value = switches[0]*2 + switches[1] + switches[8]*4 + switches[2]*8

    #calibration
    x0 = WIDTH - width_8
    y0 = height_16
    button_size = 64

    #cali_button
    cali_b = pygame.Rect(x0, y0, button_size, button_size)
    pygame.draw.rect(WIN, value_color[4], cali_b)
    if cali_b.collidepoint((mx, my)):
        if click:
            for x in range(nos):
                calibrations[x] = compass[x][orientation['FB'][x]]
            click = False


    #value print
    x0 = width_32
    y0 = height_8
    bar_width = 32
    bar_height = 32

    if analytics == 1:


        for x in range(nos):

            value_t = small_font.render(str(compass[x][orientation['FB'][x]]), True, (255, 255, 255))
            WIN.blit(value_t, (x0 + bar_width*2*x, y0))

            value_t = small_font.render(str(calibrations[x]), True, (255, 255, 255))
            WIN.blit(value_t, (x0 + bar_width*2*x, y0 + bar_height))

            gv = compass[x][orientation['FB'][x]]

            gyrui_b = pygame.Rect(x0 + bar_width*2*x, y0 + height_8, bar_width, gv)
            pygame.draw.rect(WIN, value_color[4], gyrui_b)

            #switches
            switch_b = pygame.Rect(x0 + bar_width*2*x, y0 + height_2, bar_width, bar_height)
            pygame.draw.rect(WIN, value_color[switches[x]*7], switch_b)


        #rotation
        rot_v = glove_values[1][1][2]
        value_t = small_font.render(str(round(rot_v, 3)), True, (255, 255, 255))
        WIN.blit(value_t, (x0 + bar_width*2*8, y0 + bar_height))

        #bar
        gyrui_b = pygame.Rect(x0 + bar_width * 2 * 8, y0 + height_8, bar_width, abs(rot_v*300))
        pygame.draw.rect(WIN, value_color[4 - switches[8]*3], gyrui_b)

        # switch
        switch_b = pygame.Rect(x0 + bar_width * 2 * 8, y0 + height_2 + height_8, bar_width, bar_height)
        pygame.draw.rect(WIN, value_color[switches[8] * 7], switch_b)

    if typwrite == 1:
        #digibet
        letter = digibetu[letter_value]

        value_t = lable_font.render(str(letter_value), True, (255, 255, 255))
        WIN.blit(value_t, (x0 + bar_width*2*15, y0 + bar_height))
        value_t = lable_font.render(str(digibetu[letter_value]), True, (255, 255, 255))
        WIN.blit(value_t, (x0 + bar_width*2*16, y0 + bar_height))

        #armbet
        av = armbet[letter][arm_value%len(armbet[letter])]

        value_t = lable_font.render(str(arm_value), True, (255, 255, 255))
        WIN.blit(value_t, (x0 + bar_width*2*15, y0 + bar_height * 3))
        value_t = lable_font.render(str(av), True, (255, 255, 255))
        WIN.blit(value_t, (x0 + bar_width*2*16, y0 + bar_height * 3))

        t0 = time.time()
        if av == av1:
            if t0 - timer > cadence:
                if av != av0:
                    if av == '!':
                        phrase = phrase[:-2]

                    elif av == '?':
                        phrase = ':'

                    elif letter == ' ':
                        phrase += ' '
                        av0 = av
                        timer = t0

                        if switches[8] == 1:
                            phrase = phrase[:-2]
                            if switches[1] == 1:
                                phrase = ':'


                    else:
                        phrase += av
                        av0 = av
                        timer = t0
        else:
            av1 = av
            timer = t0


    value_t = lable_font.render(str(round(t0-timer, 3)), True, (255, 255, 255))
    WIN.blit(value_t, (x0 + bar_width*2*16, y0 - height_16))

    value_t = lable_font.render(str(phrase), True, (255, 255, 255))
    WIN.blit(value_t, (x0 + bar_width*2*12, y0 + bar_height * 5))

    #typing button
    typ_b = pygame.Rect(x0, y0 - height_16, button_size, button_size)
    pygame.draw.rect(WIN, value_color[1], typ_b)
    if typ_b.collidepoint((mx, my)):
        if click:
            typwrite += 1
            typwrite = typwrite % 2
            print('click')
            click = False

    #analytics button
    ana_b = pygame.Rect(x0 + button_size*2, y0-height_16, button_size, button_size)
    pygame.draw.rect(WIN, value_color[1], ana_b)
    if ana_b.collidepoint((mx, my)):
        if click:
            analytics += 1
            analytics = analytics % 2
            print('click')
            click = False

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


