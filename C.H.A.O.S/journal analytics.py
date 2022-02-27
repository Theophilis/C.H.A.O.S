import pickle
import numpy as np

infile = open("journals/journal_155", "rb")
journal = pickle.load(infile)
infile.close


journal = dict(sorted(journal.items(), key=lambda x:len(x[1][0]), reverse=True))

print(len(list(journal.keys())))

for k in list(journal.keys())[:10]:
    print('')
    print(k)
    jk = journal[k]
    print(len(jk[0]))


