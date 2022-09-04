from ctypes import *

import numpy as np

so_file = "/Users/edwar/.vscode/chaos/chaos_2d.so"
my_functions = CDLL(so_file)

board = np.zeros((9), dtype='uint8')
a_rule = np.zeros((32), dtype="uint8")
board[4] = 1
a_rule[2] = 1
a_rule[1] = 1
a_rule[4] = 1
a_rule[8] = 1
a_rule[15] = 1
lw = 9
base = 2
width = 3

print(board)
print(a_rule)



print(type(my_functions))

my_functions.step(board, a_rule, base, lw, width)

