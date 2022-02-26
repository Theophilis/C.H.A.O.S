import pickle
import numpy as np

infile = open("cell-journal", "rb")
journal = pickle.load(infile)
infile.close


journal = dict(sorted(journal.items(), key=lambda x:len(x[1]), reverse=True))

print(len(list(journal.keys())))

for k in list(journal.keys()):
    print(k)
    jk = journal[k]
    for j in jk:
        if len(j) > 1:
            print(len(j))

