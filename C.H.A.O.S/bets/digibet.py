import pickle

text = open('library/bible-Theophilis.txt', 'r')
read = text.read()

read = read[1:]
read = read.lower()
read = read.translate({ord('\n'): ' '})
read = read.translate({ord("'"): ' '})
read = read.translate({ord('-'): ' '})
read = read.translate({ord('.'): ' '})

#dirty
print('dirty')
print(read[:100])

#split
read_s = read.split(" ")
print('split')
print(read_s[:100])

digibet = {}

for x in range(len(read_s)):
    word = read_s[x]

    for y in range(len(word)):

        bigram = word[y:y+2]

        if bigram == "":
            continue
        if bigram[0] == " ":
            continue
        if len(bigram) == 1:
            continue
        if bigram in digibet:
            digibet[bigram] += 1
        else:
            digibet[bigram] = 1

digibet_s = list(sorted(digibet.items(), key = lambda ele: ele[1], reverse=True))

print()
print("digibet_s")
print(digibet_s)