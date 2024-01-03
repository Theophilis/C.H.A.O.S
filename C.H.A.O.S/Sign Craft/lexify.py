import pickle

text = open('library/bible-niv.txt', 'r')
read = text.read()

lyrics = read.split('\n')

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

# read = read.lower()

uniques = []

splits = read.split()

# print(splits)

print("splitting")
for s in splits:
    if s not in uniques:
        uniques.append(s)

print(uniques)
print(len(uniques))

filename = 'library/niv_bible_words'
outfile = open(filename, 'wb')
pickle.dump(uniques, outfile)
outfile.close

filename = 'library/niv_bible_words'
infile = open(filename, "rb")
lexicon = pickle.load(infile)
infile.close


print()
print(lexicon)
print(len(lexicon))

if uniques == lexicon:
    print("true")

