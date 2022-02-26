print('C311UL4R H4PT1C 4T0M4T4 0P3R4T1NG 5Y5T3M')

# begin = input('Begin? (yes/no): ')
#
# if begin.lower() == 'yes':
#
#     print("Begun.")

cnvs = np.zeros((length, width), dtype='int8')
cnvs[0, start] = 1

# print(cnvs)

rule = rule_gen(90, base)

d_rule = rule[0]
i_rule = rule[1]

# print(" ")
# print("d_rule")
# print(d_rule)
# print("i_rule")
# print(i_rule)


def play_move(move):

    if move =='done':

        lose = 1

    else:

        lose = 0

    char = 1

    if move == 'a':

        if i_rule[0] == 0:

            i_rule[0] = char
            d_rule[list(d_rule.keys())[0]] = char

        else:
            i_rule[0] = 0
            d_rule[list(d_rule.keys())[0]] = 0

    if move == 's':

        if i_rule[1] == 0:

            i_rule[1] = char
            d_rule[list(d_rule.keys())[1]] = char

        else:
            i_rule[1] = 0
            d_rule[list(d_rule.keys())[1]] = 0

    if move == 'd':

        if i_rule[2] == 0:

            i_rule[2] = char
            d_rule[list(d_rule.keys())[2]] = char

        else:
            i_rule[2] = 0
            d_rule[list(d_rule.keys())[2]] = 0

    if move == 'f':

        if i_rule[3] == 0:

            i_rule[3] = char
            d_rule[list(d_rule.keys())[3]] = char

        else:
            i_rule[3] = 0
            d_rule[list(d_rule.keys())[3]] = 0

    if move == 'j':

        if i_rule[4] == 0:

            i_rule[4] = char
            d_rule[list(d_rule.keys())[4]] = char

        else:
            i_rule[4] = 0
            d_rule[list(d_rule.keys())[4]] = 0

    if move == 'k':

        if i_rule[5] == 0:

            i_rule[5] = char
            d_rule[list(d_rule.keys())[5]] = char

        else:
            i_rule[5] = 0
            d_rule[list(d_rule.keys())[5]] = 0

    if move == 'l':

        if i_rule[6] == 0:

            i_rule[6] = char
            d_rule[list(d_rule.keys())[6]] = char

        else:
            i_rule[6] = 0
            d_rule[list(d_rule.keys())[6]] = 0

    if move == ';':

        if i_rule[7] == 0:

            i_rule[7] = char
            d_rule[list(d_rule.keys())[7]] = char

        else:
            i_rule[7] = 0
            d_rule[list(d_rule.keys())[7]] = 0


    print(" ")
    # print("d_rule")
    # print(d_rule)
    print("i_rule")
    print(i_rule)


    for x in reversed(range(length - 1)):

        c_a = cnvs[x]

        # print(" ")
        # print("c_a")
        # print(c_a)
        # print(len(c_a))

        for y in range(len(c_a)):

            if direction != 0:

                y = len(c_a) - y - 1

            v_0 = []

            # print(" ")
            # print("y")
            # print(y)

            v_0 = tuple(viewer(c_a, y, view, v_0))

            # print("v_0")
            # print(v_0)

            # print("rule")
            # print(rules[v_0])

            cnvs[x + 1, y] = d_rule[v_0]

    # print(" ")
    # print("cnvs")
    print(cnvs)

    if base == 3:
        cMap = c.ListedColormap(['k', 'c', 'm'], 'tri', 3)

    if base == 2:
        cMap = c.ListedColormap(['w', 'k'])

    plt.pcolormesh(cnvs, cmap=cMap)

    # matplotlib.axes.Axes.set_aspect(plt, 'auto')

    axes = plt.gca()
    axes.set_aspect('auto')

    # plt.xticks(np.arange(0, width, step=1))
    # plt.yticks(np.arange(0, length, step=1))

    # plt.figtext(.3, .925, int_rule, fontsize=14)
    # plt.figtext(.0075, .05, rules, fontsize=7)
    # plt.grid(visible=True, axis='both', )

    plt.show()
    plt.close()

    return lose

lose = 1

while lose == 0:

    move = input('>>>   ')

    print("bingo")

    play_move(move)