
import numpy as np
from datetime import datetime
import random
import os
import pickle
import sys
import matplotlib.pyplot as plt
from matplotlib import colors

infile = open("polar maps/polar_u-16", "rb")
polar_u_i = pickle.load(infile)
infile.close

infile = open("polar maps/polar_d-16", "rb")
polar_d = pickle.load(infile)
infile.close

# polar_d = dict()

for p in polar_u_i:

    if p not in polar_d:
        polar_d[p] = 0

print(len(polar_u_i))
print(len(polar_d))

filename = 'polar maps/polar_d-16'
outfile = open(filename, 'wb')
pickle.dump(polar_d, outfile)
outfile.close()

