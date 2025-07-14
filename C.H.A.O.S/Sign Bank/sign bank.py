import time
import pygame
import math
import pickle

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

    click = False

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
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))

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


            elif n == 12:
                pygame.draw.line(WIN, value_color[7], (x, y), (x, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s/3), y-s), (x + int(s/3) + int(s/1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3) + int(s/1.5), y - s), (x + int(s / 3) + int(s / 1.5), y-int(s/3)), int(s / 8))

            elif n == 13:
                pygame.draw.line(WIN, value_color[7], (x, y), (x, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s/3), y-int(s/3)), (x + int(s/3) + int(s/1.5), y - int(s/3)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3) + int(s/1.5), y - s), (x + int(s / 3) + int(s / 1.5), y-int(s/3)), int(s / 8))

            elif n == 14:
                pygame.draw.line(WIN, value_color[7], (x + int(s), y), (x + int(s), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x, y-s), (x + int(s/1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x, y-int(s/3)), int(s / 8))

            elif n == 15:
                pygame.draw.line(WIN, value_color[7], (x+s, y), (x+s, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x, y-int(s/3)), (x+ int(s/1.5), y - int(s/3)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x, y-int(s/3)), int(s / 8))

        else:
            n -= 16

            pygame.draw.circle(WIN, value_color[7], (x + 48, y - height_4), 32)

            if n == 0:
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))

            elif n == 1:
                pygame.draw.line(WIN, value_color[7], (x, y + int(s / 16)), (x, y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 2), y + int(s / 16)), (x + int(s / 2), y - s),
                                 int(s / 8))

            elif n == 2:
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


            elif n == 12:
                pygame.draw.line(WIN, value_color[7], (x, y), (x, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 3), y - s), (x + int(s / 3) + int(s / 1.5), y - s),
                                 int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3) + int(s / 1.5), y - s),
                                 (x + int(s / 3) + int(s / 1.5), y - int(s / 3)), int(s / 8))

            elif n == 13:
                pygame.draw.line(WIN, value_color[7], (x, y), (x, y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x + int(s / 3), y - int(s / 3)),
                                 (x + int(s / 3) + int(s / 1.5), y - int(s / 3)), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x + int(s / 3) + int(s / 1.5), y - s),
                                 (x + int(s / 3) + int(s / 1.5), y - int(s / 3)), int(s / 8))

            elif n == 14:
                pygame.draw.line(WIN, value_color[7], (x + int(s), y), (x + int(s), y - s), int(s / 8))

                pygame.draw.line(WIN, value_color[7], (x, y - s), (x + int(s / 1.5), y - s), int(s / 8))
                pygame.draw.line(WIN, value_color[7], (x, y - s), (x, y - int(s / 3)), int(s / 8))

            elif n == 15:
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

    #basic
    run = 1
    power = [0, 0]

    #clock
    clock = [0, 0]
    clock[0] = time.time()

    #Bank Entries
    phrase = 'LOVE'
    phrase_link = 0
    sign = 'sign'
    sign_t = 'hand'
    time_m = '4'
    time_s = '16'
    reps = '1'
    date = '5-13-2025'
    signer = 'TheophiLis Chaotomata'

    bank_entries = [sign, sign_t, time_m, time_s, reps, date, signer]
    entry_guide = ['sign', 'type', 'min', 'sec', 'reps', 'date', 'signer']
    modes = ['entry', 'look up']

    mode = 0
    go = 0
    matches = []


    #bet
    digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
                     's': 4, 'c': 5, 'd': 6, 'm': 7,
                     'g': 8, 'f': 9, 'w': 10, 'v': 11,
                     'z': 12, 'q': 13, ',': 14, '"': 15,
                     '/': 16, '.': 17, ';': 18, 'j': 19,
                     'x': 20, 'k': 21, 'y': 22, 'b': 23,
                     'h': 24, 'p': 25, 'u': 26, 'l': 27,
                     'n': 28, 'o': 29, 'r': 30, 'e': 31}
    digibetu = {v: k for k, v in digibet.items()}

    filename = 'bets/armbet_2'
    infile = open(filename, "rb")
    armbet = pickle.load(infile)
    infile.close



    ###profile name###
    record_name = 'Eldership'

    try:
        filename = 'records/' + record_name
        infile = open(filename, "rb")
        bank = pickle.load(infile)
        infile.close
    except:
        bank = [entry_guide]




    value_color = {0:(0, 0, 0), 1:(255, 0, 0), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255),
                   6:(255, 0, 255), 7:(255, 255, 255), 8:(127, 127, 127)}

    value_color_16 = {0:(0, 0, 0), 1:(127, 0, 0), 2:(255, 0, 0), 3:(255, 127, 0), 4:(255, 255, 0), 5:(127, 255, 0),
                      6:(0, 255, 0), 7:(0, 255, 127), 8:(0, 255, 255), 9:(0, 127, 255), 10:(0, 0, 255), 11:(127, 0, 255),
                      12:(255, 0, 255), 13:(255, 0, 127), 14:(127, 127, 127), 15:(255, 255, 255)}

    text_color = value_color[7]

    while run == 1:

        WIN.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        time_0 = round(time.time() - clock[0], 3)

        #####mode#####
        x = WIDTH - width_8
        y = HEIGHT - height_8
        w = 140
        h = 50

        design = pygame.Rect(x, y, w, h)
        pygame.draw.rect(WIN, (170, 40, 160), design)
        lesson_t = main_font.render(str(modes[mode]), True, text_color)
        WIN.blit(lesson_t, (x + 10, y))
        if design.collidepoint((mx, my)):
            if click:
                mode += 1

        lesson_t = main_font.render(str(phrase), True, text_color)
        WIN.blit(lesson_t, (width_2 - lesson_t.get_width() / 2, height_32))

        #bank entry
        if mode == 0:

            for b in range(len(bank_entries)):
                #####sign#####
                x = width_32 + (width_16+width_32)*b
                y = height_8
                w = 140
                h = 50

                color = (70, 10, 10)

                if b > 0 and b < len(bank_entries)-1:
                    x += 250
                if b > len(bank_entries) -2:
                    x += 300

                if b == phrase_link:
                    color = (70, 70, 70)

                design = pygame.Rect(x, y, w, h)
                pygame.draw.rect(WIN, color, design)
                lesson_t = main_font.render(str(entry_guide[b]), True, text_color)
                WIN.blit(lesson_t, (x + 10, y))
                if design.collidepoint((mx, my)):
                    if click:
                        print('click')
                        phrase = bank_entries[b]
                        phrase_link = b
                        click = False

                lesson_t = main_font.render(str(bank_entries[b]), True, text_color)
                WIN.blit(lesson_t, (x, y + h))

                bank_entries[phrase_link] = phrase

            #####submit#####
            x = width_32
            y = height_32
            w = 140
            h = 50

            design = pygame.Rect(x, y, w, h)
            pygame.draw.rect(WIN, (70, 10, 100), design)
            lesson_t = main_font.render(str('submit'), True, text_color)
            WIN.blit(lesson_t, (x + 10, y))
            if design.collidepoint((mx, my)):
                if click:
                    if bank_entries not in bank:
                        bank.append(bank_entries[::])
                    else:
                        print('oopsie')
                    print(bank)
                    phrase_link = 0
                    click = False


            #####delete#####
            x = WIDTH - width_8
            y = height_32
            w = 140
            h = 50

            design = pygame.Rect(x, y, w, h)
            pygame.draw.rect(WIN, (70, 10, 100), design)
            lesson_t = main_font.render(str('delete'), True, text_color)
            WIN.blit(lesson_t, (x + 10, y))
            if design.collidepoint((mx, my)):
                if click:
                    bank = bank[:-1]
                    phrase_link = 0
                    click = False


            #bank display
            for b in range(len(bank)):
                x = width_32
                y = height_4 + height_32*b
                lesson_t = small_font.render(str(b) + ': ' + str(bank[-b]), True, text_color)
                WIN.blit(lesson_t, (x, y))

        #look up
        if mode == 1:

            if go == 1:
                signs = phrase.split('.')
                matches = []

                for b in bank:
                    for s in signs:
                        if s in b[0]:
                            if b not in matches:
                                matches.append(b)
                go = 0

            #matches display
            total_m = 0
            total_s = 0

            for m in range(len(matches)):
                x = width_32
                y = height_4 + height_32*m
                lesson_t = small_font.render(str(m) + ': ' + str(matches[m]), True, text_color)
                WIN.blit(lesson_t, (x, y))

                total_m += int(matches[m][2])
                total_s += int(matches[m][3])

            s_m = int(total_s/60)
            total_m += s_m
            total_s -= s_m*60

            lesson_t = small_font.render(str(total_m), True, text_color)
            WIN.blit(lesson_t, (width_2 + width_4, height_4))
            lesson_t = small_font.render(str(total_s), True, text_color)
            WIN.blit(lesson_t, (width_2 + width_4, height_4 + height_8))




        #event
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            #keyboard

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    run = 2

                elif event.key == pygame.K_RETURN:

                    if mode == 0:
                        print()
                        print(phrase)
                        print(len(phrase))
                        if bank_entries not in bank:
                            bank.append(bank_entries[::])
                        else:
                            print('oopsie')
                        print(bank)
                        phrase_link = 0
                        phrase = bank_entries[phrase_link]

                        filename = 'records/' + record_name
                        outfile = open(filename, 'wb')
                        pickle.dump(bank, outfile)
                        outfile.close

                    if mode == 1:
                        go = 1


                elif event.key == pygame.K_TAB:
                    phrase_link += 1
                    if phrase_link > len(entry_guide)-1:
                        phrase_link = 0

                    phrase = bank_entries[phrase_link]



                elif event.key == pygame.K_F1:


                    print()


                elif event.key == pygame.K_LEFT:
                    print()

                elif event.key == pygame.K_RIGHT:
                    print()

                elif event.key == pygame.K_UP:
                    mode += 1
                    mode = mode%len(modes)

                elif event.key == pygame.K_DOWN:
                    mode -= 1
                    mode = mode % len(modes)



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




                elif event.key == pygame.K_BACKSPACE and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase = ''

                elif event.key == pygame.K_BACKSPACE:
                    phrase = phrase[:-1]


        pygame.display.update()


Chaos_Window()

