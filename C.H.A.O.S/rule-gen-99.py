import sys
sys.setrecursionlimit(999999999)

view = 3

def base_xx(n, b):
    e = n // b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q) + ','
    else:
        return base_xx(e, b) + str(q) + ","


def rule_gen_xx(rule, base=2):

    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_xx(int(rule), (base))

    int_rule = int_rule.split(',')[:-1]

    x = int_rule[::-1]

    while len(x) < base ** view:
        x += '0'

    bnr = x[::-1]
    int_rul = list(bnr)
    int_rule = []
    for i in int_rul:
        if i != ',':
            int_rule.append(int(i))

    for x in reversed(range(len(int_rule))):

        key = base_xx(x, base)
        key = list(key.split(',')[:-1])

        if len(key) < view:

            for y in range((view - len(key))):
                key.insert(0, '0')

        rules[tuple(key)] = int(int_rule[-x - 1])

    return rules, int_rule[:base ** view]


base = 11

d_rule, i_rule = rule_gen_xx(base**base**3-1, base)

print('')
print(i_rule)
print(d_rule)