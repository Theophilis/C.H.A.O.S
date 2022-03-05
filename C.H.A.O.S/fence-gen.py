import numpy as np

import pickle

rule = 1001
base = 4
size = 505
view = 4
start = (int(size/2), int(size/2))
zero = (0, 0)


def fencing(zero, level = 0):
    # print(" ")
    # print("zero")
    # print(zero)
    fence = []
    for x in range(4):
        if x % 2 == 0:
            if x < 2:
                # print(x)
                for y in range(2 * (level + 1)):
                    post = (zero[0], zero[0] + (y + 1))
                    # print("post")
                    # print(post)
                    fence.append(post)
            else:
                # print(x)
                for y in range(2 * (level + 1)):
                    post = (zero[0] + 2 * (level + 1), zero[0] + 2 * (level + 1) - (y + 1))
                    fence.append(post)

        else:
            if x < 2:
                # print(x)
                for y in range(2 * (level + 1)):
                    post = (zero[0] + (y + 1), zero[0] + 2 * (level + 1))
                    fence.append(post)
            else:
                # print(x)
                for y in range(2 * (level + 1) + 1):
                    post = (zero[0] + 2 * (level + 1) - (y + 1), zero[0])
                    fence.append(post)
    # print(fence)
    return fence

def fence_map(start, order=0):

    if order == 0:
        fence = dict()

        for x in range(int(size/2)):
            zero = (start[0] - (x + 1), start[0] - (x + 1))
            fence[x] = fencing(zero, x)

        full_fence = []
        for k in list(fence.keys()):
            for f in fence[k][:len(fence[k]) - 1]:
                full_fence.append(f)

        canvas_f = np.zeros((size, size), dtype='int8')
        full_fence.insert(0, start)

        # for f in full_fence:
        #     canvas_f[f] = full_fence.index(f)

        return full_fence

    elif order == 1:
        canvas_t = np.zeros((size, size), dtype='int8')

        t_fence = []

        for x in range(size):
            for y in range(size):
                t_fence.append((x, y))

        for t in t_fence:
            canvas_t[t] = t_fence.index(t)

        return t_fence, canvas_t

    elif order == 2:
        canvas = np.zeros((size, size), dtype='int8')

        fence = []

        for x in range(size):
            for y in range(size):
                fence.append((x, y))

        fence = sorted(fence, key=lambda x: abs(x[0] + x[1]))

        for f in fence:
            canvas[f] = fence.index(f)

        return fence, canvas


for x in range(10):

    size = x * 100 + 1

    print("")
    print(size)

    start = (int(size / 2), int(size / 2))

    full_fence = fence_map(start, 0)

    filename = '2d-fences/full-fence_spiral_' + str(size)
    outfile = open(filename, 'wb')
    pickle.dump(full_fence, outfile)
    outfile.close