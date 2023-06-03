import numpy as np
import pygame
from pygame import MOUSEBUTTONDOWN, K_ESCAPE
import pygame.constants

pygame.font.init()
pygame.init()
pygame.display.init()
current_display = pygame.display.Info()
WIDTH, HEIGHT = 1600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("C.H.A.O.S")
click = False

text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
title_font = pygame.font.SysFont("leelawadeeuisemilight", 64)

# wall_1 = [8, 4]
# size = 9
# fsi = 2
# scale = 4.25
#
# for x in range(2):
#     wall_1[x] = int((wall_1[x] * 12)/4.25)
#
# wall = np.zeros((wall_1[1], wall_1[0]), dtype='uint8')
#
# print("")
# print("wall")
# print(wall_1)
# print(wall)
# for fsi in range(1, 5):
#     for x in range(wall_1[0]):
#         for y in range(wall_1[1]):
#             if x >= y:
#                 # print(x, y)
#                 wall[y, x] = int((x + 1)/fsi)
#             else:
#                 # print(x, y)
#                 wall[y, x] = int((y+1)/fsi)
#
#     print("fsi")
#     print(fsi)
#     print(wall)

def Chaos_Window():

    run = 1

    def redraw_window():

        mx, my = pygame.mouse.get_pos()


        pygame.display.update()

    wall_1 = [54, 12]
    walls = [36, 12]
    fsi = 15
    scale = 4.25
    tile_size = 8
    shade = fsi
    offset = 50

    for x in range(2):
        wall_1[x] = int((wall_1[x] * 12) / scale)

    wall_x = np.zeros((wall_1[1], wall_1[0]), dtype='uint8')


    for x in range(wall_1[0]):
        for y in range(wall_1[1]):
            if x >= y:
                # print(x, y)
                wall_x[wall_1[1] - y - 1, x] = int((x) / fsi) + 1
            else:
                # print(x, y)
                wall_x[wall_1[1] - y - 1, x] = int((y) / fsi) + 1






    for x in range(2):
        walls[x] = int((walls[x] * 12) / scale)

    wall_y = np.zeros((walls[1], walls[0]), dtype='uint8')

    for x in range(walls[0]):
        for y in range(walls[1]):
            if x >= y:
                # print(x, y)
                wall_y[walls[1] - y - 1, x] = int((x) / fsi) + 1
            else:
                # print(x, y)
                wall_y[walls[1] - y - 1, x] = int((y) / fsi) + 1

    for x in range(walls[0]):

        if x % 8 == 0:
            min_burn = small_font.render(str(wall_y[walls[1] - 1, x]) + ",", 1, (255, 255, 255))
            WIN.blit(min_burn, (x * tile_size + min_burn.get_width(), (walls[1] * (tile_size) + 10) * 2 + offset))

        for y in range(walls[1]):
            tile = pygame.Rect(10 + (x * (tile_size)), 10 + (y * (tile_size)) +walls[1] * (tile_size) + offset, tile_size, tile_size)
            pygame.draw.rect(WIN, ((shade * wall_y[y, x])%255, (shade * wall_y[y, x])%255, (shade * wall_y[y, x])%255), tile)


    #main loop
    while run == 1:

        redraw_window()
        WIN.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()

        #walls
        for x in range(wall_1[0]):

            if x % 8 == 0:
                min_burn = small_font.render(str(wall_x[wall_1[1] - 1, x]) + ",", 1, (255, 255, 255))
                WIN.blit(min_burn, (x * tile_size + min_burn.get_width(), (wall_1[1] * (tile_size) + 10)))

            for y in range(wall_1[1]):
                tile = pygame.Rect(10 + (x * (tile_size)), 10 + (y * (tile_size)), tile_size, tile_size)
                pygame.draw.rect(WIN, (
                (shade * wall_x[y, x]) % 255, (shade * wall_x[y, x]) % 255, (shade * wall_x[y, x]) % 255), tile)
        for x in range(walls[0]):

            if x % 8 == 0:
                min_burn = small_font.render(str(wall_y[walls[1] - 1, x]) + ",", 1, (255, 255, 255))
                WIN.blit(min_burn, (x * tile_size + min_burn.get_width(), (walls[1] * (tile_size) + 10) * 2 + offset))

            for y in range(walls[1]):
                tile = pygame.Rect(10 + (x * (tile_size)), 10 + (y * (tile_size)) + walls[1] * (tile_size) + offset,
                                   tile_size, tile_size)
                pygame.draw.rect(WIN, (
                (shade * wall_y[y, x]) % 255, (shade * wall_y[y, x]) % 255, (shade * wall_y[y, x]) % 255), tile)

        fsi_l = title_font.render(str(fsi), 1, (255, 255, 255))
        WIN.blit(fsi_l, (WIDTH - fsi_l.get_width() - 50, 10))

        wall_1_l = title_font.render(str(wall_1), 1, (255, 255, 255))
        WIN.blit(wall_1_l, (tile_size * wall_1[0] + 10, wall_1[1] * tile_size/2))
        walls_l = title_font.render(str(walls), 1, (255, 255, 255))
        WIN.blit(walls_l, (tile_size * walls[0] + 10, (walls[1] * tile_size/2 + offset) * 2))


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            #keyboard
            if event.type == pygame.KEYDOWN:

                if event.key == K_ESCAPE:
                    run = 2


Chaos_Window()







