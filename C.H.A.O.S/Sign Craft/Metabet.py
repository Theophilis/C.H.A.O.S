import pickle

text = open('library/bible-niv.txt', 'r')
read = text.read()

read = read[3:]
read = read.lower()
#dirty
print('dirty')
print(read[:32])

read = read.translate({ord('\n'): ' '})
read = read.translate({ord(':'): None})
read = read.translate({ord(';'): None})
read = read.translate({ord('.'): None})
read = read.translate({ord('?'): None})
read = read.translate({ord('!'): None})
read = read.translate({ord(','): None})
read = read.translate({ord("'"): None})
read = read.translate({ord('"'): None})
read = read.translate({ord('('): None})
read = read.translate({ord(')'): None})
read = read.translate({ord('-'): ' '})

read = read.translate({ord('0'): None})
read = read.translate({ord('1'): None})
read = read.translate({ord('2'): None})
read = read.translate({ord('3'): None})
read = read.translate({ord('4'): None})
read = read.translate({ord('5'): None})
read = read.translate({ord('6'): None})
read = read.translate({ord('7'): None})
read = read.translate({ord('8'): None})
read = read.translate({ord('9'): None})


print()
print("clean")
print(read[:32])

engrams = dict()
bigrams = dict()

en = 3
digits = 10
digibet_l = 96

for d in range(en-1):
    d = d+2
    engrams[d] = dict()

    for x in range(len(read)-d):

        gram = read[x:x + d]

        if ' ' in gram:
            continue

        if gram not in engrams[d]:
            engrams[d][gram] = 1
        else:
            engrams[d][gram] += 1

    engrams[d] = {key: val for key, val in sorted(engrams[d].items(), key = lambda ele: ele[1], reverse=True)}


print()
print("grams")
print("bigrams")
print(list(engrams[2].keys()))
print(len(engrams[2]))

tri_cap = 2**digits - len(engrams[2]) - digibet_l
print("trigrams")
print(list(engrams[3].keys())[:tri_cap])
print('tri_cap')
print(tri_cap)



#metabet
digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, ',': 14, '"': 15,
           '/': 16, '.': 17, ';': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}
metabet_6 = {0: ' ', 1: 't', 2: 'o', 3: 'n', 4: 'h', 5: 'd', 6: 'u', 7: 'm', 8: 'w', 9: 'y', 10: 'b', 11: 'k',
             12: 'j', 13: 'z', 14: ",",
             15: 'th', 16: 'in', 17: 'an', 18: 'nd', 19: 'en', 20: 'ou', 21: 'ha', 22: 'or', 23: 'is', 24: 'es',
             25: 'the', 26: 'ing',
             27: 'hat', 28: 'tha', 29: 'for', 30: 'ion', 31: 'was', 32: 'you', 33: 'ter', 34: 'ent', 35: 'ere',
             36: 'his', 37: 'her',
             38: 'and', 39: 'ng', 40: 'hi', 41: 'it', 42: 'to', 43: 'ed', 44: 'at', 45: 'on', 46: 're', 47: 'er',
             48: 'he', 49: "'",
             50: '.', 51: 'q', 52: 'x', 53: 'v', 54: 'p', 55: 'g', 56: 'f', 57: 'c', 58: 'l', 59: 'r', 60: 's',
             61: 'i', 62: 'a', 63: 'e'}

metabet = {' ': 0, 'a': 1, 'i': 2, 't': 3, 's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11, 'z': 12, 'q': 13, '0': 14, '1': 15,
           '2': 16, '3': 17, '4': 18, 'j': 19, 'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27, 'n': 28, 'o': 29, 'r': 30, 'e': 31,

           '.': 32, 'A': 33, 'I': 34, 'T': 35, 'S': 36, 'C': 37, 'D': 38, 'M': 39,
           'G': 40, 'F': 41, 'W': 42, 'V': 43, 'Z': 44, 'Q': 45, '5': 46, '6': 47,
           '7': 48, '8': 49, '9': 50, 'J': 51, 'X': 52, 'K': 53, 'Y': 54, 'B': 55,
           'H': 56, 'P': 57, 'U': 58, 'L': 59, 'N': 60, 'O': 61, 'R': 62, 'E': 63,

           '?': 64, ',': 65, "'": 66, '(': 67, ':': 68, '+': 69, '[': 70, '*': 71,
           '@': 72, '{': 73, '%': 74, '<': 75, '/': 76, '|': 77, 'last': 78, 'enter': 79,
           'back': 80, 'pause': 81, 'next': 82, '$': 83, '~': 84, '>': 85, '^': 86, '}': 87,
           '#': 88, '&': 89, ']': 90, '-': 91, ')': 92, '"': 93, ';': 94, '!': 95
           }

print(metabet)

place = digibet_l
for x in range(len(engrams[2])):
    gram = list(engrams[2].keys())[x]
    metabet[gram] = place
    place += 1

print(metabet)


for x in range(tri_cap):
    gram = list(engrams[3].keys())[x]
    metabet[gram] = place
    place += 1
print(metabet)


filename = 'bets/metabet'
outfile = open(filename, 'wb')
pickle.dump(metabet, outfile)
outfile.close

filename = 'bets/metabet'
infile = open(filename, "rb")
metabet = pickle.load(infile)
infile.close
print(metabet)