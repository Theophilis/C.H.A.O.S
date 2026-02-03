import time
import pygame
import pygame.midi
import math
import pickle
from pygame import mixer



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

    def bin_gen(n, b, p):
        def base_x(n, b):
            e = n // b
            q = n % b
            if n == 0:
                return '0'
            elif e == 0:
                return str(q)
            else:
                return base_x(e, b) + str(q)

        bin = base_x(n, b)

        while len(bin) < p:
            bin = '0' + bin
        return bin

    def punchroglyph(n, s, x, y, rl = 0):

        if rl == 0:
            # first position
            if n % 4 == 0:

                # arm
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x + s, y), int(s / 8))

                # hand
                if n % 16 < 8:
                    pygame.draw.circle(WIN, value_color[int(n % 8 / 4) + 7], (x + s, y), s / 4)
                else:
                    guide_b = pygame.Rect(x + s - int(s / 8), y - int(s / 4), s / 2, s / 2)
                    pygame.draw.rect(WIN, value_color[int(n % 8 / 4) + 7], guide_b)

                # shoulder
                if n > 15:
                    pygame.draw.circle(WIN, value_color[7], (x, y - s + int(s / 16)), s / 4)

            # second position
            if n % 4 == 1:

                # arm
                pygame.draw.line(WIN, value_color[7], (x, y), (x + s, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x - s, y - s), int(s / 8))

                # hand
                if n % 16 < 8:
                    pygame.draw.circle(WIN, value_color[7 + int(n % 8 / 5)], (x + s, y - s), s / 4)
                else:
                    guide_b = pygame.Rect(x + s - int(s / 4), y - s - int(s / 4), s / 2, s / 2)
                    pygame.draw.rect(WIN, value_color[int(n % 8 / 4) + 7], guide_b)

                # shoulder
                if n > 15:
                    pygame.draw.circle(WIN, value_color[7], (x - s, y - s + int(s / 16)), s / 4)

            # third position
            if n % 4 == 2:

                # arm
                pygame.draw.line(WIN, value_color[7], (x, y - int(s / 2)), (x + s, y - int(s / 2)), int(s / 8))

                # hand
                if n % 16 < 8:
                    pygame.draw.circle(WIN, value_color[int(n % 8 / 4) + 7], (x + s, y - int(s / 2)), s / 4)
                else:
                    guide_b = pygame.Rect(x + s - int(s / 8), y - int(s / 4) - int(s / 2), s / 2, s / 2)
                    pygame.draw.rect(WIN, value_color[int(n % 8 / 4) + 7], guide_b)

                # shoulder
                if n > 15:
                    pygame.draw.circle(WIN, value_color[7], (x, y - int(s / 2)), s / 4)

            # fourth position
            if n % 4 == 3:

                # arm
                pygame.draw.line(WIN, value_color[7], (x + s, y + int(s / 16)), (x + s, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x + s, y), int(s / 8))

                # hand
                if n % 16 < 8:
                    pygame.draw.circle(WIN, value_color[int(n % 8 / 4) + 7], (x + s, y - s), s / 4)
                else:
                    guide_b = pygame.Rect(x + s - int(s / 4), y - s - int(s / 4), s / 2, s / 2)
                    pygame.draw.rect(WIN, value_color[int(n % 8 / 4) + 7], guide_b)

                # shoulder
                if n > 15:
                    pygame.draw.circle(WIN, value_color[7], (x, y), s / 4)

        if rl == 1:
            # first position
            if n % 4 == 0:

                # arm
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x - s, y), int(s / 8))

                # hand
                if n % 16 < 8:
                    pygame.draw.circle(WIN, value_color[int(n % 8 / 4) + 7], (x - s, y), s / 4)
                else:
                    guide_b = pygame.Rect(x - s - int(s / 8), y - int(s / 4), s / 2, s / 2)
                    pygame.draw.rect(WIN, value_color[int(n % 8 / 4) + 7], guide_b)

                # elbow
                if n > 15:
                    pygame.draw.circle(WIN, value_color[7], (x, y - s + int(s / 16)), s / 4)

            # second position
            if n % 4 == 1:

                # arm
                pygame.draw.line(WIN, value_color[7], (x, y), (x + s, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x - s, y - s), int(s / 8))

                # hand
                if n % 16 < 8:
                    pygame.draw.circle(WIN, value_color[7 + int(n % 8 / 5)], (x + s, y - s), s / 4)
                else:
                    guide_b = pygame.Rect(x + s - int(s / 4), y - s - int(s / 4), s / 2, s / 2)
                    pygame.draw.rect(WIN, value_color[int(n % 8 / 4) + 7], guide_b)

                # elbow
                if n > 15:
                    pygame.draw.circle(WIN, value_color[7], (x - s, y - s + int(s / 16)), s / 4)

            # third position
            if n % 4 == 2:

                # arm
                pygame.draw.line(WIN, value_color[7], (x, y - int(s / 2)), (x + s, y - int(s / 2)), int(s / 8))

                # hand
                if n % 16 < 8:
                    pygame.draw.circle(WIN, value_color[int(n % 8 / 4) + 7], (x + s, y - int(s / 2)), s / 4)
                else:
                    guide_b = pygame.Rect(x + s - int(s / 8), y - int(s / 4) - int(s / 2), s / 2, s / 2)
                    pygame.draw.rect(WIN, value_color[int(n % 8 / 4) + 7], guide_b)

                # elbow
                if n > 15:
                    pygame.draw.circle(WIN, value_color[7], (x, y - int(s / 2)), s / 4)

            # fourth position
            if n % 4 == 3:

                # arm
                pygame.draw.line(WIN, value_color[7], (x + s, y + int(s / 16)), (x + s, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x + s, y), int(s / 8))

                # hand
                if n % 16 < 8:
                    pygame.draw.circle(WIN, value_color[int(n % 8 / 4) + 7], (x + s, y - s), s / 4)
                else:
                    guide_b = pygame.Rect(x + s - int(s / 4), y - s - int(s / 4), s / 2, s / 2)
                    pygame.draw.rect(WIN, value_color[int(n % 8 / 4) + 7], guide_b)

                # elbow
                if n > 15:
                    pygame.draw.circle(WIN, value_color[7], (x, y), s / 4)

    def kickroglyph(n, s, x, y):

        if n < 16:
            if n == 0:
                pygame.draw.line(WIN, value_color[7], (x + s/7, y + int(s / 16)), (x + s/7, y - s), int(s / 8))

            elif n == 1:
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s/2), y + int(s / 16)), (x + int(s/2), y - s), int(s / 8))

            elif n == 2:
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s /3), y), (x + int(s / 2) + int(s/3), y), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s/3), y + int(s / 16)), (x + int(s/3), y - s), int(s / 8))

            elif n == 3:
                pygame.draw.line(WIN, value_color[7], (x + int(s/3), y + int(s / 16)), (x + int(s/3), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s/3)*2, y + int(s / 16)), (x + int(s/3)*2, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x - int(s /2) + int(s/3), y), (x + int(s/3), y), int(s / 8))



            elif n == 4:
                pygame.draw.line(WIN, value_color[7], (x-int(s/4), y + int(s / 16)), (x + int(s/2) - int(s/4), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s/2) + int(s/1.5), y + int(s / 16)), (x+ int(s/2) + int(s/1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s/2), y -s), (x + int(s/2) + int(s/1.5), y-s), int(s / 8))

            elif n == 5:
                pygame.draw.line(WIN, value_color[7], (x+int(s/4) + s, y + int(s / 16)), (x +int(s/4) + int(s/2), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x-int(s/4), y + int(s / 16)), (x-int(s/4), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x-int(s/4), y -s), (x-int(s/4)+ int(s/1.5), y-s), int(s / 8))


            elif n == 6:
                #right
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2) + int(s / 1.5), y + int(s / 16)), (x + int(s / 2) + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2), y - s), (x + int(s / 2) + int(s / 1.5), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x-int(s/4), y + int(s / 16)), (x-int(s/4), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x-int(s/4), y -s), (x-int(s/4)+ int(s/1.5), y-s), int(s / 8))

            elif n == 7:
                pygame.draw.line(WIN, value_color[7], (x+int(s/4) + s, y + int(s / 16)), (x +int(s/4) + int(s/2), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x - int(s / 4), y + int(s / 16)), (x + int(s / 2) - int(s / 4), y - s), int(s / 8))



            elif n == 8:
                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5) + int(s / 1.5), y + int(s / 16)), (x + int(s / 1.5) + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5), y - s), (x + int(s / 1.5) + int(s / 1.5), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5), y + int(s / 16)), (x + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x + int(s / 1.5), y), int(s / 8))


            elif n == 9:
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x + (s/1.5), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5), y + int(s / 16)), (x + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s/1.5), y), (x + int(s/1.5) + int(s / 1.5), y), int(s / 8))


            elif n == 10:
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x + (s/1.5), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5), y + int(s / 16)), (x + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x + int(s / 1.5), y), int(s / 8))

            elif n == 11:
                pygame.draw.line(WIN, value_color[7], (x + int(s/2), y), (x + int(s/2) + int(s/2), y -int(s/2)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s/2), y), (x + int(s/2) - int(s / 2), y - int(s / 2)), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s/2), y-s), (x + int(s/2) + int(s / 2), y - int(s / 2)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s/2) + int(s / 2) - int(s/2), y - s), (x + int(s/2) -int(s/2), y - int(s / 2)), int(s / 8))


            elif n == 13:
                pygame.draw.line(WIN, value_color[7], (x, y), (x, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s/3), y-s), (x + int(s/3) + int(s/1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3) + int(s/1.5), y - s), (x + int(s / 3) + int(s / 1.5), y-int(s/3)), int(s / 8))

            elif n == 12:
                pygame.draw.line(WIN, value_color[7], (x, y), (x, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s/3), y-int(s/3)), (x + int(s/3) + int(s/1.5), y - int(s/3)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3) + int(s/1.5), y - s), (x + int(s / 3) + int(s / 1.5), y-int(s/3)), int(s / 8))

            elif n == 15:
                pygame.draw.line(WIN, value_color[7], (x + int(s), y), (x + int(s), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x, y-s), (x + int(s/1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x, y-int(s/3)), int(s / 8))

            elif n == 14:
                pygame.draw.line(WIN, value_color[7], (x+s, y), (x+s, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x, y-int(s/3)), (x+ int(s/1.5), y - int(s/3)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x, y-int(s/3)), int(s / 8))



        else:
            n -= 16

            pygame.draw.circle(WIN, value_color[8], (x + 16, y - 48), 16)

            if n == 0:
                pygame.draw.line(WIN, value_color[7], (x+12, y + int(s / 16)), (x+12, y - s), int(s / 8))

            elif n == 1:
                x = x + 5
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2), y + int(s / 16)), (x + int(s / 2), y - s),
                                 int(s / 8))

            elif n == 2:

                x = x + 8

                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3), y), (x + int(s / 2) + int(s / 3), y), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 3), y + int(s / 16)), (x + int(s / 3), y - s),
                                 int(s / 8))

            elif n == 3:
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3), y + int(s / 16)), (x + int(s / 3), y - s),
                                 int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 3) * 2, y + int(s / 16)),
                                 (x + int(s / 3) * 2, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x - int(s / 2) + int(s / 3), y), (x + int(s / 3), y), int(s / 8))



            elif n == 4:
                pygame.draw.line(WIN, value_color[7], (x - int(s / 4), y + int(s / 16)),
                                 (x + int(s / 2) - int(s / 4), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 2) + int(s / 1.5), y + int(s / 16)),
                                 (x + int(s / 2) + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2), y - s), (x + int(s / 2) + int(s / 1.5), y - s),
                                 int(s / 8))

            elif n == 5:
                pygame.draw.line(WIN, value_color[7], (x + int(s / 4) + s, y + int(s / 16)),
                                 (x + int(s / 4) + int(s / 2), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x - int(s / 4), y + int(s / 16)), (x - int(s / 4), y - s),
                                 int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x - int(s / 4), y - s), (x - int(s / 4) + int(s / 1.5), y - s),
                                 int(s / 8))


            elif n == 6:
                # right
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2) + int(s / 1.5), y + int(s / 16)),
                                 (x + int(s / 2) + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2), y - s), (x + int(s / 2) + int(s / 1.5), y - s),
                                 int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x - int(s / 4), y + int(s / 16)), (x - int(s / 4), y - s),
                                 int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x - int(s / 4), y - s), (x - int(s / 4) + int(s / 1.5), y - s),
                                 int(s / 8))

            elif n == 7:
                pygame.draw.line(WIN, value_color[7], (x + int(s / 4) + s, y + int(s / 16)),
                                 (x + int(s / 4) + int(s / 2), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x - int(s / 4), y + int(s / 16)),
                                 (x + int(s / 2) - int(s / 4), y - s), int(s / 8))



            elif n == 8:
                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5) + int(s / 1.5), y + int(s / 16)),
                                 (x + int(s / 1.5) + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5), y - s),
                                 (x + int(s / 1.5) + int(s / 1.5), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5), y + int(s / 16)), (x + int(s / 1.5), y - s),
                                 int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x + int(s / 1.5), y), int(s / 8))


            elif n == 9:
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x + (s / 1.5), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5), y + int(s / 16)), (x + int(s / 1.5), y - s),
                                 int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5), y), (x + int(s / 1.5) + int(s / 1.5), y),
                                 int(s / 8))


            elif n == 10:
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x + (s / 1.5), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 1.5), y + int(s / 16)), (x + int(s / 1.5), y - s),
                                 int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y), (x + int(s / 1.5), y), int(s / 8))

            elif n == 11:
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2), y),
                                 (x + int(s / 2) + int(s / 2), y - int(s / 2)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2), y),
                                 (x + int(s / 2) - int(s / 2), y - int(s / 2)), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 2), y - s),
                                 (x + int(s / 2) + int(s / 2), y - int(s / 2)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2) + int(s / 2) - int(s / 2), y - s),
                                 (x + int(s / 2) - int(s / 2), y - int(s / 2)), int(s / 8))


            elif n == 13:
                pygame.draw.line(WIN, value_color[7], (x, y), (x, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 3), y - s), (x + int(s / 3) + int(s / 1.5), y - s),
                                 int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3) + int(s / 1.5), y - s),
                                 (x + int(s / 3) + int(s / 1.5), y - int(s / 3)), int(s / 8))

            elif n == 12:
                pygame.draw.line(WIN, value_color[7], (x, y), (x, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 3), y - int(s / 3)),
                                 (x + int(s / 3) + int(s / 1.5), y - int(s / 3)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3) + int(s / 1.5), y - s),
                                 (x + int(s / 3) + int(s / 1.5), y - int(s / 3)), int(s / 8))

            elif n == 15:
                pygame.draw.line(WIN, value_color[7], (x + int(s), y), (x + int(s), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x, y - s), (x + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x, y - int(s / 3)), int(s / 8))

            elif n == 14:
                pygame.draw.line(WIN, value_color[7], (x + s, y), (x + s, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x, y - int(s / 3)), (x + int(s / 1.5), y - int(s / 3)),
                                 int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x, y - int(s / 3)), int(s / 8))


    print(HEIGHT, WIDTH)
    width_2 = int(WIDTH/2)
    width_3 = int(WIDTH/3)
    width_4 = int(WIDTH/4)
    width_8 = int(WIDTH/8)
    width_16 = int(WIDTH/16)
    width_32 = int(WIDTH/32)
    width_64 = int(WIDTH/64)
    height_2 = int(HEIGHT/2)
    height_4 = int(HEIGHT/4)
    height_8 = int(HEIGHT/8)
    height_16 = int(HEIGHT/16)
    height_32 = int(HEIGHT/32)
    height_64 = int(HEIGHT/64)

    #core
    run = 1

    #bets
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

    guide = 7
    guide_max = 9

    armbet_size = 1

    #phrase
    phrase = 'i am the one who lik es all the pr et ty son gs and i lov es to si ng al ong and i lov es to si gn for fu n but i kno ws not wh at i me ans wh en i say ye ah'



    value_color = {0:(0, 0, 0), 1:(255, 0, 0), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255),
                   6:(255, 0, 255), 7:(255, 255, 255), 8:(64, 64, 64)}

    value_color_16 = {0:(0, 0, 0), 1:(127, 0, 0), 2:(255, 0, 0), 3:(255, 127, 0), 4:(255, 255, 0), 5:(127, 255, 0),
                      6:(0, 255, 0), 7:(0, 255, 127), 8:(0, 255, 255), 9:(0, 127, 255), 10:(0, 0, 255), 11:(127, 0, 255),
                      12:(255, 0, 255), 13:(255, 0, 127), 14:(127, 127, 127), 15:(255, 255, 255)}

    while run == 1:

        WIN.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()


        lesson_t = main_font.render(phrase, True, value_color[7])
        WIN.blit(lesson_t,(width_16, height_2 + height_4 + height_8 + height_16))

        # digibet-c
        if guide == 0:
            space = 64
            step = 0
            step_lim = 14

            for y in range(32):

                bin_value = bin_gen(y, 2, 5)[::-1]

                x0 = width_16 + int(step / step_lim) * width_4
                y0 = 32 + step % step_lim * space

                for x in range(5):
                    x1 = x0 + space + space + space / 2 * x
                    y1 = y0 + 8

                    finger_sign = pygame.Rect(x1, y1, 31, 31)
                    pygame.draw.rect(WIN, value_color[8 - int(bin_value[x])], finger_sign)

                lesson_t = main_font.render(str(y), True, value_color[7])
                WIN.blit(lesson_t, (x1 - space * 3, y1 - 8))

                lesson_t = main_font.render(str(digibetu[y]), True, value_color[7])
                WIN.blit(lesson_t, (x1 + space, y1 - 8))

                step += 1

        #digroglyph-c
        if guide == 1:
            space = 64
            step = 0
            step_lim = 6
            size = 31

            for y in range(32):

                x0 = width_8 + int(step / step_lim) * width_8
                y0 = height_8 + step % step_lim * (space*2)


                bin_value = bin_gen(y, 2, 5)[::-1]


                for x in range(5):
                    x1 = x0
                    y1 = y0

                    if x == 1:
                        x1 = x1 + size
                    if x == 2:
                        x1 = x1 + size
                        y1 = y1 + size
                    if x == 3:
                        x1 = x1 + size
                        y1 = y1 + size*2
                    if x == 4:
                        x1 = x1
                        y1 = y1 + size*2




                    finger_sign = pygame.Rect(x1, y1, size, size)
                    pygame.draw.rect(WIN, value_color[8 - int(bin_value[x])], finger_sign)

                lesson_t = main_font.render(str(y), True, value_color[7])
                WIN.blit(lesson_t, (x1-size/2 * 3, y1 - 8))

                lesson_t = main_font.render(str(digibetu[y]), True, value_color[7])
                WIN.blit(lesson_t, (x1 + space + size/2, y1 - 8))

                step += 1

        #punchroglph-c
        if guide == 2:

            space = 192

            for x in range(16):
                x0 = width_16 +int(x/4)*(space)
                y0 = height_8 + x%4 * space
                punchroglyph(x, 64, x0, y0)

                if len(phrase) > 1:
                    if phrase in digibet.keys():
                        try:
                            bigram_t = lable_font.render(str(armbet[phrase][x]), True, value_color[7])
                            WIN.blit(bigram_t, (x0, y0))
                        except:
                            continue

                else:
                    try:
                        bigram_t = lable_font.render(str(armbet[phrase[0]][x]), True, value_color[7])
                        WIN.blit(bigram_t, (x0, y0))
                    except:
                        continue

        #kickroglyph-c
        if guide == 3:

            space = 192

            for x in range(16):
                x0 = width_16 +int(x/4)*(space)
                y0 = height_8 + x%4 * space
                kickroglyph(x, 64, x0, y0)

                try:
                    bigram_t = lable_font.render(str(armbet[phrase[0]][x]), True, value_color[7])
                    WIN.blit(bigram_t, (x0, y0))
                except:
                    continue


        #digibet-s
        if guide == 4:
            space = 64
            step = 0
            step_lim = 14

            for p in phrase:
                p = p.lower()
                if p in digibet:

                    x0 = width_16 + int(step/step_lim)*width_4
                    y0 = 16 + step%step_lim * space

                    p_value = digibet[p]
                    bin_value = bin_gen(p_value, 2, 5)[::-1]


                    lesson_t = main_font.render(str(p), True, value_color[7])
                    WIN.blit(lesson_t, (x0, y0))

                    lesson_t = main_font.render(str(digibet[p]), True, value_color[7])
                    WIN.blit(lesson_t, (x0 + space, y0))


                    for x in range(5):

                        x1 = x0 + space + space + space/2*x
                        y1 = y0 + 8


                        # lesson_t = main_font.render(str(bin_value[x]), True, value_color[7])
                        # WIN.blit(lesson_t, (x0,y0))

                        finger_sign = pygame.Rect(x1, y1, 31, 31)
                        pygame.draw.rect(WIN, value_color[8 - int(bin_value[x])], finger_sign)

                step += 1

        #armbet-s
        if guide == 5:

            phrase = phrase.lower()

            #bigrams
            bigrams = []

            step = 0
            stagger = 0
            check = ''
            while check != phrase:
                bigram = phrase[step*2 + stagger:step*2+2 + stagger]

                if ' ' in bigram:
                    if bigram[0] == ' ':
                        stagger += 1
                        bigrams.append(' ')
                        bigram = phrase[step * 2 + stagger:step * 2 + 2 + stagger]
                        bigrams.append(bigram)
                    else:
                        bigrams.append(bigram[0])
                        bigrams.append(bigram[1])
                else:
                    bigrams.append(bigram)
                step += 1

                check = ''
                for b in bigrams:
                    check += b


            space = 128
            step = 0
            step_lim = 7
            x0 = width_32
            y0 = height_32

            for x in range(len(bigrams)):

                x1 = x0 + int(x/step_lim)*space*2
                y1 = y0 + x%step_lim*space

                lesson_t = main_font.render(str(bigrams[x]), True, value_color[7])
                WIN.blit(lesson_t, (x1, y1))

                if len(bigrams[x]) == 2:

                    glyph = armbet[bigrams[x][0]].index(bigrams[x])
                    punchroglyph(glyph, 64, x1 + space, y1 + int(space/2))

                else:
                    punchroglyph(0, 64, x1+ space, y1 + int(space/2))

        #legbet-s
        if guide == 6:

            phrase = phrase.lower()

            #bigrams
            bigrams = []

            step = 0
            stagger = 0
            check = ''
            while check != phrase:
                bigram = phrase[step*2 + stagger:step*2+2 + stagger]

                if ' ' in bigram:
                    if bigram[0] == ' ':
                        stagger += 1
                        bigrams.append(' ')
                        bigram = phrase[step * 2 + stagger:step * 2 + 2 + stagger]
                        bigrams.append(bigram)
                    else:
                        bigrams.append(bigram[0])
                        bigrams.append(bigram[1])
                else:
                    bigrams.append(bigram)
                step += 1

                check = ''
                for b in bigrams:
                    check += b


            space = 128
            step = 0
            step_lim = 7
            x0 = width_32
            y0 = height_32

            for x in range(len(bigrams)):

                x1 = x0 + int(x/step_lim)*space*2
                y1 = y0 + x%step_lim*space

                lesson_t = main_font.render(str(bigrams[x]), True, value_color[7])
                WIN.blit(lesson_t, (x1, y1))

                if len(bigrams[x]) == 2:

                    glyph = armbet[bigrams[x][0]].index(bigrams[x])
                    kickroglyph(glyph, 64, x1 + space, y1 + int(space/2))

                else:
                    kickroglyph(0, 64, x1+ space, y1 + int(space/2))

        #bodyglyph
        if guide == 7:


            done = 0
            space = 64
            step = 0
            step_lim = 6
            size = 16
            index = []
            arm_size = 48

            place = 0

            words = phrase.split(' ')

            lesson_t = text_font.render(str(words), True, value_color[7])
            WIN.blit(lesson_t, (width_16, height_2 + height_4 + height_8))


            word_chunks = []
            for x in range(len(words)):
                chunks = []
                y = 0

                while y < len(words[x]):

                    len_word = len(words[x])


                    d_h = 0
                    if words[x][y:y+2] in digibet:
                        print('double hand')
                        print(words[x][y:y+2])
                        d_h = 1




                    if d_h == 1:
                        if len_word == 3:
                            if words[x][y:y+3] in armbet[words[x][y:y+2]]:
                                chunks.append([words[x][y:y+3]])
                                y += 3

                        else:
                            if words[x][y:y+4] in armbet[words[x][y:y+2]]:
                                chunks.append([words[x][y:y+4]])
                                y += 4


                    elif d_h == 0:
                        if len_word%2 == 1:
                            if words[x][y:y+3] in armbet[words[x][y]]:
                                chunks.append([words[x][y:y+3]])
                                y += 3
                            elif words[x][y:y+2] in armbet[words[x][y]]:
                                chunks.append([words[x][y:y+2]])
                                y += 2
                        else:
                            if words[x][y:y+2] in armbet[words[x][y]]:
                                chunks.append([words[x][y:y+2]])
                                y += 2
                            elif words[x][y:y+3] in armbet[words[x][y]]:
                                chunks.append([words[x][y:y+3]])
                                y += 3





                word_chunks.append(chunks)





                # lesson_t = lable_font.render(str(chunks), True, value_color[7])
                # WIN.blit(lesson_t, (width_16, height_2 + height_16*x))


            space = 70
            step = 0
            step_lim = 14
            x0 = int(step / step_lim) * width_32 - width_32
            y0 = height_16 + step % step_lim * space

            lesson_t = text_font.render(str(word_chunks), True, value_color[7])
            WIN.blit(lesson_t, (width_16, height_2 + height_4 + height_16))


            print()
            print('word chunks')
            print(word_chunks)
            line_lim = 13

            for z in range(len(word_chunks)):
                word_chunk = word_chunks[z]
                print()
                print('word chunks z')
                print(word_chunk)
                print('z')
                print(z)
                print('place')
                print(place)
                print('line_lim')
                print(line_lim)






                for x in range(len(word_chunk)):


                    x0 += space*2.5


                    for y in range(len(word_chunk[x])):


                        print("word chunk x y")
                        print(word_chunk[x][y])
                        place +=1
                        print('place +1')
                        print(place)

                        if place == line_lim:
                            print('new line please')
                            x0 = width_16 + int(step / step_lim) * width_32
                            y0 = height_4 + height_8 + step % step_lim * space - width_16

                        if place == line_lim * 2 - 1:
                            print('new line please too')
                            x0 = width_16 + int(step / step_lim) * width_32
                            y0 = height_2 + height_8 + step % step_lim * space - width_16 - width_32

                        if place == line_lim * 3 - 2:
                            print('new line please too')
                            x0 = width_16 + int(step / step_lim) * width_32
                            y0 = height_2 + height_4 + step % step_lim * space - height_8 + height_64

                        lesson_t = main_font.render(str(word_chunk[x][y]), True, value_color[7])
                        WIN.blit(lesson_t, (x0 - space * .5, y0 + space*.6))


                        hand_bin = digibet[word_chunk[x][y][0]]
                        bin_value = bin_gen(hand_bin, 2, 5)[::-1]

                        # print(hand_bin)
                        # print(bin_value)

                        try:
                            arm_pos = armbet[word_chunk[x][y][0]].index(word_chunk[x][y])
                        except:
                            arm_pos = armbet[word_chunk[x][y][0:2]].index(word_chunk[x][y])

                        print('arm pos')
                        print(arm_pos)

                        s=size*2

                        x2 = x0
                        y2 = y0

                        finger_scales_r = [.8, .9, 1, .7, .5]
                        finger_scales_l = finger_scales_r[::-1]

                        bin_value_l = bin_value[::-1]
                        bin_value_r = bin_value[::]

                        def right_arm(x2, y2):

                            # first position
                            if arm_pos % 4 == 0:

                                x2 = x2 - size*1.5
                                y2 = y2 + size*1.5

                                for z in range(5):

                                    x1 = x0
                                    y1 = y0

                                    if z == 1:
                                        x1 = x1 + size
                                    elif z == 2:
                                        x1 = x1 + size
                                        y1 = y1 + size
                                    elif z == 3:
                                        x1 = x1 + size
                                        y1 = y1 + size * 2
                                    elif z == 4:
                                        x1 = x1
                                        y1 = y1 + size * 2

                                    # print(z)
                                    # print(x1,y1)

                                    finger_sign = pygame.Rect(x1, y1, size*finger_scales_r[z], size*finger_scales_r[z])
                                    pygame.draw.rect(WIN, value_color[8 - int(bin_value_r[z])], finger_sign)

                                # arm
                                pygame.draw.line(WIN, value_color[7], (x2, y2 + int(s / 16)), (x2, y2 - s), int(s / 8))
                                pygame.draw.line(WIN, value_color[7], (x2, y2), (x2 + s, y2), int(s / 8))

                                # hand
                                if arm_pos % 16 < 8:
                                    pygame.draw.circle(WIN, value_color[int(arm_pos % 8 / 4) + 7], (x2 + s, y2), s / 4)
                                else:
                                    guide_b = pygame.Rect(x2 + s - int(s / 4), y2 - int(s / 4), s / 2, s / 2)
                                    pygame.draw.rect(WIN, value_color[int(arm_pos % 8 / 4) + 7], guide_b)

                                # elbow
                                if arm_pos > 15:
                                    pygame.draw.circle(WIN, value_color[7], (x2, y2 - s + int(s / 16)), s / 4)

                            # second position
                            if arm_pos % 4 == 1:

                                for z in range(5):

                                    x1 = x0-size/2
                                    y1 = y0+size/2

                                    if z == 1:
                                        x1 = x1
                                        y1 = y1-size
                                    elif z == 2:
                                        x1 = x1 + size
                                        y1 = y1 - size
                                    elif z == 3:
                                        x1 = x1 + size*2
                                        y1 = y1 - size
                                    elif z == 4:
                                        x1 = x1 + size*2
                                        y1 = y1

                                    # print(z)
                                    # print(x1,y1)

                                    finger_sign = pygame.Rect(x1, y1, size*finger_scales_r[z], size*finger_scales_r[z])
                                    pygame.draw.rect(WIN, value_color[8 - int(bin_value_r[z])], finger_sign)

                                x2 = x2
                                y2 = y2 + size*3

                                # arm
                                pygame.draw.line(WIN, value_color[7], (x2, y2), (x2 + s/2, y2 - s), int(s / 8))
                                pygame.draw.line(WIN, value_color[7], (x2, y2), (x2 - s/2, y2 - s), int(s / 8))

                                # hand
                                if arm_pos % 16 < 8:
                                    pygame.draw.circle(WIN, value_color[7 + int(arm_pos % 8 / 5)], (x2 + s/2, y2 - s), s / 4)
                                else:
                                    guide_b = pygame.Rect(x2 + s/2 - int(s / 4), y2 - s - int(s / 4), s / 2, s / 2)
                                    pygame.draw.rect(WIN, value_color[int(arm_pos % 8 / 4) + 7], guide_b)

                                # elbow
                                if arm_pos > 15:
                                    pygame.draw.circle(WIN, value_color[7], (x2 - s/2, y2 - s + int(s / 16)), s / 4)

                            # third position
                            if arm_pos % 4 == 2:

                                x2 = x2 - size
                                y2 = y2 + size*2.5

                                for z in range(5):

                                    x1 = x0 + size*.75
                                    y1 = y0

                                    if z == 1:
                                        x1 = x1 + size
                                    elif z == 2:
                                        x1 = x1 + size
                                        y1 = y1 + size
                                    elif z == 3:
                                        x1 = x1 + size
                                        y1 = y1 + size * 2
                                    elif z == 4:
                                        x1 = x1
                                        y1 = y1 + size * 2

                                    # print(z)
                                    # print(x1,y1)

                                    finger_sign = pygame.Rect(x1, y1, size*finger_scales_r[z], size*finger_scales_r[z])
                                    pygame.draw.rect(WIN, value_color[8 - int(bin_value_r[z])], finger_sign)

                                # arm
                                pygame.draw.line(WIN, value_color[7], (x2, y2 - int(s / 2)), (x2 + s, y2 - int(s / 2)), int(s / 8))

                                # hand
                                if arm_pos % 16 < 8:
                                    pygame.draw.circle(WIN, value_color[int(arm_pos % 8 / 4) + 7], (x2 + s + 5, y2 - int(s / 2)), s / 4)
                                else:
                                    guide_b = pygame.Rect(x2 + s - int(s / 8), y2 - int(s / 4) - int(s / 2), s / 2, s / 2)
                                    pygame.draw.rect(WIN, value_color[int(arm_pos % 8 / 4) + 7], guide_b)

                                # elbow
                                if arm_pos > 15:
                                    pygame.draw.circle(WIN, value_color[7], (x2, y2 - int(s / 2)), s / 4)

                            # fourth position
                            if arm_pos % 4 == 3:

                                for z in range(5):

                                    x1 = x0-size/2
                                    y1 = y0+size/2

                                    if z == 1:
                                        x1 = x1
                                        y1 = y1-size
                                    elif z == 2:
                                        x1 = x1 + size
                                        y1 = y1 - size
                                    elif z == 3:
                                        x1 = x1 + size*2
                                        y1 = y1 - size
                                    elif z == 4:
                                        x1 = x1 + size*2
                                        y1 = y1

                                    # print(z)
                                    # print(x1,y1)

                                    finger_sign = pygame.Rect(x1, y1, size*finger_scales_r[z], size*finger_scales_r[z])
                                    pygame.draw.rect(WIN, value_color[8 - int(bin_value_r[z])], finger_sign)

                                x2 = x2 - size
                                y2 = y2 + size*3

                                # arm
                                pygame.draw.line(WIN, value_color[7], (x2 + s, y2 + int(s / 16)), (x2 + s, y2 - s), int(s / 8))
                                pygame.draw.line(WIN, value_color[7], (x2, y2), (x2 + s, y2), int(s / 8))

                                # hand
                                if arm_pos % 16 < 8:
                                    pygame.draw.circle(WIN, value_color[int(arm_pos % 8 / 4) + 7], (x2 + s, y2 - s), s / 4)
                                else:
                                    guide_b = pygame.Rect(x2 + s - int(s / 4), y2 - s - int(s / 4), s / 2, s / 2)
                                    pygame.draw.rect(WIN, value_color[int(arm_pos % 8 / 4) + 7], guide_b)

                                # elbow
                                if arm_pos > 15:
                                    pygame.draw.circle(WIN, value_color[7], (x2, y2), s / 4)

                        right_arm(x2, y2)


                        x2 = x0-space * .85
                        y3 = y0



                        print('bin')
                        print(bin_value)
                        bin_value_l = bin_value[::-1]
                        bin_value_r = bin_value[::]

                        def left_arm(x2, y2):
                            y0 = y2

                            # first position
                            if arm_pos % 4 == 0:

                                x2 = x2 - size*1.5 + size
                                y2 = y2 + size*1.5

                                for z in range(5):

                                    x1 = x0 - size
                                    y1 = y0

                                    if z == 1:
                                        x1 = x1 - size
                                    elif z == 2:
                                        x1 = x1 - size
                                        y1 = y1 + size
                                    elif z == 3:
                                        x1 = x1 - size
                                        y1 = y1 + size * 2
                                    elif z == 4:
                                        x1 = x1
                                        y1 = y1 + size * 2

                                    # print(z)
                                    # print(x1,y1)


                                    finger_sign = pygame.Rect(x1, y1, size*finger_scales_r[z], size*finger_scales_r[z])
                                    pygame.draw.rect(WIN, value_color[8 - int(bin_value_r[z])], finger_sign)

                                # arm
                                pygame.draw.line(WIN, value_color[7], (x2+s, y2 + int(s / 16)), (x2+s, y2 - s), int(s / 8))
                                pygame.draw.line(WIN, value_color[7], (x2, y2), (x2 + s, y2), int(s / 8))

                                # hand
                                if arm_pos % 16 < 8:
                                    pygame.draw.circle(WIN, value_color[int(arm_pos % 8 / 4) + 7], (x2, y2), s / 4)
                                else:
                                    guide_b = pygame.Rect(x2 - int(s / 4 ), y2 - int(s / 4), s / 2, s / 2)
                                    pygame.draw.rect(WIN, value_color[int(arm_pos % 8 / 4) + 7], guide_b)

                                # shoulder
                                if arm_pos > 15:
                                    pygame.draw.circle(WIN, value_color[7], (x2 + s, y2 - s + int(s / 16)), s / 4)

                            # second position
                            if arm_pos % 4 == 1:

                                for z in range(5):

                                    x1 = x0-size/2 - size*1.5
                                    y1 = y0+size/2

                                    if z == 1:
                                        x1 = x1
                                        y1 = y1-size
                                    elif z == 2:
                                        x1 = x1 + size
                                        y1 = y1 - size
                                    elif z == 3:
                                        x1 = x1 + size*2
                                        y1 = y1 - size
                                    elif z == 4:
                                        x1 = x1 + size*2
                                        y1 = y1

                                    # print(z)
                                    # print(x1,y1)

                                    finger_sign = pygame.Rect(x1, y1, size*finger_scales_l[z], size*finger_scales_l[z])
                                    pygame.draw.rect(WIN, value_color[8 - int(bin_value_l[z])], finger_sign)

                                x2 = x2 + size/2
                                y2 = y2 + size*3

                                # arm
                                pygame.draw.line(WIN, value_color[7], (x2, y2), (x2 + s/2, y2 - s), int(s / 8))
                                pygame.draw.line(WIN, value_color[7], (x2, y2), (x2 - s/2, y2 - s), int(s / 8))

                                # hand
                                if arm_pos % 16 < 8:
                                    pygame.draw.circle(WIN, value_color[7 + int(arm_pos % 8 / 5)], (x2 - s/2, y2 - s), s / 4)
                                else:
                                    guide_b = pygame.Rect(x2 - s/2 - int(s / 4), y2 - s - int(s / 4), s / 2, s / 2)
                                    pygame.draw.rect(WIN, value_color[int(arm_pos % 8 / 4) + 7], guide_b)

                                # shoulder
                                if arm_pos > 15:
                                    pygame.draw.circle(WIN, value_color[7], (x2 + s/2, y2 - s + int(s / 16)), s / 4)

                            # third position
                            if arm_pos % 4 == 2:

                                x2 = x2 - size
                                y2 = y2 + size*2.5

                                for z in range(5):

                                    x1 = x0 + size - size
                                    y1 = y0

                                    if z == 1:
                                        x1 = x1 - size
                                    elif z == 2:
                                        x1 = x1 - size
                                        y1 = y1 + size
                                    elif z == 3:
                                        x1 = x1 - size
                                        y1 = y1 + size * 2
                                    elif z == 4:
                                        x1 = x1
                                        y1 = y1 + size * 2

                                    # print(z)
                                    # print(x1,y1)

                                    finger_sign = pygame.Rect(x1, y1, size*finger_scales_r[z], size*finger_scales_r[z])
                                    pygame.draw.rect(WIN, value_color[8 - int(bin_value_r[z])], finger_sign)

                                # arm
                                pygame.draw.line(WIN, value_color[7], (x2 + size, y2 - int(s / 2)), (x2 + s*1.8, y2 - int(s / 2)), int(s / 8))

                                # hand
                                if arm_pos % 16 < 8:
                                    pygame.draw.circle(WIN, value_color[int(arm_pos % 8 / 4) + 7], (x2 + size + 13, y2 - int(s / 2)), s / 4)
                                else:
                                    guide_b = pygame.Rect(x2 + size, y2 - int(s / 4) - int(s / 2), s / 2, s / 2)
                                    pygame.draw.rect(WIN, value_color[int(arm_pos % 8 / 4) + 7], guide_b)

                                # shoulder
                                if arm_pos > 15:
                                    pygame.draw.circle(WIN, value_color[7], (x2 + s*2, y2 - int(s / 2)), s / 4)

                            # fourth position
                            if arm_pos % 4 == 3:


                                for z in range(5):

                                    x1 = x0-size/2 - size
                                    y1 = y0+size/2

                                    if z == 1:
                                        x1 = x1
                                        y1 = y1-size
                                    elif z == 2:
                                        x1 = x1 + size
                                        y1 = y1 - size
                                    elif z == 3:
                                        x1 = x1 + size*2
                                        y1 = y1 - size
                                    elif z == 4:
                                        x1 = x1 + size*2
                                        y1 = y1

                                    # print(z)
                                    # print(x1,y1)

                                    finger_sign = pygame.Rect(x1, y1, size*finger_scales_l[z], size*finger_scales_l[z])
                                    pygame.draw.rect(WIN, value_color[8 - int(bin_value_l[z])], finger_sign)

                                x2 = x2 - size - size
                                y2 = y2 + size*3

                                # arm
                                pygame.draw.line(WIN, value_color[7], (x2 + s, y2 + int(s / 16)), (x2 + s, y2 - s), int(s / 8))
                                pygame.draw.line(WIN, value_color[7], (x2 + s, y2), (x2 + s*2, y2), int(s / 8))

                                # hand
                                if arm_pos % 16 < 8:
                                    pygame.draw.circle(WIN, value_color[int(arm_pos % 8 / 4) + 7], (x2 + s, y2 - s), s / 4)
                                else:
                                    guide_b = pygame.Rect(x2 + s - int(s / 4), y2 - s - int(s / 4), s / 2, s / 2)
                                    pygame.draw.rect(WIN, value_color[int(arm_pos % 8 / 4) + 7], guide_b)

                                # shoulder
                                if arm_pos > 15:
                                    pygame.draw.circle(WIN, value_color[7], (x2 + s*2, y2), s / 4)


                        x0 -= space * .85

                        left_arm(x2, y3)

                        x0 += space * .3


                        y4 = height_2 - height_8 + step % step_lim * space - space * 2.3

                        if place > line_lim-1:
                            y4 = height_2 + height_8 + step % step_lim * space - space * 3.05

                        if place > (line_lim*2)-2:
                            y4 = height_2 + height_4 + step % step_lim * space - space * 2.1

                        if place > (line_lim*3)-3:
                            y4 = height_2 + height_4 + height_8 + step % step_lim * space - space * 1.2


                        kickroglyph(arm_pos, s, x0, y4)











        #inputs
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2

            click = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            #keyboard

            elif event.type == pygame.KEYDOWN:

                def type(phrase, letter):
                    print("letter")

                    phrase += letter

                    return phrase

                if event.key == pygame.K_ESCAPE:
                    run = 2

                elif event.key == pygame.K_RETURN:

                    phrase = ''


                elif event.key == pygame.K_F1:


                    print()


                elif event.key == pygame.K_LEFT:
                    print()
                    guide -= 1
                    if guide < 0:
                        guide = guide_max-1

                elif event.key == pygame.K_RIGHT:
                    guide += 1
                    guide = guide%guide_max

                elif event.key == pygame.K_UP:
                    print()

                elif event.key == pygame.K_DOWN:
                    print()

                #upper
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

                #number
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



                #lower
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


        #buttons
        x = WIDTH - width_16
        y = height_32
        guide_b = pygame.Rect(x, y, 64, 64)
        pygame.draw.rect(WIN, value_color[8], guide_b)
        if guide_b.collidepoint((mx, my)):
            guide_t = main_font.render(str(guide), True, (255, 255, 255))
            WIN.blit(guide_t, (x + 24, y + 8))
            if click:
                guide += 1
                guide = guide % guide_max
                click = False


        pygame.display.update()


Chaos_Window()


