import math


duration = 10
start = 1
list = []


def fibonacci(a, duration, list, b=0):

    if b == 0:

        b = a

        list.append(a)
        list.append(b)

    c = a + b

    list.append(c)

    if duration != 0:

        duration -= 1

        fibonacci(c, duration, list, a)

fibonacci(start, duration, list)

print(list)








