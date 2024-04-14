import pickle

text = open('library/bible-niv.txt', 'r')
read = text.read()

read = read[3:]
read = read.lower()
read = read.translate({ord('\n'): ' '})

#dirty
print('dirty')
print(read[:100])

bibliogram = {0:{}, 1:{}, 2:{}, 3:{}}
depth = 4

for x in range(len(read)):
    for y in range(depth):
        gram = read[x:(x+y+1)%len(read)]
        if gram in bibliogram[y]:
            bibliogram[y][gram] += 1
        else:
            bibliogram[y][gram] = 1

armbet = {}
for x in range(depth):

    print()
    print(list(bibliogram[x].items())[:100])

    bibliogram[x] = {key: val for key, val in sorted(bibliogram[x].items(), key = lambda ele: ele[1], reverse=True)}

    print(list(bibliogram[x].items())[:100])

    for y in range(len(bibliogram[x]) - x):

        if x == 0:
            # print(list(bibliogram[x].items())[y][0])
            armbet[list(bibliogram[x].items())[y][0]] =[]

        else:

            try:
                # print(list(bibliogram[x].items())[y][0])
                # print(list(bibliogram[x].items())[y][0][0])
                armbet[list(bibliogram[x].items())[y][0][0]].append(list(bibliogram[x].items())[y])
            except:
                continue


digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, ',': 14, '!': 15,
           '?': 16, '.': 17, '"': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}

for key in armbet:

    armbet[key] = list(sorted(armbet[key], key = lambda ele: ele[1], reverse=True))

    if key in digibet:
        print()
        print(key)
        print(armbet[key])






