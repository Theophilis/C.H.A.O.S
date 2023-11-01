
text = open('Holy Bible,.txt', 'r')
read = text.read()
read = read.translate({ord('\n'): None})
read = read.translate({ord(' '): None})
for x in range(10):
    read = read.translate({ord(str(x)): None})
read = read.translate({ord(':'): None})
read = read.lower()
length = len(read)

engrams = {}
bigrams = {}
trigrams = {}
quadgrams = {}
fullgrams = []

for x in range(length):
    #engrams
    if read[x] not in engrams:
        engrams[read[x]] = 1
    else:
        engrams[read[x]] += 1

    #bigrams
    if read[x:(x+2)%length] not in bigrams:
        bigrams[read[x:(x+2)%length]] = 1
    else:
        bigrams[read[x:(x+2)%length]] += 1

    #trigrams
    if read[x:(x+3)%length] not in trigrams:
        trigrams[read[x:(x+3)%length]] = 1
    else:
        trigrams[read[x:(x+3)%length]] += 1

    #quadgrams
    if read[x:(x+4)%length] not in quadgrams:
        quadgrams[read[x:(x+4)%length]] = 1
    else:
        quadgrams[read[x:(x+4)%length]] += 1

tail = 32

engrams = {key: val for key, val in sorted(engrams.items(), key = lambda ele: ele[1], reverse=True)}
bigrams = {key: val for key, val in sorted(bigrams.items(), key = lambda ele: ele[1], reverse = True)}
trigrams = {key: val for key, val in sorted(trigrams.items(), key = lambda ele: ele[1], reverse = True)}
quadgrams = {key: val for key, val in sorted(quadgrams.items(), key = lambda ele: ele[1], reverse = True)}

bigrams = {key: val for key, val in list(bigrams.items())[:tail]}
trigrams = {key: val for key, val in list(trigrams.items())[:int(tail/2)]}
quadgrams = {key: val for key, val in list(quadgrams.items())[:int(tail/4)]}


# print(engrams)
# print(bigrams)
# print(trigrams)
# print(quadgrams)
#
# print()
for key_q in quadgrams:
    for key_t in trigrams:
        if key_t in key_q:
            # print()
            # print(key_q, key_t)
            # print(int(quadgrams[key_q]/2))
            # print(trigrams[key_t])
            trigrams[key_t] -= int(quadgrams[key_q]/2)
            # print(trigrams[key_t])
trigrams = {key: val for key, val in sorted(list(trigrams.items()), key = lambda ele: ele[1], reverse = True)}

for key_t in trigrams:
    for key_b in bigrams:
        if key_b in key_t:
            bigrams[key_b] -= int(trigrams[key_t]/2)
bigrams = {key: val for key, val in sorted(bigrams.items(), key=lambda ele: ele[1], reverse = True)}

for key_b in bigrams:
    for key_e in engrams:
        if key_e in key_b:
            engrams[key_e] -= int(bigrams[key_b]/2)
engrams = {key: val for key, val in sorted(engrams.items(), key=lambda ele: ele[1], reverse=True)}


# print(quadgrams)
# print(trigrams)
# print(bigrams)
# print(engrams)

for key in engrams:
    engrams[key] = round(engrams[key]/length*100, 3)

for key in bigrams:
    bigrams[key] = round(bigrams[key]/length*100, 3)

for key in trigrams:
    trigrams[key] = round(trigrams[key]/length*100, 3)

for key in quadgrams:
    quadgrams[key] = round(quadgrams[key]/length*100, 3)

print()
print(quadgrams)
print(trigrams)
print(bigrams)
print(engrams)

for x in range(len(engrams)):
    fullgrams.append(list(engrams.items())[x])
for x in range(len(bigrams)):
    fullgrams.append(list(bigrams.items())[x])
for x in range(len(trigrams)):
    fullgrams.append(list(trigrams.items())[x])
for x in range(len(quadgrams)):
    fullgrams.append(list(quadgrams.items())[x])

fullgrams = sorted(fullgrams, key=lambda ele:ele[1], reverse=True)
print()
print(fullgrams)
print(len(fullgrams))








