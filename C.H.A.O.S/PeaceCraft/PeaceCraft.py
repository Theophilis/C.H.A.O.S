import numpy as np
import pygame

#####game#####

pygame.init()
pygame.display.init()
current_display = pygame.display.Info()
WIDTH, HEIGHT = current_display.current_w - 50, current_display.current_h - 100
# WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)

def Chaos_Window():

    print(HEIGHT, WIDTH)

    run = 1
    rule = 90
    base = 2
    view = 3
    bv = base ** view
    bbv = base ** base ** view

    path = []
    click_color = np.zeros((16), dtype='uint8')

    value_color = {0:(0, 0, 0), 1:(255, 255, 255), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255), 6:(255, 0, 255), 7:(255, 255, 255)}

    rule_d = {}
    height = HEIGHT-1
    width = WIDTH
    width_3 = width*3
    tile_h = 101
    tile_w = 101
    tile_w3 = tile_w*3

    block = np.zeros((height*width*3), dtype='uint8')
    block[int(width/2*3)-1] = 255
    block[int(width/2*3)] = 255
    block[int(width/2*3)+1] = 255

    tile = np.zeros((tile_h*tile_w*3), dtype='uint8')
    tile[int(tile_w/2*3)-1] = 255
    tile[int(tile_w/2*3)] = 255
    tile[int(tile_w/2*3)+1] = 255

    xset = 650
    yset = 300
    xyset = xset*yset*3*3
    tile_s = tile_w*tile_h * 3


    def draw_text(text, font, color_dt, surface, x, y):
        textobj = font.render(text, 1, color_dt)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


    def print_3d(array, h, w):
        for x in range(int(h/3)):
            print(array[x*w:x*w+w])
    def rule_gen(rule_d, rule, base, view, new=0):
        for x in range(bv):
            e = rule//base
            q = rule%base
            key = []

            if new == 0:
                for y in range(view):
                    r = x//base
                    w = x%base
                    key += value_color[w]
                    x = r
            else:
                key = list(rule_d.keys())[x]

            rule = e
            rule_d[tuple(key)] = value_color[q]

        return rule_d
    def mitosis(block, rule_d, width, width_3):
        block = np.roll(block, width_3)

        for x in range(width):
            x3 = x*3
            hood = tuple(block[width_3-3+x3:width_3+6+x3])
            dojo = rule_d[hood]

            block[0+x3] = dojo[0]
            block[1+x3] = dojo[1]
            block[2+x3] = dojo[2]

        return block


    rule_d = rule_gen(rule_d, rule, base, view)


    while run == 1:

        mx, my = pygame.mouse.get_pos()

        WIN.fill((0, 0, 0))

        WIN.blit(pygame.surfarray.make_surface(
            np.rot90(np.reshape(block, (height, width, 3)), 1, (1, 0))), (0, 0))

        WIN.blit(pygame.surfarray.make_surface(
            np.rot90(np.reshape(tile, (tile_h, tile_w, 3)), 1, (1, 0))), (xset + 100, yset - 100))

        draw_text(str(rule), TITLE_FONT, (10, 100, 10), WIN, WIDTH - 100, 10)

        draw_text(str(path), main_font, (10, 100, 10), WIN, 500, 100)

        for x in range(4):
            for y in range(4):
                p = y+x*4

                corner = pygame.Rect(x*tile_w + xset, y*tile_h + yset, 15, 15)
                pygame.draw.rect(WIN, (click_color[p] + 64, click_color[p], click_color[p]), corner)
                if corner.collidepoint((mx, my)):
                    if click:
                        path.append((x, y))
                        click_color[y+x*4] = 128
                        click = False


        pygame.display.update()

        #inputs
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2

            click = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print('click')
                    click = True

            #keyboard
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    run = 2

                if event.key == pygame.K_UP:
                    rule += 1
                    rule_d = rule_gen(rule_d, rule, base, view, 1)
                if event.key == pygame.K_DOWN:
                    rule -= 1
                    rule_d = rule_gen(rule_d, rule, base, view, 1)

        #mitosis
        if len(path) > 1:

            block = mitosis(block, rule_d, width, width_3)
            tile = mitosis(tile, rule_d, tile_w, tile_w3)









Chaos_Window()