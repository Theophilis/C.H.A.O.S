import pickle

text = open('library/bible-niv.txt', 'r')
read = text.read()

read = read[1:]
read = read.lower()
read = read.translate({ord('\n'): ' '})
read = read.translate({ord("'"): ' '})
read = read.translate({ord('-'): ' '})

#dirty
print('dirty')
print(read[:100])

bibliogram = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}
depth = 5

for x in range(len(read)):
    for y in range(depth):
        gram = read[x:(x+y+1)%len(read)]
        if ' ' in gram:
            continue
        if gram in bibliogram[y]:
            bibliogram[y][gram] += 1
        else:
            bibliogram[y][gram] = 1


for x in range(depth):

    bibliogram[x] = dict(list(sorted(bibliogram[x].items(), key = lambda ele: ele[1], reverse=True)))

    print()
    print(list(bibliogram[x].items())[:100])



digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, 'an': 14, 'er': 15,
           'ou': 16, 'in': 17, 'th': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}

armbet = {}

for d in digibet:
    print()
    print(d)

    if d == ' ':
        armbet[d] = ['', '']
        continue

    bet = [d]

    for b in bibliogram[len(d)]:
        if b[:len(d)] == d and b[-1] in digibet:
            bet.append(b)

    it = 1
    while len(bet) < 64:
        for b in bibliogram[len(d) + it]:
            if b[:len(d)] == d and b[-1] in digibet:
                if len(bet) == 64:
                    break
                bet.append(b)
        it += 1

    print(bet)
    print(len(bet))

    armbet[d] = bet

for d in digibet:
    print(armbet[d])


filename = 'bets/armbet_2'
outfile = open(filename, 'wb')
pickle.dump(armbet, outfile)
outfile.close