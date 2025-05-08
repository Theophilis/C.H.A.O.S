import socket
import pickle
from struct import unpack
import pygame
import math

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
               6: (255, 0, 255), 7: (255, 255, 255), 8: (127, 127, 127)}

run = 1
number_of_sensors = 8
AC = [[(0, 0, 0), [(0, (1, 1)), (0, (1, 1)), (0, (1, 1))]] for n in range(number_of_sensors)]



#chaotomata
orientation = {'FB':{0:1, 1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0},
               'LR':{0:0, 1:0, 2:0, 3:1, 4:1, 5:1, 6:1, 7:1},
               'UD':{0:2, 1:2, 2:2, 3:3, 4:3, 5:2, 6:2, 7:2}}
#gos
orientation = {'FB':{0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0},
               'LR':{0:0, 1:0, 2:0, 3:1, 4:1, 5:1, 6:1, 7:1},
               'UD':{0:2, 1:2, 2:2, 3:3, 4:3, 5:2, 6:2, 7:2}}

positions = {'FB':[0, 0, 0, 0, 0, 0, 0, 0],
             'LR':[0, 0, 0, 0, 0, 0, 0, 0],
             'UD':[0, 0, 0, 0, 0, 0, 0, 0]}

midpoints = {'FB':[0, 0, 0, 0, 0, 0, 0, 0],
             'LR':[0, 0, 0, 0, 0, 0, 0, 0],
             'UD':[0, 0, 0, 0, 0, 0, 0, 0]}
deadpoints = {'FB':[0, 0, 0, 0, 0, 0, 0, 0],
             'LR':[0, 0, 0, 0, 0, 0, 0, 0],
             'UD':[0, 0, 0, 0, 0, 0, 0, 0]}

switches = {'FB':[0, 0, 0, 0, 0, 0, 0, 0],
            'LR':[0, 0, 0, 0, 0, 0, 0, 0],
            'UD':[0, 0, 0, 0, 0, 0, 0, 0]}
zones = {'FB':[0, 0, 0, 0, 0, 0, 0, 0],
            'LR':[0, 0, 0, 0, 0, 0, 0, 0],
            'UD':[0, 0, 0, 0, 0, 0, 0, 0]}

calibrations = {'FB': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'LR': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'UD': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]}



#calibrations
glove_name = 'chaotomata'
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




#quads
poles = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
quadrants = [(1, 1), (1, 1), (1, 1)]

#angles
angles = [0, 0, 0, 0, 0, 0, 0, 0]
tangles = [(0, 0), (0, 0), (0, 0)]
xyz_dict = {0:'X:', 1:'Y:', 2:'Z:'}


#lables
Ascale = 1
lables = 0


clock = pygame.time.Clock()

#active
angle_step = 1
angle_max = 1.5 * angle_step
cali_round = 2

#heat map
scale = 12

#typing
signing = 0
toggle = 0
digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, ',': 14, '"': 15,
           '/': 16, '.': 17, '?': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}
digibetu = {v: k for k, v in digibet.items()}

letter_value = 0
phrase = ''
almanac = []

while run == 1:

    clock.tick()
    WIN.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()

    # Wait for message
    message, address = sock.recvfrom(4096)

    Ax, Ay, Az, channel = unpack('4f', message)
    channel = int(channel)


    #angle
    try:
        angles[0] = math.atan2(Ay, Az)
    except:
        continue

    try:
        angles[1] = math.atan2(Ax, Az)
    except:
        continue

    try:
        angles[2] = math.atan2(Ax, Ay)
    except:
        continue

    #positions
    positions['FB'][channel] = 180 + int(math.degrees(angles[orientation['FB'][channel]]))


    #typing
    if signing == 1:
        letter_value = 0
        letter_value += switches['FB'][7] * 1 + switches['FB'][6] * 2 + switches['FB'][5] * 4 + switches['FB'][4] * 8 + switches['FB'][3] * 16

        if switches['FB'][1] != toggle:
            phrase += digibetu[letter_value]
            toggle = switches['FB'][1]

            if letter_value == 15:
                almanac.append(phrase)
                phrase = ''
            if letter_value == 16:
                try:
                    phrase = phrase[:-2]
                except:
                    continue

        #display
        time_t = main_font.render(str(digibetu[letter_value]), True, (255, 255, 255))
        WIN.blit(time_t, (width_2, height_8))

        time_t = main_font.render('{' + str(phrase) + '}', True, (255, 255, 255))
        WIN.blit(time_t, (width_2 - int(time_t.get_width() / 2), height_16))

        for x in range(len(almanac)):
            time_t = main_font.render('{' + str(almanac[x]) + '}', True, (255, 255, 255))
            WIN.blit(time_t, (width_2 - int(time_t.get_width() / 2), height_16 + height_8*x))


    x0 = width_32
    y0 = height_16
    x_space = width_8
    y_space = height_32 + height_64
    for x in range(number_of_sensors):

        # calibration
        if x == 0:
            calibrations['FB'][x][0] = revelations['FB'][x][0]
            calibrations['FB'][x][1] = revelations['FB'][x][1]
        elif x == 1:
            # shift0 = -(relatives['FB'][0] - revelations['FB'][x][2])
            # shift1 = -(relatives['FB'][0] - revelations['FB'][x][3])
            calibrations['FB'][x][0] = revelations['FB'][x][0]
            calibrations['FB'][x][1] = revelations['FB'][x][1]
        elif x == 2:
            shift0 = positions['FB'][1] - revelations['FB'][x][4]
            shift1 = positions['FB'][1] - revelations['FB'][x][5]
            calibrations['FB'][x][0] = revelations['FB'][x][0] + shift0
            calibrations['FB'][x][1] = revelations['FB'][x][1] + shift1
        else:
            shift0 = positions['FB'][2] - revelations['FB'][x][6]
            shift1 = positions['FB'][2] - revelations['FB'][x][7]
            calibrations['FB'][x][0] = revelations['FB'][x][0] + shift0
            calibrations['FB'][x][1] = revelations['FB'][x][1] + shift1

        # midpoints
        midpoints['FB'][x] = calibrations['FB'][x][1] + int((calibrations['FB'][x][0] - calibrations['FB'][x][1]) / 2)
        deadpoints['FB'][x] = (midpoints['FB'][x]+180)%360

        if midpoints['FB'][x] > deadpoints['FB'][x]:
            if positions['FB'][x] < midpoints['FB'][x] and positions['FB'][x] > deadpoints['FB'][x]:
                switches['FB'][x] = 1
            else:
                switches['FB'][x] = 0
        else:
            if positions['FB'][x] > midpoints['FB'][x] and positions['FB'][x] < deadpoints['FB'][x]:
                switches['FB'][x] = 0
            else:
                switches['FB'][x] = 1

        x=x

        if Ascale == 1:

            # positions
            pos_t = small_font.render(str(positions['FB'][x]), True, (255, 255, 255))
            WIN.blit(pos_t, (x0 + x_space * x, y0))

            # zones
            zone_t = small_font.render(str(zones['FB'][x]), True, (255, 255, 255))
            WIN.blit(zone_t, (x0 + x_space * x, y0 + y_space))

            #stand
            pos_stand = pygame.Rect(x0 + x_space*x, y0 + y_space*7, 8, 360)
            pygame.draw.rect(WIN, value_color[1], pos_stand)

            # mark
            pos_mark = pygame.Rect(x0 + x_space * x, y0 + y_space*7 + positions['FB'][x]%360, 64, 4)
            pygame.draw.rect(WIN, value_color[2], pos_mark)

            # cali
            pos_cali = pygame.Rect(x0 + x_space * x, y0 + y_space*7 + calibrations['FB'][x][0]%360, 32, 4)
            pygame.draw.rect(WIN, value_color[3], pos_cali)
            pos_cali = pygame.Rect(x0 + x_space * x, y0 + y_space*7 + calibrations['FB'][x][1]%360, 32, 4)
            pygame.draw.rect(WIN, value_color[3], pos_cali)

            # midpoint
            pos_mark = pygame.Rect(x0 + x_space * x, y0 + y_space*7 + midpoints['FB'][x]%360, 64, 4)
            pygame.draw.rect(WIN, value_color[4], pos_mark)
            # deadpoint
            pos_mark = pygame.Rect(x0 + x_space * x, y0 + y_space*7 + deadpoints['FB'][x]%360, 64, 4)
            pygame.draw.rect(WIN, value_color[5], pos_mark)

            # high calibration
            cali_high = pygame.Rect(x0 + x_space * x, y0 + y_space*7 + 380, 48, 48)
            pygame.draw.rect(WIN, value_color[7], cali_high)
            if cali_high.collidepoint((mx, my)):
                if click:
                    revelations['FB'][x][1] = positions['FB'][x]

                    if x > 0:
                        revelations['FB'][x][3] = positions['FB'][0]
                    if x > 1:
                        revelations['FB'][x][5] = positions['FB'][1]
                    if x > 2:
                        revelations['FB'][x][7] = positions['FB'][2]

                    filename = 'calibrations/' + glove_name
                    outfile = open(filename, 'wb')
                    pickle.dump(revelations, outfile)
                    outfile.close

            # low calibration
            cali_low = pygame.Rect(x0 + x_space * x, y0 + y_space*8 + 380, 48, 48)
            pygame.draw.rect(WIN, value_color[8], cali_low)
            if cali_low.collidepoint((mx, my)):
                if click:
                    revelations['FB'][x][0] = positions['FB'][x]

                    if x > 0:
                        revelations['FB'][x][2] = positions['FB'][0]
                    if x > 1:
                        revelations['FB'][x][4] = positions['FB'][1]
                    if x > 2:
                        revelations['FB'][x][6] = positions['FB'][2]


                    filename = 'calibrations/' + glove_name
                    outfile = open(filename, 'wb')
                    pickle.dump(revelations, outfile)
                    outfile.close

            #switches
            switch_sign = pygame.Rect(x0 + x_space * x, y0 + y_space*5, 32, 32)
            pygame.draw.rect(WIN, value_color[7*switches['FB'][x]], switch_sign)




    #display
    # time_t = main_font.render(str(int(clock.get_fps())), True, (255, 255, 255))
    # WIN.blit(time_t, (WIDTH-width_32, height_128))
    #
    # time_t = main_font.render(str(letter_value), True, (255, 255, 255))
    # WIN.blit(time_t, (width_2, height_8 + height_16))
    #
    # time_t = main_font.render(str(digibetu[letter_value]), True, (255, 255, 255))
    # WIN.blit(time_t, (width_2, height_8))
    #
    # time_t = main_font.render('{' + str(phrase) + '}', True, (255, 255, 255))
    # WIN.blit(time_t, (width_2 - int(time_t.get_width()/2), height_16))

    # time_t = main_font.render(str((int(Ax*10))), True, (255, 255, 255))
    # WIN.blit(time_t, (width_2, height_2))
    # time_t = main_font.render(str((int(Ay*10))), True, (255, 255, 255))
    # WIN.blit(time_t, (width_2, height_2 + height_16))
    # time_t = main_font.render(str((int(Az*10))), True, (255, 255, 255))
    # WIN.blit(time_t, (width_2, height_2 + height_8))



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


