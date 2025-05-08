import pickle

text = open('../library/bible-niv.txt', 'r')
read = text.read()

read = read[3::]

read = read.translate({ord('\n'): '*'})

book = read.split(' ')

record = dict()

for x in range(len(book)):
    record[x] = [book[x], 999]


record['current'] = 0
record['pace'] = 1
record['length'] = len(list(record.items()))


name = 'Edward MacLean'
title = 'bible-niv'

filename = name + '/' + title
outfile = open(filename, 'wb')
pickle.dump(record, outfile)
outfile.close

filename = name + '/' + title
infile = open(filename, "rb")
record = pickle.load(infile)
infile.close

