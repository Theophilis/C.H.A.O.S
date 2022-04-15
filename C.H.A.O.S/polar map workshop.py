
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

# polar_paths = dict()
#
# for p in polar_u_i:
#
#     fb = (p[0], p[1])
#
#     # print(fb)
#
#     if fb not in polar_paths:
#
#         # print("new")
#
#         polar_paths[fb] = []
#
#         if p not in polar_paths[fb]:
#
#             # print("append")
#
#             polar_paths[fb].append(p)
#
#     else:
#
#         if p not in polar_paths[fb]:
#
#             # print("append")
#
#             polar_paths[fb].append(p)
#
# # print(len(polar_u_i))
# # print(len(polar_d))
#
#
# polar_paths = dict(sorted(list(polar_paths.items()), key=lambda x:len(x[1]), reverse=True))
#
# pos = 0
#
# for p in polar_paths:
#
#     print("")
#     print(p)
#     print(polar_paths[p][10:])
#     print(len(polar_paths[p]))
#
#     pos += 1
#
#     if pos == 10:
#
#         break

filename = 'polar maps/polar_d-16'
outfile = open(filename, 'wb')
pickle.dump(polar_d, outfile)
outfile.close()

# filename = 'polar maps/polar_paths-16'
# outfile = open(filename, 'wb')
# pickle.dump(polar_paths, outfile)
# outfile.close()


polar_u_c = []

for p in polar_d:

    if polar_d[p] > 0:

        polar_u_c.append(p)

print(len(polar_u_c))

filename = 'polar maps/polar_u_c-16'
outfile = open(filename, 'wb')
pickle.dump(polar_u_c, outfile)
outfile.close()
