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

#quads
poles = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
quadrants = [(1, 1), (1, 1), (1, 1)]

#angles
angles = [0, 0, 0, 0, 0, 0, 0, 0, 0]
tangles = [(0, 0), (0, 0), (0, 0)]
xyz_dict = {0:'X:', 1:'Y:', 2:'Z:'}

#calibration
calibrate = 0
try:
    filename = 'calibrations/mpu_6050_0'
    infile = open(filename, "rb")
    calibrations = pickle.load(infile)
    infile.close
except:
    calibrations = {0:{}, 1:{}, 2:{}}
    for x in range(3):
        for y in range(len(poles)):
            calibrations[x][poles[y]] = {'pop':{}}

#lables
lables = 1

#integrations
integrate = 1
graphs_a = [[0], [0], [0], [0], [0], [0]]
graphs_v = [[0], [0], [0]]
graphs_s = [[0], [0], [0]]
pos = [0, 0, 0]



clock = pygame.time.Clock()

#active
angle_step = 5
angle_max = 1.5 * angle_step
cali_round = 2

#heat map
scale = 12

#calibration
type = 'point'
calibrate = 0
try:
    filename = 'calibrations/mpu_6050_0_' + type + '_step' + str(angle_step) + '_round' + str(cali_round)
    infile = open(filename, "rb")
    calibrations = pickle.load(infile)
    infile.close
except:
    calibrations = {0:{}, 1:{}, 2:{}}
    for x in range(3):
        for y in range(len(poles)):
            calibrations[x][poles[y]] = {'pop':{}}

while run == 1:

    clock.tick()
    WIN.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()

    # Wait for message
    message, address = sock.recvfrom(4096)

    Ax, Ay, Az, Gx, Gy, Gz = unpack('6f', message)

    A = [Ax, Ay, Az]
    G = [Gx, Gy, Gz]


    try:
        angles[0] = int(math.atan(Ay/Az)*angle_step)
        quadrants[0] = (int(Az / abs(Az)), int(Ay / abs(Ay)))
    except:
        continue

    try:
        angles[1] = int(math.atan(Ax/Az)*angle_step)
        quadrants[1] = (int(Az / abs(Az)), int(Ax / abs(Ax)))
    except:
        continue

    try:
        angles[2] = int(math.atan(Ax/Ay)*angle_step)
        quadrants[2] = (int(Ay / abs(Ay)), int(Ax / abs(Ax)))
    except:
        continue

    #angles
    for x in range(3):
        Ar = round(A[x], cali_round)
        if angles[x] > angles[x+3]:
            angles[x+3] = angles[x]
        elif angles[x] < angles[x+6]:
            angles[x+6] = angles[x]

        tangles[x] = (angles[(x+1)%3], angles[(x+2)%3])
        if tangles[x] == (0, 0):
            tangles0 = (0, 0, angles[x])

            if tangles0 == (0, 0, 0):
                continue
            else:
                tangles[x] = tangles0




        if calibrate == 1:
            if tangles[x] in calibrations[x][quadrants[x]]:
                if Ar in calibrations[x][quadrants[x]][tangles[x]]:
                    calibrations[x][quadrants[x]][tangles[x]][Ar] += 1
                else:
                    calibrations[x][quadrants[x]][tangles[x]][Ar] = 1

            else:
                calibrations[x][quadrants[x]][tangles[x]] = {Ar:1}

            cali_pop = sorted(calibrations[x][quadrants[x]][tangles[x]].items(), key=lambda x: x[1], reverse=True)[0]
            calibrations[x][quadrants[x]]['pop'][tangles[x]] = cali_pop
            calibrations[x][quadrants[x]]['pop'] = dict(sorted(calibrations[x][quadrants[x]]['pop'].items(), key=lambda x:x[1][1], reverse=True))

            filename = 'calibrations/mpu_6050_0_' + type + '_step' + str(angle_step) + '_round' + str(cali_round)
            outfile = open(filename, 'wb')
            pickle.dump(calibrations, outfile)
            outfile.close

    #graph
    graph_max = 100
    for x in range(3):


        graphs_a[x].append(A[x]-calibrations[x][quadrants[x]]['pop'][tangles[x]][0])
        graphs_a[x+3].append(calibrations[x][quadrants[x]]['pop'][tangles[x]][0])

        if len(graphs_a[x]) > graph_max:
            graphs_a[x] = graphs_a[x][1::]
            graphs_a[x+3] = graphs_a[x+3][1::]

        graphs_v[x].append(sum(graphs_a[x]))
        if len(graphs_v[x]) > graph_max:
            graphs_v[x] = graphs_v[x][1::]

        graphs_s[x].append(sum(graphs_v[x]))
        if len(graphs_s[x]) > graph_max:
            graphs_s[x] = graphs_s[x][1::]

        pos[x] += (graphs_s[x][-1]/100)


    #display
    time_t = main_font.render(str(int(clock.get_fps())), True, (255, 255, 255))
    WIN.blit(time_t, (WIDTH-width_16, height_16))

    #lables
    for x in range(3):

        #heat map
        if calibrate == 1:
            for y in range(len(poles)):
                for z in range(len(calibrations[x][poles[y]]['pop'])):
                    pop_cord = list(calibrations[x][poles[y]]['pop'].keys())[z]
                    x0 = width_8 + width_16 + pop_cord[0]*scale + scale*40*x + scale*angle_max*poles[y][0]
                    y0 = height_2 - pop_cord[1]*scale - scale*angle_max*poles[y][1]
                    if len(pop_cord) > 2:
                        x0 = width_4 + width_16 + width_32 + scale*angle_max*poles[y][0] + pop_cord[2]*scale
                        y0 = height_4 + x*scale
                    calibrate_button = pygame.Rect(x0, y0, scale, scale)

                    shade = (calibrations[x][poles[y]]['pop'][list(calibrations[x][poles[y]]['pop'].keys())[z]][1])
                    color = (0, 0, shade)
                    if shade > 255:
                        color = (255, 255, 0)
                        shade = 255

                    if quadrants[x] == poles[y] and pop_cord == tangles[x]:
                        color = (255, 0, shade)
                        if shade == 255:
                            color = (0, 255, 0)


                    pygame.draw.rect(WIN, color, calibrate_button)


        #graphs
        if integrate == 1:
            for y in range(len(graphs_a[x])):
                graph_scale = 3
                #acceleration & calibration
                x0 = width_16 + y*graph_scale
                y0 = height_4 - graphs_a[x][y]*graph_scale**2 + x*200
                graph_point = pygame.Rect(x0, y0, graph_scale, graph_scale)
                pygame.draw.rect(WIN, value_color[1], graph_point)
                x0 = width_16 + y*graph_scale
                y0 = height_4 - graphs_a[x+3][y]*graph_scale**2 + x*200
                graph_point = pygame.Rect(x0, y0, graph_scale, graph_scale)
                pygame.draw.rect(WIN, value_color[2], graph_point)

                graph_scale = 5
                #velocity
                x0 = width_8 + width_8 + y
                y0 = height_4 - graphs_v[x][y]*2 + x*200
                graph_point = pygame.Rect(x0, y0, graph_scale, graph_scale)
                pygame.draw.rect(WIN, value_color[3 + x], graph_point)

                graph_scale = 4
                #speed
                x0 = width_4 + width_8 + y
                y0 = height_4 - graphs_s[x][y]/100 + x*200
                graph_point = pygame.Rect(x0, y0, graph_scale, graph_scale)
                pygame.draw.rect(WIN, value_color[6 + x], graph_point)

                graph_scale = 4
                #pos
                x0 = width_2 + pos[x]*100
                y0 = height_4 + x*200
                graph_point = pygame.Rect(x0, y0, graph_scale, graph_scale)
                pygame.draw.rect(WIN, value_color[6 + x], graph_point)

        #values
        if lables == 1:
            time_t = main_font.render('X:' + str(Ax), True, (255, 255, 255))
            WIN.blit(time_t, (10, 10))
            time_t = main_font.render('Y:' + str(Ay), True, (255, 255, 255))
            WIN.blit(time_t, (10, 64))
            time_t = main_font.render('Z:' + str(Az), True, (255, 255, 255))
            WIN.blit(time_t, (10, 128))

            time_t = main_font.render(str(round(graphs_a[x][-1], 3)), True, (255, 255, 255))
            WIN.blit(time_t, (width_8 + width_16, 10 + height_16*x))
            time_t = main_font.render(str(round(graphs_v[x][-1], 3)), True, (255, 255, 255))
            WIN.blit(time_t, (width_4, 10 + height_16*x))
            time_t = main_font.render(str(round(graphs_s[x][-1], 3)), True, (255, 255, 255))
            WIN.blit(time_t, (width_4 + width_16, 10 + height_16*x))


            spacing = 64

            #angles
            x0 = width_2
            for x in range(3):

                time_t = main_font.render(xyz_dict[x], True, (255, 255, 255))
                WIN.blit(time_t, (x0, height_128 + spacing * x))

                time_t = main_font.render(str(angles[x]), True, (255, 255, 255))
                WIN.blit(time_t, (x0 + width_16, height_128 + spacing * x))

                time_t = main_font.render(str(angles[x + 3]), True, (255, 255, 255))
                WIN.blit(time_t, (x0 + width_8, height_128 + spacing * x))

                time_t = main_font.render(str(angles[x + 6]), True, (255, 255, 255))
                WIN.blit(time_t, (x0 + width_8 + width_16, height_128 + spacing * x))

                time_t = main_font.render(str(quadrants[x]), True, (255, 255, 255))
                WIN.blit(time_t, (x0 + width_4, height_128 + spacing * x))

                if calibrate == 1:
                    cali_pop = calibrations[x][quadrants[x]]['pop'][tangles[x]]

                    time_t = main_font.render(str(tangles[x]),True, (255, 255, 255))
                    WIN.blit(time_t, (width_64, height_2 + height_4 + spacing * x))
                    time_t = main_font.render(str(cali_pop[0]),True, (255, 255, 255))
                    WIN.blit(time_t, (width_32 + width_16, height_2 + height_4 + spacing * x))
                    time_t = main_font.render(str(cali_pop[1]),True, (255, 255, 255))
                    WIN.blit(time_t, (width_32 + width_8, height_2 + height_4 + spacing * x))




    #acc angle
    x = width_8
    y = height_2 + height_4 + height_8
    x_1 = x + Az*100
    y_1 = y - Ay*100
    pygame.draw.line(WIN, value_color[3], (x, y), (x_1, y_1), 4)

    x = width_4
    x_1 = x + Az*100
    y_1 = y - Ax*100
    pygame.draw.line(WIN, value_color[3], (x, y), (x_1, y_1), 4)

    x = width_4 + width_8
    x_1 = x + Ay*100
    y_1 = y - Ax*100
    pygame.draw.line(WIN, value_color[3], (x, y), (x_1, y_1), 4)

    for i in range(3):

        x = width_2 + width_8 + width_8*i
        y = height_2 + height_4 + height_16
        x_1 = x
        y_1 = y - A[i]*100
        pygame.draw.line(WIN, value_color[4], (x, y), (x_1, y_1), 6)

        if calibrate == 1:
            x = width_2 + width_8 + width_8*i
            y = height_2 + height_4 + height_16
            x_1 = x
            y_1 = y - calibrations[i][quadrants[i]]['pop'][tangles[i]][0]*100
            pygame.draw.line(WIN, value_color[5], (x, y), (x_1, y_1), 4)


    #buttons
    x = WIDTH - width_8 - width_32
    y = height_8
    calibrate_button = pygame.Rect(x, y, width_8 - width_64, height_16)
    pygame.draw.rect(WIN, value_color[4], calibrate_button)
    calibrate_button = pygame.Rect(x+2, y+2, width_8 - width_64-4, height_16-4)
    pygame.draw.rect(WIN, value_color[0], calibrate_button)
    if calibrate_button.collidepoint((mx, my)):
        record_t = main_font.render('calibrate: ' + str(calibrate), True, value_color[7])
        WIN.blit(record_t, (x+width_128, y+height_128))
        if click:
            calibrate = (calibrate + 1)%2
            click = False

    x = WIDTH - width_8 - width_32
    y = height_8 + height_8
    lable_button = pygame.Rect(x, y, width_8 - width_64, height_16)
    pygame.draw.rect(WIN, value_color[5], lable_button)
    lable_button = pygame.Rect(x+2, y+2, width_8 - width_64-4, height_16-4)
    pygame.draw.rect(WIN, value_color[0], lable_button)
    if lable_button.collidepoint((mx, my)):
        record_t = main_font.render('lable: ' + str(lables), True, value_color[7])
        WIN.blit(record_t, (x+width_128, y+height_128))
        if click:
            lables= (lables + 1)%2
            click = False

    x = WIDTH - width_8 - width_32
    y = height_4 + height_8
    integrate_button = pygame.Rect(x, y, width_8 - width_64, height_16)
    pygame.draw.rect(WIN, value_color[3], integrate_button)
    integrate_button = pygame.Rect(x+2, y+2, width_8 - width_64-4, height_16-4)
    pygame.draw.rect(WIN, value_color[0], integrate_button)
    if integrate_button.collidepoint((mx, my)):
        record_t = main_font.render('integrate: ' + str(integrate), True, value_color[7])
        WIN.blit(record_t, (x+width_128, y+height_128))
        if click:
            integrate= (integrate + 1)%2
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