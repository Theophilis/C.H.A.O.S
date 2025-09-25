
limit = 256*256*256 + 256*256 + 256

print("")
print(limit)



colors = 1

print(limit/2)

def digit_rgb (digit):

    r = 1
    g = 256
    b = 256*256

    bd = int(digit/b)

    if bd > 256:
        bd = 256

    digit_b = digit-bd*b

    gd = int(digit_b/g)

    if gd> 256:
        gd = 256

    digit_g = digit_b-gd*g

    rd = int(digit_g)

    rgb = (rd, gd, bd)

    return rgb



color_l = digit_rgb(limit/2)

print("color_l")
print(color_l)

def color_split(colors):

    limit = 256 * 256 * 256 + 256 * 256 + 256
    color_list = []

    color_0 = (0, 0, 0)
    color_w = (256, 256, 256)

    if colors == 1:
        color_list.append(color_0)

    elif colors == 2:
        color_list.append(color_0)
        color_list.append(color_w)

    else:
        color_list.append(color_0)

        step = int(limit/(colors-1))
        print(step)

        for x in range(colors-2):
            color_list.append(digit_rgb(step*(x+1)))

        color_list.append(color_w)


    return color_list

for x in range(32):
    print()
    print(x)
    color_list = color_split(x+1)
    print(color_list)

# print(color_split(3))