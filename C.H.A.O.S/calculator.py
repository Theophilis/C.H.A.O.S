
def decimal(n, b):

    n = list(reversed(n))
    n = [int(v) for v in n]

    value = 0
    place = 0


    for c in n:

        value += int(c) * b ** place
        place += 1

    return value

max = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# print("max")
# print(max)
# print(len(max))

max = decimal(max, 2)

base = 3

a = base ** base ** 3
b = 2 ** 16



print(a)
print(b)

print(int(b/a))



