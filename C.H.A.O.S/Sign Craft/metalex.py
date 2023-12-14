import pickle

text = open('library/Holy Bible,.txt', 'r')
read = text.read()
# read = read.translate({ord('\n'): None})
# read = read.lower()

test = 'deep. And the Spirit of Go'

lyrics = read.split('\n')
for x in range(10):
    print()
    print(lyrics[x])
    if test in lyrics[x]:
        print('true')


read = read.translate({ord(':'): None})
read = read.translate({ord(';'): None})
read = read.translate({ord('.'): None})
read = read.translate({ord('?'): None})
read = read.translate({ord('!'): '.'})
read = read.translate({ord(','): None})
read = read.translate({ord("'"): None})
read = read.translate({ord('('): None})
read = read.translate({ord(')'): None})

read = read.lower()
