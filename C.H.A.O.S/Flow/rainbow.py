

black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
magenta = (255, 0, 255)
white = (255, 255, 255)

color_list = [black, red, yellow, green, cyan, blue, magenta, white]

limit = (len(color_list)-1) * 255

print(limit)


def rainbow_split(colors):

    value_color = []

    black = (0, 0, 0)
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    cyan = (0, 255, 255)
    blue = (0, 0, 255)
    magenta = (255, 0, 255)
    white = (255, 255, 255)

    color_list = [black, red, yellow, green, cyan, blue, magenta, white]

    color_buckets = [0, 1, 0, 2, 1, 0, 1]

    limit = (len(color_list)-1) * 255


    if colors == 2:
        value_color = [black, white]

    else:

        value_color.append(black)

        for x in range(colors-2):

            splat = int(limit / (colors))
            split = int(limit / (colors)) * (x+1)

            # print('')
            # print('split')
            # print(split)
            # print(splat)

            color = int(split/255)
            sand = split-(color)*255


            # print('color')
            # print(color)
            # print('sand')
            # print(sand)

            new_color = list(color_list[color])

            # print(new_color)


            new_color[color_buckets[color]] = sand

            # print(new_color)
            # print(color_buckets[color])

            value_color.append(tuple(new_color))

        value_color.append(white)


    return value_color

for x in range(7):
    print()
    print('rainbow split')
    print(x+2)
    print(rainbow_split(x+2))